import time
import os
import glob
import git
import time
import giteapy
from giteapy.rest import ApiException
from pprint import pprint

# Configure API key authorization: AccessToken
configuration = giteapy.Configuration()
configuration.api_key['access_token'] = <insert Access Token here>


# create an instance of the API class
configuration.host="https://gitbox.org/api/v1"
api_instance = giteapy.OrganizationApi(giteapy.ApiClient(configuration))
username = 'cpyarger' # str | username of the user that will own the created organization
org = 'BOSI' # str | name of organization




for subdir, dirs, files in os.walk(".\Files"):
    cnt=0
    for dir in dirs:
        x = os.path.join(subdir, dir)
        #print("Line {}: {}".format(cnt, x))
        file=dir+'.html'
        try:
            os.replace(os.path.join(x,file), os.path.join(x, 'index.html'))
        except:
            print("file exception -- "+file)
        try:

            api_instance2 = giteapy.RepositoryApi(giteapy.ApiClient(configuration))


            # Create a file in a repository

            #body = giteapy.CreateRepoOption(name=dir) # CreateRepoOption |  (optional)
            filepath = os.path.join(x, 'index.html') # str | path of the file to create
            body2 = giteapy.CreateFileOptions(content=filepath) # CreateFileOptions |

            #print(filepath)
            #api_response = api_instance.create_org_repo(org, body=body)
            #pprint(api_response)
            api_response2 = api_instance2.repo_create_file(org, dir, filepath, body2)
            pprint(api_response2)
            #pprint(api_response)
        except ApiException as e:
            print("Exception when calling AdminApi->admin_create_org: %s\n" % e)
        cnt += 1
