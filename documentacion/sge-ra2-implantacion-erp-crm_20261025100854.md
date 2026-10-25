# Reporte de proyecto

## Información de generación

- **Fecha:** 2026-10-25 10:08:54 +0100
- **Usuario:** freak
- **Equipo:** JARVIS
- **Sistema operativo:** Windows
- **Arquitectura:** x86_64
- **Directorio de ejecución:** `C:/Users/freak/DAM2`
- **Proyecto documentado:** `C:/Users/freak/Documents/DAM2-entregas/sge-ra2-implantacion-erp-crm`
- **HMAC-SHA-256 de autenticidad:** `5a234d5002a7945805745f1f1f631a5e827573ee49e8bc65a0657d70d7c916ce`

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
│       ├── aplicacion.js
│       ├── configuracion.json
│       ├── estilos.css
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
**aplicacion.js**
```js
const $ = selector => document.querySelector(selector);
const textoSeguro = texto => String(texto ?? '').replace(/[&<>'"]/g, caracter => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[caracter]));

async function cargarEstado() {
  const estado = await (await fetch('/api/estado')).json();
  const botones = [...document.querySelectorAll('[data-perfil]')];
  botones.forEach(boton => boton.disabled = estado.instalado);
  if (!estado.instalado) {
    $('#mensaje').textContent = estado.mensaje;
    return;
  }
  const configuracion = estado.configuracion;
  $('#estadoGeneral').textContent = 'Instalación operativa';
  $('#estadoGeneral').className = 'insignia verde';
  $('#contadorModulos').textContent = estado.modulos.length;
  $('#estadoBase').textContent = 'Activa';
  $('#contadorOperaciones').textContent = estado.operaciones.length;
  $('#perfilActual').textContent = `Perfil ${configuracion.perfil}`;
  $('#mensaje').textContent = `Instalado para ${configuracion.empresa}. Para cambiar de supuesto se prepara una instalación nueva.`;
  $('#listaModulos').innerHTML = estado.modulos.map(modulo => `<article class="modulo"><b>${textoSeguro(modulo.codigo)}</b><span>${textoSeguro(modulo.nombre)}</span></article>`).join('');
  $('#operaciones').innerHTML = estado.operaciones.map(operacion => `<tr><td>${textoSeguro(operacion.accion)}</td><td>${textoSeguro(operacion.detalle)}</td><td>${textoSeguro(operacion.momento)}</td></tr>`).join('');
}

async function instalar(perfil) {
  $('#mensaje').textContent = 'Instalando perfil…';
  const respuesta = await fetch('/api/instalar', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({perfil})});
  const resultado = await respuesta.json();
  if (!respuesta.ok) { $('#mensaje').textContent = resultado.error; return; }
  await cargarEstado();
}

async function verificar() {
  const pruebas = await (await fetch('/api/verificar')).json();
  $('#contadorPruebas').textContent = `${pruebas.filter(prueba => prueba.ok).length}/${pruebas.length}`;
  $('#pruebas').innerHTML = pruebas.map(prueba => `<li class="${prueba.ok ? 'ok' : 'fallo'}"><strong>${prueba.ok ? 'OK' : 'FALLO'}</strong> · ${textoSeguro(prueba.nombre)} — ${textoSeguro(prueba.detalle)}</li>`).join('');
}

document.querySelectorAll('[data-perfil]').forEach(boton => boton.addEventListener('click', () => instalar(boton.dataset.perfil)));
$('#botonVerificar').addEventListener('click', verificar);
cargarEstado().catch(error => { $('#mensaje').textContent = `Error de conexión: ${error.message}`; });
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
**estilos.css**
```css
:root{--azul:#56b7ff;--verde:#72efb2;--fondo:#f6fbff;--tinta:#172536;--suave:#6b7788;--borde:#dbe8ee;--panel:#fff;--lateral:#072236}*{box-sizing:border-box}body{margin:0;font:15px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif;background:var(--fondo);color:var(--tinta)}.aplicacion{min-height:100vh}.barra-lateral{position:fixed;inset:0 auto 0 0;width:260px;padding:24px 14px;display:flex;flex-direction:column;background:linear-gradient(180deg,#071f31,#0a3448 62%,#07523d);color:#b8d0dc}.marca{display:flex;gap:10px;align-items:center;padding:0 10px 28px;color:#fff}.marca-icono{display:grid;place-items:center;width:38px;height:38px;border-radius:10px;background:linear-gradient(135deg,var(--azul),var(--verde));color:#06243a;font-size:12px;font-weight:900}.marca strong,.marca small{display:block}.marca small{font-size:11px;color:#98b0bc}.seccion{margin:17px 11px 6px;font-size:10px;letter-spacing:.1em;color:#77a1b5}.enlace{display:block;margin:2px 0;padding:9px 11px;border-radius:8px;color:#bbd0da;text-decoration:none}.enlace:hover,.enlace.activo{background:rgba(139,209,255,.17);color:#fff}.plan{margin-top:auto;padding:13px;border-top:1px solid rgba(255,255,255,.16);font-size:12px;color:#b6ccd6}.plan strong{color:#fff}.contenido{margin-left:260px}.cabecera{height:78px;padding:14px 34px;display:flex;justify-content:space-between;align-items:center;background:rgba(255,255,255,.92);border-bottom:1px solid var(--borde)}.cabecera h1{margin:0;font-size:21px}.ruta{margin:0;color:var(--suave);font-size:12px}.usuario{display:flex;gap:9px;align-items:center;font-size:13px}.usuario b{display:grid;place-items:center;width:34px;height:34px;border-radius:50%;color:#063a30;background:var(--verde)}.pagina{max-width:1250px;margin:auto;padding:30px}.titulo-pagina,.tarjeta-cabecera{display:flex;justify-content:space-between;align-items:flex-start;gap:20px}.titulo-pagina h2{margin:0;font-size:25px}.titulo-pagina p,.texto-secundario{margin:5px 0;color:var(--suave)}.rejilla-indicadores{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:24px 0}.indicador,.tarjeta{background:var(--panel);border:1px solid var(--borde);border-radius:16px;box-shadow:0 8px 24px rgba(10,61,90,.06)}.indicador{padding:18px;display:flex;gap:13px}.indicador>span{display:grid;place-items:center;width:39px;height:39px;border-radius:11px;background:#e8f6ff;color:#168fe8;font-size:20px}.indicador small,.indicador em{display:block;color:var(--suave);font-size:12px;font-style:normal}.indicador strong{display:block;margin:2px 0;font-size:23px}.rejilla-dos{display:grid;grid-template-columns:1.2fr 1fr;gap:18px;margin-bottom:18px}.tarjeta{padding:21px;margin-bottom:18px}.tarjeta h3{margin:0;font-size:16px}.insignia{display:inline-block;padding:5px 9px;border-radius:999px;font-size:12px;font-weight:700}.neutra{background:#edf2f5;color:#52616c}.azul{background:#e3f4ff;color:#0874b8}.verde{background:#e4f8ed;color:#137044}.perfiles{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:18px 0}.perfil{border:1px solid #cfe5ef;border-radius:12px;padding:15px;text-align:left;background:#fbfdff;cursor:pointer;color:var(--tinta)}.perfil:hover{border-color:var(--azul);background:#f1faff}.perfil:disabled{opacity:.55;cursor:not-allowed}.perfil strong,.perfil span,.perfil small{display:block}.perfil span{margin:6px 0;color:#0874b8;font-size:13px}.perfil small{color:var(--suave)}button{font:inherit}.boton-secundario{padding:8px 11px;border:1px solid #b9d8e7;border-radius:8px;background:#f6fbff;color:#0874b8;font-weight:700;cursor:pointer}.estado-texto{min-height:22px;margin:0;color:var(--suave)}.lista-pruebas{padding:0;margin:18px 0 0;list-style:none}.lista-pruebas li{margin:8px 0;padding:9px 10px;border-radius:7px;background:#f8fafc}.ok{color:#137044;background:#effbf4!important}.fallo{color:#b42318;background:#fff1f1!important}.pendiente{color:var(--suave)}.rejilla-modulos{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:18px}.modulo{padding:15px;border:1px solid var(--borde);border-radius:11px;background:#fbfdff}.modulo b{display:block;color:#0874b8;text-transform:uppercase;font-size:12px}.modulo span{color:var(--suave)}.tabla-contenedor{overflow:auto;margin-top:16px}table{width:100%;border-collapse:collapse;text-align:left}th,td{padding:11px;border-bottom:1px solid var(--borde)}th{font-size:12px;color:var(--suave)}@media(max-width:850px){.barra-lateral{position:static;width:auto}.contenido{margin:0}.rejilla-indicadores,.rejilla-dos{grid-template-columns:1fr 1fr}.pagina{padding:18px}}@media(max-width:560px){.rejilla-indicadores,.rejilla-dos,.perfiles,.rejilla-modulos{grid-template-columns:1fr}.cabecera{padding:12px 18px}.usuario span{display:none}}
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
  <title>Configuración · Integra Tech Consulting</title>
  <link rel="stylesheet" href="estilos.css">
</head>
<body>
  <div class="aplicacion">
    <aside class="barra-lateral">
      <div class="marca"><span class="marca-icono">ITC</span><div><strong>Integra Tech</strong><small>Gestión Empresarial</small></div></div>
      <p class="seccion">PRINCIPAL</p>
      <a href="#resumen" class="enlace activo">▦ Dashboard</a>
      <a href="#modulos" class="enlace">▣ Módulos</a>
      <p class="seccion">OPERACIONES</p>
      <a href="#modulos" class="enlace">♧ Clientes</a>
      <a href="#modulos" class="enlace">◈ Soporte</a>
      <a href="#modulos" class="enlace">▤ Inventario</a>
      <p class="seccion">SISTEMA</p>
      <a href="#implantacion" class="enlace activo">⚙ Configuración</a>
      <div class="plan">Plan académico<br><strong>Entorno local</strong></div>
    </aside>
    <main class="contenido">
      <header class="cabecera">
        <div><p class="ruta">Sistema / Configuración / Implantación</p><h1>Configuración</h1></div>
        <div class="usuario"><span>Administrador ITC</span><b>AD</b></div>
      </header>
      <div class="pagina">
        <section id="resumen" class="titulo-pagina"><div><h2>Estado de la implantación</h2><p>Configuración local de módulos para el entorno académico ITC.</p></div><span id="estadoGeneral" class="insignia neutra">Comprobando…</span></section>
        <section class="rejilla-indicadores">
          <article class="indicador"><span>▣</span><div><small>Módulos activos</small><strong id="contadorModulos">—</strong><em>Perfil seleccionado</em></div></article>
          <article class="indicador"><span>◉</span><div><small>Base de datos</small><strong id="estadoBase">—</strong><em>SQLite local</em></div></article>
          <article class="indicador"><span>✓</span><div><small>Comprobaciones</small><strong id="contadorPruebas">—</strong><em>Última ejecución</em></div></article>
          <article class="indicador"><span>◷</span><div><small>Operaciones</small><strong id="contadorOperaciones">—</strong><em>Bitácora local</em></div></article>
        </section>
        <section class="rejilla-dos">
          <article id="implantacion" class="tarjeta">
            <div class="tarjeta-cabecera"><h3>Implantación de módulos</h3><span class="insignia azul">RA2</span></div>
            <p class="texto-secundario">Selecciona el supuesto empresarial. El instalador registra la configuración y activa solo los módulos necesarios.</p>
            <div class="perfiles">
              <button class="perfil" data-perfil="soporte"><strong>Soporte técnico</strong><span>CRM · Soporte · Inventario</span><small>Para gestionar clientes, incidencias y equipos.</small></button>
              <button class="perfil" data-perfil="comercial"><strong>Comercial</strong><span>CRM · Ventas · Facturación</span><small>Para presupuestos, pedidos y cobros.</small></button>
            </div>
            <p id="mensaje" class="estado-texto" role="status">Conectando con el instalador…</p>
          </article>
          <article class="tarjeta">
            <div class="tarjeta-cabecera"><h3>Verificación del sistema</h3><button id="botonVerificar" class="boton-secundario">Ejecutar prueba</button></div>
            <ul id="pruebas" class="lista-pruebas"><li class="pendiente">Aún no se han ejecutado las comprobaciones.</li></ul>
          </article>
        </section>
        <section id="modulos" class="tarjeta">
          <div class="tarjeta-cabecera"><div><h3>Módulos instalados</h3><p class="texto-secundario">Vista del perfil que tendría disponible la organización.</p></div><span id="perfilActual" class="insignia neutra">Sin perfil</span></div>
          <div id="listaModulos" class="rejilla-modulos"><p class="pendiente">No hay módulos activados.</p></div>
        </section>
        <section class="tarjeta">
          <div class="tarjeta-cabecera"><h3>Operaciones realizadas</h3><span class="texto-secundario">Registro de instalación</span></div>
          <div class="tabla-contenedor"><table><thead><tr><th>Acción</th><th>Detalle</th><th>Momento</th></tr></thead><tbody id="operaciones"><tr><td colspan="3" class="pendiente">Sin operaciones registradas.</td></tr></tbody></table></div>
        </section>
      </div>
    </main>
  </div>
  <script src="aplicacion.js"></script>
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
