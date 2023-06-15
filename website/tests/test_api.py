import pytest
from .. import *

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

@pytest.mark.parametrize("tag", ['head', 'home', 'href', 'body'])
def test_university_page_loading(tag, client):
    check_page_loading(client, '/university_list')

@pytest.mark.parametrize("tag", ['head', 'home', 'href', 'body'])
def test_university_page_includes_tags(tag, client):
    check_page_includes_tags(tag, client, '/university_list')

@pytest.mark.parametrize("tag", ['head', 'home', 'href', 'body'])
def test_compare_page_loading(tag, client):
    check_page_loading(client, '/compare')

@pytest.mark.parametrize("tag", ['head', 'home', 'href', 'body'])
def test_compare_page_includes_tags(tag, client):
    check_page_includes_tags(tag, client, '/compare')


@pytest.mark.parametrize("tag", ['head', 'home', 'href', 'body'])
def test_compare_page_loading(tag, client):
    check_page_loading(client, '/top_universities')

@pytest.mark.parametrize("tag", ['head', 'home', 'href', 'body'])
def test_compare_page_includes_tags(tag, client):
    check_page_includes_tags(tag, client, '/top_universities')


