"""
Le pide a una IA que lea cada aviso y diga qué habilidades pide.

Por qué existe: contar palabras con LIKE solo encuentra lo que vos pusiste en
la lista de antemano, y se confunde ("maintain" contaba como "AI"). Una IA lee
el aviso entero y devuelve lo que de verdad pide, sin lista previa.

Guarda el avance en habilidades_ia.json después de cada aviso, así si se corta
no se pierde nada: la próxima vez arranca donde quedó.
"""
import io
import json
import os
import re
import sqlite3
import time

import requests

URL = "https://generativelanguage.googleapis.com/v1beta/interactions"
# Cada modelo tiene su propia cuota diaria en el plan gratis (500 pedidos).
# Si uno se agota, se cambia a otro: la instruccion es la misma y el estilo
# de respuesta tambien, asi que los resultados se pueden mezclar sin problema.
MODELO = "gemini-3.5-flash-lite"
SALIDA = "habilidades_ia.json"
# El plan gratis permite 15 pedidos por minuto, o sea uno cada 4 segundos.
# Cada pedido tarda ~2 s, así que esperamos 2,2 más para no pasarnos.
# Pasarse es contraproducente: Google te frena y perdés más tiempo del que ganás.
PAUSA = 2.2

# La instrucción. Tres partes: qué hacer, en qué formato, y qué NO hacer.
INSTRUCCION = """Leé este anuncio de trabajo y sacá las habilidades más importantes que pide.
Devolvelas separadas por comas, todas en una sola línea.
Escribilas SIEMPRE en español, en minúscula, y lo más cortas posible: una o dos palabras cada una.
Usá el término más común y general, no frases largas ni variantes.
No agregues explicaciones, ni títulos, ni viñetas, ni nada antes o después de la lista.

Anuncio:
"""


def leer_clave():
    """La clave vive en .env, que está en el .gitignore y nunca se sube."""
    texto = io.open(".env", encoding="utf-8").read()
    m = re.search(r"GEMINI_API_KEY\s*=\s*(\S+)", texto)
    if not m:
        raise SystemExit("No encontré GEMINI_API_KEY en el archivo .env")
    return m.group(1)


def sin_html(h):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h or "")).strip()


def texto_de(respuesta):
    """La respuesta del modelo viene adentro del paso de tipo model_output."""
    for paso in respuesta.get("steps", []):
        if paso.get("type") == "model_output":
            for parte in paso.get("content", []):
                if parte.get("type") == "text":
                    return parte.get("text", "")
    return ""


def preguntar(clave, aviso, intentos=4):
    """Un pedido, con reintentos si el modelo está ocupado."""
    for n in range(intentos):
        try:
            r = requests.post(
                URL,
                headers={"x-goog-api-key": clave, "Content-Type": "application/json"},
                json={"model": MODELO, "input": INSTRUCCION + aviso},
                timeout=90)
        except Exception:
            time.sleep(5 * (n + 1))
            continue

        if r.status_code == 200:
            return texto_de(r.json()).strip()
        # 429 = te pasaste del límite, 503 = está saturado. Se espera y se reintenta.
        if r.status_code in (429, 503):
            time.sleep(25)   # el propio error sugiere esperar ~26 s
            continue
        return None
    return None


def main():
    clave = leer_clave()

    # lo que ya se hizo en corridas anteriores
    hechos = {}
    if os.path.exists(SALIDA):
        hechos = json.load(io.open(SALIDA, encoding="utf-8"))
        print("Ya había", len(hechos), "avisos leídos de antes.")

    cursor = sqlite3.connect("avisos.db").cursor()
    cursor.execute("SELECT titulo, empresa, descripcion FROM avisos")
    avisos = cursor.fetchall()

    pendientes = [a for a in avisos if a[0] not in hechos]
    print("Faltan", len(pendientes), "de", len(avisos))
    print()

    for n, (titulo, empresa, desc) in enumerate(pendientes, 1):
        texto = preguntar(clave, sin_html(desc)[:4000])
        if texto is None:
            print("  %d/%d  (falló, lo dejo para después)" % (n, len(pendientes)))
            continue

        habilidades = [h.strip() for h in texto.split(",") if h.strip()]
        hechos[titulo] = {"empresa": empresa, "habilidades": habilidades}

        # se guarda en cada vuelta: si se corta la luz, no se pierde nada
        json.dump(hechos, io.open(SALIDA, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)

        if n % 10 == 0 or n == 1:
            print("  %d/%d  %s (%d habilidades)" %
                  (n, len(pendientes), titulo[:40], len(habilidades)))
        time.sleep(PAUSA)

    print()
    print("Listo:", len(hechos), "avisos leídos por la IA, guardados en", SALIDA)


if __name__ == "__main__":
    main()
