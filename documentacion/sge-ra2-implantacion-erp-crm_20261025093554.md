# Reporte de proyecto

## Información de generación

- **Fecha:** 2026-10-25 09:35:54 +0100
- **Usuario:** freak
- **Equipo:** JARVIS
- **Sistema operativo:** Windows
- **Arquitectura:** x86_64
- **Directorio de ejecución:** `C:/Users/freak/DAM2`
- **Proyecto documentado:** `C:/Users/freak/Documents/DAM2-entregas/sge-ra2-implantacion-erp-crm`
- **HMAC-SHA-256 de autenticidad:** `5b989706202a8730da9866a0b9fb1e36256ec65dae2a190a813a4e9856b46bf9`

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
python instalar.py --perfil soporte
python verificar.py
python -m http.server 8080
```

Abrir `http://127.0.0.1:8080/panel.html`. Para repetir la demostración con otro
perfil, eliminar manualmente `data/itc_erp.sqlite` y ejecutar de nuevo el
instalador. El perfil `comercial` instala CRM, ventas y facturación; `soporte`
instala CRM, incidencias e inventario.

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
  <title>ITC ERP · Estado de implantación</title>
  <style>
    :root { color-scheme: dark; font-family: system-ui, sans-serif; background:#111827; color:#e5e7eb; }
    body { max-width: 920px; margin: 0 auto; padding: 2rem; }
    header { border-bottom: 1px solid #374151; margin-bottom: 2rem; }
    h1 { margin-bottom: .25rem; } .subtitulo { color:#9ca3af; }
    .aviso { padding: 1rem; border-left: 4px solid #f59e0b; background:#1f2937; }
    .rejilla { display:grid; grid-template-columns:repeat(auto-fit,minmax(210px,1fr)); gap:1rem; margin:1rem 0; }
    article { background:#1f2937; padding:1rem; border-radius:.5rem; }
    .activo { color:#86efac; } .inactivo { color:#9ca3af; } code { color:#c4b5fd; }
  </style>
</head>
<body>
  <header>
    <p>INTEGRA TECH CONSULTING · IMPLANTACIÓN LOCAL</p>
    <h1>Estado de la instalación</h1>
    <p class="subtitulo">Panel de lectura para comprobar el perfil y los módulos configurados.</p>
  </header>
  <main>
    <p id="estado" class="aviso">Leyendo <code>configuracion.json</code>…</p>
    <section>
      <h2>Perfiles disponibles</h2>
      <div id="perfiles" class="rejilla"></div>
    </section>
    <section>
      <h2>Módulos</h2>
      <div id="modulos" class="rejilla"></div>
    </section>
    <section class="aviso">
      <strong>Comprobación completa:</strong> ejecuta <code>python verificar.py</code>.
      El panel informa de la configuración preparada; el verificador revisa la base SQLite creada por el instalador.
    </section>
  </main>
  <script>
    fetch('configuracion.json')
      .then(respuesta => {
        if (!respuesta.ok) throw new Error('No se pudo leer la configuración');
        return respuesta.json();
      })
      .then(configuracion => {
        document.querySelector('#estado').textContent = `Empresa de demostración: ${configuracion.empresa}. Moneda: ${configuracion.moneda}.`;
        document.querySelector('#perfiles').innerHTML = Object.entries(configuracion.perfiles)
          .map(([nombre, modulos]) => `<article><strong>${nombre}</strong><p>${modulos.join(', ')}</p></article>`).join('');
        document.querySelector('#modulos').innerHTML = Object.entries(configuracion.modulos)
          .map(([codigo, nombre]) => `<article><strong>${codigo}</strong><p>${nombre}</p><span class="activo">Disponible para configurar</span></article>`).join('');
      })
      .catch(error => { document.querySelector('#estado').textContent = `Incidencia: ${error.message}`; });
  </script>
</body>
</html>

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
| b) Diferentes instalaciones | `instalar.py` acepta `--perfil comercial` y `--perfil soporte`; ambos crean la misma estructura técnica con módulos activos diferentes. |
| c) Configuración de módulos | El instalador lee empresa, moneda, zona horaria y perfiles desde `configuracion.json` y los registra en SQLite. El panel muestra la configuración disponible. |
| d) Instalaciones adaptadas | `OPERACIONES.md` explica dos supuestos. Soporte activa CRM, incidencias e inventario; comercial activa CRM, ventas y facturación. |
| e) Verificación | `verificar.py` comprueba que existen las cuatro tablas, que el perfil es válido, que hay tres módulos activos y que se registró la instalación. |
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
