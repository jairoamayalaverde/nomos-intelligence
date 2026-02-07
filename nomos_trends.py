import json
from pytrends.request import TrendReq
from datetime import datetime

# 1. Configuración de Escucha (Lenguaje del Dolor real)
# Buscamos términos que un usuario preocupado escribiría hoy
monitor_config = {
    "Poco Tráfico": ["my site disappeared from google", "traffic dropped"],
    "Baja Conversión": ["why people don't buy from my site", "no sales"],
    "Competencia": ["competitor stealing my traffic", "better than me"],
    "Técnico": ["site error google search console", "website too slow"]
}

# 2. Inicializar conexión con Google
print("🚀 NOMOS-Trends: Iniciando conexión con Google...")
pytrends = TrendReq(hl='es-ES', tz=360)

brain_update = {
    "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "insights": {}
}

# 3. Procesar cada categoría
for category, terms in monitor_config.items():
    print(f"📡 Analizando pulso de: {category}...")
    try:
        # Consultamos el interés en las últimas 24 horas
        pytrends.build_payload(terms, timeframe='now 1-d')
        data = pytrends.interest_over_time()
        
        if not data.empty:
            # Calculamos la media de interés (0 a 100)
            avg_score = int(data.iloc[-1].drop('isPartial', errors='ignore').mean())
            intensity = "ALTA" if avg_score > 50 else "ESTABLE"
        else:
            avg_score = 0
            intensity = "SIN DATOS SUFICIENTES"
            
    except Exception as e:
        print(f"❌ Error en {category}: {e}")
        intensity = "ERROR"
        avg_score = 0
    
    brain_update["insights"][category] = {
        "status": intensity,
        "score": avg_score,
        "message": f"Tendencia {intensity.lower()} detectada en las últimas 24h."
    }

# 4. Generar el archivo para el Wizzard
with open('nomos_intelligence.json', 'w', encoding='utf-8') as f:
    json.dump(brain_update, f, indent=4, ensure_ascii=False)

print("\n✅ NOMOS Intelligence (Trends) actualizado correctamente.")
print("Archivo generado: nomos_intelligence.json")
