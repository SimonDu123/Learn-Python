import requests

username = "simon.du@quest.com"
password = "Password"
artifactory = "https://artifactory.labs.quest.com/" #artifactory URL
api = "api/storage/SpotlightCloud-OnPremConfig/builds/" #you can change this API URL to any API method you'd like to use

url = artifactory + api
r = requests.get(url, auth = (username, password)) #this script is only for API methods that use GET

if r.status_code == 200:
    print("Authenticate Succeed")



