import requests

def joke(subcommand=None):
    """Command which uses jokeapi.dev's API to get a random joke"""
    url = "https://v2.jokeapi.dev/joke/Miscellaneous,Pun" \
    "?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"
    #'?blacklist' prevents offensive jokes

    r = requests.get(url) #http request to the site
    data = r.json()

    #Check if the joke is two part or a one liner
    if data["type"] == "twopart":
        delivery = data["delivery"]
        setup = data["setup"]
        joke = f"{setup} {delivery}"
    else:
        joke = data["joke"].replace("\n", "")

    return {"speech": joke, "action": None}
