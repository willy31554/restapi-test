import requests
import json
import pandas as pd
from datetime import datetime, timedelta

# Replace with the actual API endpoint
api_url = 'http://192.168.20.86:8080/score/ke'  # Replace with your API URL

# Read parameters from an Excel file
excel_file = 'parameters.xlsx'  # Replace with the path to your Excel file
parameters_df = pd.read_excel(excel_file)

# Function to assert a condition and display the result
def assert_and_display(condition, message):
    if condition:
        print(f"Assertion PASSED: {message}")
        return True
    else:
        print(f"Assertion FAILED: {message}")
        return False

# Function to assert field presence and data types
def assert_field(data, field_name, expected_data_type):
    if field_name in data:
        actual_data_type = type(data[field_name])
        assert_and_display(actual_data_type == expected_data_type,
                           f"'{field_name}' is present and has data type {actual_data_type.__name__}.")
    else:
        assert_and_display(False, f"'{field_name}' is missing.")

# Function to check if an account should be excluded based on conditions
def should_exclude_account(account):
    if account["account_status"] == "Closed" and \
            account["days_in_arrears"] == 0 and \
            datetime.strptime(account["loaded_at"], "%Y-%m-%d").year <= datetime.now().year - 5:
        return True
    return False

# Loop through the rows in the Excel file
for index, row in parameters_df.iterrows():
    # Extract parameters from the Excel file
    identity_number = row['identity_number']
    identity_type = row['identity_type']
    report_type = row['report_type']

    # Make a GET request to the API with parameters
    params = {
        'identity_number': identity_number,
        'identity_type': identity_type,
        'report_type': report_type
    }
    response = requests.get(api_url, params=params)

    # Check if the API request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        json_response = response.json()

        # Get Delinquency Code from the JSON response
        delinquency_code = json_response.get("delinquency_code")

        if delinquency_code == "002":
            # Check response structure for Delinquency Code '002'
            assert_and_display("account_info" in json_response, "'account_info' field is present.")
            # Add assertions for the fields specific to Delinquency Code '002'

        elif delinquency_code in ["003", "004"]:
            # Check response structure for Delinquency Code '003' or '004'
            assert_and_display("account_info" in json_response, "'account_info' field is present.")
            account_info = json_response.get("account_info")
            if account_info:
                # Initialize counters for Delinquency Codes
                delinquency_counts = {"002": 0, "003": 0, "004": 0, "005": 0}
                # Initialize counter for 'account_npa' with Delinquency Code '004'
                account_npa_count = 0
                # Initialize flag to check exclusion
                exclude_account = False
                for account in account_info:
                    # Assert each field within the "account_info" dictionary
                    assert_field(account, "account_number", str)
                    assert_field(account, "account_status", str)
                    # Add assertions for other fields as needed

                    # Additional assertion to check Delinquency Code within account_info
                    if "delinquency_code" in account:
                        delinquency_counts[account["delinquency_code"]] += 1

                        # Check if 'account_npa' is present and Delinquency Code is '004'
                        if "account_npa" in account and account["delinquency_code"] == "004":
                            account_npa_count += 1

                    # Check if the account should be excluded
                    if should_exclude_account(account):
                        exclude_account = True
                        break

                # Display count of accounts for each Delinquency Code
                for code, count in delinquency_counts.items():
                    print(f"Delinquency Code '{code}': {count} accounts")

                # Assert 'account_npa' count for Delinquency Code '004'
                assert_and_display(account_npa_count == 3, f"'account_npa' count for Delinquency Code '004' is {account_npa_count}")

                # Assert 'reported_name' field based on conditions
                reported_name = json_response.get("reported_name")
                if not reported_name:
                    assert_and_display(False, "'reported_name' is empty.")
                else:
                    assert_field(reported_name, "first_name", str)
                    assert_field(reported_name, "other_name", str)
                    assert_field(reported_name, "surname", str)

                # Check if the account should be excluded
                if exclude_account:
                    assert_and_display(False, "Excluded account found based on conditions.")
            else:
                assert_and_display(False, "'account_info' is missing or empty for Delinquency Code '003' or '004'.")

        else:
            print(f"Unknown Delinquency Code: {delinquency_code}")

        # Assert data types for other fields in the response
        assert_field(json_response, "api_code", str)
        assert_field(json_response, "api_code_description", str)
        assert_field(json_response, "credit_score", int)
        assert_field(json_response, "delinquency_code", str)
        assert_field(json_response, "has_error", bool)
        assert_field(json_response, "has_fraud", bool)
        assert_field(json_response, "identity_number", str)
        assert_field(json_response, "identity_type", str)
        assert_field(json_response, "is_gurantor", bool)
    else:
        print(f"API request failed with status code: {response.status_code}")
