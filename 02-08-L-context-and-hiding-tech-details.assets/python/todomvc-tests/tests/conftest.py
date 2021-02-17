import pytest
from selene.support.shared import browser


@pytest.fixture(scope='function', autouse=True)
def browser_setup():
    browser.config.set_value_by_js = True
