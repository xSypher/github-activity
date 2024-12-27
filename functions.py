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