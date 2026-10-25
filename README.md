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

