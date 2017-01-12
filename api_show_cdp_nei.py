import sys
import requests
import json

"""
Setup the API parameters to pull the CDP Data
"""
url = 'http://' +  sys.argv[1] + '/ins'
switchuser = sys.argv[2]
switchpassword = sys.argv[3]

myheaders={'content-type':'application/json-rpc'}
payload=[
  {
    "jsonrpc": "2.0",
    "method": "cli",
    "params": {
      "cmd": "show cdp neighbor",
      "version": 1.2
    },
    "id": 1
  }
]
response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()
path = response['result']['body']['TABLE_cdp_neighbor_brief_info']['ROW_cdp_neighbor_brief_info']

x = 0
cmd_dict = {}
for items in path:
  local_int = items['intf_id']
  remote_int = items['port_id']
  remote_device = items['device_id']
  command = 'interface ' + local_int + ' ; ' + 'description [-[ Link to ' + remote_device + ' port ' + remote_int + ' ]-]'
  cmd_dict[x] = command
  x+=1

myheaders_json={'content-type':'application/json'}

for cmd, values in cmd_dict.iteritems():
  payload={
    "ins_api": {
      "version": "1.2",
      "type": "cli_conf",
      "chunk": "0",
      "sid": "1",
      "input": values,
      "output_format": "json"
    }
  }
  response_conf = requests.post(url,data=json.dumps(payload), headers=myheaders_json,auth=(switchuser,switchpassword)).json()

