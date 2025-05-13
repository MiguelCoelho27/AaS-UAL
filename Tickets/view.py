from flask import Blueprint, request, jsonify
from controller import TicketController
from model import Ticket

ticket_blueprint = Blueprint('ticket', __name__)
#CRIAR PAGAMENTO
@ticket_blueprint.route('/tickets', methods=['POST'])
def create_ticket():
    data = request.json
    response, status = TicketController.create_ticket(data)
    return jsonify(response), status

#PEGAR TODOS OS PAGAMENTO
@ticket_blueprint.route('/tickets', methods=['GET'])
def get_all_tickets():
    response, status = TicketController.get_all_tickets()
    return jsonify(response), status

#PEGAR TODOS OS PAGAMENTO
@ticket_blueprint.route('/tickets/event/<int:event_id>', methods=['GET'])
def get_total_tickets_event(event_id):
    id_event = event_id
    response, status = TicketController.get_total_tickets_event(id_event)
    return jsonify(response), status

#PEGAR UM PAGAMENTO PELO ID DO EVENTO E ID DO USER
@ticket_blueprint.route('/tickets/pay', methods=['GET']) #modificar para pegar pelo id do user e evento
def get_ticket_user_even():
    data = request.json
    response, status = TicketController.get_ticket_by_user_event(data)
    return jsonify(response), status

#ATUALIZAR UM PAGAMENTO
@ticket_blueprint.route('/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    data = request.json
    response, status = TicketController.update_ticket(ticket_id, data)
    return jsonify(response), status

@ticket_blueprint.route('/tickets/<int:ticket_id>', methods = ['GET'])
def get_ticket(ticket_id):
    response, status = TicketController.get_ticket_by_id(ticket_id)
    return jsonify(response), status
    
@ticket_blueprint.route('/tickets/user/<int:user_id>', methods = ['GET'])
def get_tickets_userid(user_id):
    response, status = TicketController.get_ticket_by_userid(user_id)
    return jsonify(response), status
    

#DELETAR UM PAGAMENTO
@ticket_blueprint.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    response, status = TicketController.delete_event(ticket_id)
    return jsonify(response), status
