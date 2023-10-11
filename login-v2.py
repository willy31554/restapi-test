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

        # Wait for the dashboard page to load (or some expected condition)
        dashboard_title = wait.until(EC.title_contains("Dashboard"))
        
        # Assert that we are redirected to a dashboard page
        self.assertTrue(dashboard_title)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
