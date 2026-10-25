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

