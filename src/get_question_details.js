// Returns details about question including details about author of the
// question like his name and reputation

let poster = document.querySelector(".question-poster");

let title = document.querySelector(".question-title");
let date = poster.querySelector(".date");

let avatar = poster.querySelector(".loggedin-avatar");
let name = poster.querySelector(".loggedin-name");

let reputation = poster.querySelector(".muted.small");

// Returns UNIX timestamp from UTC date string
function getUnixTimestamp(string) {
  string = string.replace(" UTC", "");

  return Date.parse(string) / 1000;
}

return {
  name: name.innerText,
  avatar: `https://scriptinghelpers.org${avatar.getAttribute('src')}`,
  reputation: parseInt(reputation.innerText),
  title: title.innerText,
  time: getUnixTimestamp(date.getAttribute('title'))
};
