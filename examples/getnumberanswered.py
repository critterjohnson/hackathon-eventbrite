# getnumberanswered.py - gets the number of people going to Ireton.
import json
import hackbi_eventbrite as he

with open("secret.json", "r") as file:
    secret = json.load(file)
event_id = secret["event_id"]
token = secret["token"]

attendees = he.get_attendee_list(event_id, token)
answered = he.get_number_answered(attendees,
                                 "Bishop Ireton High School",
                                 question_text="what school do you go to?")
print(answered)
