import requests
import json

artifactory = "https://artifactory.labs.quest.com/" #artifactory URL
api = "api/storage/SpotlightCloud-OnPremConfig/builds" #you can change this API URL to any API method you'd like to use
headers = {"X-JFrog-Art-Api": "ACCESS_TOKEN"} # headers for authentication

url = artifactory + api
r = requests.get(url, headers=headers) #Use JFrog api as headers to authenticate

if r.status_code == 200:
    response = json.loads(r.text)
    response2_download_list = []
    response2_api_list = []
    response2_sub_list = []
    response3_download_list = []
    for i in response['children']:
        if i['folder'] is False:
            response2 = requests.get(url + i['uri'], headers=headers)
            if response2.status_code == 200:
                response = json.loads(response2.text)
                response2_download_list.append(response['downloadUri'])
                response2_api_list.append(response['uri'])
        else:
           response2_sub_list.append(i['uri'])

    with open("response2_download_list.html", "a+") as out_file:
        for item in sorted(response2_download_list):
            out_file.write('<div><a href=' + item + '>' + item + '</a></div>')

    with open("response2_api_list.html", "a+") as out_file:
        for item in sorted(response2_api_list):
            out_file.write('<div><a href=' + item + '>' + item + '</a></div>')

    response4_download_list = []
    response4_api_list = []
    response6_download_list = []
    response6_api_list = []
    response6_folder = []
    for i in response2_sub_list:
            response3 = requests.get(url + i, headers=headers)
            response = json.loads(response3.text)
            for j in response['children']:
                if j['folder'] is False:
                    response4 = requests.get(url + i + j['uri'], headers=headers)
                    if response4.status_code == 200:
                        response = json.loads(response4.text)
                        response4_download_list.append(response['downloadUri'])
                        response4_api_list.append(response['uri'])
                else:
                    response5 = requests.get(url + i + j['uri'], headers=headers)
                    response = json.loads(response5.text)
                    for k in response['children']:
                        if k['folder'] is False:
                            response6 = requests.get(url + i + j['uri'] + k['uri'], headers=headers)
                            if response6.status_code == 200:
                                response = json.loads(response6.text)
                                response6_download_list.append(response['downloadUri'])
                                response6_api_list.append((response['uri']))
                        else:
                            response6_folder.append(k['uri'])

    with open("response2_download_list.html", "a+") as out_file:
        for item in sorted(response4_download_list):
            out_file.write('<div><a href=' + item + '>' + item + '</a></div>')

    with open("response2_api_list.html", "a+") as out_file:
        for item in sorted(response4_api_list):
            out_file.write('<div><a href=' + item + '>' + item + '</a></div>')

    with open("response2_download_list.html", "a+") as out_file:
        for item in sorted(response6_download_list):
            out_file.write('<div><a href=' + item + '>' + item + '</a></div>')

    with open("response2_api_list.html", "a+") as out_file:
        for item in sorted(response6_api_list):
            out_file.write('<div><a href=' + item + '>' + item + '</a></div>')

    with open("response6_folder.txt", "w") as out_file:
        for item in sorted(response6_folder):
            out_file.write("%s\n" % item)

else:
  print("Fail")
  response = json.loads(r.content)
  print(response["errors"])

print("Status Code : " + str(r.status_code))