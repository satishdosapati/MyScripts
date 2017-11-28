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

# Create a Tenant name Autotenant
url = controller + "/api/node/mo/uni/tn-Autotenant.json"
payload = {"fvTenant":{"attributes":{"dn":"uni/tn-Autotenant","name":"Autotenant","rn":"tn-Autotenant","status":"created"},"children":[]}}
response= requests.post(url,data=json.dumps(payload), cookies=cookie,verify=False)
print(response.status_code)
print("Step3: AutoTenant Created successfully")


# Printing the list of tenants
url = controller + "/api/class/fvTenant.json"
response = requests.get(url,data=json.dumps(payload), cookies=cookie, verify=False)
resp = response.json()
i = 0
print("Step4: The list of tenants configured on APIC are")
for i in range(0,int(resp['totalCount'])):
    print(resp['imdata'][i]['fvTenant']['attributes']['name'])
    i += 1

# Create an application profile
url = controller + "/api/node/mo/uni/tn-Autotenant/ap-Auto_Appprofile.json"
payload = {"fvAp":{"attributes":{"dn":"uni/tn-Autotenant/ap-Auto_Appprofile","name":"Auto_Appprofile","rn":"ap-Auto_Appprofile","status":"created"},"children":[]}}
response= requests.post(url,data=json.dumps(payload), cookies=cookie,verify=False)
print(response.status_code)
print("Step5: Application Profile created successfully")

# Create Private Network
url = controller + "/api/node/mo/uni/tn-Autotenant/ctx-AutoVRF.json"
payload = {"fvCtx":{"attributes":{"dn":"uni/tn-Autotenant/ctx-AutoVRF","name":"AutoVRF","rn":"ctx-AutoVRF","status":"created"},"children":[]}}
response= requests.post(url,data=json.dumps(payload), cookies=cookie,verify=False)
print(response.status_code)
print("Step6: Private network Created successfully")

# Create Bridge Domain
url = controller + "/api/node/mo/uni/tn-Autotenant/BD-WEB.json"
payload = {"fvBD":{"attributes":{"dn":"uni/tn-Autotenant/BD-WEB","mac":"00:22:BD:F8:19:FF","name":"WEB","rn":"BD-WEB","status":"created"},"children":[{"fvRsCtx":{"attributes":{"tnFvCtxName":"AutoVRF","status":"created,modified"},"children":[]}}]}}
response = requests.post(url,data=json.dumps(payload), cookies=cookie,verify=False)
print(response.status_code)

url = controller + "/api/node/mo/uni/tn-Autotenant/BD-APP.json"
payload = {"fvBD":{"attributes":{"dn":"uni/tn-Autotenant/BD-APP","mac":"00:22:BD:F8:19:FF","name":"APP","rn":"BD-APP","status":"created"},"children":[{"fvRsCtx":{"attributes":{"tnFvCtxName":"AutoVRF","status":"created,modified"},"children":[]}}]}}
response = requests.post(url,data=json.dumps(payload), cookies=cookie,verify=False)
print(response.status_code)

url = controller + "/api/node/mo/uni/tn-Autotenant/BD-DB.json"
payload = {"fvBD":{"attributes":{"dn":"uni/tn-Autotenant/BD-DB","mac":"00:22:BD:F8:19:FF","name":"DB","rn":"BD-DB","status":"created"},"children":[{"fvRsCtx":{"attributes":{"tnFvCtxName":"AutoVRF","status":"created,modified"},"children":[]}}]}}
response = requests.post(url,data=json.dumps(payload), cookies=cookie,verify=False)
print(response.status_code)
print("Step7: Bridge Domains (WEB, APP, DB) Created successfully")

# Create End Point Groups
url = controller + "/api/node/mo/uni/tn-Autotenant/ap-Auto_Appprofile/epg-WEB.json"
payload = {"fvAEPg":{"attributes":{"dn":"uni/tn-Autotenant/ap-Auto_Appprofile/epg-WEB","name":"WEB","rn":"epg-WEB","status":"created"},"children":[{"fvRsBd":{"attributes":{"tnFvBDName":"WEB","status":"created,modified"},"children":[]}}]}}
response = requests.post(url,data=json.dumps(payload), cookies=cookie,verify=False)
print(response.status_code)

url = controller + "/api/node/mo/uni/tn-Autotenant/ap-Auto_Appprofile/epg-APP.json"
payload = {"fvAEPg":{"attributes":{"dn":"uni/tn-Autotenant/ap-Auto_Appprofile/epg-APP","name":"APP","rn":"epg-APP","status":"created"},"children":[{"fvRsBd":{"attributes":{"tnFvBDName":"APP","status":"created,modified"},"children":[]}}]}}
response = requests.post(url,data=json.dumps(payload), cookies=cookie,verify=False)
print(response.status_code)

url = controller + "/api/node/mo/uni/tn-Autotenant/ap-Auto_Appprofile/epg-DB.json"
payload = {"fvAEPg":{"attributes":{"dn":"uni/tn-Autotenant/ap-Auto_Appprofile/epg-DB","name":"DB","rn":"epg-DB","status":"created"},"children":[{"fvRsBd":{"attributes":{"tnFvBDName":"DB","status":"created,modified"},"children":[]}}]}}
response = requests.post(url,data=json.dumps(payload), cookies=cookie,verify=False)
print(response.status_code)
print("Step8: End Point Groups (WEB, APP, DB) Created successfully")