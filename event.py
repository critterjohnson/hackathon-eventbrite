# event.py - functions to use eventbrite api
import requests
import json

# TODO: tests

# makes a request to an event endpoint, handles pagination if needed
# assumes https://www.eventbriteapi.com/v3/events/{event_id}/{endpoint} if url is not passed
# if url is passed, hits url/{event_id}/{endpoint}
def make_event_request(endpoint:str, 
                       event_id:str,
                       token:str, 
                       params:dict=None,
                       continuation:str=None,
                       url:str=None):
    if url is None:
        full_url = f"https://www.eventbriteapi.com/v3/events/{event_id}/{endpoint}"
    else:
        full_url = f"{url}/{event_id}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    if continuation is not None:
        if params is None:
            params = {}
        params["continuation"] = continuation

    response = requests.get(full_url, headers=headers, params=params)
    if response.status_code != 200:
        # is something better than ValueError here...?
        raise ValueError(f"Bad response: {response.status_code}")
    
    resp_json = response.json()
    resp_list = [resp_json]

    # handles pagination
    if "pagination" in resp_json.keys():
        pagination = resp_json["pagination"]
        if pagination["has_more_items"]:
            resp_list.extend(make_event_request(endpoint, 
                                                event_id, 
                                                token, 
                                                params=params,
                                                continuation=pagination["continuation"],
                                                url=url))
    return resp_list


# returns a list of attendees, handles pagination automatically
def get_attendee_list(event_id:str, token:str, url:str=None):
    endpoint = "attendees"

    responses = make_event_request(endpoint, event_id, token, url=url)

    # creates the list of attendees
    att_list = [attendee for response in responses 
                for attendee in response["attendees"]]

    return att_list


# returns a list of attendees with the same name
def get_duplicates(event_id:str, token:str, url:str=None):
    attendees = get_attendee_list(event_id, token, url)

    names = []
    dupes = []
    for attendee in attendees:
        name = (attendee["profile"]["first_name"], attendee["profile"]["last_name"])
        if name not in names:
            names.append(name)
        else:
            dupes.append(name)
    return dupes


# gets the list of questions associated with an event
def get_question_list(event_id:str, 
                      token:str, 
                      as_owner:bool=False,
                      url:str=None):
    endpoint = "questions"

    params = {
        "as_owner": as_owner
    }
    responses = make_event_request(endpoint, event_id, token, params, None, url=url)
    # creates the list of questions
    question_list = [question for response in responses 
                     for question in response["questions"]]

    return question_list


# gets all the answers for a particular question/s
# passing a list of ids or texts gets all of the the questions
# returns a 2d list
# follow_up only works if there's only single followup questions
def get_answers_for(event_id:str,
                    token:str,
                    question_id=None,
                    question_text=None,
                    follow_up:bool=True,
                    url:str=None):
    if question_id is None and question_text is None:
        return ValueError("must pass question_id or question_text")

    if follow_up:
        # get a list of questions and map question id to follow up question ids (if they exist)
        # {question_id: (followup_choice, followup_id)}
        questions = get_question_list(event_id, token, True, url=url)
        followups = {}
        for question in questions:
            for choice in question["choices"]:
                for qid in choice["subquestion_ids"]:
                    followups[question["id"]] = (choice["answer"]["text"], qid)

    # get attendees and map them so their email maps to answers (used for followup questions later)
    attendees = get_attendee_list(event_id, token, url=url)
    answer_dict = {}
    for attendee in attendees:
        answer_dict[attendee["profile"]["email"]] = [answer for answer in attendee["answers"]]
    answers = []
    
    # gets the answers from a search list using a lookup
    def get_answers_from(search_list, answer_dict, lookup):
        for search in search_list:
            question_answers = []
            for att, questions in answer_dict.items():
                for question in questions:
                    if question[lookup].lower() == search.lower():
                        try:
                            answer = question["answer"]
                        except KeyError:
                            question_answers.append(None)
                            continue

                        # adds followup answers if required
                        if follow_up and question["question_id"] in followups.keys() and answer == followups[question["question_id"]][0]:
                            followup_id = followups[question["question_id"]][1]

                            for fquestion in answer_dict[att]:
                                if fquestion["question_id"] == followup_id:
                                    try:
                                        followup_answer = fquestion["answer"]
                                    except KeyError:
                                        followup_answer = "NONE_GIVEN"
                            question_answers.append(followup_answer)
                            
                        else:
                            question_answers.append(answer)
            answers.append(question_answers)
    
    # gets the list of texts 
    if question_text is not None:
        search_list = question_text
        lookup = "question"
        if isinstance(search_list, str):
            search_list = [search_list]
        get_answers_from(search_list, answer_dict, lookup)
    if question_id is not None:
        search_list = question_id
        if isinstance(search_list, str):
            search_list = [search_list]
        lookup = "question_id"
        get_answers_from(search_list, answer_dict, lookup)

    return answers


# gets the number of people who answered something to a specific question
def get_number_answered(event_id:str,
                        token:str,
                        expected_answer:str,
                        question_id:str=None,
                        question_text=None,
                        url:str=None):
    if question_id is None and question_text is None:
        return ValueError("must pass question_id or question_text")
    if question_id is not None and question_text is not None:
        return ValueError("pass only question_id or question_text, not both")

    answers = get_answers_for(event_id, token, question_id, question_text, url=url)[0]
    # returns the number of people that answered as expected
    return len(list(filter(lambda s: s is not None and s.lower() == expected_answer.lower(), answers)))


# returns the number of people who answered to each possible response
def get_all_number_answered(event_id:str,
                            token:str,
                            question_id:str=None,
                            question_text:str=None,
                            url:str=None):
    if question_id is None and question_text is None:
        return ValueError("must pass question_id or question_text")
    if question_id is not None and question_text is not None:
        return ValueError("pass only question_id or question_text, not both")

    answers = get_answers_for(event_id, token, question_id, question_text, url=url)[0]
    number_answers = {}
    for answer in answers:
        if answer not in number_answers.keys():
            number_answers[answer] = 1
        else:
            number_answers[answer] += 1
    return number_answers


# gets all the people who answered something to a specific question
def get_people_answered(event_id:str,
                        token:str,
                        expected_answer:str,
                        question_id:str=None,
                        question_text:str=None,
                        url:str=None):
    if question_id is None and question_text is None:
        return ValueError("must pass question_id or question_text")
    if question_id is not None and question_text is not None:
        return ValueError("pass only question_id or question_text, not both")

    attendees = get_attendee_list(event_id, token, url=url)
    if question_id is not None:
        answers = [attendee for attendee in attendees 
                   for answer in attendee["answers"]
                   if answer["question_id"] == question_id
                   and "answer" in answer.keys()
                   and answer["answer"].lower() == expected_answer.lower()]
    elif question_text is not None:
        answers = [attendee for attendee in attendees
                   for answer in attendee["answers"]
                   if answer["question"].lower() == question_text.lower()
                   and "answer" in answer.keys()
                   and answer["answer"].lower() == expected_answer.lower()]

    return answers
