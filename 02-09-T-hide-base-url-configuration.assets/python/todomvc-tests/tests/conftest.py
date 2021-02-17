import pytest
from selene.support.shared import browser


# todo: update commented code
# def pytest_addoption(parser):
#     parser.addoption('--base_url', default='http://todomvc4tasj.herokuapp.com/', action='store')
#     parser.addoption('--timeout', default='6', action='store')
#     parser.addoption('--save_page_source_on_failure', default='True', action='store')
#
#
# @pytest.fixture(scope='function', autouse=True)
# def browser_setup(request):
#     def option(name):
#         return request.config.getoption(f'--{name}')
#
#     browser.config.base_url = option('base_url')
#     browser.config.timeout = float(option('timeout'))
#     browser.config.save_page_source_on_failure = \
#         option('save_page_source_on_failure') == 'True'
#     browser.config.set_value_by_js = True
#
#
# OR ...


# class Option:
#
#     def __init__(self, name, **attributes):
#         self.name = name
#         self.attributes = attributes
#
#     def value(self, from_request) -> str:
#         return from_request.config.getoption(self.name)
#
#     def boolean(self, from_request) -> bool:
#         return self.value(from_request) == 'True'
#
#     def float(self, from_request) -> float:
#         return float(self.value(from_request))
#
#
# def option(**attributes):
#     def wrapper(fun):
#         fun.option = Option(f'--{fun.__name__}', action='store', **attributes)
#         return fun
#     return wrapper
#
# OR...


class Option:

    @staticmethod
    def is_property(field):
        return hasattr(field, 'fget') and hasattr(field.fget, 'option')

    @staticmethod
    def from_property(prop):
        return prop.fget.option

    @staticmethod
    def default(value, **attributes):
        def decorator(fun_on_self_with_request):
            option = Option(
                f'--{fun_on_self_with_request.__name__}',
                action='store',
                default=value,
                type=type(value),
                **attributes)

            def fun(self):
                return option.value(self.request)

            # fun.__name__ = fun_on_self_with_request.__name__
            fun.option = option
            # fun.name = option.name
            # fun.attributes = option.attributes
            # fun.value = fun.option.value

            return property(fun)

        return decorator

    def __init__(self, name, **attributes):
        self.name = name
        self.attributes = attributes

    def value(self, from_request):
        return from_request.config.getoption(self.name)

    def register(self, parser):
        parser.addoption(self.name, **self.attributes)


class Config:

    @classmethod
    def options(cls):
        return [Option.from_property(field) for field in cls.__dict__.values()
                if Option.is_property(field)]

    @classmethod
    def register(cls, parser):
        for option in cls.options():
            option.register(parser)

    def __init__(self, request):
        self.request = request

    @Option.default('http://todomvc4tasj.herokuapp.com/')
    def base_url(self):
        pass

    @Option.default(8.0)
    def timeout(self):
        pass

    @Option.default(True)
    def save_page_source_on_failure(self):
        pass


def pytest_addoption(parser):
    Config.register(parser)


@pytest.fixture
def config(request):
    return Config(request)


@pytest.fixture(scope='function', autouse=True)
def browser_setup(config):

    browser.config.base_url = config.base_url
    browser.config.timeout = config.timeout
    browser.config.save_page_source_on_failure = config.save_page_source_on_failure
    browser.config.set_value_by_js = True
