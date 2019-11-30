# getanswersfor.py - gets all the answers for schools and prints it.
import json
import hackbi_eventbrite as he

with open("secret.json", "r") as file:
    secret = json.load(file)
event_id = secret["event_id"]
token = secret["token"]

attendees = he.get_attendee_list(event_id, token)
questions = he.get_question_list(event_id, token)
answers = he.get_answers_for(attendees, 
                             question_text="what school do you go to?",
                             follow_up=True,      # handles followup quuestions
                             questions=questions) # required if follow_up is True

print(answers)
