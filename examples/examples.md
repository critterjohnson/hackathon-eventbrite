# Examples
The examples in this directory all have these lines of code:
```python
with open("secret.json", "r") as file:
    secret = json.load(file)
event_id = secret["event_id"]
token = secret["token"]
```
This way, all of the examples can be used without exposing any private information.

If you want to use any of these examples directly, you can create a file called `secret.json` with the following structure:
```json
{
    "event_id": "your_event_id_here",
    "token": "your_api_token_here"
}
```
In the examples directory. Make sure you've also [installed the libraries](./README.md).

Do note that none of this is actually necessary - you can just pass `event_id` and `token` to any methods that require it directly. Just make sure you don't put it anywhere public so people can't make changes to your events.

Any of these exmamples can be run directly by following the above instructions and running them with `python example_name.py`.
