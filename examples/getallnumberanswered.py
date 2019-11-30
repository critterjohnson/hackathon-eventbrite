# getallnumberanswered.py - gets all t-shirt sizes.
import json
import hackbi_eventbrite as he

with open("secret.json", "r") as file:
    secret = json.load(file)
event_id = secret["event_id"]
token = secret["token"]

attendees = he.get_attendee_list(event_id, token)
numbers = he.get_all_number_answered(attendees,
                                     question_text="what is your t-shirt size?")

print(numbers)
