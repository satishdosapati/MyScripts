import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Login Details
controller = 'https://10.155.65.63'
username = 'admin'
password = 'P1mc0Cl0ud'

# Logging in the APIC
url = controller + "/api/aaaLogin.json"
payload = {"aaaUser" : {"attributes" : {"name" : username, "pwd" : password}}}
header = {"content-type": "application/json"}
response= requests.post(url,data=json.dumps(payload), headers=header, verify=False)
resp = response.json()
print(response.status_code)
print("Step1: Logged into APIC successfully")

# Collect the token
login_attributes = resp['imdata'][0]['aaaLogin']['attributes']
auth_token = login_attributes['token']
cookie = {'APIC-Cookie': auth_token}
print("Step2: Token used for communication")
print(auth_token)


# Delete the tenant
url = controller + "/api/node/mo/uni.json"
payload = {"polUni":{"attributes":{"dn":"uni","status":"modified"},"children":[{"fvTenant":{"attributes":{"dn":"uni/tn-Autotenant","status":"deleted"},"children":[]}}]}}
response = requests.post(url,data=json.dumps(payload), cookies=cookie,verify=False)
print(response.status_code)
print("Successfully deleted the tenant")