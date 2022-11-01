import logging
from os import path, environ
from typing import Union

import pytest
from _pytest.config import Config, ExitCode

logger = logging.getLogger(__name__)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: Config):
    """ Setup framework loggers levels """
    loggers = {
        'urllib3.connectionpool': logging.INFO,
        'selenium.webdriver.remote.remote_connection': logging.INFO,
        'faker.factory': logging.INFO,
    }
    for logger_name, log_level in loggers.items():
        logging.getLogger(logger_name).setLevel(log_level)


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session: pytest.Session, exitstatus: Union[int, ExitCode]) -> None:
    """ Save environment variables for allure """
    allure_dir = session.config.getoption('allure_report_dir', None)
    if allure_dir:
        allure_env_file = path.join(allure_dir, 'environment.properties')
        logger.info(f'Save environment variables for Allure Report to: {allure_env_file}')
        with open(allure_env_file, 'w') as ef:
            for ev in sorted(environ.keys()):
                ef.write(f'{ev}={environ.get(ev)}\n')


def pytest_addoption(parser):
    parser.addoption('-H', '--headless', action='store_true', default=False, help='Run browser in headless mode')


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """ Making test result information available in fixtures

    https://docs.pytest.org/en/7.1.x/example/simple.html#making-test-result-information-available-in-fixtures
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f'rep_{rep.when}', rep)
