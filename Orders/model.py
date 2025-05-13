import psycopg2
from psycopg2.extras import RealDictCursor
from decimal import Decimal

DB_CONFIG = {
    "dbname": "order_db",
    "user": "admin",
    "password": "admin123",
    "host": "postgres-orders",
    "port": 5432
}

class Order:
    def __init__(self, order_id,id_event, id_user, id_payment,status):
        self.id = order_id
        self.id_event = id_event
        self.id_user = id_user
        self.id_payment = id_payment
        self.status = status

    def to_dict(self):
        """Converte o evento em um dicionário."""
        return {
            "id": self.id,
            "id_event": self.id_event,
            "id_user": self.id_user,
            "id_payment": self.id_payment,
            "status": self.status,
            
        }

    @staticmethod
    def get_db_connection():
        """Cria uma conexão com o banco de dados."""
        return psycopg2.connect(**DB_CONFIG)

    @classmethod
    def create(cls, data):
        """Cria um novo order no banco de dados."""
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO orders (id_user,id_event,id_payment,status) VALUES (%s, %s, %s, %s) RETURNING id;",
                (data["id_user"],data["id_event"],data["id_payment"], data["status"])
            )
            order_id = cursor.fetchone()[0]
            conn.commit()
            return order_id
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
            cursor.execute("SELECT * FROM orders;")
            orders = cursor.fetchall()
            return orders
        except Exception as e:
            conn.rollback()  
            raise e
        finally:
            cursor.close()
            conn.close()
            

    @classmethod
    def update_order(cls, order_id, id_event=None,id_user=None,id_payment=None, status=None):
  
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        try:
          
            update_query = "UPDATE orders SET "
            updates = []
            params = []
            if id_event:
                updates.append("id_event = %s")
                params.append(id_event)
            if id_user:
                updates.append("id_user = %s")
                params.append(id_user)
            if id_payment:
                updates.append("id_payment = %s")
                params.append(id_payment)
            if status:
                updates.append("status = %s")
                params.append(status)
            if not updates:
                raise ValueError("No fields provided for update.")

            update_query += ", ".join(updates) + " WHERE id = %s;"
            params.append(order_id)

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
    def delete_order(cls,order_id):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM orders WHERE id = %s;", (order_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
            
    @classmethod
    def get_by_id(cls,order_id):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, id_event,id_user, id_payment, status FROM orders WHERE id = %s;", (order_id,))
            #conn.commit()#Usado quando altera dados na tabela
            order = cursor.fetchone()
            if not order:
                return None
            return cls(*order)
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    @classmethod
    def get_by_userid(cls,user_id):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, id_event,id_user, id_payment, status FROM orders WHERE id_user = %s;", (user_id,))
            #conn.commit()#Usado quando altera dados na tabela
            orders = cursor.fetchall()
            order_objects = []
            for order in orders:
                order_dict = {
                    'id': order[0],
                    'id_event': order[1],
                    'id_user': order[2],
                    'id_payment': order[3],
                    'status': order[4]         
                }
                order_objects.append(order_dict)
            
            return order_objects  # Retorna uma lista de objetos
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
        
    
        
