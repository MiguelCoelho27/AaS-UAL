from flask import Blueprint, request, jsonify
from controller import EventController
from model import Event

event_blueprint = Blueprint('events', __name__)
#CRIAR EVENTO
@event_blueprint.route('/events', methods=['POST'])
def create_event():
    data = request.json
    response, status = EventController.create_event(data)
    return jsonify(response), status

#PEGAR TODOS OS EVENTOS
@event_blueprint.route('/events', methods=['GET'])
def get_all_events():
    response, status = EventController.get_all_events()
    return jsonify(response), status

@event_blueprint.route('/events/placeavailable/<int:event_id>', methods=['GET'])
def get_place_available():
    event_id = event_id
    response, status = EventController.get_place_available(event_id)
    return jsonify(response), status

#PEGAR UM EVENTO PELO ID
@event_blueprint.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    response, status = EventController.get_event_by_id(event_id)
    return jsonify(response), status

#ATUALIZAR UM EVENTO
@event_blueprint.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.json
    response, status = EventController.update_event(event_id, data)
    return jsonify(response), status

#DELETAR UM EVENTO
@event_blueprint.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    response, status = EventController.delete_event(event_id)
    return jsonify(response), status
