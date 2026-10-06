import sqlite3

conexion = sqlite3.connect("avisos.db")
cursor = conexion.cursor()

# Cuantos avisos hay en total, para poder sacar porcentajes
cursor.execute("SELECT COUNT(*) FROM avisos")
total = cursor.fetchone()[0]


def contar(patron):
    """Cuenta en cuantos avisos aparece ese patron dentro de la descripcion."""
    cursor.execute(
        "SELECT COUNT(*) FROM avisos WHERE descripcion LIKE ?",
        (patron,),
    )
    return cursor.fetchone()[0]


print("=== Las empresas que mas avisos publican ===")
cursor.execute("""
    SELECT empresa, COUNT(*) AS cuantos
    FROM avisos
    GROUP BY empresa
    ORDER BY cuantos DESC
    LIMIT 5
""")
for empresa, cuantos in cursor.fetchall():
    print(cuantos, "avisos -", empresa)

print()
print("=== Habilidades: la cuenta mala contra la buena ===")
print("%-10s %10s %10s" % ("", "suelto", "palabra"))

habilidades = ["SQL", "Python", "Excel", "English", "AI", "Git"]
for h in habilidades:
    mal = contar("%" + h + "%")
    bien = contar("% " + h + " %")
    print("%-10s %10s %10s" % (h, mal, bien))

print()
print("=== Lo que de verdad piden (bien contado) ===")
for h in habilidades:
    bien = contar("% " + h + " %")
    porcentaje = round(bien * 100 / total)
    barra = "#" * (porcentaje // 2)
    print("%-10s %3s%%  %s" % (h, porcentaje, barra))

print()
print("Sobre", total, "avisos.")

conexion.close()
