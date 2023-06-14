import pytest
#from __init__py import create_app, db
from .. import *

@pytest.fixture
def app():
    app = create_app()
    app.config['PROPAGATE_EXCEPTIONS'] = True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page_loading(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.text

def test_university_page_loading(client):
    response = client.get('/university_list')
    assert response.status_code == 200
    assert response.text

def test_compare_page_loading(client):
    response = client.get('/compare')
    assert response.status_code == 200
    assert response.text

def test_top_universities_page_loading(client):
    response = client.get('/top_universities')
    assert response.status_code == 200
    assert response.text

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
    pass