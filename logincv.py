import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import logging

# Configure logging to print to the console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


# Specify the path to the ChromeDriver executable (replace with your path)
chrome_driver_path = 'C:\\Users\\Admin\\Downloads\\chromedriver-win64\\chromedriver.exe'
webdriver.chrome.service.Service().chromedriver_executable = chrome_driver_path

# Create a WebDriver instance using Chrome
browser = webdriver.Chrome()

# Rest of your code...

# Define the URL of the login page
login_url = 'https://practicetestautomation.com/practice-test-login/'  # Replace with the actual login page URL

# Function to perform login test

# ... Your previous code ...

# Function to perform login test
# ... Your previous code ...

# Function to perform logout
# Function to perform logout
def perform_logout():
    try:
        # Find and click the logout button using CSS selector
        logout_button = browser.find_element(By.CSS_SELECTOR, '#loop-container > div > article > div.post-content > div > div > div > a')
        logout_button.click()
        logging.info("Clicked logout button")
    except NoSuchElementException:
        logging.error("Logout button not found")


# Function to perform login test
def perform_login(username, password):
    # Log the input values (username and password)
    logging.info(f"Logging in with username: {username}, password: {password}")

    # Open the login page
    browser.get(login_url)
    logging.info("Opened login page")

    # Find and fill the username and password fields using CSS selectors
    username_field = browser.find_element(By.CSS_SELECTOR, '#username')
    password_field = browser.find_element(By.CSS_SELECTOR, '#password')

    username_field.send_keys(username)
    password_field.send_keys(password)
    logging.info("Entered username and password")

    # Find and click the login button using CSS selector
    login_button = browser.find_element(By.CSS_SELECTOR, '#submit')
    login_button.click()
    logging.info("Clicked login button")

    try:
        # Wait for the success message to appear
        wait = WebDriverWait(browser, 30)
        success_message = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.success')))
        
        # Check if the success message is displayed
        if success_message.is_displayed():
            logging.info("Login successful")
            # Validate the URL after successful login
            if browser.current_url == 'https://practicetestautomation.com/logged-in-successfully/':
                logging.info("URL after login is correct")
                # Perform logout after successful login
                perform_logout()
                return "Passed"
            else:
                logging.error("URL after login is incorrect")
                return "Failed"
    except TimeoutException:
        # Handle the case of a failed login
        error_message = browser.find_elements(By.CSS_SELECTOR, '#error')
        if error_message:
            if error_message[0].text.strip() == "Your username is invalid!":
                logging.error("Invalid username or password")
            else:
                logging.error("Login failed")
            return "Failed"
        else:
            # If there is no error message element, consider it a successful login
            logging.info("Login successful without error message")
            # Validate the URL after successful login
            if browser.current_url == 'https://practicetestautomation.com/logged-in-successfully/':
                logging.info("URL after login is correct")
                # Perform logout after successful login
                perform_logout()
                return "Passed"
            else:
                logging.error("URL after login is incorrect")
                return "Failed"




# Read test data from the CSV file
csv_file_path = 'test_data.csv'  # Replace with the path to your CSV file

with open(csv_file_path, 'r', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    
    for row in csv_reader:
        print(row)
        username = row['username']
        password = row['password']
        expected_result = row['expected_result']
        result = perform_login(username, password)

        # Print the result of each test case
        print(f'Test Case - Username: {username}, Password: {password} - Result: {result}')
        
        # Compare the result with the expected outcome
        if result == expected_result:
            print('Test Passed\n')
        else:
            print('Test Failed\n')

# Close the web browser when done
browser.quit()
