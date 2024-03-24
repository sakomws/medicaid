import requests
import json
import os

fw_api_key = os.environ["FIREWORKS_API_KEY"]
url = "https://api.fireworks.ai/inference/v1/completions"
payload = {
  "model": "accounts/sahriyarm-b6065d/models/1bc4ef642865488692d371896b7aebc2",
  "max_tokens": 512,
  "top_p": 1,
  "top_k": 40,
  "presence_penalty": 0,
  "frequency_penalty": 0,
  "temperature": 0.1,
  "prompt": "hey"
}
headers = {
  "Accept": "application/json",
  "Content-Type": "application/json",
  "Authorization": "Bearer "+fw_api_key
}
result=requests.request("POST", url, headers=headers, data=json.dumps(payload))

print(json.dumps(result.json(), indent=4))