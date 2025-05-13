import psycopg2
from psycopg2.extras import RealDictCursor
from decimal import Decimal

DB_CONFIG = {
    "dbname": "event_db",
    "user": "admin",
    "password": "admin123",
    "host": "postgres-events",
    "port": 5432
}

class Event:
    def __init__(self, event_id, name, description, price, vagas, date_time):
        self.id = event_id
        self.name = name
        self.description = description
        self.price = float(price)
        self.vagas = vagas
        self.date_time = date_time

    def to_dict(self):
        """Converte o evento em um dicionário."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "vagas": self.vagas,
            "date_time": self.date_time
        }

    @staticmethod
    def get_db_connection():
        """Cria uma conexão com o banco de dados."""
        return psycopg2.connect(**DB_CONFIG)

    @classmethod
    def create(cls, name, description, price, vagas, date_time):
        """Cria um novo evento no banco de dados."""
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        try:
            price = Decimal(price)
            cursor.execute(
                "INSERT INTO events (name, description, price, vagas, date_time) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
                (name, description, price, vagas, date_time)
            )
            event_id = cursor.fetchone()[0]
            conn.commit()
            return event_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def get_all(cls):
        conn = cls.get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("SELECT * FROM events;")
            events = cursor.fetchall()
            return events
        except Exception as e:
            conn.rollback()  
            raise e
        finally:
            cursor.close()
            conn.close()
            

    @classmethod
    def update_event(cls, event_id, event_name=None, event_description=None, event_price=None, event_vagas=None, event_date_time=None):
  
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        try:
          
            update_query = "UPDATE events SET "
            updates = []
            params = []
            if event_name:
                updates.append("name = %s")
                params.append(event_name)
            if event_description:
                updates.append("description = %s")
                params.append(event_description)
            if event_price:
                updates.append("price = %s")
                params.append(event_price)
            if event_vagas:
                updates.append("vagas = %s")
                params.append(event_vagas)
            if event_date_time:
                updates.append("date_time = %s")
                params.append(event_date_time)

            if not updates:
                raise ValueError("No fields provided for update.")

            update_query += ", ".join(updates) + " WHERE id = %s;"
            params.append(event_id)

            cursor.execute(update_query, params)
            conn.commit()
                      
            return cursor.rowcount  
        except Exception as e:
            conn.rollback()  
            raise e
        finally:
            cursor.close()
            conn.close()
            
    @classmethod
    def delete_event(cls,event_id):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM events WHERE id = %s;", (event_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
            
    @classmethod
    def get_by_id(cls,event_id):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, name, description, price, vagas, date_time FROM events WHERE id = %s;", (event_id,))
            #conn.commit()#Usado quando altera dados na tabela
            event = cursor.fetchone()
            if not event:
                return None
            return cls(*event)
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
        
        
        
