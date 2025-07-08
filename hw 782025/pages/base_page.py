from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.config_reader import ConfigReader

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = ConfigReader.get_implicit_timeout()

    def wait_element(self, locator):
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            print(f"[Timeout] Element {locator} not found in {self.timeout}s")
            return None

    def click(self, locator):
        element = self.wait_element(locator)
        if element:
            element.click()

    def send_keys(self, locator, keys):
        element = self.wait_element(locator)
        if element:
            element.send_keys(keys)