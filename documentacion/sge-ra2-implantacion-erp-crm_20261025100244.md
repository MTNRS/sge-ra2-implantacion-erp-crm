# Reporte de proyecto

## Información de generación

- **Fecha:** 2026-10-25 10:02:44 +0100
- **Usuario:** freak
- **Equipo:** JARVIS
- **Sistema operativo:** Windows
- **Arquitectura:** x86_64
- **Directorio de ejecución:** `C:/Users/freak/DAM2`
- **Proyecto documentado:** `C:/Users/freak/Documents/DAM2-entregas/sge-ra2-implantacion-erp-crm`
- **HMAC-SHA-256 de autenticidad:** `ec88361838411aa14dac5a8b99aea29e7193efc85a70ddfc3f931463c652087e`

> El HMAC-SHA-256 se calcula sobre el documento completo usando un secreto incluido en el programa y 64 ceros en el propio campo del HMAC. El secreto no se escribe en el informe. Este mecanismo permite comprobar integridad y que el documento fue generado con el mismo secreto.

## Estructura del proyecto

```
C:/Users/freak/Documents/DAM2-entregas/sge-ra2-implantacion-erp-crm
├── .gitignore
├── 01-ejercicios
│   ├── 01-modulos.py
│   ├── 02-perfiles.py
│   └── 03-comprobacion.py
├── 02-proyecto-unidad
│   └── itc-erp-implantacion
│       ├── OPERACIONES.md
│       ├── configuracion.json
│       ├── instalar.py
│       ├── panel.html
│       ├── servidor.py
│       └── verificar.py
├── 03-criterios-evaluacion
│   └── RESPUESTAS-CRITERIOS.md
└── README.md
```

## Bases de datos SQLite

Esta sección documenta únicamente el esquema de las bases SQLite detectadas. No se vuelcan registros ni datos de usuario.

No se han encontrado bases SQLite con extensiones .db, .sqlite o .sqlite3.

## Código (intercalado)

# sge-ra2-implantacion-erp-crm
**README.md**
```markdown
# RA2 — Implantación ERP-CRM

Continuación del caso de estudio de **ITC ERP** iniciado en RA1. En esta
unidad se plantea una implantación local, independiente y reproducible para una
pequeña empresa de soporte técnico. No utiliza datos reales.

## Estructura

- `01-ejercicios`: tres prácticas pequeñas sobre módulos, perfiles y comprobación.
- `02-proyecto-unidad/itc-erp-implantacion`: instalador, configuración, verificador y panel local.
- `03-criterios-evaluacion`: respuesta razonada a los criterios del RA2.

## Ejecutar el proyecto

Se necesita Python 3, incluido `sqlite3` (biblioteca estándar).

```powershell
cd 02-proyecto-unidad/itc-erp-implantacion
python servidor.py
```

Abrir `http://127.0.0.1:8080/panel.html`. El asistente permite instalar un
perfil desde la interfaz y ejecutar la verificación. El perfil `comercial`
instala CRM, ventas y facturación; `soporte` instala CRM, incidencias e
inventario.

## Relación con el RA1

El RA1 definía el caso de uso, los módulos posibles y una arquitectura inicial
para ITC ERP. Este RA2 no copia aquella interfaz: implanta una versión local
propia, con una configuración explícita, una base de datos SQLite y una prueba
de funcionamiento.

```
## 01-ejercicios
**01-modulos.py**
```python
MODULOS = {
    "crm": "Clientes y oportunidades",
    "ventas": "Presupuestos y pedidos",
    "facturacion": "Facturas y cobros",
    "inventario": "Existencias y equipos",
    "incidencias": "Soporte técnico",
}

for codigo, descripcion in MODULOS.items():
    print(f"{codigo:12} {descripcion}")

```
**02-perfiles.py**
```python
PERFILES = {
    "comercial": ["crm", "ventas", "facturacion"],
    "soporte": ["crm", "incidencias", "inventario"],
}

for nombre, modulos in PERFILES.items():
    print(f"{nombre}: {', '.join(modulos)}")

```
**03-comprobacion.py**
```python
import sqlite3
from pathlib import Path

ruta = Path("../02-proyecto-unidad/itc-erp-implantacion/data/itc_erp.sqlite")
if not ruta.exists():
    raise SystemExit("No existe una instalación. Ejecuta instalar.py primero.")

with sqlite3.connect(ruta) as conexion:
    modulos = conexion.execute("SELECT codigo FROM modulos WHERE activo = 1").fetchall()

print("Módulos activos:", ", ".join(codigo for (codigo,) in modulos))

```
## 02-proyecto-unidad
### itc-erp-implantacion
**OPERACIONES.md**
```markdown
# Operaciones e incidencias

## Supuesto de implantación

Integra Tech Consulting necesita registrar clientes, incidencias y equipos
prestados en un entorno de demostración. Por ello se utiliza el perfil
`soporte`: CRM, incidencias e inventario. Todos los datos son ficticios y
locales.

## Instalación realizada

1. Se comprobó que Python 3 estaba disponible.
2. Se ejecutó `python instalar.py --perfil soporte`.
3. El instalador creó `data/itc_erp.sqlite`, las tablas necesarias y el registro
   de la operación.
4. Se ejecutó `python verificar.py` para revisar las tablas, el perfil, los tres
   módulos activos y la bitácora de instalación.
5. Se abrió `panel.html` mediante un servidor HTTP local para revisar los
   perfiles y los módulos definidos en la configuración.

## Segunda instalación adaptada

El mismo instalador permite el perfil `comercial`, con CRM, ventas y
facturación. Se trata de un segundo supuesto: una empresa que prioriza pedidos
y cobros en lugar de la gestión de incidencias.

## Incidencias previstas

| Incidencia | Prevención o resolución |
| --- | --- |
| Se vuelve a ejecutar el instalador | Se detiene sin sobrescribir la base existente. |
| Se indica un perfil no válido | `argparse` limita los valores a `comercial` y `soporte`. |
| No existe la base al verificar | El verificador informa de que debe ejecutarse el instalador. |
| Se abre el panel como archivo | Se debe usar `python -m http.server` para que `fetch()` pueda leer el JSON. |

```
**configuracion.json**
```json
{
  "empresa": "Integra Tech Consulting (demostración)",
  "moneda": "EUR",
  "zona_horaria": "Europe/Madrid",
  "perfiles": {
    "comercial": ["crm", "ventas", "facturacion"],
    "soporte": ["crm", "incidencias", "inventario"]
  },
  "modulos": {
    "crm": "Clientes y oportunidades",
    "ventas": "Presupuestos y pedidos",
    "facturacion": "Facturas y cobros",
    "inventario": "Existencias y equipos",
    "incidencias": "Soporte técnico"
  }
}

```
**instalar.py**
```python
"""Instalador local y didáctico de ITC ERP para el RA2."""
import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).parent
RUTA_CONFIG = BASE / "configuracion.json"
RUTA_BD = BASE / "data" / "itc_erp.sqlite"


def cargar_configuracion():
    with RUTA_CONFIG.open(encoding="utf-8") as archivo:
        return json.load(archivo)


def instalar(perfil):
    configuracion = cargar_configuracion()
    if perfil not in configuracion["perfiles"]:
        raise ValueError(f"Perfil no válido: {perfil}")
    if RUTA_BD.exists():
        raise FileExistsError("Ya existe una instalación. No se sobrescribe la base de datos.")

    RUTA_BD.parent.mkdir(exist_ok=True)
    modulos_activos = configuracion["perfiles"][perfil]
    marca_tiempo = datetime.now(timezone.utc).isoformat(timespec="seconds")

    with sqlite3.connect(RUTA_BD) as conexion:
        conexion.executescript(
            """
            CREATE TABLE configuracion (clave TEXT PRIMARY KEY, valor TEXT NOT NULL);
            CREATE TABLE modulos (codigo TEXT PRIMARY KEY, nombre TEXT NOT NULL, activo INTEGER NOT NULL);
            CREATE TABLE usuarios (usuario TEXT PRIMARY KEY, rol TEXT NOT NULL);
            CREATE TABLE operaciones (momento TEXT NOT NULL, accion TEXT NOT NULL, detalle TEXT NOT NULL);
            """
        )
        conexion.executemany(
            "INSERT INTO configuracion VALUES (?, ?)",
            [("empresa", configuracion["empresa"]), ("moneda", configuracion["moneda"]),
             ("zona_horaria", configuracion["zona_horaria"]), ("perfil", perfil)],
        )
        conexion.executemany(
            "INSERT INTO modulos VALUES (?, ?, ?)",
            [(codigo, nombre, int(codigo in modulos_activos))
             for codigo, nombre in configuracion["modulos"].items()],
        )
        conexion.execute("INSERT INTO usuarios VALUES (?, ?)", ("administrador", "administración"))
        conexion.execute(
            "INSERT INTO operaciones VALUES (?, ?, ?)",
            (marca_tiempo, "instalación", f"Perfil {perfil}; módulos: {', '.join(modulos_activos)}"),
        )

    print(f"Instalación {perfil} creada en {RUTA_BD}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Instala ITC ERP en SQLite.")
    parser.add_argument("--perfil", required=True, choices=("comercial", "soporte"))
    argumentos = parser.parse_args()
    try:
        instalar(argumentos.perfil)
    except (ValueError, FileExistsError, sqlite3.Error) as error:
        raise SystemExit(f"ERROR DE INSTALACIÓN: {error}")

```
**panel.html**
```html
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ITC ERP · Asistente de implantación</title>
  <style>
    :root { font-family:system-ui,sans-serif; color:#e5e7eb; background:#0f172a; }
    body { max-width:1050px; margin:auto; padding:2rem; } header { border-bottom:1px solid #334155; margin-bottom:1.5rem; }
    .etiqueta { color:#67e8f9; font-size:.8rem; letter-spacing:.12em; } .subtitulo,.muted { color:#94a3b8; }
    .rejilla { display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:1rem; }
    section { background:#172033; border:1px solid #334155; padding:1.25rem; border-radius:.6rem; }
    button { background:#0891b2; border:0; padding:.7rem 1rem; border-radius:.35rem; color:white; cursor:pointer; font-weight:700; }
    button:disabled { opacity:.45; cursor:not-allowed; } .ok { color:#86efac; } .fallo { color:#fca5a5; }
    ul { padding-left:1.25rem; } #mensaje { min-height:1.5rem; }
  </style>
</head>
<body>
  <header>
    <p class="etiqueta">INTEGRA TECH CONSULTING · RA2</p>
    <h1>Asistente de implantación ITC ERP</h1>
    <p class="subtitulo">Instala un perfil local, revisa sus módulos y verifica el resultado sin datos reales.</p>
  </header>
  <main class="rejilla">
    <section>
      <h2>1. Elegir perfil</h2>
      <p><strong>Soporte</strong>: CRM, incidencias e inventario.</p>
      <button data-perfil="soporte">Instalar perfil de soporte</button>
      <p><strong>Comercial</strong>: CRM, ventas y facturación.</p>
      <button data-perfil="comercial">Instalar perfil comercial</button>
      <p id="mensaje" class="muted" role="status">Comprobando instalación local…</p>
    </section>
    <section><h2>2. Módulos activos</h2><ul id="modulos"><li class="muted">Sin instalación.</li></ul></section>
    <section><h2>3. Verificación</h2><button id="botonVerificar">Ejecutar comprobación</button><ul id="pruebas"><li class="muted">Aún no ejecutada.</li></ul></section>
    <section><h2>Bitácora de operaciones</h2><ul id="operaciones"><li class="muted">Sin operaciones.</li></ul></section>
  </main>
  <script>
    const $ = selector => document.querySelector(selector);
    const escapeHtml = texto => String(texto).replace(/[&<>'"]/g, caracter => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[caracter]));
    async function cargarEstado() {
      const estado = await (await fetch('/api/estado')).json();
      [...document.querySelectorAll('[data-perfil]')].forEach(boton => boton.disabled = estado.instalado);
      if (!estado.instalado) { $('#mensaje').textContent = estado.mensaje; return; }
      $('#mensaje').innerHTML = `<span class="ok">Instalado:</span> perfil ${escapeHtml(estado.configuracion.perfil)} para ${escapeHtml(estado.configuracion.empresa)}.`;
      $('#modulos').innerHTML = estado.modulos.map(modulo => `<li><strong>${escapeHtml(modulo.codigo)}</strong> — ${escapeHtml(modulo.nombre)}</li>`).join('');
      $('#operaciones').innerHTML = estado.operaciones.map(operacion => `<li>${escapeHtml(operacion.accion)}: ${escapeHtml(operacion.detalle)}</li>`).join('');
    }
    async function instalar(perfil) {
      $('#mensaje').textContent = 'Instalando…';
      const respuesta = await fetch('/api/instalar', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({perfil})});
      const resultado = await respuesta.json();
      if (!respuesta.ok) { $('#mensaje').innerHTML = `<span class="fallo">${escapeHtml(resultado.error)}</span>`; return; }
      await cargarEstado();
    }
    async function ejecutarVerificacion() {
      const pruebas = await (await fetch('/api/verificar')).json();
      $('#pruebas').innerHTML = pruebas.map(prueba => `<li class="${prueba.ok ? 'ok' : 'fallo'}">${prueba.ok ? 'OK' : 'FALLO'} — ${escapeHtml(prueba.nombre)}: ${escapeHtml(prueba.detalle)}</li>`).join('');
    }
    document.querySelectorAll('[data-perfil]').forEach(boton => boton.addEventListener('click', () => instalar(boton.dataset.perfil)));
    $('#botonVerificar').addEventListener('click', ejecutarVerificacion);
    cargarEstado().catch(error => { $('#mensaje').textContent = `No se puede conectar con el servidor: ${error.message}`; });
  </script>
</body>
</html>
```
**servidor.py**
```python
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
```
**verificar.py**
```python
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

```
## 03-criterios-evaluacion
**RESPUESTAS-CRITERIOS.md**
```markdown
# Respuestas a los criterios de evaluación — RA2

## Contexto

La entrega continúa el caso ITC ERP del RA1. En aquella fase se definían un
núcleo, módulos y datos de muestra; aquí se realiza una implantación local e
independiente para Integra Tech Consulting. El código de esta entrega se ha
escrito de forma propia.

| Criterio | Evidencia en la entrega |
| --- | --- |
| a) Módulos ERP-CRM | `configuracion.json` identifica CRM, ventas, facturación, inventario e incidencias. `01-ejercicios/01-modulos.py` los lista con su finalidad. |
| b) Diferentes instalaciones | `instalar.py` acepta `--perfil comercial` y `--perfil soporte`; ambos crean la misma estructura técnica con módulos activos diferentes. `servidor.py` permite iniciar la instalación desde el asistente local. |
| c) Configuración de módulos | El instalador lee empresa, moneda, zona horaria y perfiles desde `configuracion.json` y los registra en SQLite. El asistente muestra los módulos que han quedado activos. |
| d) Instalaciones adaptadas | `OPERACIONES.md` explica dos supuestos. Soporte activa CRM, incidencias e inventario; comercial activa CRM, ventas y facturación. |
| e) Verificación | `verificar.py` y el botón «Ejecutar comprobación» del asistente comprueban que existen las cuatro tablas, que el perfil es válido, que hay tres módulos activos y que se registró la instalación. |
| f) Documentación e incidencias | `OPERACIONES.md` registra el procedimiento y cuatro incidencias previstas con su solución. El instalador deja una fila en la tabla `operaciones`. |

## Prueba de la entrega

```powershell
cd 02-proyecto-unidad/itc-erp-implantacion
python instalar.py --perfil soporte
python verificar.py
```

Resultado esperado: cuatro líneas que comienzan por `OK` y código de salida
`0`.

```
