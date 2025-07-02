from selenium.webdriver.common.by import By
from time import sleep
from tests.base_test import BaseTest
from pages.login_page import LoginPage

class Test_Login(BaseTest):
    def test_login_valid_user(self):
        self.driver.find_element(By.NAME, "username").send_keys("Admin")
        self.driver.find_element(By.NAME, "password").send_keys("admin123")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        sleep(5)
        assert "dashboard" in self.driver.current_url.lower()
        print("Login successful!")

    def test_login_wrong_username(self):
        self.driver.find_element(By.NAME, "username").send_keys("SaiTen")
        self.driver.find_element(By.NAME, "password").send_keys("admin123")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        sleep(5)
        error_msg = self.driver.find_element(By.XPATH, "//p[@class='oxd-text oxd-text--p oxd-alert-content-text']").text
        assert "Invalid credentials" in error_msg
        print("Wrong username!")

    def test_login_wrong_password(self):
        self.driver.find_element(By.NAME, "username").send_keys("Admin")
        self.driver.find_element(By.NAME, "password").send_keys("wrong_password")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        sleep(5)
        error_msg = self.driver.find_element(By.XPATH, "//p[@class='oxd-text oxd-text--p oxd-alert-content-text']").text
        assert "Invalid credentials" in error_msg
        print("Wrong password!")

    def test_blank_username(self):
        self.driver.find_element(By.NAME, "password").send_keys("admin123")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        sleep(5)
        error_msg = self.driver.find_element(By.CLASS_NAME, "oxd-input-field-error-message").text
        assert "Required" in error_msg
        print("Blank username!")

    def test_blank_password(self):
        self.driver.find_element(By.NAME, "username").send_keys("Admin")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        sleep(5)
        error_msg = self.driver.find_element(By.CLASS_NAME, "oxd-input-field-error-message").text
        assert "Required" in error_msg
        print("Blank password!")

    def test_blank_both(self):
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        sleep(5)
        error_msges = self.driver.find_elements(By.CLASS_NAME, "oxd-input-field-error-message")
        assert len(error_msges) == 2
        assert error_msges[0].text == "Required"
        assert error_msges[1].text == "Required"
        print("Blank username and password!")
        
