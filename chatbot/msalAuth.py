import msal
import webbrowser
import requests
from urllib.parse import urlparse, parse_qs
from msal import PublicClientApplication

def msalAuth():
    
    APPLICATION_ID = 'b36d5992-a108-4d87-a0cd-23af691a176b'
    Authority_url = 'https://login.microsoftonline.com/6b8b8296-bdff-4ad8-93ad-84bcbf3842f5/'

    SCOPES = ['api://b36d5992-a108-4d87-a0cd-23af691a176b/User.Read.All','User.Read']
    # teams_scope =['Team.ReadBasic.All','Directory.Read.All','Directory.ReadWrite.All','TeamSettings.Read.All','TeamSettings.ReadWrite.All','User.Read.All','User.ReadWrite.All']

    app = PublicClientApplication(
        APPLICATION_ID,
        authority = Authority_url   
    )

    flow = app.initiate_device_flow(scopes=SCOPES) 
    print(flow)
    print(flow['message'])
    webbrowser.open(flow['verification_uri'])

    result = app.acquire_token_by_device_flow(flow)
    print("result",result)
    print("result - access_token", result['access_token'])

    access_token_id = result['access_token']
    return access_token_id  