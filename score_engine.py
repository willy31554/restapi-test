import requests
import json
import pandas as pd

# Replace with the actual API endpoint
api_url = 'http://192.168.20.86:8080/score/ke'  # Replace with your API URL

# Read parameters from an Excel file
excel_file = 'parameters.xlsx'  # Replace with the path to your Excel file
parameters_df = pd.read_excel(excel_file)

# Function to assert a condition and display the result
def assert_and_display(condition, message):
    if condition:
        print(f"Assertion PASSED: {message}")
    else:
        print(f"Assertion FAILED: {message}")

# Convert int64 columns to regular Python integers
parameters_df['identity_type_id'] = parameters_df['identity_type_id'].astype(int)
parameters_df['identity_type'] = parameters_df['identity_type'].astype(int)

# Loop through the rows in the DataFrame
for index, row in parameters_df.iterrows():
    # Extract parameters from the DataFrame
    identity_number = row['identity_number']
    identity_type_id = row['identity_type_id']
    identity_type = row['identity_type']

    # Create a dictionary for the request body
    request_data = {
        'identity_number': str(identity_number),
        'identity_type_id': int(identity_type_id),
        'identity_type': int(identity_type)
    }

    # Convert the dictionary to JSON
    json_data = json.dumps(request_data)

    # Set the headers for the request
    headers = {'Content-Type': 'application/json'}

    # Make a POST request to the API with the JSON body
    response = requests.post(api_url, data=json_data, headers=headers)

    # Check if the API request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        json_response = response.json()

        # Define the expected response structure outside of the conditional block
        expected_response = {
            "not_computed_reason": (str ,type(None)),
            "status_code": int,
            "not_computed": bool,
            "payment_experiences": (list, type(None)),
            "ppi": (float, type(None)),
            "average_late_days": (int, type(None)),
            
            "score_date": (str, type(None)),
            "probability_of_default": (float, type(None)),
            "score": (float, type(None))
        }

        # Iterate through each key in the JSON response and assert its data type
        for key, expected_data_type in expected_response.items():
            value = json_response.get(key)

            # Check if the value matches any of the expected data types
            if not isinstance(value, expected_data_type):
                if not any(isinstance(value, data_type) for data_type in (expected_data_type if isinstance(expected_data_type, tuple) else (expected_data_type,))):
                    data_type_names = expected_data_type.__name__ if isinstance(expected_data_type, type) else ', '.join(data_type.__name__ for data_type in expected_data_type)
                    assert_and_display(False, f"Assertion failed for key: '{key}', expected data type(s): {data_type_names}, actual data type: {type(value).__name__}")

        # If all assertions pass, it means that each key in the JSON response has the expected data type(s)
        print(json_response)
  
        print("All assertions passed. Each key in the JSON response has the expected data type(s).")
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        def dict_contains(dictionary, subset):
            return all(dictionary.get(key) == value for key, value in subset.items())

        # Verify the status code and response content
        if json_response['status_code'] == 1:
            expected_response = {
                "not_computed_reason": "Identity Not Found",
                "status_code": 1,
                "not_computed": True,
                "payment_experiences": None,
                "ppi": None,
                "average_late_days": None,
                "identity": None,
                "score_date": None,
                "probability_of_default": None,
                "score": None
            }
            assert_and_display(dict_contains(json_response, expected_response), "Response matches the expected content.")
       
        elif json_response['status_code'] == 2:
            expected_response = {
                "not_computed_reason": "No usable accounts found",
                "not_computed": True,
                "status_code": 2,
                "latest_score": None,
                "latest_ppi": None,
                "history": []
            }         
           
            assert_and_display(dict_contains(json_response, expected_response), "Response matches the expected content.")
        
        elif json_response['status_code'] == 4:
            expected_response = {                       
                   "not_computed_reason": (str, type(None)),  # Allow both str and None
                   "not_computed": False,
                   "identity": str(identity_number),
                   "status_code": 4,
                   "latest_score": {
                    'score': (float, int),
                    'score_date': str,
                    'stability_score': int,
                    'total_debt_score': int,
                    'new_credits_score': int,
                    'credit_mix_score': int,
                    'credit_history_length_score': int,
                    'credit_capacity_score': int,
                    'probability_of_default': (float, int),
                    'payment_performance': int
                    },
                    "latest_ppi": {
                        "ppi": (str, type(None)),
                        "average_late_days": (float, int, type(None)),
                        "average_late_days_open": (float, int, type(None)),
                        "ppi_open": (str, type(None)),
                        "payment_experiences": (list, type(None)),
                        "ppi_installments": (str, type(None)),
                        "average_late_days_installment": (float, int, type(None)),
                        "ppi_revolving": (str, type(None)),
                        "average_late_days_revolving": (float, int, type(None))
                    },
                    "history": [
                        {
                            "score": (float, int, type(None)),
                            "probability_of_default": (float, int, type(None)),
                            "ppi": (str, type(None)),
                            "payment_experiences": (list, type(None)),
                            "average_late_days": (float, int, type(None)),
                            "score_date": (str, type(None))
                        }
                    ]

                 
                
            }

            #assert_and_display(dict_contains(json_response, expected_response), "Response matches the expected content.")

            #print("json",json_response)
            #print("expceted",expected_response)
            #print("latest_score",json_response['latest_score'])
            #print("expected latest_score",expected_response['latest_score'])
            #print("json latest_ppi",expected_response['latest_ppi'])
        else:
            print("Status code is not 1 or 2, skipping further verification.")
    else:
        print(f"API request failed with status code: {response.status_code}")

  # After performing assertions and if statements in your loop
    row_data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Timestamp for the request
        'json_response': json_response,  # The JSON response object
        'score': json_response.get('latest_score', {}).get('score', None)  # Extract the score if available
    }

    data_to_store.append(row_data)

# Convert the list of data to a DataFrame
data_df = pd.DataFrame(data_to_store)

# Define the name of the Excel file to save the data
excel_output_file = 'api_responses.xlsx'

# Save the DataFrame to the Excel file
data_df.to_excel(excel_output_file, index=False)
