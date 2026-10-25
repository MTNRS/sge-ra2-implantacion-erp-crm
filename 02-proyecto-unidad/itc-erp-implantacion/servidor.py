"""Servidor local del módulo de implantación de ITC ERP."""
import json
import sqlite3
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import instalar

BASE = Path(__file__).parent
RUTA_BD = BASE / "data" / "itc_erp.sqlite"
TABLAS = {"clientes": ("nombre", "email"), "incidencias": ("asunto", "estado"), "equipos": ("nombre", "estado")}
MODULO_POR_TABLA = {"clientes": "crm", "incidencias": "incidencias", "equipos": "inventario"}


def ahora():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def asegurar_esquema():
    if not RUTA_BD.exists():
        return
    with sqlite3.connect(RUTA_BD) as conexion:
        conexion.executescript("""
        CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, email TEXT NOT NULL, creado TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS incidencias (id INTEGER PRIMARY KEY AUTOINCREMENT, asunto TEXT NOT NULL, estado TEXT NOT NULL, creado TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS equipos (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, estado TEXT NOT NULL, creado TEXT NOT NULL);
        """)


def leer_estado():
    if not RUTA_BD.exists():
        return {"instalado": False, "mensaje": "No existe todavía una instalación local."}
    asegurar_esquema()
    with sqlite3.connect(RUTA_BD) as conexion:
        configuracion = dict(conexion.execute("SELECT clave, valor FROM configuracion"))
        modulos = [{"codigo": codigo, "nombre": nombre} for codigo, nombre in conexion.execute("SELECT codigo, nombre FROM modulos WHERE activo = 1 ORDER BY codigo")]
        operaciones = [{"momento": momento, "accion": accion, "detalle": detalle} for momento, accion, detalle in conexion.execute("SELECT momento, accion, detalle FROM operaciones ORDER BY rowid DESC LIMIT 5")]
        conteos = {tabla: conexion.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0] for tabla in TABLAS}
    return {"instalado": True, "configuracion": configuracion, "modulos": modulos, "operaciones": operaciones, "conteos": conteos}


def registrar_operacion(conexion, accion, detalle):
    conexion.execute("INSERT INTO operaciones VALUES (?, ?, ?)", (ahora(), accion, detalle))


def cambiar_perfil(perfil):
    configuracion = instalar.cargar_configuracion()
    if perfil not in configuracion["perfiles"]:
        raise ValueError("Perfil no válido.")
    if not RUTA_BD.exists():
        instalar.instalar(perfil)
        return
    asegurar_esquema()
    activos = configuracion["perfiles"][perfil]
    with sqlite3.connect(RUTA_BD) as conexion:
        conexion.execute("UPDATE configuracion SET valor=? WHERE clave='perfil'", (perfil,))
        conexion.executemany("UPDATE modulos SET activo=? WHERE codigo=?", [(int(codigo in activos), codigo) for codigo in configuracion["modulos"]])
        registrar_operacion(conexion, "configuración", f"Perfil actualizado a {perfil}; módulos: {', '.join(activos)}")


def verificar():
    estado = leer_estado()
    if not estado["instalado"]:
        return [{"nombre": "Base de datos", "ok": False, "detalle": "Instala un perfil primero."}]
    with sqlite3.connect(RUTA_BD) as conexion:
        tablas = {fila[0] for fila in conexion.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        operaciones = conexion.execute("SELECT COUNT(*) FROM operaciones").fetchone()[0]
    requeridas = {"configuracion", "modulos", "usuarios", "operaciones", *TABLAS}
    perfil = estado["configuracion"].get("perfil")
    return [
        {"nombre": "Estructura SQLite", "ok": requeridas.issubset(tablas), "detalle": "Tablas de configuración y módulos creadas."},
        {"nombre": "Perfil", "ok": perfil in {"comercial", "soporte"}, "detalle": perfil or "sin perfil"},
        {"nombre": "Módulos", "ok": len(estado["modulos"]) == 3, "detalle": f"{len(estado['modulos'])} módulos activos."},
        {"nombre": "Bitácora", "ok": operaciones >= 1, "detalle": f"{operaciones} operación(es) registrada(s)."},
    ]


def listar_datos(tabla):
    if tabla not in TABLAS:
        raise ValueError("Módulo no reconocido.")
    if not RUTA_BD.exists():
        return []
    asegurar_esquema()
    with sqlite3.connect(RUTA_BD) as conexion:
        activo = conexion.execute("SELECT activo FROM modulos WHERE codigo=?", (MODULO_POR_TABLA[tabla],)).fetchone()
        if not activo or not activo[0]:
            raise ValueError("El módulo no está activo en el perfil seleccionado.")
        conexion.row_factory = sqlite3.Row
        return [dict(fila) for fila in conexion.execute(f"SELECT * FROM {tabla} ORDER BY id DESC")]


def crear_dato(tabla, datos):
    if tabla not in TABLAS:
        raise ValueError("Módulo no reconocido.")
    if not RUTA_BD.exists():
        raise ValueError("Instala un perfil antes de registrar información.")
    valores = [str(datos.get(campo, "")).strip() for campo in TABLAS[tabla]]
    if any(not valor for valor in valores):
        raise ValueError("Completa todos los campos del formulario.")
    asegurar_esquema()
    campos = ", ".join(TABLAS[tabla]) + ", creado"
    marcas = ", ".join("?" for _ in range(len(valores) + 1))
    with sqlite3.connect(RUTA_BD) as conexion:
        activo = conexion.execute("SELECT activo FROM modulos WHERE codigo=?", (MODULO_POR_TABLA[tabla],)).fetchone()
        if not activo or not activo[0]:
            raise ValueError("El módulo no está activo en el perfil seleccionado.")
        conexion.execute(f"INSERT INTO {tabla} ({campos}) VALUES ({marcas})", (*valores, ahora()))
        registrar_operacion(conexion, f"alta en {tabla}", valores[0])


class Manejador(SimpleHTTPRequestHandler):
    def responder_json(self, datos, codigo=HTTPStatus.OK):
        cuerpo = json.dumps(datos, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers(); self.wfile.write(cuerpo)

    def do_GET(self):
        if self.path == "/api/estado": return self.responder_json(leer_estado())
        if self.path == "/api/verificar": return self.responder_json(verificar())
        if self.path.startswith("/api/datos/"):
            try: return self.responder_json(listar_datos(self.path.rsplit("/", 1)[-1]))
            except ValueError as error: return self.responder_json({"error": str(error)}, HTTPStatus.NOT_FOUND)
        return super().do_GET()

    def do_POST(self):
        try:
            longitud = int(self.headers.get("Content-Length", "0")); datos = json.loads(self.rfile.read(longitud).decode("utf-8"))
            if self.path == "/api/perfil": cambiar_perfil(datos.get("perfil", "")); return self.responder_json(leer_estado())
            if self.path.startswith("/api/datos/"):
                crear_dato(self.path.rsplit("/", 1)[-1], datos); return self.responder_json({"ok": True}, HTTPStatus.CREATED)
            return self.responder_json({"error": "Ruta no encontrada."}, HTTPStatus.NOT_FOUND)
        except (json.JSONDecodeError, ValueError) as error:
            return self.responder_json({"error": str(error)}, HTTPStatus.BAD_REQUEST)
        except sqlite3.Error as error:
            return self.responder_json({"error": f"Error de SQLite: {error}"}, HTTPStatus.INTERNAL_SERVER_ERROR)


if __name__ == "__main__":
    asegurar_esquema(); print("ITC ERP disponible en http://127.0.0.1:8080")
    ThreadingHTTPServer(("127.0.0.1", 8080), Manejador).serve_forever()
