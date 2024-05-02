import re
import requests
from .teamsidMapping import teamsidMapping
from .chatidMapping import chatidMapping
import difflib

# Define the API endpoint mappings
api_mappings = {
    'teams-joined': {'endpoint': 'https://graph.microsoft.com/v1.0/me/joinedTeams', 'method': 'GET'},
    'channels': {'endpoint': 'https://graph.microsoft.com/v1.0/teams/{teams_id}/channels', 'method': 'GET'},
    'members': {'endpoint': 'https://graph.microsoft.com/v1.0/teams/{teams_id}/members', 'method': 'GET'},
    'drive lists': {'endpoint': 'https://graph.microsoft.com/v1.0/me/drive/recent', 'method': 'GET'},
    'tasks': {'endpoint': 'https://graph.microsoft.com/v1.0/me/todo/lists/AAMkAGM2YzVlNGM1LWYwZmYtNDg2OS1hNThlLWI3OGU3OGQ2YjUyMgAuAAAAAABmFZHVSi48R5PIkGcDt626AQCUKxx8eWawR7UHOV9lmUikAAAAAAESAAA=/tasks', 'method': 'GET'},
    'new task': {'endpoint': 'https://graph.microsoft.com/v1.0/me/todo/lists/AAMkAGM2YzVlNGM1LWYwZmYtNDg2OS1hNThlLWI3OGU3OGQ2YjUyMgAuAAAAAABmFZHVSi48R5PIkGcDt626AQCUKxx8eWawR7UHOV9lmUikAAAAAAESAAA=/tasks', 'method': 'POST'},
    'create teams': {'endpoint': 'https://graph.microsoft.com/v1.0/teams', 'method': 'POST'},
    'group-chats': {'endpoint': 'https://graph.microsoft.com/v1.0/chats', 'method': 'GET'},
    'chat': {'endpoint': 'https://graph.microsoft.com/v1.0/{chat_id}/messages', 'method': 'GET'},
    'message': {'endpoint': 'https://graph.microsoft.com/v1.0/{chat_id}/messages', 'method': 'POST'}
}

# Additional keywords for GET and POST methods
get_keywords = ['get', 'give', 'fetch', 'provide']
post_keywords = ['post', 'send', 'save', 'create','add']

# Initialize an empty dictionary to store display names and ids
data = teamsidMapping()
teams_dict = {}
# Iterate through the teams data and store display names and ids in the dictionary
for team in data['value']:
    teams_dict[team['displayName']] = team['id']

chatData = chatidMapping()
chat_dict = {}
# Iterate through the teams data and store display names and ids in the dictionary
for chat in chatData['value']:
    chat_dict[chat['topic']] = chat['id']




def get_team_id(team_name):
    matches = difflib.get_close_matches(team_name, teams_dict.keys(), n=1, cutoff=0.6)
    if matches:
        print("teams_dict[matches[0]]",teams_dict[matches[0]])
        return teams_dict[matches[0]]
    else:
        return None

def get_chat_id(chat_name):
    matches = difflib.get_close_matches(chat_name, chat_dict.keys(), n=1, cutoff=0.6)
    print("came here")
    if matches:
        print("chat_dict[matches[0]]",chat_dict[matches[0]])
        return chat_dict[matches[0]]
    else:
        return None


def receive_message_from_user(user_input):
    # Parse the input to extract the task body if it's a POST request for adding a new task
    if 'new task' in user_input.lower() and any(keyword in user_input.lower() for keyword in post_keywords):
        # Extracting the task body from the input message
        task_body = user_input.split('-')[-1].strip()
        return task_body # Return task body and HTTP method POST
    
    elif 'members' in user_input.lower() and any(keyword in user_input.lower() for keyword in api_mappings.keys()):
        # Extracting the task body from the input message
        teams_name = user_input.split('-')[-1].strip()
        print(teams_name)
        return teams_name # Return task body and HTTP method POST
    
    elif ('chat' in user_input.lower() or 'message' in user_input.lower()) and any(keyword in user_input.lower() for keyword in api_mappings.keys()):
        # Extracting the task body from the input message
        chat_name = user_input.split('-')[-1].strip()
        print("chat_name", chat_name)
        return chat_name # Return task body and HTTP method POST
    else:
        return user_input # Return the user input and HTTP method GET
    
    

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
    # id_match = re.search(r'\b\d+\b', query)
    # if id_match:
    #     id_value = id_match.group()
    if main_keyword == 'members':
        team_name = receive_message_from_user(query)
        id_value = get_team_id(team_name)
        print("team name and id_value",team_name,id_value)

    elif main_keyword == 'chat' or main_keyword == 'message':
        print("came here")
        chat_name = receive_message_from_user(query)
        id_value = get_chat_id(chat_name)
        print("chat name and id_value",chat_name,id_value)

    print(method_keyword, main_keyword, id_value) 
    return method_keyword, main_keyword, id_value

def match_query_to_api(method_keyword, main_keyword, id_value):
    if main_keyword not in api_mappings:
        print("Main keyword not found.")
        return None, None
    
    endpoint = api_mappings[main_keyword]['endpoint']
    method = api_mappings[main_keyword]['method']
    print("before function")
    if '{teams_id}' in endpoint:
        endpoint = endpoint.replace('{teams_id}', id_value)
        
    
    elif '{chat_id}' in endpoint:
        endpoint = endpoint.replace('{chat_id}', id_value)

        
    elif '{list_id}' in endpoint:
        endpoint = endpoint.replace('{list_id}', id_value)
       
    print('endpoint', endpoint)
    return endpoint, method

def call_api(endpoint, method, body=None, teams_id=None):
    access_token = "eyJ0eXAiOiJKV1QiLCJub25jZSI6InZGVW0tOGxWLXNQY0QxSEJabVd0VUdvNFVsNnpzaGF5R2M0WjRPMXpTTGsiLCJhbGciOiJSUzI1NiIsIng1dCI6InEtMjNmYWxldlpoaEQzaG05Q1Fia1A1TVF5VSIsImtpZCI6InEtMjNmYWxldlpoaEQzaG05Q1Fia1A1TVF5VSJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC82YjhiODI5Ni1iZGZmLTRhZDgtOTNhZC04NGJjYmYzODQyZjUvIiwiaWF0IjoxNzEzMTE1Mjk5LCJuYmYiOjE3MTMxMTUyOTksImV4cCI6MTcxMzIwMjAwMCwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFWUUFxLzhXQUFBQWZrNzRrVnB5SGs2QW0rVXg2aTh1eGNCb2JobTBVc2tsOHQ4bU1jYVNnbDhTTUJMdWg1c2ErK1NZWnN0ZnlLMDFXdUpQa1I1NVRoSlJkRFhDVVNNc2gyR3l3NnhNTVpINk1yanF6Y3JrcEk0PSIsImFtciI6WyJwd2QiLCJtZmEiXSwiYXBwX2Rpc3BsYXluYW1lIjoiR3JhcGggRXhwbG9yZXIiLCJhcHBpZCI6ImRlOGJjOGI1LWQ5ZjktNDhiMS1hOGFkLWI3NDhkYTcyNTA2NCIsImFwcGlkYWNyIjoiMCIsImZhbWlseV9uYW1lIjoiMjBCSVMwMDciLCJnaXZlbl9uYW1lIjoiQWtzaGF5IFMiLCJpZHR5cCI6InVzZXIiLCJpcGFkZHIiOiIxMDMuMTE0LjI1MS4xOTkiLCJuYW1lIjoiQWtzaGF5IFMgLiAyMEJJUzAwNyIsIm9pZCI6IjgyYjI0NDFmLTQ4NDktNGZkZi1hN2Y0LTY3ZjVjOGE1NWRiYiIsInBsYXRmIjoiNSIsInB1aWQiOiIxMDAzMjAwMEY1NEM1MkExIiwicmgiOiIwLkFVb0Fsb0tMYV8tOTJFcVRyWVM4dnpoQzlRTUFBQUFBQUFBQXdBQUFBQUFBQUFCS0FOZy4iLCJzY3AiOiJDYWxlbmRhcnMuUmVhZCBDYWxlbmRhcnMuUmVhZC5TaGFyZWQgQ2FsZW5kYXJzLlJlYWRCYXNpYyBDYWxlbmRhcnMuUmVhZFdyaXRlIENoYW5uZWwuUmVhZEJhc2ljLkFsbCBDaGFubmVsU2V0dGluZ3MuUmVhZC5BbGwgQ2hhdC5SZWFkIENoYXQuUmVhZEJhc2ljIENoYXQuUmVhZFdyaXRlIERpcmVjdG9yeS5BY2Nlc3NBc1VzZXIuQWxsIERpcmVjdG9yeS5SZWFkLkFsbCBEaXJlY3RvcnkuUmVhZFdyaXRlLkFsbCBFZHVBc3NpZ25tZW50cy5SZWFkIEVkdUFzc2lnbm1lbnRzLlJlYWRCYXNpYyBFZHVBc3NpZ25tZW50cy5SZWFkV3JpdGUgRWR1QXNzaWdubWVudHMuUmVhZFdyaXRlQmFzaWMgRWR1Um9zdGVyLlJlYWRCYXNpYyBGaWxlcy5SZWFkIEZpbGVzLlJlYWQuQWxsIEZpbGVzLlJlYWRXcml0ZSBGaWxlcy5SZWFkV3JpdGUuQWxsIEdyb3VwLlJlYWQuQWxsIEdyb3VwLlJlYWRXcml0ZS5BbGwgTWFpbC5SZWFkIE1haWwuUmVhZEJhc2ljIE1haWwuUmVhZFdyaXRlIG9wZW5pZCBPcmdDb250YWN0LlJlYWQuQWxsIFBlb3BsZS5SZWFkIFBlb3BsZS5SZWFkLkFsbCBQcmVzZW5jZS5SZWFkIFByZXNlbmNlLlJlYWQuQWxsIHByb2ZpbGUgU2l0ZXMuUmVhZFdyaXRlLkFsbCBUYXNrcy5SZWFkIFRhc2tzLlJlYWRXcml0ZSBUZWFtTWVtYmVyLlJlYWQuQWxsIFVzZXIuUmVhZCBVc2VyLlJlYWRXcml0ZSBVc2VyLlJlYWRXcml0ZS5BbGwgVXNlckFjdGl2aXR5LlJlYWRXcml0ZS5DcmVhdGVkQnlBcHAgZW1haWwiLCJzaWduaW5fc3RhdGUiOlsia21zaSJdLCJzdWIiOiJjVVVTUmxPNjZUNE81Q193Qnl1NzVHekctNzRDOWpCcV8yYWRPVUkxRmVvIiwidGVuYW50X3JlZ2lvbl9zY29wZSI6IkFTIiwidGlkIjoiNmI4YjgyOTYtYmRmZi00YWQ4LTkzYWQtODRiY2JmMzg0MmY1IiwidW5pcXVlX25hbWUiOiJha3NoYXkuMjBpc0BrY3QuYWMuaW4iLCJ1cG4iOiJha3NoYXkuMjBpc0BrY3QuYWMuaW4iLCJ1dGkiOiI4QWV4cUF0dEJrcTJmU1ZOT3YwMkFBIiwidmVyIjoiMS4wIiwid2lkcyI6WyJjZjFjMzhlNS0zNjIxLTQwMDQtYTdjYi04Nzk2MjRkY2VkN2MiLCJmMjhhMWY1MC1mNmU3LTQ1NzEtODE4Yi02YTEyZjJhZjZiNmMiLCI2OTA5MTI0Ni0yMGU4LTRhNTYtYWE0ZC0wNjYwNzViMmE3YTgiLCI5Yjg5NWQ5Mi0yY2QzLTQ0YzctOWQwMi1hNmFjMmQ1ZWE1YzMiLCJiNzlmYmY0ZC0zZWY5LTQ2ODktODE0My03NmIxOTRlODU1MDkiXSwieG1zX2NjIjpbIkNQMSJdLCJ4bXNfc3NtIjoiMSIsInhtc19zdCI6eyJzdWIiOiJxSV9ydXJVQTVRekxDT0ZVTTdCVE05VmZjSnRIdHNDaFZOMFFwaW94UzNJIn0sInhtc190Y2R0IjoxNTg4ODU0NzMxfQ.lZHgL1aMVZxvDh9XiBgJ2SlagVvnN1Q-6ZAVBGwCEgwaXA4mEa9CE8Be4OU4Ht41e7UhAfPtnyHQ76Fh0yO_RT9HXrerLLJzk20otZUJDHrKXxhBmh2BkNwqzPruJ_xUzFVDHRETNfyPjZbmpj29zhgmdL-4YjsbdSpLcGWkp3qpY9DA47Cf4pprSDfOOanjjZCX9_IBC5UeEC2Rdohx9D5uAQVRdm8ZU516K3uJopIy2POHhF0w7ODXiKERZSgUC2lbef2-dqAA7UfHK_H5MvQGxVw_LKa3mbjmlQmXM-aTiVEz4jeCntg2ozJYGWvt5356-Jn1SaR-BIxdbC8KJg"
    if endpoint is None or method is None:
        print("Unable to match query to API.")
        return
    
    # Make API call
    if method == 'GET':
        headers = {'Authorization': 'Bearer ' + access_token}
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

# Example function for sending messages to the user (replace this with your method of sending messages)
def send_message_to_user(message):
    print("Bot:", message)

def apiMapping(message):
    user_query = message
    print("message", user_query) 
    method_keyword, main_keyword, id_value = parse_query(user_query)
    api_endpoint, http_method = match_query_to_api(method_keyword, main_keyword, id_value)
    # If the method is POST and the main keyword is 'new task', prompt the user for a task body
    if http_method == 'POST' and main_keyword == 'new task':
        task_body = receive_message_from_user(message)  # This function should handle receiving messages from the user
        body = {'title': task_body}  # Construct the request body
        resp = call_api(api_endpoint, http_method, body=body)  # Pass the body to the call_api function
    else:
        resp = call_api(api_endpoint, http_method)
    return resp


