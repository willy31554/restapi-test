import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestLogin(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://v2-stage.analytics.metropol.co.ug/")  # Replace with your website URL

    def test_login_valid_credentials(self):
        wait = WebDriverWait(self.driver, 10)  # Initialize WebDriverWait with a timeout of 10 seconds
        
        # Step 1: Enter username
        username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.send_keys("willy.barmasai@metropol.co.ke")
        
        # Step 5: Click password input field
        password_input = wait.until(EC.element_to_be_clickable((By.ID, "textfield-1019-inputEl")))
        password_input.click()
        
        # Step 8: Enter password
        password_input.send_keys("Tume@3154")
        
        # Step 9: Click login button
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "button-1023-btnEl")))
        login_button.click()

            # ... Previous steps ...

        # Step 10: Wait for the target element to be clickable and click it
        after_login_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#widget-creditApplicationManager-1055-innerCt > .descriptiondiv')))
        after_login_element.click()
        
        # Step 11: Click on the specified button
        button_element = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@id="button-1067-btnInnerEl"]')))
        button_element.click()
        
     # Step 15: Click on an element with a specific CSS selector
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#ext-element-23')))
        element.click()
        
        # ... Continue adding the rest of the steps ...

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
