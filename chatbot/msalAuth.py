import msal
import webbrowser
import requests
from urllib.parse import urlparse, parse_qs
from msal import PublicClientApplication

def msalAuth():
    
    APPLICATION_ID = '65491031-610e-4a74-9e74-a6a57f57759b'
    Authority_url = 'https://login.microsoftonline.com/consumers'

    SCOPES = ['User.Read','User.ReadBasic.All']

    app = PublicClientApplication(
        client_id=APPLICATION_ID,
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
