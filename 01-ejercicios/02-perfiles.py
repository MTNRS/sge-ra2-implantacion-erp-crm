PERFILES = {
    "comercial": ["crm", "ventas", "facturacion"],
    "soporte": ["crm", "incidencias", "inventario"],
}

for nombre, modulos in PERFILES.items():
    print(f"{nombre}: {', '.join(modulos)}")

