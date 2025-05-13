from model import Event
import requests
from flask import jsonify

class EventController:
    @staticmethod
    def create_event(data):
        required_fields = ['name', 'description', 'price', 'vagas', 'date_time']
        if not all(field in data for field in required_fields):
            return {"error": "Invalid input data"}, 400

        try:
            event_id = Event.create(
                data['name'], data['description'], data['price'], data['vagas'], data['date_time']
            )
            return {"message": "Event created", "id": event_id}, 201
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_all_events():
        try:
            events = Event.get_all()
            return events, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_event_by_id(event_id):
        try:
            event = Event.get_by_id(event_id)
            if not event:
                return {"error": "Event not found"}, 404
            try:
                # Chama a função get_place_available e trata o erro se ocorrer
                available_place = EventController.get_place_available(event_id)
                
                # Verifica se a resposta da função get_place_available é um erro
                if isinstance(available_place, dict) and 'error' in available_place:
                    return available_place, 501  # Retorna o erro do serviço de tickets
                
                return {
                    "id": event.id,
                    "name": event.name,
                    "description": event.description,
                    "price": event.price,
                    "vagas": available_place
                }, 200
            
            except Exception as e:
                # Caso ocorra outro erro dentro da função get_place_available
                return {"error": str(e)}, 501
            
        except Exception as e:
            # Caso ocorra erro ao obter o evento
            return {"error": str(e)}, 500


    @staticmethod
    def get_place_available(event_id):
        try:
            response = requests.get(f'http://tycket-service:5002/tyckets/event/{event_id}')
            if response.status_code == 200:
                data_tycket = response.json()
                total_tyckets = data_tycket['total']
                event = Event.get_by_id(event_id)
                total = event.vagas - total_tyckets
                return total
            else:
                # Se o código de resposta não for 200, retornar um erro
                return {"error": f"Error: {response.status_code} - {response.text}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Error contacting Tycket Service: {str(e)}"}

           
    @staticmethod
    def update_event(event_id, data):
        if not data:
            return {"error": "No data provided"}, 400

        try:
            Event.update_event(
                event_id,
                event_name=data.get('name'),
                event_description=data.get('description'),
                event_price=data.get('price'),
                event_vagas=data.get('vagas'),
                event_date_time=data.get('date_time')
            )
            return {"message": "Event updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        
    @staticmethod
    def delete_event(event_id):
        if not event_id:
            return {"error":"No event_id provider"}
        try:
            Event.delete_event(event_id)
            return{"message":"Item deletado com sucesso."},200
        except Exception as e:
            return{"error": str(e)},500
        
    