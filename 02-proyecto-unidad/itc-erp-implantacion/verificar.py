"""Comprobación posterior a la instalación de ITC ERP."""
import sqlite3
from pathlib import Path

RUTA_BD = Path(__file__).parent / "data" / "itc_erp.sqlite"


def comprobar(condicion, mensaje):
    print(("OK" if condicion else "FALLO") + " — " + mensaje)
    return condicion


if not RUTA_BD.exists():
    raise SystemExit("FALLO — No existe data/itc_erp.sqlite. Ejecuta instalar.py.")

with sqlite3.connect(RUTA_BD) as conexion:
    tablas = {fila[0] for fila in conexion.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    configuracion = dict(conexion.execute("SELECT clave, valor FROM configuracion"))
    activos = [fila[0] for fila in conexion.execute("SELECT codigo FROM modulos WHERE activo = 1")]
    operaciones = conexion.execute("SELECT COUNT(*) FROM operaciones").fetchone()[0]

resultados = [
    comprobar({"configuracion", "modulos", "usuarios", "operaciones"}.issubset(tablas), "tablas creadas"),
    comprobar(configuracion.get("perfil") in {"comercial", "soporte"}, "perfil guardado"),
    comprobar(len(activos) == 3, "tres módulos activos"),
    comprobar(operaciones >= 1, "operación de instalación registrada"),
]
raise SystemExit(0 if all(resultados) else 1)

