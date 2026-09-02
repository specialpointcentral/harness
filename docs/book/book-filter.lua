local current_chapter = "本章"
local table_index = 0

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
  if el.level == 1 then
    current_chapter = pandoc.utils.stringify(el.content)
    table_index = 0
  end
  return el
end

function Table(el)
  if #el.caption.long == 0 then
    table_index = table_index + 1
    el.caption.long = {
      pandoc.Plain({pandoc.Str(current_chapter .. "：对照表（" .. table_index .. "）")})
    }
  end
  return el
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
