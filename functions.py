import requests

"""
main functios for the github-activity cli app.
Functions to get a github user's activity and print it
"""


def get_activity(user: str) -> list[dict]:

    if not isinstance(user, str):
        user_type = str(type(user)).split()[1].strip("'>")
        raise TypeError(
            f"Invalid user name of type: {user_type}. should be of type: 'str'."
        )

    url = f"https://api.github.com/users/{user}/events"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # throw HTTPError if the status is not between 200-399
        return response.json()
    
    except requests.exceptions.Timeout:
        print("Error: connection timeout is over. check your internet.")
    
    except requests.exceptions.ConnectionError:
        print("Error: connection error.")
    
    except requests.exceptions.HTTPError as e:
        print(f"invalid user: {user}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    return []


def parse_events(events: list[dict]) -> list[str]:

    events_list = []
    if not events:
        raise ValueError(
            "The object given as events is empty."
        )
    
    try:
        
        for event in events:
            user = event["actor"]["login"]
            repo = event["repo"]["name"]
            
            match event["type"]:

                case "CreateEvent":
                    ref_type = event["payload"]["ref_type"]
                    if ref_type == "repository":
                        events_list.append(
                            f"- {user} created a repository: {repo}."
                        )
                
                    else:
                        events_list.append(
                            f"- {user} created a {ref_type} in {repo}."
                        )

                case "PushEvent":
                    events_list.append(
                        f"- {user} pushed {len(event["payload"]["commits"])} commits to {repo}."
                    ) 

                case "DeleteEvent":
                    events_list.append(
                        f"- {user} deleted a {event["payload"]["ref_type"]} in {repo}"
                    )   

                case "IssueEvent":
                    events_list.append(
                        f"- {user} {event["payload"]["action"]} an issue in {repo}"
                    )

                case "IssueCommentEvent":
                    events_list.append(
                        f"- {user} {event["payload"]["action"]} an issue comment in {repo}."
                    )

                case "ReleaseEvent":
                    events_list.append(
                        f"- {user} {event["payload"]["action"]} tag in {repo}."
                    )

                case _:
                    events_list.append(
                        f"- {event["type"]} in {repo}."
                    )
        
    except KeyError:
        print(f"Something is wrong with {events}.")

    return events_list


def print_events(events: list[str]) -> None:
    
    if not isinstance(events, list):
        object_type = str(type(events)).split()[1].strip(">'")
        raise TypeError(
            f"argument should be of type 'list'. a {object_type} was given."
        )

    
    if events:
        for event in events:
            print(event)

    else:
        print("The list is empty.")