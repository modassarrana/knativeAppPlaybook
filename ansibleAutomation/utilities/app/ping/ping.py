import os
import json
import time
from flask import Flask , request

app = Flask(__name__)

@app.route('/ping',methods=['POST'])

def ping():
    req_data = request.get_json(force=True)
    ip = req_data["ip"]
    #validate whether user has passed IP string
    if not ip.strip():
        data = {
                 'status': 'ERROR',
                 'msg': 'IP string is empty. Pass the Json with IP value',
                 'ip': ip
        }
        resp = json.dumps(data)
        return '{}\n'.format(resp)
    res = os.system("ping -c 2 " + ip)
    if res == 0:
        data = {
                 'status': 'SUCCESS',
                 'msg': 'HOST is pinging',
                 'ip': ip
        }
        resp = json.dumps(data)
        time.sleep(5)
        return '{}\n'.format(resp)
    else:
        data = {
                 'status': 'ERROR',
                 'msg': 'HOST is not reachable',
                 'ip': ip
        }
        resp = json.dumps(data)
        return '{}\n'.format(resp)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
