import sqlite3
from pathlib import Path

ruta = Path("../02-proyecto-unidad/itc-erp-implantacion/data/itc_erp.sqlite")
if not ruta.exists():
    raise SystemExit("No existe una instalación. Ejecuta instalar.py primero.")

with sqlite3.connect(ruta) as conexion:
    modulos = conexion.execute("SELECT codigo FROM modulos WHERE activo = 1").fetchall()

print("Módulos activos:", ", ".join(codigo for (codigo,) in modulos))

