# duplicates.py - puts the names of all duplicates in a list and prints it.
import json
import hackbi_eventbrite as he

with open("secret.json", "r") as file:
    secret = json.load(file)
event_id = secret["event_id"]
token = secret["token"]

attendees = he.get_attendee_list(event_id, token)
duplicates = he.get_duplicates(attendees) # gets all duplicate attendees

# creates a list with the structure:
# [(last, first), (last, first)]
names = []
for dupe in duplicates:
    names.append((dupe["profile"]["last_name"], dupe["profile"]["first_name"]))
print(names)
