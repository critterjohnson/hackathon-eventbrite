# getpeopleanswered.py - gets everyone going to Ireton and prints their first and last name.
import json
import hackbi_eventbrite as he

with open("secret.json", "r") as file:
    secret = json.load(file)
event_id = secret["event_id"]
token = secret["token"]

attendees = he.get_attendee_list(event_id, token)
people = he.get_people_answered(attendees, 
                                "Bishop Ireton High School",
                                question_text="what school do you go to?")

for person in people:
    print(person["profile"]["first_name"], person["profile"]["last_name"])
