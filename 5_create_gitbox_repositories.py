import time
import os
import glob
import git
import time
import giteapy
from giteapy.rest import ApiException
from pprint import pprint
fp = open('accesstoken', 'r')
line = fp.readline()
# Configure API key authorization: AccessToken
configuration = giteapy.Configuration()
configuration.api_key['access_token'] = line
# create an instance of the API class
configuration.host="https://gitbox.org/api/v1"
username = 'cpyarger' # str | username of the user that will own the created organization
org = 'BOSI' # str | name of organization
api_instance = giteapy.OrganizationApi(giteapy.ApiClient(configuration))

for subdir, dirs, files in os.walk(".\Files"):
    cnt=0
    for dir in dirs:
        x = os.path.join(subdir, dir)
        #print("Line {}: {}".format(cnt, x))
        file=dir+'.html'
        try:
            body = giteapy.CreateRepoOption(name=dir) # CreateRepoOption |  (optional)
            api_response = api_instance.create_org_repo(org, body=body)
        except ApiException as e:
            print("Exception when calling AdminApi->admin_create_org: %s\n" % e)
        cnt += 1
