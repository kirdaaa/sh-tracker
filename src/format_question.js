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

// Formats paragraph to Discord format
function formatParagraph(element) {
  let text = element.innerHTML;

  text = text
    .replace(/<code>(.*?)<\/code>/, "`\1`")
    .replace(/<strong>(.*?)<\/strong>/, "**\1**")
    .replace(/<i>(.*?)<\/i>/, "*\1*");

  text = text.replace(
    /<a target="_blank" href="(.*?)">(.*?)<\/a>/,
    (a, b, c) => {
      console.log(a, b, c)
    }
  );

  return formatEntities(text);
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

// Writes formatted <ul> text to the content
function processList(element) {
  for (let item of element.child)
    writeLine(`- ${formatParagraph(item.innerText)}`);
}

// Scans all HTML elements in the question content and formats them
for (let element of markdown.children) {
  switch (element.tagName) {
  case "P":
    writeText(formatParagraph(element) + "\n");
    break;
  case "UL":
    processList(element);
    break;
  case "BLOCKQUOTE":
    writeText("> " + formatParagraph(element) + "\n");
    break;
  case "DIV":
    if (element.classList.contains("syntaxhighlighter"))
      processCode(element);
  }
}

return content;
