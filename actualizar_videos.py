import json
import requests

# Configuración
API_KEY = "TU_API_KEY_DE_YOUTUBE"
PLAYLIST_ID = "ID_DE_TU_LISTA_DE_REPRODUCCION"
OUTPUT_FILE = "renal.json"  # El archivo que leerá tu página web

def obtener_videos_playlist():
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={PLAYLIST_ID}&key={API_KEY}"
    
    response = requests.get(url)
    data = response.json()
    
    videos = []
    
    if "items" in data:
        for item in data["items"]:
            snippet = item["snippet"]
            
            # Extraemos solo lo que necesitamos
            video_data = {
                "title": snippet["title"],
                "description": snippet["description"],
                "videoId": snippet["resourceId"]["videoId"],
                "thumbnail": snippet["thumbnails"].get("high", snippet["thumbnails"]["default"])["url"],
                "publishedAt": snippet["publishedAt"]
            }
            videos.append(video_data)
            
        # Guardamos los datos en un archivo JSON local
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(videos, f, ensure_ascii=False, indent=4)
            
        print(f"¡Éxito! Se guardaron {len(videos)} videos en {OUTPUT_FILE}")

if __name__ == "__main__":
    obtener_videos_playlist()
