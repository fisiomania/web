"""Actualiza los archivos .json de cada tema con los videos de sus listas de YouTube.

Lo ejecuta el workflow .github/workflows/actualizar.yml todos los días.
Requiere la variable de entorno YOUTUBE_API_KEY.
"""
import json
import os
import sys

import requests

API_KEY = os.getenv("YOUTUBE_API_KEY")
API_URL = "https://www.googleapis.com/youtube/v3/playlistItems"

# Listas de reproducción (IDs sin parámetros extra como &si=...)
PLAYLISTS = {
    "renal": "PLOL2fcAe3Lt-Y0BzabTF3pSIMcxLI_6sn",
    "medio-interno": "PLOL2fcAe3Lt8XHuebpcaheTMnuZIPAUax",
    "regulacion-ph": "PLOL2fcAe3Lt-lJo6JQ5GHmQZogMVWfeJR",
    "sangre": "PLOL2fcAe3Lt9Imf1LzLZtDJVwqUD4FmXJ",
    "respiratorio": "PLOL2fcAe3Lt9I-R7ZUgyE2o0exYOFLkhh",
}

OMITIR = {"Private video", "Deleted video"}


def obtener_items(playlist_id):
    """Devuelve todos los items de la lista, recorriendo todas las páginas."""
    items = []
    page_token = None
    while True:
        params = {
            "part": "snippet",
            "maxResults": 50,
            "playlistId": playlist_id,
            "key": API_KEY,
        }
        if page_token:
            params["pageToken"] = page_token
        response = requests.get(API_URL, params=params, timeout=30)
        data = response.json()
        if "items" not in data:
            raise RuntimeError(data)
        items.extend(data["items"])
        page_token = data.get("nextPageToken")
        if not page_token:
            return items


def actualizar_playlist(categoria, playlist_id):
    print(f"Obteniendo videos para la categoría: {categoria}...")
    videos = []
    for item in obtener_items(playlist_id):
        snippet = item["snippet"]
        if snippet["title"] in OMITIR:
            continue
        thumbs = snippet.get("thumbnails", {})
        thumb = thumbs.get("maxres") or thumbs.get("high") or thumbs.get("default") or {}
        videos.append({
            "title": snippet["title"],
            "description": snippet["description"],
            "videoId": snippet["resourceId"]["videoId"],
            "thumbnail": thumb.get("url", ""),
            "publishedAt": snippet["publishedAt"],
            "channelTitle": snippet.get("videoOwnerChannelTitle", ""),
        })

    with open(f"{categoria}.json", "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=4)
    print(f"Se guardaron {len(videos)} videos en {categoria}.json\n")


if __name__ == "__main__":
    if not API_KEY:
        sys.exit("Falta la variable de entorno YOUTUBE_API_KEY")

    errores = 0
    for categoria, playlist_id in PLAYLISTS.items():
        try:
            actualizar_playlist(categoria, playlist_id)
        except Exception as exc:  # una lista que falla no frena a las demás
            errores += 1
            print(f"Error al obtener los datos para {categoria}: {exc}\n")

    print("Proceso de actualización finalizado.")
    sys.exit(1 if errores else 0)
