from django.shortcuts import render
import json
import requests
from django.conf import settings

REQUEST_URL = settings.REQUEST_URL
BOT_TOKEN = settings.BOT_TOKEN

TEMP_VARS = {
    "WG": 0,
    "Cloak": 1,
    "AWG": 2,
    "Reverse WG": 3,
    "Reverse Cloak": 4,
    "Reverse AWG": 5,
}


# Create your views here.
def index(request):
    print(request)
    body = json.loads(request.body)
    tgid = body["message"]["from"]["id"]
    chat_id = body["message"]["chat"]["id"]
    res = requests.post(REQUEST_URL, json={"tgid": tgid})
    if res.status_code != 200:
        return render(request, "index.html")
    only = [x for x in res.json() if x["service_type"] in ("WG", "AC")]
    for item in only:
        item["api_endpoint"] = f"https://dev.amzsvc.com{item['api_endpoint']}"
        item["service_type"] = TEMP_VARS[item["service_type"]]
    res = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": json.dumps(only)},
    )
