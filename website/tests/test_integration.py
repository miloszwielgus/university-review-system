import pytest
#from __init__py import create_app, db
from .. import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import time
import multiprocessing
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys



@pytest.fixture
def selenium_driver():
    # First install selenium on WSL using `install_selenium.sh`

    # Set up Chrome options for running in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode

    # Set up the WebDriver with the specified Chrome options
    driver = webdriver.Chrome(options=chrome_options)
    return driver

@pytest.fixture
def flask_server(app):
    def run_flask_app():
        app.run(debug=True)

    # Create a multiprocessing process for Flask app
    flask_process = multiprocessing.Process(target=run_flask_app)

    # Start the Flask app process
    flask_process.start()

    # Wait for the Flask app to initialize (optional)
    time.sleep(5) # :)

    yield

    # Terminate the Flask app process
    flask_process.terminate()

def test_empty_list_courses_button(selenium_driver, flask_server):
    # Open the website
    selenium_driver.get('http://127.0.0.1:5000')

    # Find the button element using its ID
    button = WebDriverWait(selenium_driver, 10).until(EC.presence_of_element_located((By.ID, 'process_input')))

    # Click the button
    button.click()

    # Find the <div> element with ID 'course_list' and retrieve its inner HTML
    course_list_element = selenium_driver.find_element(By.ID, 'course_list')
    html_for_course_list = course_list_element.get_attribute('innerHTML')

    assert html_for_course_list == ""

def test_list_courses_button(selenium_driver, flask_server):
    # Open the website
    selenium_driver.get('http://127.0.0.1:5000')

    # Find the option element corresponding to 'Bydgoszcz' and click it
    WebDriverWait(selenium_driver, 30).until(
    expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".select2-container .select2-selection")))
    selenium_driver.find_element(By.CSS_SELECTOR, ".select2-container .select2-selection").click()
    selenium_driver.find_element(By.XPATH, "//li[contains(text(), 'Bydgoszcz')]").click()
    selenium_driver.find_element(By.ID, "process_input").click()

    # Find the <div> element with ID 'course_list' and retrieve its inner HTML
    course_list_element = selenium_driver.find_element(By.ID, 'course_list')
    html_for_course_list = course_list_element.text

    assert html_for_course_list == (
         'Administracja\n'
         'Uniwersytet Kazimierza Wielkiego w Bydgoszczy\n'
         'Tytuł: licencjat (6 semestrów)\n'
         'Typ: I stopnia\n'

         'Biologia\n'
         'Uniwersytet Kazimierza Wielkiego w Bydgoszczy\n'
         'Tytuł: licencjat\n'
         'Typ: I stopnia'
    )

    # Close the WebDriver
    selenium_driver.quit()

@pytest.fixture
def app():
    app = create_app()
    app.config['PROPAGATE_EXCEPTIONS'] = True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()