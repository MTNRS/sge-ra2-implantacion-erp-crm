# Reporte de proyecto

## Información de generación

- **Fecha:** 2026-10-25 10:23:19 +0100
- **Usuario:** freak
- **Equipo:** JARVIS
- **Sistema operativo:** Windows
- **Arquitectura:** x86_64
- **Directorio de ejecución:** `C:/Users/freak/DAM2`
- **Proyecto documentado:** `C:/Users/freak/Documents/DAM2-entregas/sge-ra2-implantacion-erp-crm`
- **HMAC-SHA-256 de autenticidad:** `5f5abb4b38e9e9ac6a2c9ba309e601d8c3dcca84b0a962ddfce0b8756dfc3b94`

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
│       ├── modulo.css
│       ├── modulo.html
│       ├── modulo.js
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

Abrir `http://127.0.0.1:8080/panel.html`. El panel permite cambiar el perfil
sin perder los datos locales, ejecutar la verificación y usar los módulos
habilitados: alta y consulta de clientes, incidencias y equipos. El perfil
`comercial` activa CRM, ventas y facturación; `soporte` activa CRM,
incidencias e inventario.

Las áreas operativas se abren como módulos independientes: `modulo.html?area=clientes`,
`modulo.html?area=incidencias` y `modulo.html?area=equipos`. Cada una incluye
sus indicadores, búsqueda, tabla y formulario modal de alta.

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
5. Se abrió `panel.html` mediante el servidor local para revisar los perfiles,
   los módulos definidos y registrar datos de demostración.

## Operativa comprobada

Desde el panel se ha comprobado el alta de un cliente, una incidencia y un
equipo ficticios. Cada alta se guarda en SQLite y deja una entrada en la
bitácora. Al pasar temporalmente al perfil `comercial`, el área de soporte se
bloqueó; al volver a `soporte` recuperó el acceso sin perder los registros.

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
| Se abre el panel como archivo | Se debe usar `python servidor.py` para que las rutas de datos estén disponibles. |
| Se intenta abrir un área no activa | El panel informa del módulo deshabilitado y el servidor rechaza la petición. |

```
**aplicacion.js**
```js
const $ = selector => document.querySelector(selector);
const textoSeguro = texto => String(texto ?? '').replace(/[&<>'"]/g, caracter => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[caracter]));

const areas = {
  clientes: {codigo: 'crm', titulo: 'Clientes', descripcion: 'Alta y consulta de clientes para el equipo comercial y de soporte.', campos: [['nombre', 'Nombre o empresa', 'text'], ['email', 'Correo de contacto', 'email']]},
  incidencias: {codigo: 'incidencias', titulo: 'Soporte técnico', descripcion: 'Registro inicial de incidencias del servicio ITC.', campos: [['asunto', 'Asunto de la incidencia', 'text'], ['estado', 'Estado', 'select']]},
  equipos: {codigo: 'inventario', titulo: 'Inventario', descripcion: 'Control básico de equipos asociados al servicio.', campos: [['nombre', 'Equipo o activo', 'text'], ['estado', 'Estado', 'select']]}
};

let estadoActual = null;
let vistaActual = 'resumen';

async function pedir(ruta, opciones = {}) {
  const respuesta = await fetch(ruta, opciones);
  const datos = await respuesta.json();
  if (!respuesta.ok) throw new Error(datos.error || 'No se pudo completar la operación.');
  return datos;
}

function pintarEstado(estado) {
  estadoActual = estado;
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
  $('#mensaje').textContent = `Perfil ${configuracion.perfil} activo. Puedes cambiarlo sin perder los registros del entorno local.`;
  $('#listaModulos').innerHTML = estado.modulos.map(modulo => `<article class="modulo"><b>${textoSeguro(modulo.codigo)}</b><span>${textoSeguro(modulo.nombre)}</span></article>`).join('');
  $('#operaciones').innerHTML = estado.operaciones.map(operacion => `<tr><td>${textoSeguro(operacion.accion)}</td><td>${textoSeguro(operacion.detalle)}</td><td>${textoSeguro(operacion.momento)}</td></tr>`).join('');
  document.querySelectorAll('[data-perfil]').forEach(boton => boton.classList.toggle('seleccionado', boton.dataset.perfil === configuracion.perfil));
}

async function cargarEstado() {
  pintarEstado(await pedir('/api/estado'));
}

async function cambiarPerfil(perfil) {
  $('#mensaje').textContent = `Actualizando el perfil ${perfil}…`;
  try {
    pintarEstado(await pedir('/api/perfil', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({perfil})}));
    if (areas[vistaActual]) await mostrarArea(vistaActual);
  } catch (error) {
    $('#mensaje').textContent = error.message;
  }
}

async function verificar() {
  try {
    const pruebas = await pedir('/api/verificar');
    $('#contadorPruebas').textContent = `${pruebas.filter(prueba => prueba.ok).length}/${pruebas.length}`;
    $('#pruebas').innerHTML = pruebas.map(prueba => `<li class="${prueba.ok ? 'ok' : 'fallo'}"><strong>${prueba.ok ? 'OK' : 'FALLO'}</strong> · ${textoSeguro(prueba.nombre)} — ${textoSeguro(prueba.detalle)}</li>`).join('');
  } catch (error) {
    $('#pruebas').innerHTML = `<li class="fallo">${textoSeguro(error.message)}</li>`;
  }
}

function activo(codigo) {
  return estadoActual && estadoActual.modulos.some(modulo => modulo.codigo === codigo);
}

function control(campo) {
  const [nombre, etiqueta, tipo] = campo;
  if (tipo === 'select') return `<label>${etiqueta}<select name="${nombre}" required><option value="abierto">Abierto</option><option value="en revisión">En revisión</option><option value="operativo">Operativo</option></select></label>`;
  return `<label>${etiqueta}<input name="${nombre}" type="${tipo}" required maxlength="100"></label>`;
}

async function mostrarArea(area) {
  const definicion = areas[area];
  vistaActual = area;
  if (!estadoActual || !estadoActual.instalado) {
    $('#zonaOperativa').innerHTML = '<p class="pendiente">Configura un perfil antes de utilizar esta área.</p>';
    return;
  }
  if (!activo(definicion.codigo)) {
    $('#zonaOperativa').innerHTML = `<div class="aviso"><strong>${definicion.titulo} no está activo en este perfil.</strong><p>Cambia al perfil de soporte para habilitar este módulo.</p></div>`;
    return;
  }
  const registros = await pedir(`/api/datos/${area}`);
  const columnas = definicion.campos.map(campo => campo[0]);
  $('#zonaOperativa').innerHTML = `
    <div class="operativa-cabecera"><div><h3>${definicion.titulo}</h3><p class="texto-secundario">${definicion.descripcion}</p></div><span class="insignia azul">${registros.length} registros</span></div>
    <form id="formularioArea" class="formulario" data-area="${area}">${definicion.campos.map(control).join('')}<button class="boton-primario" type="submit">Registrar</button></form>
    <div class="tabla-contenedor"><table><thead><tr>${columnas.map(columna => `<th>${textoSeguro(columna)}</th>`).join('')}<th>Creado</th></tr></thead><tbody>${registros.length ? registros.map(registro => `<tr>${columnas.map(columna => `<td>${textoSeguro(registro[columna])}</td>`).join('')}<td>${textoSeguro(registro.creado)}</td></tr>`).join('') : `<tr><td colspan="${columnas.length + 1}" class="pendiente">Todavía no hay registros. Añade el primero.</td></tr>`}</tbody></table></div>`;
  $('#formularioArea').addEventListener('submit', guardarRegistro);
}

async function guardarRegistro(evento) {
  evento.preventDefault();
  const formulario = evento.currentTarget;
  const area = formulario.dataset.area;
  const datos = Object.fromEntries(new FormData(formulario));
  const boton = formulario.querySelector('button');
  boton.disabled = true;
  try {
    await pedir(`/api/datos/${area}`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(datos)});
    await cargarEstado();
    await mostrarArea(area);
  } catch (error) {
    $('#mensaje').textContent = error.message;
  } finally {
    boton.disabled = false;
  }
}

function navegar(evento) {
  evento.preventDefault();
  const vista = evento.currentTarget.dataset.vista;
  document.querySelectorAll('[data-vista]').forEach(enlace => enlace.classList.toggle('activo', enlace.dataset.vista === vista));
  if (areas[vista]) return mostrarArea(vista);
  vistaActual = vista;
  const destino = vista === 'configuracion' ? '#implantacion' : `#${vista}`;
  document.querySelector(destino).scrollIntoView({behavior:'smooth', block:'start'});
}

document.querySelectorAll('[data-perfil]').forEach(boton => boton.addEventListener('click', () => cambiarPerfil(boton.dataset.perfil)));
document.querySelectorAll('[data-vista]').forEach(enlace => enlace.addEventListener('click', navegar));
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
:root{--azul:#56b7ff;--verde:#72efb2;--fondo:#f6fbff;--tinta:#172536;--suave:#6b7788;--borde:#dbe8ee;--panel:#fff;--lateral:#072236}*{box-sizing:border-box}body{margin:0;font:15px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif;background:var(--fondo);color:var(--tinta)}.aplicacion{min-height:100vh}.barra-lateral{position:fixed;inset:0 auto 0 0;width:260px;padding:24px 14px;display:flex;flex-direction:column;background:linear-gradient(180deg,#071f31,#0a3448 62%,#07523d);color:#b8d0dc}.marca{display:flex;gap:10px;align-items:center;padding:0 10px 28px;color:#fff}.marca-icono{display:grid;place-items:center;width:38px;height:38px;border-radius:10px;background:linear-gradient(135deg,var(--azul),var(--verde));color:#06243a;font-size:12px;font-weight:900}.marca strong,.marca small{display:block}.marca small{font-size:11px;color:#98b0bc}.seccion{margin:17px 11px 6px;font-size:10px;letter-spacing:.1em;color:#77a1b5}.enlace{display:block;margin:2px 0;padding:9px 11px;border-radius:8px;color:#bbd0da;text-decoration:none}.enlace:hover,.enlace.activo{background:rgba(139,209,255,.17);color:#fff}.plan{margin-top:auto;padding:13px;border-top:1px solid rgba(255,255,255,.16);font-size:12px;color:#b6ccd6}.plan strong{color:#fff}.contenido{margin-left:260px}.cabecera{height:78px;padding:14px 34px;display:flex;justify-content:space-between;align-items:center;background:rgba(255,255,255,.92);border-bottom:1px solid var(--borde)}.cabecera h1{margin:0;font-size:21px}.ruta{margin:0;color:var(--suave);font-size:12px}.usuario{display:flex;gap:9px;align-items:center;font-size:13px}.usuario b{display:grid;place-items:center;width:34px;height:34px;border-radius:50%;color:#063a30;background:var(--verde)}.pagina{max-width:1250px;margin:auto;padding:30px}.titulo-pagina,.tarjeta-cabecera{display:flex;justify-content:space-between;align-items:flex-start;gap:20px}.titulo-pagina h2{margin:0;font-size:25px}.titulo-pagina p,.texto-secundario{margin:5px 0;color:var(--suave)}.rejilla-indicadores{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:24px 0}.indicador,.tarjeta{background:var(--panel);border:1px solid var(--borde);border-radius:16px;box-shadow:0 8px 24px rgba(10,61,90,.06)}.indicador{padding:18px;display:flex;gap:13px}.indicador>span{display:grid;place-items:center;width:39px;height:39px;border-radius:11px;background:#e8f6ff;color:#168fe8;font-size:20px}.indicador small,.indicador em{display:block;color:var(--suave);font-size:12px;font-style:normal}.indicador strong{display:block;margin:2px 0;font-size:23px}.rejilla-dos{display:grid;grid-template-columns:1.2fr 1fr;gap:18px;margin-bottom:18px}.tarjeta{padding:21px;margin-bottom:18px}.tarjeta h3{margin:0;font-size:16px}.insignia{display:inline-block;padding:5px 9px;border-radius:999px;font-size:12px;font-weight:700}.neutra{background:#edf2f5;color:#52616c}.azul{background:#e3f4ff;color:#0874b8}.verde{background:#e4f8ed;color:#137044}.perfiles{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:18px 0}.perfil{border:1px solid #cfe5ef;border-radius:12px;padding:15px;text-align:left;background:#fbfdff;cursor:pointer;color:var(--tinta)}.perfil:hover{border-color:var(--azul);background:#f1faff}.perfil.seleccionado{border-color:#23a66f;background:#edfff5;box-shadow:inset 0 0 0 1px #72efb2}.perfil strong,.perfil span,.perfil small{display:block}.perfil span{margin:6px 0;color:#0874b8;font-size:13px}.perfil small{color:var(--suave)}button{font:inherit}.boton-secundario{padding:8px 11px;border:1px solid #b9d8e7;border-radius:8px;background:#f6fbff;color:#0874b8;font-weight:700;cursor:pointer}.estado-texto{min-height:22px;margin:0;color:var(--suave)}.lista-pruebas{padding:0;margin:18px 0 0;list-style:none}.lista-pruebas li{margin:8px 0;padding:9px 10px;border-radius:7px;background:#f8fafc}.ok{color:#137044;background:#effbf4!important}.fallo{color:#b42318;background:#fff1f1!important}.pendiente{color:var(--suave)}.rejilla-modulos{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:18px}.modulo{padding:15px;border:1px solid var(--borde);border-radius:11px;background:#fbfdff}.modulo b{display:block;color:#0874b8;text-transform:uppercase;font-size:12px}.modulo span{color:var(--suave)}.tabla-contenedor{overflow:auto;margin-top:16px}table{width:100%;border-collapse:collapse;text-align:left}th,td{padding:11px;border-bottom:1px solid var(--borde)}th{font-size:12px;color:var(--suave)}.zona-operativa{margin-top:18px}.operativa-cabecera{display:flex;justify-content:space-between;gap:18px;align-items:start}.operativa-cabecera h3{margin:0}.formulario{display:grid;grid-template-columns:1fr 1fr auto;gap:12px;align-items:end;margin-top:18px;padding:15px;border:1px solid var(--borde);border-radius:11px;background:#fbfdff}.formulario label{display:grid;gap:5px;color:var(--suave);font-size:12px;font-weight:700}.formulario input,.formulario select{min-width:0;padding:9px 10px;border:1px solid #bfd5e1;border-radius:7px;background:#fff;font:inherit;color:var(--tinta)}.boton-primario{padding:10px 15px;border:0;border-radius:8px;background:#0874b8;color:#fff;font-weight:700;cursor:pointer}.boton-primario:disabled{opacity:.6;cursor:wait}.aviso{padding:14px;border:1px solid #f0cf91;border-radius:10px;background:#fff9ec;color:#77520a}.aviso p{margin:5px 0 0}@media(max-width:850px){.barra-lateral{position:static;width:auto}.contenido{margin:0}.rejilla-indicadores,.rejilla-dos{grid-template-columns:1fr 1fr}.pagina{padding:18px}}@media(max-width:700px){.formulario{grid-template-columns:1fr}.operativa-cabecera{display:block}}@media(max-width:560px){.rejilla-indicadores,.rejilla-dos,.perfiles,.rejilla-modulos{grid-template-columns:1fr}.cabecera{padding:12px 18px}.usuario span{display:none}}
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
            CREATE TABLE clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, email TEXT NOT NULL, creado TEXT NOT NULL);
            CREATE TABLE incidencias (id INTEGER PRIMARY KEY AUTOINCREMENT, asunto TEXT NOT NULL, estado TEXT NOT NULL, creado TEXT NOT NULL);
            CREATE TABLE equipos (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, estado TEXT NOT NULL, creado TEXT NOT NULL);
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
**modulo.css**
```css
:root{--nav:#072236;--blue:#168fe8;--line:#dce6eb;--muted:#667785;--bg:#f5f8fa}*{box-sizing:border-box}body{margin:0;font:14px system-ui;color:#1d2c39;background:var(--bg)}.layout{display:grid;grid-template-columns:245px 1fr;min-height:100vh}.sidebar{padding:22px 13px;background:linear-gradient(#071f31,#0a3448 65%,#07523d);color:#b8d0dc}.brand{display:flex;gap:10px;align-items:center;padding:0 8px 24px;color:#fff!important;font-size:16px!important}.brand b,.account b{display:grid;place-items:center;width:35px;height:35px;border-radius:10px;background:#72efb2;color:#073044}.brand small{display:block;color:#91adba;font-size:10px}.sidebar p{margin:18px 10px 7px;font-size:10px;letter-spacing:.12em;color:#77a1b5}.sidebar a{display:block;padding:10px;border-radius:8px;color:#b8d0dc;text-decoration:none}.sidebar a:hover,.sidebar a.active{background:#ffffff1c;color:white}header{height:76px;padding:13px 30px;background:white;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center}header h1{margin:2px 0;font-size:20px}header small{color:var(--muted)}.account{display:flex;gap:8px;align-items:center}.account b{border-radius:50%}.content{padding:28px;max-width:1250px}.heading{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px}.heading h2{margin:0;font-size:25px}.heading p{margin:5px 0;color:var(--muted)}button{font:inherit;cursor:pointer;border:0;border-radius:7px;padding:9px 14px;background:var(--blue);color:#fff;font-weight:700}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:18px}.stat,.card{background:#fff;border:1px solid var(--line);border-radius:13px}.stat{padding:16px}.stat b{display:block;font-size:25px;color:#0874b8}.stat span{color:var(--muted);font-size:12px}.card{overflow:hidden}.card-head{display:flex;justify-content:space-between;align-items:center;padding:17px 20px;border-bottom:1px solid var(--line)}.card-head h3{margin:0}.card input{padding:8px;border:1px solid var(--line);border-radius:7px}.table-wrap{overflow:auto}table{width:100%;border-collapse:collapse}th,td{padding:13px 16px;border-bottom:1px solid var(--line);text-align:left}th{font-size:11px;text-transform:uppercase;color:var(--muted);background:#fbfdfe}.badge{display:inline-block;padding:4px 7px;border-radius:999px;background:#e8f6ff;color:#0874b8;font-size:12px}.modal-backdrop{display:none;position:fixed;inset:0;background:#071f3166;place-items:center}.modal-backdrop.open{display:grid}.modal{width:min(650px,92vw);background:#fff;border-radius:13px;overflow:hidden}.modal header{height:auto;padding:15px 20px}.modal header h3{margin:0}.modal header button{background:none;color:#40515e;font-size:24px;padding:0}.fields{display:grid;grid-template-columns:1fr 1fr;gap:14px;padding:20px}.fields label{display:grid;gap:5px;color:var(--muted);font-size:12px;font-weight:700}.fields input,.fields select{padding:10px;border:1px solid var(--line);border-radius:7px;font:inherit}footer{display:flex;justify-content:flex-end;gap:10px;padding:15px 20px;border-top:1px solid var(--line)}footer button:first-child{background:#edf2f5;color:#344452}@media(max-width:800px){.layout{grid-template-columns:1fr}.sidebar{display:none}.stats{grid-template-columns:1fr 1fr}.content{padding:17px}}
```
**modulo.html**
```html
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Módulo · Integra ERP</title><link rel="stylesheet" href="modulo.css">
</head>
<body>
  <div class="layout">
    <aside class="sidebar"><a class="brand" href="panel.html"><b>ITC</b><span>Integra ERP<small>Gestión empresarial</small></span></a>
      <p>PRINCIPAL</p><a href="panel.html">▦ Dashboard</a><a href="panel.html#modulos">▣ Módulos</a>
      <p>OPERACIONES</p><a data-link="clientes" href="modulo.html?area=clientes">♧ Clientes</a><a data-link="incidencias" href="modulo.html?area=incidencias">◈ Soporte</a><a data-link="equipos" href="modulo.html?area=equipos">▤ Inventario</a>
      <p>SISTEMA</p><a href="panel.html#implantacion">⚙ Configuración</a>
    </aside>
    <main><header><div><small id="breadcrumb">ERP / Operaciones</small><h1 id="title">Cargando módulo…</h1></div><div class="account">Administrador ITC <b>AD</b></div></header>
      <section class="content"><div class="heading"><div><h2 id="heading"></h2><p id="description"></p></div><button id="newButton">+ Nuevo</button></div>
      <div id="stats" class="stats"></div>
      <section class="card"><div class="card-head"><h3 id="tableTitle"></h3><input id="filter" placeholder="Buscar…"></div><div class="table-wrap"><table><thead id="thead"></thead><tbody id="tbody"></tbody></table></div></section></section>
    </main>
  </div>
  <div id="modal" class="modal-backdrop"><section class="modal"><header><h3 id="modalTitle"></h3><button id="close">×</button></header><form id="form"><div id="fields" class="fields"></div><footer><button type="button" id="cancel">Cancelar</button><button type="submit">Guardar</button></footer></form></section></div>
  <script src="modulo.js"></script>
</body></html>
```
**modulo.js**
```js
const area=new URLSearchParams(location.search).get('area')||'clientes';
const config={clientes:{name:'Clientes',desc:'Relación comercial y datos de contacto',fields:[['nombre','Nombre o empresa','text'],['email','Correo electrónico','email']]},incidencias:{name:'Soporte',desc:'Gestión de tickets y solicitudes de servicio',fields:[['asunto','Asunto','text'],['estado','Estado','select']]},equipos:{name:'Inventario',desc:'Control de equipos y activos del servicio',fields:[['nombre','Equipo o activo','text'],['estado','Estado','select']]}};
const meta=config[area]||config.clientes;let rows=[];
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
async function api(path,options={}){const r=await fetch(path,options),j=await r.json();if(!r.ok)throw Error(j.error);return j}
function render(){const cols=meta.fields.map(f=>f[0]);document.title=`${meta.name} · Integra ERP`;title.textContent=meta.name;heading.textContent=meta.name;description.textContent=meta.desc;tableTitle.textContent=`${meta.name} registrados`;newButton.textContent=`+ Nuevo ${meta.name.slice(0,-1)||meta.name}`;document.querySelector('[data-link="'+area+'"]').classList.add('active');thead.innerHTML='<tr>'+cols.map(c=>'<th>'+esc(c)+'</th>').join('')+'<th>Creado</th></tr>';tbody.innerHTML=rows.filter(r=>Object.values(r).join(' ').toLowerCase().includes(filter.value.toLowerCase())).map(r=>'<tr>'+cols.map(c=>'<td>'+esc(r[c])+'</td>').join('')+'<td><span class="badge">'+esc(r.creado)+'</span></td></tr>').join('')||'<tr><td colspan="3">No hay registros todavía.</td></tr>';stats.innerHTML=`<article class="stat"><b>${rows.length}</b><span>Total registrados</span></article><article class="stat"><b>${rows.filter(r=>r.estado==='abierto').length}</b><span>Abiertos</span></article><article class="stat"><b>${rows.filter(r=>r.estado==='operativo').length}</b><span>Operativos</span></article><article class="stat"><b>Local</b><span>SQLite ITC</span></article>`;}
function open(){modal.classList.add('open');modalTitle.textContent='Nuevo '+meta.name;fields.innerHTML=meta.fields.map(([n,l,t])=>t==='select'?'<label>'+l+'<select name="'+n+'"><option value="abierto">Abierto</option><option value="en revisión">En revisión</option><option value="operativo">Operativo</option></select></label>':'<label>'+l+'<input required name="'+n+'" type="'+t+'"></label>').join('')}
async function load(){try{rows=await api('/api/datos/'+area);render()}catch(e){description.textContent=e.message;newButton.disabled=true;render()}}
newButton.onclick=open;close.onclick=cancel.onclick=()=>modal.classList.remove('open');filter.oninput=render;form.onsubmit=async e=>{e.preventDefault();await api('/api/datos/'+area,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(Object.fromEntries(new FormData(form)))});modal.classList.remove('open');load()};load();
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
      <a href="#resumen" class="enlace activo" data-vista="resumen">▦ Dashboard</a>
      <a href="#modulos" class="enlace" data-vista="modulos">▣ Módulos</a>
      <p class="seccion">OPERACIONES</p>
      <a href="modulo.html?area=clientes" class="enlace">♧ Clientes</a>
      <a href="modulo.html?area=incidencias" class="enlace">◈ Soporte</a>
      <a href="modulo.html?area=equipos" class="enlace">▤ Inventario</a>
      <p class="seccion">SISTEMA</p>
      <a href="#implantacion" class="enlace" data-vista="configuracion">⚙ Configuración</a>
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
        <section id="operativa" class="tarjeta" aria-live="polite">
          <div class="tarjeta-cabecera"><div><h3>Operativa del módulo</h3><p class="texto-secundario">Selecciona Clientes, Soporte o Inventario en el menú lateral.</p></div></div>
          <div id="zonaOperativa" class="zona-operativa"><p class="pendiente">Todavía no has seleccionado un área operativa.</p></div>
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
| b) Diferentes instalaciones | `instalar.py` acepta `--perfil comercial` y `--perfil soporte`; ambos crean la misma estructura técnica con módulos activos diferentes. `servidor.py` permite aplicar cada perfil desde el panel local. |
| c) Configuración de módulos | El instalador lee empresa, moneda, zona horaria y perfiles desde `configuracion.json` y los registra en SQLite. El panel actualiza los módulos activos y el servidor bloquea las áreas que el perfil no habilita. |
| d) Instalaciones adaptadas | `OPERACIONES.md` explica dos supuestos. Soporte activa CRM, incidencias e inventario; comercial activa CRM, ventas y facturación. |
| e) Verificación | `verificar.py` y el botón «Ejecutar comprobación» comprueban la estructura SQLite, el perfil, tres módulos activos y la bitácora. Se han probado además altas locales de cliente, incidencia y equipo. |
| f) Documentación e incidencias | `OPERACIONES.md` registra el procedimiento, los cambios de perfil, las altas comprobadas y las incidencias previstas. Cada operación deja una fila en la tabla `operaciones`. |

## Prueba de la entrega

```powershell
cd 02-proyecto-unidad/itc-erp-implantacion
python instalar.py --perfil soporte
python verificar.py
```

Resultado esperado: cuatro líneas que comienzan por `OK` y código de salida
`0`.

```
