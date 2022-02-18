import saver
import yaml
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from discord_webhook import DiscordWebhook
from time import sleep

with open('webhook.txt', 'r') as file:
	webhook_url = file.read()

# Creates automated browser application
def setup_driver():
	options = webdriver.FirefoxOptions()
	options.add_argument('--headless')

	return webdriver.Firefox(options=options)

# Removes elements that should not be visible in question screenshot and
# changes their CSS to improve screenshot quality
def clean_question(driver):
	driver.execute_script('''
	var content = document.querySelector(".question-content");
	var points = document.querySelector(".question-points");

	points.remove();

	content.style.padding = "16px 32px";
	''')

# Extracts question ID from its URL
def extract_id(url):
	question_id = re.search('\d+', url).group(0)

	return int(question_id)

# Returns URLs of 20 newest questions on the home page
def get_urls(driver):
	driver.get('https://scriptinghelpers.org/')

	urls = []

	for element in driver.find_elements(By.CLASS_NAME, 'q-link'):
		anchor = element.find_element(By.TAG_NAME, 'a')
		url = anchor.get_attribute('href')

		urls.append(url)

	return urls

# Returns details about person who posted the question including his username
# and URL to his Roblox avatar thumbnail
def get_poster_details(driver):
	details = driver.execute_script('''
	var poster = document.querySelector(".question-poster-username");

	var avatar = poster.querySelector(".loggedin-avatar");
	var name = poster.querySelector(".loggedin-name");

	return [
		name.innerText,
		`https://scriptinghelpers.org${avatar.getAttribute('src')}`
	]
	''')

	return details[0], details[1]

# Uploads question to the webhook
def upload_question(driver, url):
	driver.get(url)
	clean_question(driver)

	element = driver.find_element(By.CLASS_NAME, 'question-content')
	name, avatar = get_poster_details(driver)

	webhook = DiscordWebhook(
		url=webhook_url,
		content=f"<@&920585996519735306>\n<{url}>",
		username=name,
		avatar_url=avatar
	)

	webhook.add_file(file=element.screenshot_as_png, filename='a.png')
	webhook.execute()

# Tracks untracked questions from the home page
def update(driver):
	urls = get_urls(driver)
	tracked = saver.get_tracked()

	for url in urls:
		question_id = extract_id(url)

		if question_id in tracked or str(question_id) in tracked:
			continue

		upload_question(driver, url)
		tracked.append(question_id)

	saver.save_tracked(tracked)

# Setups, controls and exits the driver
def main():
	driver = setup_driver()

	while True:
		update(driver)
		sleep(40)

	driver.quit()

if __name__ == "__main__":
	main()
