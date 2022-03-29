import requests

#open file that holds API key
with open("Keys/newsapi_key.txt", "r") as fp:
    key = fp.read().strip("\n")

#news urls
GB_URL = f"https://newsapi.org/v2/top-headlines?country=gb&apiKey={key}&pageSize=5"
WORLD_URL = f"https://newsapi.org/v2/top-headlines?apiKey={key}&pageSize=5"

#dictionary url
DICT_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

def news(subcommand="britain"):
    """Retrieves news headlines using the newsapi.org API"""

    url = GB_URL if subcommand == "britain" else WORLD_URL

    r = requests.get(url)
    result = r.json()

    try:
        headlines = [x["title"].partition(" - ")[0] for x in result["articles"]]
    except KeyError:
        return {"speech": "Sorry, something went wrong retrieving the latest news headlines. Please try again later", "action": None}

    speech = ""
    for i, headline in enumerate(headlines[:3]):
        speech += f"Number {i+1}. {headline}."

    font = "Helvetica 16"

    text = ""
    for headline in headlines:
        if len(headline) > 80:
            font = "Helvetica 14"
        text += f"• {headline}\n"

    return {
        "speech": speech,
        "action": {
            "TEXT_M": {"text": "News Headlines", "font": "Helvetica 40"},
            "TEXT_S": {"text": text, "font": font}
        }
    }


def dictionary(params=None):
    """Command to return definition(s) of words specified"""

    if params is None:
        return {"speech": "Error: you need to specify a word.", "action": None}

    r = requests.get(f"{DICT_URL}{params}")
    result = r.json()

    total = 0

    speech = ""
    #loop for voice output
    for i, x in enumerate(result[0]["meanings"]):
        for y in x["definitions"]:
            definition = y["definition"]
            speech += f"{params} is defined as: '{definition}'" if i == 0 else f". it also means {definition}"
            total += 1

            if total == 3:
                #too many to read out, so exit
                break

    text = ""
    #loop for text output
    for i, x in enumerate(result[0]["meanings"]):
        for y in x["definitions"]:
            definition = y["definition"]
            text += f"{i}. {definition}\n"

    return {
        "speech": speech,
        "action": {
            "TEXT_M": {"text": params, "font": "Helvetica 40"},
            "TEXT_S": {"text": text, "font": "Helvetica 13"}
        }
    }
