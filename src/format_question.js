// Formats question as a Discord message

const ENTITIES = {
  "&amp;": "&",
  "&lt;": "<",
  "&gt;": ">",
  "&quot;": "\""
};

let content = "";

let markdown = document.querySelector(".question-markdown");

// Writes plain text to the content
function writeText(text) {
  content += text;
}

// Replaces HTML entities to their ASCII symbols
function formatEntities(text) {
  return text.replace(/&(.*?);/, entity => ENTITIES[entity]);
}

// Extracts URL from <a> element and fixes incorrectly posted links
function extractURL(element) {
  let href = element.getAttribute("href");

  return href == "http://" ? element.innerText : href;
}

// Writes formatted code element to the content, truncates the code block
// if it's too long
function processCode(element) {
  let lines = element.getElementsByClassName("content");

  writeText("```lua\n");

  for (let line of lines) {
    let text = line.innerText;

    if (content.length + text.length > 1600)
      break;

    writeText(text + "\n");
  }

  writeText("```");
}

// Writes formatted paragraph text to the content
function processParagraph(element) {
  for (let child of element.children) {
    let text = child.innerText;

    switch (child.tagName) {
    case "strong": text = formatEntities(`**${text}**`); break;
    case "code": text = formatEntities(`\`${text}\``); break;
    case "i": text = formatEntities(`*${text}*`); break;
    case "a": text = extractURL(child);
    }

    if (content.length + text.length > 1600)
      break;

    writeLine(text);
  }
}

// Writes formatted <ul> text to the content
function processList(element) {
  for (let item of element.child)
    writeLine(`- ${formatEntities(item.innerText)}`);
}

// Scans all HTML elements in the question content and formats them
for (let element of markdown.children) {
  switch (element.tagName) {
  case "P":
    processParagraph(element);
    break;
  case "UL":
    processList(element);
    break;
  case "BLOCKQUOTE":
    writeMarkdownText("> " + formatEntities(element.innerText) + "\n");
    break;
  case "DIV":
    if (element.classList.contains("syntaxhighlighter"))
      processCode(element);
  }
}

return content;
