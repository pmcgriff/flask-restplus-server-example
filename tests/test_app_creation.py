# encoding: utf-8
# pylint: disable=missing-docstring
import pytest

from app import CONFIG_NAME_MAPPER, create_app


def test_create_app():
    with pytest.raises(SystemExit):
        create_app()

@pytest.mark.parametrize('flask_config_name', ['production', 'development', 'testing'])
def test_create_app_passing_flask_config_name(flask_config_name):
    create_app(flask_config_name=flask_config_name)

@pytest.mark.parametrize('flask_config_name', ['production', 'development', 'testing'])
def test_create_app_passing_FLASK_CONFIG_env(flask_config_name):
    import os
    assert 'FLASK_CONFIG' not in os.environ
    os.environ['FLASK_CONFIG'] = flask_config_name
    create_app()
    del os.environ['FLASK_CONFIG']

def test_create_app_with_conflicting_config():
    import os
    assert 'FLASK_CONFIG' not in os.environ
    os.environ['FLASK_CONFIG'] = 'production'
    with pytest.raises(AssertionError):
        create_app('development')
    del os.environ['FLASK_CONFIG']

def test_create_app_with_non_existing_config():
    with pytest.raises(KeyError):
        create_app('non-existing-config')

def test_create_app_with_broken_import_config():
    CONFIG_NAME_MAPPER['broken-import-config'] = 'broken-import-config'
    with pytest.raises(ImportError):
        create_app('broken-import-config')
    del CONFIG_NAME_MAPPER['broken-import-config']
