import requests
import secrets
import json
host = "https://v6.exchangerate-api.com/v6/"
params = "latest/USD"
url = host + secrets.exchange_rate_api + params
# print(url)
response = requests.get(url)
dict = response.json()
json_file = json.dumps(dict)
text_file = open("exchange_rate_data.json", "w")

text_file.write(json_file)
text_file.close()