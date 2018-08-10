import requests
import time
start = time.time()
for i in range(1000):
    r = requests.get("http://127.0.0.1:3106/g/post")
    #print r

print time.time() - start


