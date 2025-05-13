from model import Tycket
import requests

class TycketController:
    @staticmethod
    def create_tycket(data):
        required_fields = ['user_id', 'id_event', 'quantidade', 'id_order']
        # Verifica se todos os campos obrigatórios estão presentes
        if not all(field in data for field in required_fields):
            return {"error": "Invalid input data"}, 400

        tycket_ids = []  # Lista para armazenar os IDs criados
        try:
            # Cria os tickets com base na quantidade
            for _ in range(data['quantidade']):
                data_tycket = {
                    "id_user": data['user_id'],
                    "id_event": data['id_event'],
                    "status": "RESERVADO",
                    "id_order": data['id_order']
                }
                # Cria o ticket e armazena o ID retornado
                tycket_id = Tycket.create(data_tycket # A quantidade é tratada como 1 por iteração
                )
                tycket_ids.append(tycket_id)

            return {"message": "Tyckets created", "ids": tycket_ids}, 201
        except Exception as e:
            return {"error": str(e)}, 500

        

        
    @staticmethod
    def get_all_tyckets():
        try:
            tyckets = Tycket.get_all()
            return tyckets, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_total_tyckets_event(id_event):
        try:
            total = Tycket.get_total_tyckets_event(id_event)
            if not total:
                return {"total":0}, 200
            return {"total":total}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_tycket_by_id(Tycket_id):
        try:
            tycket = Tycket.get_by_id(Tycket_id)
            if not tycket:
                return {"error": "Tycket not found"}, 404
            return tycket.to_dict(), 200
        except Exception as e:
            return {"error": str(e)}, 500
        
    @staticmethod
    def get_tycket_by_userid(user_id):
        try:
            tyckets = Tycket.get_by_userid(user_id)
            if not tyckets:
                return {"error": "Tycket not found"}, 404
            return tyckets, 200
        except Exception as e:
            return {"error": str(e)}, 500    
        
    @staticmethod
    def get_tycket_by_user_event(dados):#MODIFICAR ESSE MÉTODO PARA OUTRO RETORNO = ID DO PAGAMENTO
        
        
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
            tycket = Tycket.get_by_id(response)
            if not tycket:
                return {"error": "Tycket not found"}, 404
            return tycket.to_dict(), 200
        except Exception as e:
            return {"error": str(e)}, 500
  
        
    @staticmethod
    def update_tycket(tycket_id, data):
        if not data:
            return {"error": "No data provided"}, 400

        try:
            Tycket.update_event(
                tycket_id,
                id_tycket=data.get('id_tycket'),
                status=data.get('status'),
                valor=data.get('valor'),
                form_pay=data.get('form_pay')
            )
            return {"message": "Tycket updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        
    @staticmethod
    def delete_tycket(tycket_id):
        if not tycket_id:
            return {"error":"No Tycket_id provider"}
        try:
            Tycket.delete_tycket(tycket_id)
            return{"message":"Item deletado com sucesso."},200
        except Exception as e:
            return{"error": str(e)},500
        
    