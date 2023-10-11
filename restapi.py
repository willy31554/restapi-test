import unittest
import requests
import pandas as pd
import time
from openpyxl import Workbook

class TestUserAPI(unittest.TestCase):
    base_url = 'https://reqres.in/api/users'  # Replace with your API endpoint

    # Create a list to store test case information
    test_results = []

    def record_test_result(self, test_case_name, json_object, status_code, response_time):
        self.test_results.append({
            'Test Case': test_case_name,
            'JSON Object': json_object,
            'Status Code': status_code,
            'Response Time': response_time
        })

    def test_get_all_users(self):
        # Test GET request to retrieve all users
        start_time = time.time()
        response = requests.get(self.base_url)
        end_time = time.time()

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check the response JSON content (dictionary with 'data' field)
        response_data = response.json()
        self.assertIsInstance(response_data, dict)

        # Ensure 'data' field is present and is a list
        self.assertIn('data', response_data)
        users_list = response_data['data']
        self.assertIsInstance(users_list, list)

        # Check if 'page' is in the response_data
        page = response_data.get('page')

        # Iterate through each user in the list
        for user in users_list:
            self.assertIsInstance(user, dict)
            self.assertIn('email', user)

        # Record test results
        json_object_str = str(response_data)  # Convert JSON object to a string
        self.record_test_result('test_get_all_users', json_object_str, response.status_code, end_time - start_time)

    def test_get_existing_user_by_id(self):
        # Test GET request to retrieve an existing user by ID
        user_id = 2  # Replace with a valid user ID
        start_time = time.time()
        response = requests.get(f'{self.base_url}/{user_id}')
        end_time = time.time()

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check the response JSON content
        user_data = response.json()
        self.assertIsInstance(user_data, dict)

        # Ensure 'id' and 'email' are present within the 'data' dictionary
        self.assertIn('data', user_data)
        data = user_data['data']
        self.assertIn('id', data)
        self.assertIn('email', data)

        # Record test results
        json_object_str = str(user_data)  # Convert JSON object to a string
        self.record_test_result('test_get_existing_user_by_id', json_object_str, response.status_code, end_time - start_time)

    def test_get_non_existing_user_by_id(self):
        # Test GET request to retrieve a non-existing user by ID
        non_existing_user_id = 9999  # Replace with a non-existing user ID
        start_time = time.time()
        response = requests.get(f'{self.base_url}/{non_existing_user_id}')
        end_time = time.time()

        # Check the response status code (expecting 404 for a non-existing user)
        self.assertEqual(response.status_code, 404)

        # Record test results
        self.record_test_result('test_get_non_existing_user_by_id', None, response.status_code, end_time - start_time)

    def test_create_user(self):
        # Test POST request to create a new user with JSON data
        json_data = {
            "name": "morpheus",
            "job": "leader"
        }
        start_time = time.time()
        response = requests.post(self.base_url, json=json_data)
        end_time = time.time()

        # Check the response status code (expecting 201 for a successful creation)
        self.assertEqual(response.status_code, 201)

        # Check the response JSON content
        user_data = response.json()
        self.assertIsInstance(user_data, dict)
        self.assertIn('name', user_data)
        self.assertIn('job', user_data)

        # Record test results
        json_object_str = str(user_data)  # Convert JSON object to a string
        self.record_test_result('test_create_user', json_object_str, response.status_code, end_time - start_time)

    def test_update_user(self):
        # Test PUT request to update an existing user by ID
        user_id = 2  # Replace with a valid user ID
        json_data = {
            "name": "morpheus",
            "job": "zion resident"
        }
        start_time = time.time()
        response = requests.put(f'{self.base_url}/{user_id}', json=json_data)
        end_time = time.time()

        # Check the response status code (expecting 200 for a successful update)
        self.assertEqual(response.status_code, 200)

        # Check the response JSON content
        user_data = response.json()
        self.assertIsInstance(user_data, dict)
        self.assertIn('name', user_data)
        self.assertIn('job', user_data)

        # Record test results
        json_object_str = str(user_data)  # Convert JSON object to a string
        self.record_test_result('test_update_user', json_object_str, response.status_code, end_time - start_time)

    def test_delete_user(self):
        # Test DELETE request to delete an existing user by ID
        user_id = 2  # Replace with a valid user ID
        start_time = time.time()
        response = requests.delete(f'{self.base_url}/{user_id}')
        end_time = time.time()

        # Check the response status code (expecting 204 for a successful delete)
        self.assertEqual(response.status_code, 204)

        # Record test results (no JSON content for delete request)
        self.record_test_result('test_delete_user', None, response.status_code, end_time - start_time)

if __name__ == '__main__':
    # Create an instance of the test case class and run the tests
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestUserAPI)
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(test_suite)

    # Create and write to an Excel file
    workbook = Workbook()
    sheet = workbook.active

    # Write headers
    headers = ['Test Case', 'JSON Object', 'Status Code', 'Response Time']
    sheet.append(headers)

    # Write test results
    for result in TestUserAPI.test_results:
        row = [result['Test Case'], result['JSON Object'], result['Status Code'], result['Response Time']]
        sheet.append(row)

    # Save the Excel file
    workbook.save('test_results.xlsx')
