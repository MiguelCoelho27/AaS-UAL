from model import Order
import requests

class OrderController:
    @staticmethod
    def create_order(data):
        required_fields = ['user_id', 'id_event', 'quantidade']
        if not all(field in data for field in required_fields):
            return {"error": "Invalid input data"}, 400
        
        try:
            id_event = data['id_event']
            response = requests.get(f'http://event-service:5000/events/{id_event}', json={})
            if response.status_code == 200:
                data_event = response.json()
                if data_event['vagas']< data['quantidade']:
                    return {"Error":"Não há vagas disponiveis para essa reserva."},400
                valor_event = data_event["price"]
                total = valor_event*data['quantidade']       
                try:
                    response = requests.post(f'http://payment-service:5001/payments', json={"valor":total})
                    if response.status_code == 201:
                        data_payment = response.json()
                        id_payment = data_payment["id"]
                        try:
                            data_order = {"id_user":data['user_id'],"id_event":data['id_event'], "id_payment":id_payment,"status":"ABERTA"}
                            order_id = Order.create(data_order
                            )
                            try:
                                response = requests.put(f'http://payment-service:5001/payments/{id_payment}', json={"id_order":order_id,"form_pay":"NÃO DEFINIDA", "status":"AGUARDANDO"})
                                response = requests.post(f'http://tycket-service:5002/tyckets', 
                                                         json={"user_id":data['user_id'],"id_event":data['id_event'],"quantidade":data['quantidade'],"id_order":order_id,"status":"RESERVADO"})
                                return {"message": "order created", "id": order_id, "id_payment": id_payment}, 201
                            except Exception as e:
                                OrderController.delete_order(order_id)
                                return {"error": str(e)}, 500
                        except Exception as e:
                            return {"error": str(e)}, 500

                    else:
                        return response.json(),response.status_code
                except requests.exceptions.RequestException as e:
                    print("Erro ao conectar ao Payment Service:", e)
                    return {"error": "Falha ao tentar conectar com o Payment Service"}
            else:
                return response.json(),response.status_code
            
        except requests.exceptions.RequestException as e:
            print("Erro ao conectar ao Event Service:", e)
            return {"error": "Falha ao tentar conectar com o Event Service"}

            

        
    @staticmethod
    def get_all_orders():
        try:
            orders = Order.get_all()
            return orders, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_order_by_id(order_id):
        try:
            order = Order.get_by_id(order_id)
            if not order:
                return {"error": "order not found"}, 404
            return order.to_dict(), 200
        except Exception as e:
            return {"error": str(e)}, 500
        
    @staticmethod
    def get_orders_by_user(user_id): 
        try:
            orders = Order.get_by_userid(user_id)
            if not orders:
                return {"error": "orders not found"}, 404
            return orders, 200
        except Exception as e:
            return {"error": str(e)}, 500
  
        
    @staticmethod
    def update_order(order_id, data):
        if not data:
            return {"error": "No data provided"}, 400

        try:
            Order.update_event(
                order_id,
                id_order=data.get('id_order'),
                status=data.get('status'),
                valor=data.get('valor'),
                form_pay=data.get('form_pay')
            )
            return {"message": "order updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        
    @staticmethod
    def delete_order(order_id):
        if not order_id:
            return {"error":"No order_id provider"}
        try:
            Order.delete_order(order_id)
            return{"message":"Item deletado com sucesso."},200
        except Exception as e:
            return{"error": str(e)},500
        
    