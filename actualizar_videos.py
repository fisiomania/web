import json
import requests

# Configuración general
API_KEY = "TU_API_KEY_DE_YOUTUBE"

# Diccionario con tus listas de reproducción (Reemplaza los ID con los reales de tu canal)
PLAYLISTS = {
    "renal": "ID_DE_LA_LISTA_RENAL",
    "medio-interno": "ID_DE_LA_LISTA_MEDIO_INTERNO",
    "regulacion-ph": "ID_DE_LA_LISTA_PH",
    "sangre": "ID_DE_LA_LISTA_SANGRE",
    "respiratorio": "ID_DE_LA_LISTA_RESPIRATORIO"
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
            
            # Omitir videos privados o eliminados
            if snippet["title"] in ["Private video", "Deleted video"]:
                continue

            video_data = {
                "title": snippet["title"],
                "description": snippet["description"],
                "videoId": snippet["resourceId"]["videoId"],
                "thumbnail": snippet["thumbnails"].get("maxres", snippet["thumbnails"].get("high", snippet["thumbnails"]["default"]))["url"],
                "publishedAt": snippet["publishedAt"]
            }
            videos.append(video_data)
        
        # Guardamos en un archivo JSON nombrado según la categoría (ej: renal.json)
        output_file = f"{categoria}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(videos, f, ensure_ascii=False, indent=4)
            
        print(f"¡Éxito! Se guardaron {len(videos)} videos en {output_file}\n")
    else:
        print(f"Error al obtener los datos para {categoria}: {data}\n")

if __name__ == "__main__":
    # Opción A: Actualizar todas las listas de golpe
    for cat, pid in PLAYLISTS.items():
        if pid != "ID_DE_LA_LISTA_" + cat.upper().replace("-", "_"): # Evita correr los de ejemplo si no los cambiaste
            actualizar_playlist(cat, pid)
            
    print("¡Proceso de actualización finalizado!")
