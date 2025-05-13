from model import Payment
import requests

class PaymentController:
    @staticmethod
    def create_payment(data):

        try:
            valor = data['valor']
            payment_id = Payment.create(
               "AGUARDANDO", valor, "NÃO DEFINIDA"
            )
            return {"message": "Payment created", "id": payment_id}, 201
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_all_payments():
        try:
            payments = Payment.get_all()
            return payments, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_payment_by_id(payment_id):
        try:
            payment = Payment.get_by_id(payment_id)
            if not payment:
                return {"error": "Payment not found"}, 404
            return payment.to_dict(), 200
        except Exception as e:
            return {"error": str(e)}, 500
        
    @staticmethod
    def get_payment_by_user_event(dados):
        
        
        if not dados or not dados.get('user_id') or not dados.get('event_id'):
            return {"error": "Invalid input"}, 400

        try:
            tycket_service_url = f"http://user-service:6000/tyckets/userEvent"
            response = requests.get(tycket_service_url, json=dados)
            if response.status_code != 200:
                return {"error": "User does not exist"}, 404
        except requests.exceptions.RequestException as e:
            return {"error": f"Error contacting User Service: {str(e)}"}, 500

        
        try:
            payment = Payment.get_by_id(response)
            if not payment:
                return {"error": "Payment not found"}, 404
            return payment.to_dict(), 200
        except Exception as e:
            return {"error": str(e)}, 500
  
        
    @staticmethod
    def update_payment(payment_id, data):
        if not data:
            return {"error": "No data provided"}, 400

        try:
            Payment.update_payment(
                payment_id,
                id_order=data.get('id_order'),
                status=data.get('status'),
                form_pay=data.get('form_pay')
            )
            return {"message": "Payment updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        
    @staticmethod
    def delete_event(payment_id):
        if not payment_id:
            return {"error":"No payment_id provider"}
        try:
            Payment.delete_payment(payment_id)
            return{"message":"Item deletado com sucesso."},200
        except Exception as e:
            return{"error": str(e)},500
        
    