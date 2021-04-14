"""Test app fixture"""
from pathlib import Path

import pytest

from flask import Flask

from API_exploration import create_app

default_test_config = {'SECRET_KEY': b'some secret key',

                       'TESTING': True,
                       'WTF_CSRF_METHODS': set(),
                       'WTF_CSRF_ENABLED': False,
                       }


def app_with_test_config(db_dir_path: Path) -> Flask:
    """
    Instantiate app with given config.

    :param db_dir_path: Path to dir containing test db.
    :return: Flask app
    """
    app = create_app(test_config=default_test_config)
    assert app.config['WTF_CSRF_ENABLED'] is False
    return app


@pytest.fixture
def test_app(tmpdir):
    """Return app-providing function."""
    yield app_with_test_config(tmpdir)


def test_app_fixture(test_app):
    for key, value in default_test_config.items():
        assert test_app.config[key] == value


@pytest.fixture
def test_client(test_app):
    return test_app.test_client()
