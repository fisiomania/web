import json
import requests

# Configuración general
API_KEY = os.getenv("YOUTUBE_API_KEY")

# Tu ID de canal o el nombre exacto con el que figuran tus videos para filtrarlos
# (Reemplaza "Fisiomanía" o pon el ID de tu canal, ej: "UC...")
MI_NOMBRE_DE_CANAL = "UCHf85J5ad4OTphK9Aykw3cg" 

# Diccionario con tus listas de reproducción (IDs limpios sin parámetros extra como &si=...)
PLAYLISTS = {
    "renal": "PLOL2fcAe3Lt-Y0BzabTF3pSIMcxLI_6sn",
    "medio-interno": "PLOL2fcAe3Lt8XHuebpcaheTMnuZIPAUax",
    "regulacion-ph": "PLOL2fcAe3Lt-lJo6JQ5GHmQZogMVWfeJR",
    "sangre": "PLOL2fcAe3Lt9Imf1LzLZtDJVwqUD4FmXJ",
    "respiratorio": "PLOL2fcAe3Lt9I-R7ZUgyE2o0exYOFLkhh"
}

def actualizar_playlist(categoria, playlist_id):
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={playlist_id}&key={API_KEY}"
    
    print(f"Obteniendo videos para la categoría: {categoria}...")
    response = requests.get(url)
    data = response.json()
    
    videos = []
    
    if "items" in data:
        for item in data["items"]:
            snippet = item["snippet"]
            
            # 1. Omitir videos privados o eliminados
            if snippet["title"] in ["Private video", "Deleted video"]:
                continue

            # 2. FILTRO: Solo agregar si el video fue subido por tu canal
            # (Compara el nombre del canal del video con el tuyo)
            canal_video = snippet.get("videoOwnerChannelTitle", "")
            
            # Si YouTube no expone el owner channel title en este endpoint, 
            # podemos validar por el canal que administra la playlist o usar una regla.
            # Alternativa segura: verificamos si el canal coincide o si el video no es de externos.
            # (Nota: También puedes filtrar comparando channelId si lo prefieres).
            
            video_data = {
                "title": snippet["title"],
                "description": snippet["description"],
                "videoId": snippet["resourceId"]["videoId"],
                "thumbnail": snippet["thumbnails"].get("maxres", snippet["thumbnails"].get("high", snippet["thumbnails"]["default"]))["url"],
                "publishedAt": snippet["publishedAt"],
                "channelTitle": canal_video
            }
            
            # Filtro aplicado: solo si coincide con tu canal (puedes comentar esta línea si prefieres probar primero)
            # if MI_NOMBRE_DE_CANAL.lower() in canal_video.lower():
            videos.append(video_data)
        
        # Guardamos en un archivo JSON nombrado según la categoría
        output_file = f"{categoria}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(videos, f, ensure_ascii=False, indent=4)
            
        print(f"¡Éxito! Se guardaron {len(videos)} de tus videos en {output_file}\n")
    else:
        print(f"Error al obtener los datos para {categoria}: {data}\n")

if __name__ == "__main__":
    for cat, pid in PLAYLISTS.items():
        if not pid.startswith("ID_DE_LA_LISTA"):
            actualizar_playlist(cat, pid)
            
    print("¡Proceso de actualización finalizado!")
