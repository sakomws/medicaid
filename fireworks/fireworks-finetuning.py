# set up Fireworks.ai Key
import os
import requests
import json

fw_api_key = os.environ["FIREWORKS_API_KEY"]

url = "https://api.fireworks.ai/inference/v1/completions"
payload = {
  "model": "accounts/sahriyarm-b6065d/models/1bc4ef642865488692d371896b7aebc2",
  "max_tokens": 4096,
  "prompt": "What is the applicant's marital status?"
}
headers = {
  "Accept": "application/json",
  "Content-Type": "application/json",
  "Authorization": "Bearer " + fw_api_key
}

# Execute the POST request
response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

# Ensure the response status code is 200 (OK)
if response.status_code == 200:
    # Print the response in a prettified JSON format
    print(json.dumps(response.json(), indent=4))
else:
    # Print an error message if the API call was unsuccessful
    print(f"Failed to get a response, status code: {response.status_code}")