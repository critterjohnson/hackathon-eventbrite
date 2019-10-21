# event.py - functions to use eventbrite api
import requests
import json

# returns a list of attendees, handles pagination automatically
def get_attendee_list(event_id:str, token:str, continuation:str=None):
    endpoint = f"https://www.eventbriteapi.com/v3/events/{event_id}/attendees"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = None
    if continuation is not None:
        params = {
            "continuation": continuation
        }
    response = requests.get(endpoint, headers=headers, params=params)

    if response.status_code != 200:
        raise ValueError(f"Bad response: {response.status_code}")

    resp_json = response.json()
    att_list = resp_json["attendees"]
    pagination = resp_json["pagination"]
    if pagination["has_more_items"]:
        att_list.extend(get_attendee_list(event_id, 
                                          token, 
                                          pagination["continuation"]))

    return att_list
