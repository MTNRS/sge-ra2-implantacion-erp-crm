"""Servidor local del asistente de implantación de ITC ERP."""
import json
import sqlite3
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import instalar

BASE = Path(__file__).parent
RUTA_BD = BASE / "data" / "itc_erp.sqlite"


def leer_estado():
    if not RUTA_BD.exists():
        return {"instalado": False, "mensaje": "No existe todavía una instalación local."}
    with sqlite3.connect(RUTA_BD) as conexion:
        configuracion = dict(conexion.execute("SELECT clave, valor FROM configuracion"))
        modulos = [{"codigo": codigo, "nombre": nombre} for codigo, nombre in conexion.execute("SELECT codigo, nombre FROM modulos WHERE activo = 1 ORDER BY codigo")]
        operaciones = [{"momento": momento, "accion": accion, "detalle": detalle} for momento, accion, detalle in conexion.execute("SELECT momento, accion, detalle FROM operaciones ORDER BY rowid DESC LIMIT 5")]
    return {"instalado": True, "configuracion": configuracion, "modulos": modulos, "operaciones": operaciones}


def verificar():
    estado = leer_estado()
    if not estado["instalado"]:
        return [{"nombre": "Base de datos", "ok": False, "detalle": "Instala un perfil primero."}]
    with sqlite3.connect(RUTA_BD) as conexion:
        tablas = {fila[0] for fila in conexion.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        operaciones = conexion.execute("SELECT COUNT(*) FROM operaciones").fetchone()[0]
    configuracion = estado["configuracion"]
    return [
        {"nombre": "Estructura SQLite", "ok": {"configuracion", "modulos", "usuarios", "operaciones"}.issubset(tablas), "detalle": "Tablas necesarias creadas."},
        {"nombre": "Perfil", "ok": configuracion.get("perfil") in {"comercial", "soporte"}, "detalle": configuracion.get("perfil", "sin perfil")},
        {"nombre": "Módulos", "ok": len(estado["modulos"]) == 3, "detalle": f"{len(estado['modulos'])} módulos activos."},
        {"nombre": "Bitácora", "ok": operaciones >= 1, "detalle": f"{operaciones} operación(es) registrada(s)."},
    ]


class Manejador(SimpleHTTPRequestHandler):
    def responder_json(self, datos, codigo=HTTPStatus.OK):
        cuerpo = json.dumps(datos, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def do_GET(self):
        if self.path == "/api/estado":
            return self.responder_json(leer_estado())
        if self.path == "/api/verificar":
            return self.responder_json(verificar())
        return super().do_GET()

    def do_POST(self):
        if self.path != "/api/instalar":
            return self.responder_json({"error": "Ruta no encontrada."}, HTTPStatus.NOT_FOUND)
        try:
            longitud = int(self.headers.get("Content-Length", "0"))
            datos = json.loads(self.rfile.read(longitud).decode("utf-8"))
            instalar.instalar(datos.get("perfil", ""))
            self.responder_json({"mensaje": "Instalación completada.", "estado": leer_estado()}, HTTPStatus.CREATED)
        except (json.JSONDecodeError, ValueError) as error:
            self.responder_json({"error": str(error)}, HTTPStatus.BAD_REQUEST)
        except FileExistsError as error:
            self.responder_json({"error": str(error)}, HTTPStatus.CONFLICT)
        except sqlite3.Error as error:
            self.responder_json({"error": f"Error de SQLite: {error}"}, HTTPStatus.INTERNAL_SERVER_ERROR)


if __name__ == "__main__":
    print("ITC ERP disponible en http://127.0.0.1:8080")
    ThreadingHTTPServer(("127.0.0.1", 8080), Manejador).serve_forever()
