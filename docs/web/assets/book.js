(() => {
  const root = document.documentElement;
  const themeButton = document.querySelector("[data-theme-toggle]");
  const themeLabel = document.querySelector("[data-theme-label]");
  const themeQuery = window.matchMedia("(prefers-color-scheme: dark)");
  const storageKey = "harness-book-theme";

  const updateThemeLabel = () => {
    if (!themeButton) return;
    const next = root.dataset.theme === "dark" ? "浅色" : "深色";
    themeButton.setAttribute("aria-label", `切换到${next}主题`);
    if (themeLabel) themeLabel.textContent = `切换到${next}主题`;
  };

  updateThemeLabel();
  themeButton?.addEventListener("click", () => {
    const next = root.dataset.theme === "dark" ? "light" : "dark";
    root.dataset.theme = next;
    localStorage.setItem(storageKey, next);
    updateThemeLabel();
  });
  themeQuery.addEventListener("change", (event) => {
    if (localStorage.getItem(storageKey)) return;
    root.dataset.theme = event.matches ? "dark" : "light";
    updateThemeLabel();
  });

  const overlay = document.querySelector("[data-site-overlay]");
  const drawerPairs = [
    [document.querySelector("[data-book-nav-toggle]"), document.querySelector("[data-book-nav]")],
    [document.querySelector("[data-page-toc-toggle]"), document.querySelector("[data-page-toc]")],
  ];
  let activeDrawer = null;
  let activeToggle = null;

  const closeDrawer = () => {
    if (!activeDrawer) return;
    activeDrawer.classList.remove("is-open");
    activeToggle?.setAttribute("aria-expanded", "false");
    overlay.hidden = true;
    document.body.classList.remove("drawer-open");
    const focusTarget = activeToggle;
    activeDrawer = null;
    activeToggle = null;
    focusTarget?.focus();
  };

  const openDrawer = (toggle, drawer) => {
    if (!toggle || !drawer) return;
    closeDrawer();
    activeDrawer = drawer;
    activeToggle = toggle;
    drawer.classList.add("is-open");
    toggle.setAttribute("aria-expanded", "true");
    overlay.hidden = false;
    document.body.classList.add("drawer-open");
    drawer.querySelector("a")?.focus();
  };

  drawerPairs.forEach(([toggle, drawer]) => {
    toggle?.addEventListener("click", () => {
      if (activeDrawer === drawer) closeDrawer();
      else openDrawer(toggle, drawer);
    });
    drawer?.addEventListener("click", (event) => {
      if (event.target.closest("a")) closeDrawer();
    });
  });
  overlay?.addEventListener("click", closeDrawer);
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeDrawer();
  });

  const tocLinks = new Map(
    [...document.querySelectorAll(".page-toc a[href^='#']")].map((link) => [
      decodeURIComponent(link.hash.slice(1)),
      link,
    ])
  );
  const headings = [...document.querySelectorAll(".book-main h2[id], .book-main h3[id]")];
  if (tocLinks.size && headings.length && "IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((left, right) => left.boundingClientRect.top - right.boundingClientRect.top);
        if (!visible.length) return;
        tocLinks.forEach((link) => link.removeAttribute("aria-current"));
        tocLinks.get(visible[0].target.id)?.setAttribute("aria-current", "location");
      },
      { rootMargin: "-15% 0px -72%", threshold: [0, 1] }
    );
    headings.forEach((heading) => observer.observe(heading));
  }
})();
