import requests, json

with open('test2.sus', 'r', encoding='utf-8') as f:
    sus = f.read()

data = {"chart": sus}
headers = {'Content-Type': 'application/json'}
response = requests.post(
    "http://localhost:8080/",
    data=json.dumps(data),
    headers=headers)
with open('result.sus', 'w', encoding='utf-8') as f:
    f.write(response.text)