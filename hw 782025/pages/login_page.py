# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium import webdriver
# from pages.base_page import BasePage
# from utils.config_reader import ConfigReader


# class LoginPage(BasePage):
#     def __init__(self, driver):
#         super().__init__(driver)
#         self.username_field = (By.NAME, 'username')
#         self.password_field = (By.NAME, 'password')
#         self.login_button = (By.XPATH, "//button[@type='submit']")

#     def enter_username(self, username: str):
#         username_input = WebDriverWait(self.driver, 10).until(
#             lambda d: d.find_element(*self.username_field)
#         )
#         username_input.send_keys(username)

#     def enter_password(self, password: str):
#         password_input = WebDriverWait(self.driver, 10).until(
#             lambda d: d.find_element(*self.password_field)
#         )
#         password_input.send_keys(password)

#     def click_login(self):
#         login_button = WebDriverWait(self.driver, 10).until(
#             lambda d: d.find_element(*self.login_button)
#         )
#         login_button.click()

#     def do_login(self, username, password):
#         self.enter_username(username)
#         self.enter_password(password)
#         self.click_login()

#     def load(self):
#         self.driver.get(ConfigReader.get_base_url())

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.config_reader import ConfigReader

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.username_field = (By.NAME, 'username')
        self.password_field = (By.NAME, 'password')
        self.login_button = (By.XPATH, "//button[@type='submit']")

    def enter_username(self, username: str):
        self.send_keys(self.username_field, username)

    def enter_password(self, password: str):
        self.send_keys(self.password_field, password)

    def click_login(self):
        self.click(self.login_button)

    def do_login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def load(self):
        self.driver.get(ConfigReader.get_base_url())
