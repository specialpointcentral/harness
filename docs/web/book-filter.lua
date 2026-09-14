local function read_file(path)
  local handle, err = io.open(path, "rb")
  if handle == nil then
    error("cannot read web figure SVG " .. path .. ": " .. tostring(err))
  end
  local content = handle:read("*a")
  handle:close()
  content = content:gsub("^<%?xml.-%?>%s*", "")
  content = content:gsub("^<!DOCTYPE.-%>%s*", "")
  return content
end

local callout_classes = {
  ["学术背景｜"] = "callout-academic",
  ["设计取舍｜"] = "callout-tradeoff",
  ["安全提示｜"] = "callout-security",
  ["特色机制｜"] = "callout-feature",
}

function BlockQuote(el)
  if #el.content == 0 then
    return el
  end
  local first = el.content[1]
  if first.t ~= "Para" and first.t ~= "Plain" then
    return el
  end
  if #first.content == 0 or first.content[1].t ~= "Strong" then
    return el
  end

  local title = pandoc.utils.stringify(first.content[1].content)
  local callout_class = nil
  for prefix, class_name in pairs(callout_classes) do
    if title:sub(1, #prefix) == prefix then
      callout_class = class_name
      break
    end
  end
  if callout_class == nil then
    return el
  end

  local body = {}
  if #first.content > 1 then
    local remainder = {}
    for index = 2, #first.content do
      table.insert(remainder, first.content[index])
    end
    if #remainder > 0 then
      table.insert(body, pandoc.Para(remainder))
    end
  end
  for index = 2, #el.content do
    table.insert(body, el.content[index])
  end

  local title_block = pandoc.Div(
    {pandoc.Plain(first.content[1].content)},
    pandoc.Attr("", {"callout-title"})
  )
  local blocks = {title_block}
  for _, block in ipairs(body) do
    table.insert(blocks, block)
  end
  return pandoc.Div(
    blocks,
    pandoc.Attr("", {"callout", callout_class}, {{"role", "note"}})
  )
end

function Div(el)
  if el.classes:includes("book-figure") then
    local image = el.attributes.image
    if image == nil or image == "" then
      error("book-figure is missing its image attribute")
    end
    if el.identifier == nil or not el.identifier:match("^fig%-%d+%-%d+$") then
      error("book-figure has an invalid identifier")
    end
    if #el.content ~= 1 then
      error("book-figure must contain one source caption")
    end
    local svg = read_file(image)
    return {
      pandoc.RawBlock(
        "html",
        '<figure id="' .. el.identifier .. '" class="book-figure" data-pagefind-ignore>'
      ),
      pandoc.RawBlock(
        "html",
        '<div class="diagram">' .. svg .. "</div>"
      ),
      pandoc.RawBlock("html", "<figcaption>"),
      el.content[1],
      pandoc.RawBlock("html", "</figcaption></figure>"),
    }
  end

  if el.classes:includes("book-table") then
    if el.identifier == nil or not el.identifier:match("^tab%-%d+%-%d+$") then
      error("book-table has an invalid identifier")
    end
    if #el.content ~= 2 or el.content[2].t ~= "Table" then
      error("book-table must contain one caption and one table")
    end
    local caption = pandoc.Div(
      {el.content[1]},
      pandoc.Attr("", {"table-caption"})
    )
    local table_scroll = pandoc.Div(
      {el.content[2]},
      pandoc.Attr("", {"table-scroll"})
    )
    return pandoc.Div(
      {caption, table_scroll},
      pandoc.Attr(el.identifier, {"book-table"})
    )
  end

  return el
end
