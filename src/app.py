import saver
import yaml
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from discord_webhook import DiscordWebhook
from time import sleep

with open('config.yml', 'r') as file:
	config = yaml.safe_load(file)

# Loads JavaScript code that can be executed using driver.execute_script()
def load_script(name):
	with open('src/' + name, 'r') as file:
		return file.read()

clean_question = load_script('clean_question.js')
format_question = load_script('format_question.js')
get_question_details = load_script('get_question_details.js')

# Setups Firefox browser application
def setup_driver():
	options = webdriver.FirefoxOptions()
	# options.add_argument('--headless')

	return webdriver.Firefox(options=options)

# Extracts question ID from its URL
def extract_id(url):
	question_id = re.search('\d+', url).group(0)

	return int(question_id)

# Creates webhook username from data about question poster
def get_username(details):
	name = details['name']
	reputation = details['reputation']

	return f'{name} ({reputation})'

# Creates webhook question content including header and additional details
def get_full_question_content(url, content, details):
	question_id = extract_id(url)

	return f'''
	**{details['title']}** *{question_id}*
	<@&920585996519735306> <t:{details['time']}>

	{content}

	Question URL: <{url}>
	'''

# Returns URLs of 20 newest questions on the home page
def get_urls(driver):
	driver.get('https://scriptinghelpers.org/')

	urls = []

	for element in driver.find_elements(By.CLASS_NAME, 'q-link'):
		anchor = element.find_element(By.TAG_NAME, 'a')
		url = anchor.get_attribute('href')

		urls.append(url)

	return urls

# Uploads question content to webhook v1
def upload_question_content(driver, url, details):
	content = driver.execute_script(format_question)

	webhook = DiscordWebhook(
		url=config['webhook'],
		content=get_full_question_content(url, content, details),
		username=get_username(details),
		avatar_url=details['avatar']
	)

	webhook.execute()

# Uploads question screenshot to webhook v2
def upload_question_screenshot(driver, url, details):
	driver.execute_script(clean_question)

	webhook = DiscordWebhook(
		url=config['webhook_v2'],
		content=f"<@&920585996519735306>\n<{url}>",
		username=get_username(details),
		avatar_url=details['avatar']
	)

	webhook.add_file(file=element.screenshot_as_png, filename='a.png')
	webhook.execute()

# Uploads question to both webhooks
def upload_question(driver, url):
	driver.get(url)

	try:
		details = driver.execute_script(get_question_details)

		upload_question_content(driver, url, details)
		upload_question_screenshot(driver, url, details)

		print(f'Successfully uploaded question {url}')
	except Exception as exception:
		print(f'Failed to upload question: {exception}')

# Tracks untracked questions from the home page
def update(driver):
	urls = get_urls(driver)
	tracked = saver.get_tracked()

	for url in reversed(urls):
		question_id = extract_id(url)

		print(f'Scanning question {question_id}')

		if question_id in tracked:
			continue

		upload_question(driver, url)
		tracked.append(question_id)

	saver.save_tracked(tracked)

# Setups, controls and exits the driver
def main():
	driver = setup_driver()

	while True:
		# handling exceptions? bruh just put that shit into try and forget
		try:
			update(driver)
		except Exception as exception:
			print(f'Failed to update driver: {exception}')

		sleep(40)

	driver.quit()

if __name__ == "__main__":
	main()
