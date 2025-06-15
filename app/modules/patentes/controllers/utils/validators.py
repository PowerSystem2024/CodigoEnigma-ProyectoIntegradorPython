def validate_patente_data(data):
    required_fields = ["patente", "hora_ingreso", "precio_hora"]
    for field in required_fields:
        if field not in data or not data[field]:
            raise ValueError(f"El campo '{field}' es obligatorio.")
    if not isinstance(data["precio_hora"], (int, float)):
        raise ValueError("El campo 'precio_hora' debe ser numérico.")
