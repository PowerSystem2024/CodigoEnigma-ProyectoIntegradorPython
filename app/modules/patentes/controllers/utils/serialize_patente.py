def serialize_patente(patente):
    return {
        "id": patente.id,
        "patente": patente.patente,
        "hora_ingreso": patente.hora_ingreso,
        "precio_hora": patente.precio_hora,
        "hora_actualizacion": patente.hora_actualizacion.isoformat() if patente.hora_actualizacion else None,
    }
