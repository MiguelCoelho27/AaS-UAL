from flask import Blueprint, request, jsonify
from controller import TycketController
from model import Tycket

tycket_blueprint = Blueprint('tycket', __name__)
#CRIAR PAGAMENTO
@tycket_blueprint.route('/tyckets', methods=['POST'])
def create_tycket():
    data = request.json
    response, status = TycketController.create_tycket(data)
    return jsonify(response), status

#PEGAR TODOS OS PAGAMENTO
@tycket_blueprint.route('/tyckets', methods=['GET'])
def get_all_tyckets():
    response, status = TycketController.get_all_tyckets()
    return jsonify(response), status

#PEGAR TODOS OS PAGAMENTO
@tycket_blueprint.route('/tyckets/event/<int:event_id>', methods=['GET'])
def get_total_tyckets_event(event_id):
    id_event = event_id
    response, status = TycketController.get_total_tyckets_event(id_event)
    return jsonify(response), status

#PEGAR UM PAGAMENTO PELO ID DO EVENTO E ID DO USER
@tycket_blueprint.route('/tyckets/pay', methods=['GET']) #modificar para pegar pelo id do user e evento
def get_tycket_user_even():
    data = request.json
    response, status = TycketController.get_tycket_by_user_event(data)
    return jsonify(response), status

#ATUALIZAR UM PAGAMENTO
@tycket_blueprint.route('/tyckets/<int:tycket_id>', methods=['PUT'])
def update_tycket(tycket_id):
    data = request.json
    response, status = TycketController.update_tycket(tycket_id, data)
    return jsonify(response), status

@tycket_blueprint.route('/tyckets/<int:tycket_id>', methods = ['GET'])
def get_tycket(tycket_id):
    response, status = TycketController.get_tycket_by_id(tycket_id)
    return jsonify(response), status
    
@tycket_blueprint.route('/tyckets/user/<int:user_id>', methods = ['GET'])
def get_tyckets_userid(user_id):
    response, status = TycketController.get_tycket_by_userid(user_id)
    return jsonify(response), status
    

#DELETAR UM PAGAMENTO
@tycket_blueprint.route('/tyckets/<int:tycket_id>', methods=['DELETE'])
def delete_tycket(tycket_id):
    response, status = TycketController.delete_event(tycket_id)
    return jsonify(response), status
