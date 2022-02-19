// Removes elements that should not be visible in question screenshot and
// changes their CSS to improve screenshot quality

let content = document.querySelector(".question-content");
let points = document.querySelector(".question-points");

points.remove();

content.style.padding = "16px 32px";

return content;
