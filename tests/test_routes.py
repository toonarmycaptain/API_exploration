""" Test main routes. """
import pytest


def test_favicon(test_client):
    """Should return favicon."""
    response = test_client.get('/favicon.ico')
    assert response.status_code == 302
    assert response.headers['Location'] in 'http://localhost/static/favicon.ico?mimetype=image/vnd.microsoft.icon'


def test_base_url_redirects_to_home(test_client):
    """Base url should go to home page."""
    response = test_client.get('/')
    assert response.status_code == 301
    assert response.headers['Location'] in 'http://localhost/home/'


def test_bare_base_url_redirects_to_home(test_client):
    """Base url without / should redirect to home page."""
    response = test_client.get('')
    assert response.status_code == 308
    assert response.headers['Location'] in 'http://localhost/'

    # Ensure home page loaded.
    response = test_client.get('', follow_redirects=True)
    assert response.status_code == 200
    assert b"Home - toonarmycaptain API exploration" in response.data


@pytest.mark.parametrize('route',
                         ['home',
                          'xkcd',
                          ])
def test_subpage_routes_without_trailing_slash_redirects(test_client,
                                                         route):
    """Subpage routes without / redirect."""
    response = test_client.get(route)
    assert response.status_code == 308
    assert response.headers['Location'] == f'http://localhost/{route}/'


@pytest.mark.parametrize('route, page_title',
                         [('home', b'Home'),
                          ('xkcd', b'xkcd'),
                          ])
def test_subpage_internal_routes(test_client,
                                 route, page_title):
    """Subpages load content."""
    response = test_client.get(f'{route}/')
    assert response.status_code == 200
    # Equivalent to assert 'some string' in str(response.data)
    assert b' - toonarmycaptain API exploration' in response.data
    assert page_title in response.data
