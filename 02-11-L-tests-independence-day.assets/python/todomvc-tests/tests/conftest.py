import pytest
from selene import have
from selene.support.shared import browser


def pytest_addoption(parser):
    parser.addoption('--base_url', default='http://todomvc4tasj.herokuapp.com/', action='store')
    parser.addoption('--timeout', default=6, type=float, action='store')
    parser.addoption('--save_page_source_on_failure', default=True, type=bool, action='store')


@pytest.fixture(scope='function', autouse=True)
def browser_setup(request):
    def option(name):
        return request.config.getoption(f'--{name}')

    browser.config.base_url = option('base_url')
    browser.config.timeout = option('timeout')
    browser.config.save_page_source_on_failure = \
        option('save_page_source_on_failure')
    browser.config.set_value_by_js = True


# @pytest.fixture(scope='function', autouse=True)
# @pytest.fixture
# def with_cleared_storage_after():
#
#     yield
#
#     browser.clear_local_storage()


def open_app():
    browser.open('') \
        .should(have.js_returned(True,
             'return ($._data($("#clear-completed").get(0), "events")'
             '.hasOwnProperty("click") && '
             '(Object.keys(require.s.contexts._.defined).length === 39))'))


@pytest.fixture
def open_fresh_app():
    if browser.matching(have.url_containing('todomvc')):
        browser.clear_local_storage()
        open_app()
    else:
        open_app()


@pytest.fixture
def clear_data_after_each_test():

    yield

    browser.clear_local_storage()


# @pytest.mark.usefixtures('open_app', 'clear_data_after_each_test')
@pytest.mark.usefixtures('open_fresh_app')
class AtTodoMvcWithClearedStorageAfterEachTest:
    pass
