import requests

res=requests.post('http://127.0.0.1:5000/send',json={'test':True})

print(res.text)
