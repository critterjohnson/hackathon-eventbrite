# hackathon-eventbrite
Some tools for using eventbrite, intended for HackBI

## Eventbrite
These methods interact with the eventbrite api. Whenever something returns a list of attendees, it returns the object returned by the eventbrite API (same is true of get_question_list, which returns a list of question objects from the API). Documentation for the eventbrite api can be found [here](https://www.eventbrite.com/platform/api#/reference/attendee)

## Installation
Since it's not on PyPi (yet?), it has to be installed by cloning and going into the hackbi_eventbrite directory, and typing
`pip install .`
This will install it like any other Python package; and will allow you to import it:
```python
import hackbi_eventbrite
```

## Usage
```python
def make_event_request(endpoint:str, event_id:str, token:str, params:dict=None, url:str=None)
```
Makes a request to https://www.eventbriteapi.com/v3/events/{event_id}/{endpoint}, or {url}/{event_id}/{endpoint} if url is passed. Handles pagination and returns each resposne in a list.
This method is used as a helper method for the `get_attendee_list` and `get_question_list` methods.

```python
def get_attendee_list(event_id:str, token:str, url:str=None)
```
Returns the list of attendees for an event.

```python
def get_question_list(event_id:str, token:str, as_owner:bool=False, url:str=None)
```
Gets the list of questions for an event.

```python
def get_duplicates(attendees:list)
```
Returns a list of duplicate attendees for the attendee list passed.

```python
def get_answers_for(attendees:list, question_id=None, question_text=None, follow_up:bool=True, questions:list=None)
```
Returns all answers for a particular question or questions in the form of a 2d list, with the first list in the array being the responses to the first question, etc.
You can pass both `question_id` and `question_text` if for some reason you decide you want to do that. The question text must match exactly the text of the question on Eventbrite. Passing a list will return the answers for all questions in that list.
If `follow_up` is True, `questions` (a list of questions returned from `get_question_list`) must also be passed. If `follow_up` is true, followup questions will be automatically handled, returning instead of "Other" the answer to the followup.

```python
def get_number_answered(attendees:list, expected_answer:str, question_id:str=None, question_text=None)
```
Gets the number of people who answered something to a specific question. 
`expected_answer` is the answer to check for.
Pass only one question, and do not pass poth question_id and question_text.
If `questions` is passed (a list of questions returned from `get_question_list`), it will automatically handle followup questions.

```python
def get_all_number_answered(attendees:list, question_id:str=None, question_text:str=None, questions=None)
```
Returns the number of people who answered to each possible response. 
If `questions` is passed (a list of questions returned from `get_question_list`), it will automatically handle followup questions.
Returns a dictionary with the keys as the possible answers and values as the people who gave that answer.

```python
def get_people_answered(attendees:list, expected_answer:str, question_id:str=None, question_text:str=None)
```
Gets all attendees who answered something to a specific question. `expected_answer` is a string with the answer to look for (case insensitive). Does NOT handle follow up questions, but might in the future.
Pass either `question_id` or `question_text`, not both.

## Examples
Check out the [examples directory](examples/examples.md) for examples on how to use these methods.

## The CLI
The CLI isn't done, and I don't know when I'll finish it. The only thing it can do right now is save all attendees in a spreadsheet.
You can use it by running `cli.py` from the directory it's in `python cli.py` and it will tell you how to use it.
