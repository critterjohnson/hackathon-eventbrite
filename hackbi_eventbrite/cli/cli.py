# cli.py - cli for all of this nonsense
import argparse
import sys
import json
from hackbi_eventbrite import get_attendee_list
from hackbi_eventbrite import save_attendees

# TODO: cli for new methods

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--api_key",
                        help="your eventbrite api key")
    parser.add_argument("-i", "--event_id",
                        help="your event's event id")
    parser.add_argument("-o", "--options_file",
                        help="a .json file containing options")
    parser.add_argument("-f", "--file_name",
                        help="the file you would like to save to (.xlsx)")

    # parse, making sure to display help if no args are passed
    if len(sys.argv) == 1:
        parser.parse_args(["-h"])
        args = None
    else:
        args = parser.parse_args()

    # check to make sure either options exists or other opts were passed
    if args is not None:
        event_id = None
        api_key = None
        filename = None

        if args.options_file is not None:
            with open("options.json", "r") as file:
                options = json.load(file)
            
            try:
                event_id = options["event_id"]
            except KeyError:
                pass
            try:
                api_key = options["api_key"]
            except KeyError:
                pass
            try:
                filename = options["file_name"]
            except KeyError:
                pass

        if args.api_key is not None:
            api_key = args.api_key
        if args.event_id is not None:
            event_id = args.event_id
        if args.file_name is not None:
            filename = args.file_name
        
        msg = "missing required arguments: "
        if event_id is None:
            msg += "event_id "
        if api_key is None:
            msg += "api_key "
        if filename is None:
            msg += "file_name "
        if None in [event_id, api_key, filename]:
            raise ValueError(msg)
    
    att_list = get_attendee_list(event_id, api_key)
    save_attendees(att_list, filename)
