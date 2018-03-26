import requests
import json
fp = open("Block.py",'rb')
headers = {'Content-type': 'multipart/form-data'}
# r = requests.post("http://127.0.0.1:5000/txion",json={"type":"tx","from":"123","to":"233","amount":"10000"},data=)
files = {
     'json': ("json", json.dumps({"type":"model_data","filename":"Block.py"}), 'application/json'),
     'file': ("Block.py", open("Block.py", 'rb'), 'application/octet-stream')
}
# r = requests.post("http://127.0.0.1:5000/getStates",files=files)
r = requests.get("http://127.0.0.1:5000/getStates")
print r.text
r = requests.get("http://127.0.0.1:5000/getBlock")
print r.text
# r = requests.post("http://127.0.0.1:5000/txion",json={"type":"tx","from":"123","to":"233","amount":"10000","nonce":0})
# print r.text
r = requests.post("http://127.0.0.1:5000/mine")
print r.text
