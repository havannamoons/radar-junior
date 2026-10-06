import json
import sqlite3

# Abrimos (o creamos) la base de datos. Es un solo archivo.
conexion = sqlite3.connect("avisos.db")
cursor = conexion.cursor()

# Creamos la tabla: las columnas que va a tener cada aviso
cursor.execute("""
CREATE TABLE IF NOT EXISTS avisos (
    titulo       TEXT,
    empresa      TEXT,
    tipo         TEXT,
    moneda       TEXT,
    sueldo_min   REAL,
    sueldo_max   REAL,
    periodo      TEXT,
    link         TEXT,
    descripcion  TEXT
)
""")

# Vaciamos la tabla, para poder correr esto las veces que quieras
cursor.execute("DELETE FROM avisos")

# Leemos el archivo que bajaste en la etapa 1
with open("avisos.json", encoding="utf-8") as archivo:
    avisos = json.load(archivo)

# Metemos cada aviso como una fila
for a in avisos:
    cursor.execute(
        "INSERT INTO avisos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            a["title"],
            a["companyName"],
            a["employmentType"],
            a["currency"],
            a["minSalary"],
            a["maxSalary"],
            a["salaryPeriod"],
            a["applicationLink"],
            a["description"],
        ),
    )

conexion.commit()
conexion.close()

print("Listo: guardé", len(avisos), "avisos en avisos.db")
