import os
import json
import time
from pysnmp.hlapi import *
from flask import Flask , request

app = Flask(__name__)

@app.route('/uptime',methods=['POST'])

def uptime():
    req_data = request.get_json(force=True)
    
    ip = req_data["ip"]
    # check ip is null
    if not ip.strip():
        data = {
                'status': 'ERROR',
                'msg': 'IP value is empty. Pass input Json with IP',
                'ip': ip
        }
        resp = json.dumps(data)
        return '{}\n'.format(resp)
    
    oid = req_data["oid"]
    if not oid.strip():
        data = {
                'status': 'ERROR',
                'msg': 'OID value is empty. Pass input Json with OID',
                'ip': ip
        }
        resp = json.dumps(data)
        return '{}\n'.format(resp)
    
    # Check if oid contains "SNMPv2-MIB" or number format (1.3.6.2)
    res = "SNMPv2-MIB" in oid
    if res == True:
        x = oid.split(".")
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
               CommunityData('pod7all', mpModel=1),
               UdpTransportTarget((ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(x[0], x[1], 0)))
        )
    else:
        l = []
        # concatenate oid with 0
        l.append(oid)
        l.append("0")
        str = '.'.join([l[0],l[1]])
        newL = []
        newL.append(str)
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
               CommunityData('pod7all', mpModel=1),
               UdpTransportTarget((ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(newL[0])))
        )
    if errorIndication:
        data = {
             'status': 'ERROR',
             'msg': 'Error indication: ' + errorIndication,
             'ip': ip
           }
        resp = json.dumps(data)
        return '{}\n'.format(resp) 

    elif errorStatus:
        data = {
             'status': 'ERROR',
             'msg': 'Error indication: ' + errorStatus,
             'ip': ip
           }
        resp = json.dumps(data)
        return '{}\n'.format(resp) 
    else:
        for varBind in varBinds:
            sucMsg = ' = '.join([x.prettyPrint() for x in varBind])
            data = {
                 'status': 'SUCCESS',
                 'msg': sucMsg,
                 'ip': ip
            }
            resp = json.dumps(data)
            return '{}\n'.format(resp) 

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
