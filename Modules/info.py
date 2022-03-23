import requests

#open file that holds API key
with open("newsapi_key.txt", "r") as fp:
    key = fp.read().strip("\n")

GB_URL = f"https://newsapi.org/v2/top-headlines?country=gb&apiKey={key}&pageSize=5"
WORLD_URL = f"https://newsapi.org/v2/top-headlines?apiKey={key}&pageSize=5"

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
