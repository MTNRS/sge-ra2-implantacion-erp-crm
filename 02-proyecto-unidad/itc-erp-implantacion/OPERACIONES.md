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

