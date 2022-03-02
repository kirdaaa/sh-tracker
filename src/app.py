import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from discord_webhook import DiscordWebhook
from pathlib import Path
from time import sleep

with open('webhook.txt', 'r') as file:
    webhook_url = file.read()

# Loads JavaScript code that can be executed using driver.execute_script()
def load_script(name):
    with open('src/' + name, 'r') as file:
        return file.read()

clean_question = load_script('clean_question.js')
get_question_details = load_script('get_question_details.js')

# Returns ID of last tracked question
def can_upload(question_id):
    path = Path('l_id.txt')

    if not path.is_file():
        return True

    with open(path.name, 'r') as file:
        content = file.read()

    try:
        return question_id > int(content)
    except:
        return True

# Saves question ID to a text file, this is to keep track of where the tracker
# stopped last time
def save_upload(question_id):
    with open('l_id.txt', 'w') as file:
        file.write(str(question_id))

# Setups Firefox browser application
def setup_driver():
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')

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

# Returns URLs of 20 newest questions on the home page
def get_urls(driver):
    driver.get('https://scriptinghelpers.org/')

    urls = []

    for element in driver.find_elements(By.CLASS_NAME, 'q-link'):
        anchor = element.find_element(By.TAG_NAME, 'a')
        url = anchor.get_attribute('href')

        urls.append(url)

    return urls

# Uploads question screenshot to the webhook
def upload_question(driver, url):
    global webhook_url

    driver.get(url)

    details = driver.execute_script(get_question_details)
    element = driver.execute_script(clean_question)

    time = details['time']

    webhook = DiscordWebhook(
        url=webhook_url,
        content=f'<@&920585996519735306> <t:{time}:R>\n<{url}>',
        username=get_username(details),
        avatar_url=details['avatar']
    )

    webhook.add_file(file=element.screenshot_as_png, filename='a.png')
    webhook.execute()

# Tracks untracked questions from the home page
def update(driver):
    urls = get_urls(driver)

    for url in reversed(urls):
        question_id = extract_id(url)

        if not can_upload(question_id):
            continue

        try:
            upload_question(driver, url)
            save_upload(question_id)
        except Exception as exception:
            print(f'Failed to upload question: {exception}')

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
