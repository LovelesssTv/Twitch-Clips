import requests
import json
import os
import sys

CLIENT_ID = os.environ.get("TWITCH_CLIENT_ID")
ACCESS_TOKEN = os.environ.get("TWITCH_ACCESS_TOKEN")
USERNAME = "lovelessstv"

HEADERS = {
    "Client-ID": CLIENT_ID,
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# Ottieni ID utente
user_resp = requests.get(
    f"https://api.twitch.tv/helix/users?login={USERNAME}",
    headers=HEADERS
)

user_data = user_resp.json().get('data')
if not user_data:
    print(f"❌ ERRORE: Utente Twitch '{USERNAME}' non trovato o token invalido.")
    print("Risposta API:", user_resp.text)
    sys.exit(1)

user_id = user_data[0]['id']

# Recupera fino a 100 clip
all_clips = []
pagination = None
while True:
    params = {
        "broadcaster_id": user_id,
        "first": 100
    }
    if pagination:
        params["after"] = pagination

    resp = requests.get("https://api.twitch.tv/helix/clips", headers=HEADERS, params=params)
    data = resp.json()
    all_clips.extend(data.get("data", []))

    pagination = data.get("pagination", {}).get("cursor")
    if not pagination or len(all_clips) >= 100:
        break

embed_links = [
    f"https://clips.twitch.tv/embed?clip={clip['id']}&parent=lovelessstv.github.io"
    for clip in all_clips[:100]
]

with open("clips.json", "w") as f:
    json.dump(embed_links, f, indent=2)

print(f"✅ clips.json aggiornato con {len(embed_links)} clip.")
