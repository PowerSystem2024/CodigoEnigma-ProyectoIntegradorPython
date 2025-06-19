from flask_restx import Resource, fields
from flask import request
from app.modules.patentes import ns_patentes
from app.db.database import SessionLocal
from app.modules.patentes.controllers.utils.serialize_patente import serialize_patente
from app.modules.patentes.services.patente_service import PatenteService
from app.modules.patentes.controllers.utils.models import define_models
from app.modules.patentes.controllers.utils.validators import validate_patente_data

db = SessionLocal()
service = PatenteService(db)
api = ns_patentes

(
    patente_add_params,
    patente_model_response,
    error_model,
    success_message_model,
) = define_models(api)

@api.route("/activas")
class PatenteActivasResource(Resource):
    @api.doc(description="Listar solo las patentes activas.", responses={200: ("Éxito", [patente_model_response]), 500: ("Error interno", error_model)})
    @api.marshal_list_with(patente_model_response)
    def get(self):
        patentes = service.listar()
        return [serialize_patente(p) for p in patentes], 200

@api.route("/agregar")
class PatenteAddResource(Resource):
    @api.expect(patente_add_params)
    @api.doc(description="Agregar una patente.", responses={200: ("Patente agregada", patente_model_response), 400: ("Datos inválidos", error_model)})
    @api.marshal_with(patente_model_response)
    def post(self):
        data = request.json
        try:
            validate_patente_data(data)
            patente = service.agregar(data)
            return serialize_patente(patente), 200
        except ValueError as e:
            api.abort(400, str(e))

@api.route("/eliminar")
class PatenteDeleteResource(Resource):
    @api.doc(description="Eliminar una patente.", responses={200: ("Patente eliminada", success_message_model), 400: ("Error", error_model)})
    @api.expect(api.model("EliminarPatente", {"patente": fields.String(required=True)}))
    @api.marshal_with(success_message_model)
    def post(self):
        data = request.json
        patente = data.get("patente")
        if not patente:
            api.abort(400, "Patente no especificada")
        try:
            service.eliminar(patente)
            return {"message": "Patente eliminada correctamente."}, 200
        except ValueError as e:
            api.abort(400, str(e))

@api.route("/actualizar")
class PatenteUpdateResource(Resource):
    @api.doc(description="Actualizar una patente.", responses={200: ("Patente actualizada", patente_model_response), 400: ("Error", error_model)})
    @api.expect(api.model("ActualizarPatente", {
        "patenteOriginal": fields.String(required=True),
        "patenteNueva": fields.String(required=True),
        "precio_hora": fields.Float(required=False),
        "hora_actualizacion": fields.DateTime(required=True)
    }))
    @api.marshal_with(patente_model_response)
    def post(self):
        data = request.json
        patente_original = data.get("patenteOriginal")
        patente_nueva = data.get("patenteNueva")
        precio_hora = data.get("precio_hora")
        hora_actualizacion = data.get("hora_actualizacion")
        if not patente_original or not patente_nueva:
            api.abort(400, "Datos incompletos")
        try:
            patente = service.actualizar(patente_original, patente_nueva, precio_hora, hora_actualizacion)
            return serialize_patente(patente), 200
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/cobrar')
class PatenteCobrar(Resource):
    def post(self):
        data = request.get_json()
        patente = data.get('patente')
        if service.marcar_inactiva(patente):
            return {'msg': 'Patente marcada como inactiva'}, 200
        return {'msg': 'Patente no encontrada'}, 404

@api.route('/todas')
class PatenteTodas(Resource):
    def get(self):
        patentes = service.listar_todas()
        # Si usas marshmallow o similar, serializa aquí
        return [p.to_dict() for p in patentes], 200
