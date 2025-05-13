from flask import Blueprint, request, jsonify
from controller import OrderController
from model import Order

order_blueprint = Blueprint('order', __name__)
#CRIAR PAGAMENTO
@order_blueprint.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    response, status = OrderController.create_order(data)
    return jsonify(response), status

#PEGAR TODOS OS PAGAMENTO
@order_blueprint.route('/orders', methods=['GET'])
def get_all_orders():
    response, status = OrderController.get_all_orders()
    return jsonify(response), status

#PEGAR UM PAGAMENTO PELO ID DO EVENTO E ID DO USER
@order_blueprint.route('/orders/user/<int:user_id>', methods=['GET']) #modificar para pegar pelo id do user e evento
def get_order_by_userid(user_id):
    response, status = OrderController.get_orders_by_user(user_id)
    return jsonify(response), status

#ATUALIZAR UM PAGAMENTO
@order_blueprint.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.json
    response, status = OrderController.update_order(order_id, data)
    return jsonify(response), status

@order_blueprint.route('/orders/<int:order_id>', methods = ['GET'])
def get_order(order_id):
    response, status = OrderController.get_order_by_id(order_id)
    return jsonify(response), status
    

#DELETAR UM PAGAMENTO
@order_blueprint.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    response, status = OrderController.delete_order(order_id)
    return jsonify(response), status
