import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_test import BaseTest
from pages.login_page import LoginPage
from time import sleep
from utils.config_reader import ConfigReader
import allure

@pytest.mark.usefixtures("setup")

class Test_Login(BaseTest):
    @allure.story("Valid Login")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_success(self):
        login_page = LoginPage(self.driver)
        login_page.load()
        login_page.do_login(ConfigReader.get_username(), ConfigReader.get_password())
        sleep(5)
        assert "/dashboard" in self.driver.current_url.lower()
        print("Successful Login!")
    

    @allure.story("Invalid Username")
    def test_login_invalid_username(self):
        login_page = LoginPage(self.driver)
        login_page.load()
        login_page.do_login(ConfigReader.get_invalid_username(), ConfigReader.get_password())
        error_locator = (By.XPATH, "//p[contains(@class,'oxd-alert-content-text')]")
        error_element = WebDriverWait(self.driver, 3).until(
        EC.visibility_of_element_located(error_locator)
        )
        assert "Invalid credentials" in error_element.text
        print("Invalid username!")

    @allure.story("Blank Username")
    def test_login_invalid_password(self):
        login_page = LoginPage(self.driver)
        login_page.load()
        login_page.do_login(ConfigReader.get_blank_username(), ConfigReader.get_password())
        error_locator = (By.CLASS_NAME, "oxd-input-field-error-message")
        error_element = WebDriverWait(self.driver, 3).until(
        EC.visibility_of_element_located(error_locator)
        )
        assert "Required" in error_element.text
        print("Blank username!")
