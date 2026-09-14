#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import puppeteer from "puppeteer";

const DISPLAY_SCALE = 0.7;
const VIEWBOX_PADDING = 12;
const COLLISION_PADDING = 12;
const PATH_RATIOS = [0.5, 0.42, 0.58, 0.34, 0.66, 0.26, 0.74, 0.18, 0.82];
const NORMAL_OFFSETS = [0, -18, 18, -36, 36, -54, 54];

function usage() {
  console.error("usage: postprocess-svg.mjs INPUT.svg [PUPPETEER_CONFIG.json]");
  process.exit(2);
}

if (process.argv.length < 3 || process.argv.length > 4) {
  usage();
}

const svgPath = path.resolve(process.argv[2]);
const puppeteerConfigPath = process.argv[3]
  ? path.resolve(process.argv[3])
  : null;
const launchOptions = puppeteerConfigPath
  ? JSON.parse(await fs.readFile(puppeteerConfigPath, "utf8"))
  : {};
launchOptions.headless = true;
if (process.env.PUPPETEER_EXECUTABLE_PATH) {
  launchOptions.executablePath = process.env.PUPPETEER_EXECUTABLE_PATH;
}

const source = await fs.readFile(svgPath, "utf8");
const browser = await puppeteer.launch(launchOptions);
try {
  const page = await browser.newPage();
  await page.setViewport({ width: 2400, height: 2400, deviceScaleFactor: 1 });
  await page.setContent(source, { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);

  const result = await page.evaluate(
    ({
      collisionPadding,
      displayScale,
      normalOffsets,
      pathRatios,
      viewBoxPadding,
    }) => {
      const svg = document.querySelector("svg");
      if (!(svg instanceof SVGSVGElement)) {
        throw new Error("input does not contain an SVG root");
      }

      const activeCollisionPadding = svg.classList.contains("statediagram")
        ? collisionPadding
        : 4;
      const initialViewBox = svg.viewBox.baseVal;
      svg.style.width = `${initialViewBox.width}px`;
      svg.style.height = `${initialViewBox.height}px`;
      svg.style.maxWidth = "none";
      svg.style.maxHeight = "none";

      const labels = [...svg.querySelectorAll("g.edgeLabel")]
        .map((outer) => {
          const inner = outer.querySelector("g.label[data-id]");
          const id = inner?.getAttribute("data-id") ?? "";
          const edge = [
            ...svg.querySelectorAll(".edgePaths path[data-id]"),
          ].find((candidate) => candidate.getAttribute("data-id") === id);
          const rect = outer.getBoundingClientRect();
          if (
            !(edge instanceof SVGPathElement) ||
            !id ||
            !rect.width ||
            !rect.height
          ) {
            return null;
          }
          const localBox = outer.getBBox();
          return {
            edge,
            id,
            localCenterX: localBox.x + localBox.width / 2,
            localCenterY: localBox.y + localBox.height / 2,
            originalCenterX: rect.left + rect.width / 2,
            originalCenterY: rect.top + rect.height / 2,
            originalTransform: outer.getAttribute("transform") ?? "",
            outer,
          };
        })
        .filter(Boolean);

      const nodeElements = [...svg.querySelectorAll("g.node")];

      const expanded = (rect, padding) => ({
        left: rect.left - padding,
        right: rect.right + padding,
        top: rect.top - padding,
        bottom: rect.bottom + padding,
      });

      const overlapArea = (left, right, padding = 0) => {
        const a = expanded(left, padding);
        const b = expanded(right, padding);
        const width = Math.min(a.right, b.right) - Math.max(a.left, b.left);
        const height = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
        return width > 0 && height > 0 ? width * height : 0;
      };

      const collisionSummary = () => {
        const labelRects = labels.map((label) => ({
          id: label.id,
          rect: label.outer.getBoundingClientRect(),
        }));
        const nodeRects = nodeElements.map((node) =>
          node.getBoundingClientRect(),
        );
        const pairs = [];
        for (let left = 0; left < labelRects.length; left += 1) {
          for (let right = left + 1; right < labelRects.length; right += 1) {
            if (
              overlapArea(
                labelRects[left].rect,
                labelRects[right].rect,
                activeCollisionPadding,
              ) > 0
            ) {
              pairs.push([labelRects[left].id, labelRects[right].id]);
            }
          }
        }
        const nodeHits = [];
        for (const label of labelRects) {
          if (
            nodeRects.some(
              (nodeRect) =>
                overlapArea(label.rect, nodeRect, activeCollisionPadding) > 0,
            )
          ) {
            nodeHits.push(label.id);
          }
        }
        return { nodeHits, pairs };
      };

      const pointInParent = (label, ratio) => {
        const length = label.edge.getTotalLength();
        const offset = Math.max(0.5, Math.min(length / 100, 2));
        const distance = length * ratio;
        const before = label.edge.getPointAtLength(
          Math.max(0, distance - offset),
        );
        const point = label.edge.getPointAtLength(distance);
        const after = label.edge.getPointAtLength(
          Math.min(length, distance + offset),
        );
        const edgeMatrix = label.edge.getCTM();
        const parentMatrix = label.outer.parentElement?.getCTM();
        if (!edgeMatrix || !parentMatrix) {
          return null;
        }
        const inverseParent = parentMatrix.inverse();
        const convert = (value) =>
          new DOMPoint(value.x, value.y)
            .matrixTransform(edgeMatrix)
            .matrixTransform(inverseParent);
        const p0 = convert(before);
        const p1 = convert(point);
        const p2 = convert(after);
        const dx = p2.x - p0.x;
        const dy = p2.y - p0.y;
        const magnitude = Math.hypot(dx, dy) || 1;
        return {
          x: p1.x,
          y: p1.y,
          normalX: -dy / magnitude,
          normalY: dx / magnitude,
        };
      };

      const candidateTransforms = (label) => {
        const candidates = [
          {
            distance: 0,
            transform: label.originalTransform,
          },
        ];
        for (const ratio of pathRatios) {
          const point = pointInParent(label, ratio);
          if (!point) {
            continue;
          }
          for (const normalOffset of normalOffsets) {
            const anchorX = point.x + point.normalX * normalOffset;
            const anchorY = point.y + point.normalY * normalOffset;
            const x = anchorX - label.localCenterX;
            const y = anchorY - label.localCenterY;
            candidates.push({
              distance:
                Math.abs(ratio - 0.5) * 300 + Math.abs(normalOffset) * 1.5,
              transform: `translate(${x.toFixed(3)}, ${y.toFixed(3)})`,
            });
          }
        }
        return candidates;
      };

      const placeLabel = (label) => {
        const otherLabelRects = labels
          .filter((candidate) => candidate !== label)
          .map((candidate) => candidate.outer.getBoundingClientRect());
        const nodeRects = nodeElements.map((node) =>
          node.getBoundingClientRect(),
        );
        let best = null;
        for (const candidate of candidateTransforms(label)) {
          label.outer.setAttribute("transform", candidate.transform);
          const rect = label.outer.getBoundingClientRect();
          let collisionCount = 0;
          let collisionArea = 0;
          for (const otherRect of otherLabelRects) {
            const area = overlapArea(rect, otherRect, activeCollisionPadding);
            if (area > 0) {
              collisionCount += 1;
              collisionArea += area;
            }
          }
          for (const nodeRect of nodeRects) {
            const area = overlapArea(rect, nodeRect, activeCollisionPadding);
            if (area > 0) {
              collisionCount += 1;
              collisionArea += area;
            }
          }
          const centerX = rect.left + rect.width / 2;
          const centerY = rect.top + rect.height / 2;
          const movement = Math.hypot(
            centerX - label.originalCenterX,
            centerY - label.originalCenterY,
          );
          const score =
            collisionCount * 1_000_000_000 +
            collisionArea * 10_000 +
            candidate.distance +
            movement;
          if (best === null || score < best.score) {
            best = { score, transform: candidate.transform };
          }
        }
        label.outer.setAttribute("transform", best.transform);
      };

      let collisions = collisionSummary();
      for (
        let round = 0;
        round < 5 && (collisions.pairs.length || collisions.nodeHits.length);
        round += 1
      ) {
        const conflicted = new Set([
          ...collisions.nodeHits,
          ...collisions.pairs.flat(),
        ]);
        const ordered = [
          ...labels.filter((label) => conflicted.has(label.id)),
          ...labels.filter((label) => !conflicted.has(label.id)),
        ];
        for (const label of ordered) {
          placeLabel(label);
        }
        collisions = collisionSummary();
      }

      if (collisions.pairs.length || collisions.nodeHits.length) {
        throw new Error(
          `unresolved SVG label collisions: ${JSON.stringify(collisions)}`,
        );
      }

      const content = svg.getBBox();
      const x = content.x - viewBoxPadding;
      const y = content.y - viewBoxPadding;
      const width = content.width + viewBoxPadding * 2;
      const height = content.height + viewBoxPadding * 2;
      svg.setAttribute(
        "viewBox",
        `${x.toFixed(3)} ${y.toFixed(3)} ${width.toFixed(3)} ${height.toFixed(3)}`,
      );
      svg.setAttribute("width", (width * displayScale).toFixed(2));
      svg.setAttribute("height", (height * displayScale).toFixed(2));
      svg.setAttribute("data-natural-width", width.toFixed(3));
      svg.setAttribute("data-natural-height", height.toFixed(3));
      svg.setAttribute("data-layout-collisions", "0");
      svg.style.removeProperty("width");
      svg.style.removeProperty("height");
      svg.style.removeProperty("max-width");
      svg.style.removeProperty("max-height");

      return {
        collisions: 0,
        height,
        labels: labels.length,
        svg: svg.outerHTML,
        width,
      };
    },
    {
      collisionPadding: COLLISION_PADDING,
      displayScale: DISPLAY_SCALE,
      normalOffsets: NORMAL_OFFSETS,
      pathRatios: PATH_RATIOS,
      viewBoxPadding: VIEWBOX_PADDING,
    },
  );

  await fs.writeFile(svgPath, `${result.svg}\n`, "utf8");
  console.log(
    `postprocessed ${path.basename(svgPath)}: labels=${result.labels}, ` +
      `collisions=${result.collisions}, viewBox=${result.width.toFixed(1)}x${result.height.toFixed(1)}`,
  );
} finally {
  await browser.close();
}
