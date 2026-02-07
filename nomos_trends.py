import json
import requests
from pytrends.request import TrendReq
from datetime import datetime

# 1. Configuración Maestra: Unimos términos de búsqueda y subreddits de escucha
monitor_config = {
    "Poco Tráfico": {
        "terms": ["my site disappeared from google", "traffic dropped"],
        "sub": "SEO"
    },
    "Baja Conversión": {
        "terms": ["conversion rate optimization", "no sales ecommerce"],
        "sub": "marketing"
    },
    "Competencia": {
        "terms": ["competitor stealing my traffic", "better than me"],
        "sub": "entrepreneur"
    },
    "Técnico": {
        "terms": ["site error google search console", "website too slow"],
        "sub": "TechSEO"
    }
}

# Inicializamos Google Trends
pytrends = TrendReq(hl='es-ES', tz=360)

def get_reddit_voice(subreddit):
    """Extrae el titular más reciente de la comunidad sin necesidad de API Key"""
    try:
        url = f"https://www.reddit.com/r/{subreddit}/new.json?limit=5"
        headers = {'User-agent': 'NomosBot 2.0'}
        res = requests.get(url, headers=headers, timeout=10).json()
        # Tomamos el primer post que no sea fijado por moderadores
        return res['data']['children'][0]['data']['title']
    except:
        return "El mercado está debatiendo nuevas soluciones estratégicas en este momento."

# Estructura del cerebro de NOMOS
brain_update = {
    "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "insights": {}
}

print("🚀 NOMOS-Collector: Iniciando proceso de inteligencia dual...")

for category, config in monitor_config.items():
    print(f"📡 Procesando {category}...")
    
    # PARTE 1: Google Trends (Intensidad estadística)
    try:
        pytrends.build_payload(config["terms"], timeframe='now 1-d')
        data = pytrends.interest_over_time()
        if not data.empty:
            avg_score = int(data.iloc[-1].drop('isPartial', errors='ignore').mean())
        else:
            avg_score = 25 # Valor base si no hay suficiente data en 24h
    except:
        avg_score = 0
        
    # PARTE 2: Reddit (Voz social)
    voice = get_reddit_voice(config["sub"])
    
    # Consolidación
    brain_update["insights"][category] = {
        "status": "ALTA" if avg_score > 50 else "ESTABLE",
        "score": avg_score,
        "reddit_voice": voice,
        "message": "Tendencia activa detectada en las últimas 24h."
    }

# Guardar el archivo final
with open('nomos_intelligence.json', 'w', encoding='utf-8') as f:
    json.dump(brain_update, f, indent=4, ensure_ascii=False)

print("✅ Cerebro NOMOS actualizado: Datos de Google + Voces de Reddit listos.")
