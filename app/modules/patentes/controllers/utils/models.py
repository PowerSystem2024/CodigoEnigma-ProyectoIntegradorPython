from flask_restx import fields

def define_models(api):
    patente_add_params = api.model(
        "PatenteAdd",
        {
            "patente": fields.String(required=True, description="Patente", example="ABC123"),
            "hora_ingreso": fields.String(required=True, description="Hora de ingreso", example="2024-06-01 10:00"),
            "precio_hora": fields.Float(required=True, description="Precio por hora", example=100.0),
        },
    )

    patente_model_response = api.model(
        "PatenteResponse",
        {
            "id": fields.Integer(description="ID"),
            "patente": fields.String(description="Patente"),
            "hora_ingreso": fields.String(description="Hora de ingreso"),
            "precio_hora": fields.Float(description="Precio por hora"),
            "hora_actualizacion": fields.DateTime(description="Hora de actualización"),
        },
    )

    error_model = api.model(
        "ErrorResponse",
        {
            "message": fields.String(description="Mensaje de error", example="Ocurrió un error inesperado."),
        },
    )

    success_message_model = api.model(
        "SuccessMessage",
        {
            "message": fields.String(description="Mensaje de éxito", example="Operación exitosa."),
        },
    )

    return (
        patente_add_params,
        patente_model_response,
        error_model,
        success_message_model,
    )
