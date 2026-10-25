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

