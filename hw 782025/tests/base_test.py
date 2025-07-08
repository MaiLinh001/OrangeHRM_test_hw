import sys
# import os
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from utils.config_reader import ConfigReader
import allure

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_call", rep)

class BaseTest:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, request):
        s = Service(executable_path="D:\\chromedriver-win64\\chromedriver.exe")
        self.driver = webdriver.Chrome(service=s)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        request.cls.driver = self.driver
        yield
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=f"failure_{request.node.name}",
                attachment_type=allure.attachment_type.PNG
            )
        self.driver.quit()

    