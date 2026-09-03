local function latex_escape(text)
  local replacements = {
    ["\\"] = "\\textbackslash{}",
    ["{"] = "\\{",
    ["}"] = "\\}",
    ["$"] = "\\$",
    ["&"] = "\\&",
    ["#"] = "\\#",
    ["^"] = "\\textasciicircum{}",
    ["_"] = "\\_",
    ["%"] = "\\%",
    ["~"] = "\\textasciitilde{}",
  }
  return (text:gsub("[\\{}$&#^_%%~]", replacements))
end

function Header(el)
  if el.level == 2 or el.level == 3 then
    return {
      pandoc.RawBlock("latex", "\\FloatBarrier"),
      el,
    }
  end
  return el
end

function Div(el)
  if el.classes:includes("book-table") then
    local label = el.attributes.label
    if label == nil or not label:match("^tab%-%d+%-%d+$") then
      error("book-table has an invalid label attribute")
    end
    if #el.content ~= 2 or el.content[2].t ~= "Table" then
      error("book-table must contain one caption and one table")
    end

    el.content[2].caption.long = {}
    el.content[2].caption.short = nil
    el.content[2].identifier = ""
    return {
      pandoc.RawBlock(
        "latex",
        "\\Needspace{7\\baselineskip}\\hypertarget{" .. label .. "}{}"
      ),
      el.content[1],
      pandoc.RawBlock("latex", "\\nopagebreak[4]"),
      el.content[2],
    }
  elseif not el.classes:includes("book-figure") then
    return el
  end

  local image = el.attributes.image
  local label = el.attributes.label
  local scale = el.attributes.scale
  if image == nil or image == "" then
    error("book-figure is missing its image attribute")
  end
  if label == nil or not label:match("^fig%-%d+%-%d+$") then
    error("book-figure has an invalid label attribute")
  end
  if scale == nil or not scale:match("^0%.%d+$") then
    error("book-figure has an invalid scale attribute")
  end
  if #el.content ~= 1 then
    error("book-figure must contain one source caption")
  end

  return {
    pandoc.RawBlock(
      "latex",
      "\\hypertarget{" .. label .. "}{}\n" ..
      "\\begin{figure}[!htbp]\n" ..
      "\\begin{center}\n" ..
      "\\adjustbox{scale=" .. scale .. ",max width=0.92\\linewidth," ..
      "max height=0.78\\textheight}{" ..
      "\\includegraphics[keepaspectratio]{\\detokenize{" .. image .. "}}}\n" ..
      "\\end{center}\n" ..
      "\\begin{minipage}{0.92\\linewidth}"
    ),
    el.content[1],
    pandoc.RawBlock(
      "latex",
      "\\end{minipage}\n" ..
      "\\end{figure}"
    ),
  }
end

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
  local box = nil
  if title:match("^学术背景｜") then
    box = "academicbox"
  elseif title:match("^设计取舍｜") then
    box = "tradeoffbox"
  elseif title:match("^安全提示｜") then
    box = "securitybox"
  elseif title:match("^特色机制｜") then
    box = "featurebox"
  else
    return el
  end

  local body = {}
  if #first.content > 1 then
    local remainder = {}
    for i = 2, #first.content do
      table.insert(remainder, first.content[i])
    end
    if #remainder > 0 then
      table.insert(body, pandoc.Para(remainder))
    end
  end
  for i = 2, #el.content do
    table.insert(body, el.content[i])
  end

  local result = {pandoc.RawBlock("latex", "\\begin{" .. box .. "}{" .. latex_escape(title) .. "}")}
  for _, block in ipairs(body) do
    table.insert(result, block)
  end
  table.insert(result, pandoc.RawBlock("latex", "\\end{" .. box .. "}"))
  return result
end
