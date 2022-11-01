from app_settings import AppSettings

cfg = AppSettings()

DEFAULT_TIMEOUT = cfg.webdriver.timeouts.explicit_wait
PAGE_LOAD_TIMEOUT = cfg.webdriver.timeouts.page_load
