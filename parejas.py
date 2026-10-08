import sqlite3
conexion = sqlite3.connect("avisos.db")
cursor = conexion.cursor()
cursor.execute("SELECT descripcion FROM avisos")
descripciones = [fila[0] for fila in cursor.fetchall()]
print(len(descripciones))
from analisis 

