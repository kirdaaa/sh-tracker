// Returns details about question including details about author of the
// question like his name and reputation

let poster = document.querySelector(".question-poster");

let title = document.querySelector(".question-title");
let date = poster.querySelector(".data");

let avatar = poster.querySelector(".loggedin-avatar");
let name = poster.querySelector(".loggedin-name");

let reputation = poster.querySelector(".muted.small");

return {
	name: name.innerText,
	avatar: `https://scriptinghelpers.org${avatar.getAttribute('src')}`,
  reputation: parseInt(reputation.innerText),
  title: title.innerText,
  time: new Date(date.getAttribute('title')).getUTCSeconds()
};
