import re
import requests

# Define the API endpoint mappings
api_mappings = {
    'teams-joined': {'endpoint': 'https://graph.microsoft.com/v1.0/me/joinedTeams', 'method': 'GET'},
    'channels': {'endpoint': 'https://graph.microsoft.com/v1.0/teams/{teams-id}/channels', 'method': 'GET'},
    'members': {'endpoint': 'https://graph.microsoft.com/v1.0/teams/{teams-id}/members', 'method': 'GET'},
    'drive lists': {'endpoint': 'https://graph.microsoft.com/v1.0/me/drive/recent', 'method': 'GET'},
    'tasks': {'endpoint': 'https://graph.microsoft.com/v1.0/me/todo/lists/AAMkAGM2YzVlNGM1LWYwZmYtNDg2OS1hNThlLWI3OGU3OGQ2YjUyMgAuAAAAAABmFZHVSi48R5PIkGcDt626AQCUKxx8eWawR7UHOV9lmUikAAAAAAESAAA=/tasks', 'method': 'GET'},
    'new task': {'endpoint': 'https://graph.microsoft.com/v1.0/me/todo/lists/AAMkAGM2YzVlNGM1LWYwZmYtNDg2OS1hNThlLWI3OGU3OGQ2YjUyMgAuAAAAAABmFZHVSi48R5PIkGcDt626AQCUKxx8eWawR7UHOV9lmUikAAAAAAESAAA=/tasks', 'method': 'POST'},
    'create teams': {'endpoint': 'https://graph.microsoft.com/v1.0/teams', 'method': 'POST'}
}

# Additional keywords for GET and POST methods
get_keywords = ['get', 'give', 'fetch', 'provide']
post_keywords = ['post', 'send', 'save', 'create','add']

def parse_query(query):
    # Convert query to lowercase for case-insensitive matching
    query = query.lower()
    
    # Initialize variables to store method keyword, main keyword, and ID
    method_keyword = None
    main_keyword = None
    id_value = None
    
    # Split query into words
    words = query.split()
    
    # Check for method keyword
    for word in words:
        if word in get_keywords:
            method_keyword = 'GET'
        elif word in post_keywords:
            method_keyword = 'POST'
    
    # Check for main keyword
    for keyword in api_mappings.keys():
        if keyword in query:
            main_keyword = keyword
    
    # Extract ID if present
    id_match = re.search(r'\b\d+\b', query)
    if id_match:
        id_value = id_match.group()
    print(method_keyword, main_keyword, id_value)
    return method_keyword, main_keyword, id_value

def match_query_to_api(method_keyword, main_keyword, id_value):
    if main_keyword not in api_mappings:
        print("Main keyword not found.")
        return None, None
    
    endpoint = api_mappings[main_keyword]['endpoint']
    method = api_mappings[main_keyword]['method']
    
    # Replace {teams-id} or {list_id} placeholder if present
    if '{teams-id}' in endpoint and id_value:
        endpoint = endpoint.replace('{teams-id}', id_value)
    elif '{list_id}' in endpoint and id_value:
        endpoint = endpoint.replace('{list_id}', id_value)
    print(endpoint, method)
    return endpoint, method

def call_api(endpoint, method, body=None):
    access_token = 'eyJ0eXAiOiJKV1QiLCJub25jZSI6ImpidDB0cWxMdGsyWHZhSk5OdmQzbkpRcHdnVU1sczYyRlZFRVEtbXhUbEkiLCJhbGciOiJSUzI1NiIsIng1dCI6InEtMjNmYWxldlpoaEQzaG05Q1Fia1A1TVF5VSIsImtpZCI6InEtMjNmYWxldlpoaEQzaG05Q1Fia1A1TVF5VSJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC82YjhiODI5Ni1iZGZmLTRhZDgtOTNhZC04NGJjYmYzODQyZjUvIiwiaWF0IjoxNzEyOTE1OTAxLCJuYmYiOjE3MTI5MTU5MDEsImV4cCI6MTcxMzAwMjYwMSwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFWUUFxLzhXQUFBQXFTOTB5SVk1VTNKNUdJRVY3VGZSUlJ6Rnl6dEtzNlN3NGVKSDNqRHFibWtrckIrSDJ0dlVYTnFqb0o5b1k0d0VTZTBtZFhxMFphZlg0NjhKU3hPM0ZNTld2UHpPSGNKQ24wSkFsOE5pdGxZPSIsImFtciI6WyJwd2QiLCJtZmEiXSwiYXBwX2Rpc3BsYXluYW1lIjoiR3JhcGggRXhwbG9yZXIiLCJhcHBpZCI6ImRlOGJjOGI1LWQ5ZjktNDhiMS1hOGFkLWI3NDhkYTcyNTA2NCIsImFwcGlkYWNyIjoiMCIsImZhbWlseV9uYW1lIjoiMjBCSVMwMDciLCJnaXZlbl9uYW1lIjoiQWtzaGF5IFMiLCJpZHR5cCI6InVzZXIiLCJpcGFkZHIiOiIyNDA5OjQwZjQ6MzQ6M2E1NDphYzkzOjIyNGQ6MTAzZTo4NjExIiwibmFtZSI6IkFrc2hheSBTIC4gMjBCSVMwMDciLCJvaWQiOiI4MmIyNDQxZi00ODQ5LTRmZGYtYTdmNC02N2Y1YzhhNTVkYmIiLCJwbGF0ZiI6IjUiLCJwdWlkIjoiMTAwMzIwMDBGNTRDNTJBMSIsInJoIjoiMC5BVW9BbG9LTGFfLTkyRXFUcllTOHZ6aEM5UU1BQUFBQUFBQUF3QUFBQUFBQUFBQktBTmcuIiwic2NwIjoiQ2FsZW5kYXJzLlJlYWQgQ2FsZW5kYXJzLlJlYWQuU2hhcmVkIENhbGVuZGFycy5SZWFkQmFzaWMgQ2FsZW5kYXJzLlJlYWRXcml0ZSBDaGFubmVsLlJlYWRCYXNpYy5BbGwgQ2hhbm5lbFNldHRpbmdzLlJlYWQuQWxsIENoYXQuUmVhZCBDaGF0LlJlYWRCYXNpYyBDaGF0LlJlYWRXcml0ZSBEaXJlY3RvcnkuQWNjZXNzQXNVc2VyLkFsbCBEaXJlY3RvcnkuUmVhZC5BbGwgRGlyZWN0b3J5LlJlYWRXcml0ZS5BbGwgRWR1QXNzaWdubWVudHMuUmVhZCBFZHVBc3NpZ25tZW50cy5SZWFkQmFzaWMgRWR1QXNzaWdubWVudHMuUmVhZFdyaXRlIEVkdUFzc2lnbm1lbnRzLlJlYWRXcml0ZUJhc2ljIEVkdVJvc3Rlci5SZWFkQmFzaWMgRmlsZXMuUmVhZCBGaWxlcy5SZWFkLkFsbCBGaWxlcy5SZWFkV3JpdGUgRmlsZXMuUmVhZFdyaXRlLkFsbCBHcm91cC5SZWFkLkFsbCBHcm91cC5SZWFkV3JpdGUuQWxsIE1haWwuUmVhZCBNYWlsLlJlYWRCYXNpYyBNYWlsLlJlYWRXcml0ZSBvcGVuaWQgT3JnQ29udGFjdC5SZWFkLkFsbCBQZW9wbGUuUmVhZCBQZW9wbGUuUmVhZC5BbGwgUHJlc2VuY2UuUmVhZCBQcmVzZW5jZS5SZWFkLkFsbCBwcm9maWxlIFNpdGVzLlJlYWRXcml0ZS5BbGwgVGFza3MuUmVhZCBUYXNrcy5SZWFkV3JpdGUgVGVhbU1lbWJlci5SZWFkLkFsbCBVc2VyLlJlYWQgVXNlci5SZWFkV3JpdGUgVXNlci5SZWFkV3JpdGUuQWxsIFVzZXJBY3Rpdml0eS5SZWFkV3JpdGUuQ3JlYXRlZEJ5QXBwIGVtYWlsIiwic2lnbmluX3N0YXRlIjpbImttc2kiXSwic3ViIjoiY1VVU1JsTzY2VDRPNUNfd0J5dTc1R3pHLTc0QzlqQnFfMmFkT1VJMUZlbyIsInRlbmFudF9yZWdpb25fc2NvcGUiOiJBUyIsInRpZCI6IjZiOGI4Mjk2LWJkZmYtNGFkOC05M2FkLTg0YmNiZjM4NDJmNSIsInVuaXF1ZV9uYW1lIjoiYWtzaGF5LjIwaXNAa2N0LmFjLmluIiwidXBuIjoiYWtzaGF5LjIwaXNAa2N0LmFjLmluIiwidXRpIjoiTnVUSnY2LXNpVTJjM2lheDc4ekFBUSIsInZlciI6IjEuMCIsIndpZHMiOlsiY2YxYzM4ZTUtMzYyMS00MDA0LWE3Y2ItODc5NjI0ZGNlZDdjIiwiZjI4YTFmNTAtZjZlNy00NTcxLTgxOGItNmExMmYyYWY2YjZjIiwiNjkwOTEyNDYtMjBlOC00YTU2LWFhNGQtMDY2MDc1YjJhN2E4IiwiOWI4OTVkOTItMmNkMy00NGM3LTlkMDItYTZhYzJkNWVhNWMzIiwiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il0sInhtc19jYyI6WyJDUDEiXSwieG1zX3NzbSI6IjEiLCJ4bXNfc3QiOnsic3ViIjoicUlfcnVyVUE1UXpMQ09GVU03QlRNOVZmY0p0SHRzQ2hWTjBRcGlveFMzSSJ9LCJ4bXNfdGNkdCI6MTU4ODg1NDczMX0.CRKy2xyrWEp4f_-CaiXWjS529jpaQQYFFVu0pnxrmoEGzFyUuhBGhIGoaZAwNdy00qvyjeLZ85w3w8opM35rDyreajTbz0zqKb6uqaVQERdaU3leKmyWU3YbONRaUbY1ny7y70-0I9LLGRfX9tlhLH0aNqlAzChgMJmQ9g5aTNt8V_SfQNRpoJ-uzVL3lINgBpGVvfJ1EB0jM4TnaCZsrpcuAOsudicWDmlBkK46Ktda4YL8XwmDYS_EzU6FKAwG_dPCqp5L63mGxxnIKtH7qvua1eR-WyELwczVWf_pQ1C0PynKYQmM_6ypZG7pesbbVbY41Ia8heu_nAUW_hmeog'
    if endpoint is None or method is None:
        print("Unable to match query to API.")
        return
    
    # Make API call
    if method == 'GET':
        headers = {'Authorization': 'Bearer ' + access_token}
        # print("hello, world!")
        print("endpoint",endpoint)
        response = requests.get(endpoint, headers=headers)
        return response.json()
    elif method == 'POST':
        headers = {'Authorization': 'Bearer ' + access_token}
        print("endpoint",endpoint)
        response = requests.post(endpoint, headers=headers, json = body)
        return response.json()
    else:
        print("Unsupported HTTP method.")
    
    # Check if response is not None before accessing its attributes
    if response is not None and response.status_code == 200:
        print("API call successful.")
        print("Response:", response.json())  # Example: Print response data
    elif response is not None:
        print("API call failed. Status code:", response.status_code)
    else:
        print("API call failed.")
        return


# Example functions for sending and receiving messages in a chat interface
def send_message_to_user(message):
    print("Bot: " + message)  # Replace this with your method of sending messages to the user

def receive_message_from_user():
    return input("User: ")  # Replace this with your method of receiving messages from the user


def apiMapping(message):
    user_query = message
    print("message", user_query) 
    method_keyword, main_keyword, id_value = parse_query(user_query)
    api_endpoint, http_method = match_query_to_api(method_keyword, main_keyword, id_value)
    # If the method is POST and the main keyword is 'new task', prompt the user for a task body
    if http_method == 'POST' and main_keyword == 'new task':
        send_message_to_user("Please enter the task body:")
        task_body = receive_message_from_user()  # This function should handle receiving messages from the user
        body = {'title': task_body}  # Construct the request body
        body = {'title': task_body}  # Construct the request body
        resp = call_api(api_endpoint, http_method, body=body)  # Pass the body to the call_api function
    else:
        resp = call_api(api_endpoint, http_method)
    return resp


