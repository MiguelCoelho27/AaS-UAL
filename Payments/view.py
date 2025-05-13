from flask import Blueprint, request, jsonify
from controller import PaymentController
from model import Payment

payment_blueprint = Blueprint('payment', __name__)
#CRIAR PAGAMENTO
@payment_blueprint.route('/payments', methods=['POST'])
def create_payment():
    data = request.json
    response, status = PaymentController.create_payment(data)
    return jsonify(response), status

#PEGAR TODOS OS PAGAMENTO
@payment_blueprint.route('/payments', methods=['GET'])
def get_all_payments():
    response, status = PaymentController.get_all_payments()
    return jsonify(response), status

#PEGAR UM PAGAMENTO PELO ID DO EVENTO E ID DO USER
@payment_blueprint.route('/payments/pay', methods=['GET']) #modificar para pegar pelo id do user e evento
def get_payment_user_event():
    data = request.json
    response, status = PaymentController.get_payment_by_user_event(data)
    return jsonify(response), status

#ATUALIZAR UM PAGAMENTO
@payment_blueprint.route('/payments/<int:pay_id>', methods=['PUT'])
def update_payment(pay_id):
    data = request.json
    response, status = PaymentController.update_payment(pay_id, data)
    return jsonify(response), status

@payment_blueprint.route('/payments/<int:pay_id>', methods = ['GET'])
def get_payment(pay_id):
    response, status = PaymentController.get_payment_by_id(pay_id)
    return jsonify(response), status
    

#DELETAR UM PAGAMENTO
@payment_blueprint.route('/payments/<int:pay_id>', methods=['DELETE'])
def delete_payment(pay_id):
    response, status = PaymentController.delete_event(pay_id)
    return jsonify(response), status
