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

def test_list_courses_button(selenium_driver, flask_server):
    # Open the website
    selenium_driver.get('http://127.0.0.1:5000')

    # Find the button element using its ID
    button = WebDriverWait(selenium_driver, 10).until(EC.presence_of_element_located((By.ID, 'process_input')))

    # Click the button
    button.click()

    #TODO
    # check html

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

def check_page_loading(client, endpoint):
    response = client.get(endpoint)
    assert response.status_code == 200

@pytest.mark.parametrize("tag", ['head', 'home', 'href', 'body'])
def check_page_includes_tags(tag, client, endpoint):
    response = client.get(endpoint)
    assert tag in response.text

def test_university_page_loading(client):
    check_page_loading(client, '/university_list')

@pytest.mark.parametrize("tag", ['head', 'home', 'href', 'body'])
def test_university_page_includes_tags(tag, client):
    check_page_includes_tags(tag, client, '/university_list')

def test_compare_page_loading(client):
    check_page_loading(client, '/compare')

@pytest.mark.parametrize("tag", ['head', 'home', 'href', 'body'])
def test_compare_page_includes_tags(tag, client):
    check_page_includes_tags(tag, client, '/compare')


def test_compare_page_loading(client):
        check_page_loading(client, '/top_universities')

@pytest.mark.parametrize("tag", ['head', 'home', 'href', 'body'])
def test_compare_page_includes_tags(tag, client):
        check_page_includes_tags(tag, client, '/top_universities')

'''
def test_get_courses(client):
    response = client.get("/get_courses?universityId=Uniwersytet%20Jagielloński%20w%20Krakowie")
    assert response.status_code == 200
    assert response.json == ""

def test_home_page_city_selection(client):
    #TODO
    pass

def test_university_listing(client):
    #response = client.get('/_update_university_list')
    #assert response.status_code == 200
    #assert response.text == ""
    pass'''