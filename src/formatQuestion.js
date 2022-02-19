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

// Writes text to the content and formats bold, italic, ... text and
// replaces HTML entities with according symbols
function writeMarkdownText(text) {
  text = text
    .replace(/<b>(.*?)<\/b>/gi, "**\1**")
    .replace(/<i>(.*?)<\/i>/gi, "*\1*")
    .replace(/<u>(.*?)<\/u>/gi, "__\1__")
    .replace(/<s>(.*?)<\/s>/gi, "~~\1~~");

  text = text.replace(/&(.*?);/, entity => ENTITIES[entity]);

  writeText(text);
}

// Writes formatted code element to the content, truncates the code block
// if it's too long
function writeCode(element) {
  let lines = element.getElementsByClassName("content");

  writeText("```lua\n");

  for (let line of lines) {
    let text = line.innerText;

    if (content.length + text.length > 1600)
      break;

    writeText(line.text + "\n");
  }

  writeText("```");
}

// Scans all HTML elements in the question content and formats them
for (let element of markdown.children) {
  switch (element.tagName) {
  case "P":
    writeMarkdownText(element.innerText + "\n");
    break;
  case "DIV":
    if (element.classList.contains("syntaxhighlighter"))
      writeCode(element);
  }
}

return content;
