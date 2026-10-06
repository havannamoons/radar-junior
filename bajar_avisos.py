import requests
import json
import time

url = "https://himalayas.app/jobs/api/search"
todos = []    # una lista vacía donde vamos juntando los avisos
pagina = 1

while True:
    pedido = {"seniority": "Entry-level", "country": "Argentina", "page": pagina}
    datos = requests.get(url, params=pedido).json()
    avisos = datos["jobs"]

    if not avisos:    # si la página vino vacía, terminamos
        break

    todos.extend(avisos)
    print("Página", pagina, "- llevo", len(todos), "avisos")
    pagina = pagina + 1
    time.sleep(1)    # esperamos 1 segundo para no saturar la API

with open("avisos.json", "w", encoding="utf-8") as archivo:
    json.dump(todos, archivo, ensure_ascii=False, indent=2)

print("Listo: guardé", len(todos), "avisos")
