import sqlite3
from datetime import date

conexion = sqlite3.connect("avisos.db")
cursor = conexion.cursor()

cursor.execute("SELECT COUNT(*) FROM avisos")
total = cursor.fetchone()[0]


def contar(patron):
    cursor.execute(
        "SELECT COUNT(*) FROM avisos WHERE descripcion LIKE ?", (patron,)
    )
    return cursor.fetchone()[0]


# Las habilidades, bien contadas (rodeadas de espacios)
habilidades = ["English", "AI", "Excel", "SQL", "Python", "Git"]
datos = []
for h in habilidades:
    cuantos = contar("% " + h + " %")
    datos.append((h, cuantos, round(cuantos * 100 / total)))
datos.sort(key=lambda x: -x[1])

# Las empresas que mas publican
cursor.execute("""
    SELECT empresa, COUNT(*) AS cuantos
    FROM avisos
    GROUP BY empresa
    ORDER BY cuantos DESC
    LIMIT 8
""")
empresas = cursor.fetchall()

conexion.close()

# Armamos las filas de la tabla de habilidades
filas = ""
for nombre, cuantos, porcentaje in datos:
    filas += f"""
      <div class="fila">
        <div class="nombre">{nombre}</div>
        <div class="barra"><div class="relleno" style="width:{porcentaje}%"></div></div>
        <div class="dato">{porcentaje}% <span>({cuantos})</span></div>
      </div>"""

# Las empresas
items = ""
for nombre, cuantos in empresas:
    items += f"""
      <li><b>{cuantos}</b> {nombre}</li>"""

html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Radar Junior</title>
<style>
  :root {{
    --fondo:#0f1420; --tarjeta:#1b2436; --borde:#2a3448;
    --texto:#e8ecf4; --texto2:#a3aec4; --texto3:#6f7b93; --acento:#5eb3f6;
  }}
  * {{ box-sizing:border-box }}
  body {{
    margin:0; background:var(--fondo); color:var(--texto);
    font-family:system-ui,-apple-system,sans-serif; line-height:1.6;
  }}
  .wrap {{ max-width:720px; margin:0 auto; padding:56px 20px 90px }}
  h1 {{ font-size:2.1rem; margin:0 0 8px; letter-spacing:-.02em }}
  .bajada {{ color:var(--texto2); margin:0 0 6px }}
  .fecha {{ color:var(--texto3); font-size:.85rem; margin:0 0 40px }}
  h2 {{ font-size:1.2rem; margin:36px 0 14px }}
  .tarjeta {{
    background:var(--tarjeta); border:1px solid var(--borde);
    border-radius:14px; padding:22px 24px;
  }}
  .fila {{ display:flex; align-items:center; gap:14px; margin-bottom:12px }}
  .fila:last-child {{ margin-bottom:0 }}
  .nombre {{ width:78px; font-weight:600; flex:none }}
  .barra {{ flex:1; height:11px; background:#0d1422; border-radius:999px; overflow:hidden }}
  .relleno {{ height:100%; background:var(--acento); border-radius:999px }}
  .dato {{ width:92px; text-align:right; font-variant-numeric:tabular-nums; flex:none }}
  .dato span {{ color:var(--texto3); font-size:.85rem }}
  ul {{ list-style:none; padding:0; margin:0 }}
  li {{ padding:7px 0; border-bottom:1px solid var(--borde); color:var(--texto2) }}
  li:last-child {{ border-bottom:none }}
  li b {{ color:var(--acento); display:inline-block; width:34px }}
  .nota {{
    margin-top:36px; padding:18px 20px; border-radius:12px;
    background:rgba(240,180,94,.1); border-left:3px solid #f0b45e;
    color:var(--texto2); font-size:.93rem;
  }}
  .nota b {{ color:var(--texto) }}
</style>
</head>
<body>
<div class="wrap">

  <h1>Radar Junior</h1>
  <p class="bajada">Qué le piden a alguien sin experiencia en los avisos remotos
  abiertos a Argentina.</p>
  <p class="fecha">{total} avisos · actualizado el {date.today().strftime('%d/%m/%Y')}</p>

  <h2>Qué habilidades aparecen</h2>
  <div class="tarjeta">{filas}
  </div>

  <h2>Las empresas que más publican</h2>
  <div class="tarjeta">
    <ul>{items}
    </ul>
  </div>

  <div class="nota">
    <b>Sobre estos números.</b> Se cuentan buscando la palabra rodeada de espacios
    dentro de la descripción. Buscarla suelta daba el triple: "AI" también aparece
    dentro de <i>maintain</i> y <i>email</i>, y "Excel" dentro de <i>excellent</i>.
    Aun así la cuenta no es perfecta: se pierde la palabra cuando va seguida de coma
    o arranca una oración. Los valores reales son algo más altos que estos.
  </div>

</div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as archivo:
    archivo.write(html)

print("Listo: generé index.html con", total, "avisos")
