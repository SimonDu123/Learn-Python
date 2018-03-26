import requests
import json
import re

#enter credentials
username = "simon.du@quest.com"
password = "password"
artifactory = "https://artifactory.labs.quest.com/" #artifactory URL
api = "api/storage/SpotlightCloud-OnPremConfig/builds" #you can change this API URL to any API method you'd like to use

url = artifactory + api
r = requests.get(url, auth=(username, password)) #this script is only for API methods that use GET

if r.status_code == 200:
    response = json.loads(r.text)
    response2_download_list = []
    response2_api_list = []
    response2_sub_list = []
    response3_download_list = []
    for i in response['children']:
        #match = re.match(r'.*\.exe',i['uri']) # working on match pattern
        #if match:
        if i['folder'] is False:
            response2 = requests.get(url + i['uri'], auth=(username,password))
            if response2.status_code == 200:
                response = json.loads(response2.text)
                response2_download_list.append(response['downloadUri'])
                response2_api_list.append(response['uri'])
        else:
           response2_sub_list.append(i['uri'])

    with open("response2_download_list.txt", "w") as out_file:
        for item in sorted(response2_download_list):
            out_file.write("%s\n" % item)

    with open("response2_api_list.txt", "w") as out_file:
        for item in sorted(response2_api_list):
            out_file.write("%s\n" % item)

    with open("response2_sub_list.txt", "w") as out_file:
        for item in sorted(response2_sub_list):
            out_file.write("%s\n" % item)

    response4_download_list = []
    response4_api_list = []
    response6_download_list = []
    response6_api_list = []
    response6_folder = []
    for i in response2_sub_list:
            response3 = requests.get(url + i, auth=(username,password))
            response = json.loads(response3.text)
            for j in response['children']:
                if j['folder'] is False:
                    response4 = requests.get(url + i + j['uri'], auth=(username,password))
                    if response4.status_code == 200:
                        response = json.loads(response4.text)
                        response4_download_list.append(response['downloadUri'])
                        response4_api_list.append(response['uri'])
                else:
                    response5 = requests.get(url + i + j['uri'], auth=(username,password))
                    response = json.loads(response5.text)
                    for k in response['children']:
                        if k['folder'] is False:
                            response6 = requests.get(url + i + j['uri'] + k['uri'], auth=(username,password))
                            if response6.status_code == 200:
                                response = json.loads(response6.text)
                                response6_download_list.append(response['downloadUri'])
                                response6_api_list.append((response['uri']))
                        else:
                            response6_folder.append(k['uri'])

    with open("response4_download_list.txt", "w") as out_file:
        for item in sorted(response4_download_list):
            out_file.write("%s\n" % item)

    with open("response4_api_list.txt", "w") as out_file:
        for item in sorted(response4_api_list):
            out_file.write("%s\n" % item)

    with open("response6_download_list.txt", "w") as out_file:
        for item in sorted(response6_download_list):
            out_file.write("%s\n" % item)

    with open("response6_api_list.txt", "w") as out_file:
        for item in sorted(response6_api_list):
            out_file.write("%s\n" % item)

    with open("response6_folder.txt", "w") as out_file:
        for item in sorted(response6_folder):
            out_file.write("%s\n" % item)

else:
  print("Fail")
  response = json.loads(r.content)
  print(response["errors"])

# uri = api + response4_exe_list[0]
# r = requests.get(uri, auth = (username,password)) #this scirpt is for getting uri API
# if r.status_code == 200:
#     response = json.loads(r.text)
#     response2 = response['children']
#     response4_sub_exe_list = []
#     for response3 in response2:
#         response4 = response3['uri']
#         response4_sub_exe_list.append(response4)
#         print(response4_sub_exe_list)
#     [uri + s for s in response4_sub_exe_list]
#     print(response4_sub_exe_list)

print("Status Code : " + str(r.status_code))