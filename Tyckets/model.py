import psycopg2
from psycopg2.extras import RealDictCursor
from decimal import Decimal

DB_CONFIG = {
    "dbname": "tycket_db",
    "user": "admin",
    "password": "admin123",
    "host": "postgres-tyckets",
    "port": 5432
}

class Tycket:
    def __init__(self, tycket_id,id_event, id_user, id_payment,status):
        self.id = tycket_id
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
            "status": self.status
           
            
        }

    @staticmethod
    def get_db_connection():
        """Cria uma conexão com o banco de dados."""
        return psycopg2.connect(**DB_CONFIG)

    @classmethod
    def create(cls, data):
        """Cria um novo tycket no banco de dados."""
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO tyckets (id_user,id_event,id_order,status) VALUES (%s, %s, %s, %s) RETURNING id;",
                (data["id_user"],data["id_event"],data['id_order'], data['status'])
            )
            tycket_id = cursor.fetchone()[0]
            conn.commit()
            return tycket_id
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
            cursor.execute("SELECT * FROM tyckets;")
            tyckets = cursor.fetchall()
            return tyckets
        except Exception as e:
            conn.rollback()  
            raise e
        finally:
            cursor.close()
            conn.close()
            

    @classmethod
    def get_total_tyckets_event(cls, id_event):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        try:
            # Usamos COUNT(*) para contar quantos registros têm o id_event informado
            cursor.execute("SELECT COUNT(*) FROM tyckets WHERE id_event = %s;", (id_event,))
            total = cursor.fetchone()[0]  # Retorna apenas o valor inteiro da contagem
            return total
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()


    @classmethod
    def update_tycket(cls, tycket_id, id_event=None,id_user=None,id_payment=None, status=None, quantidade=None):
  
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        try:
          
            update_query = "UPDATE tyckets SET "
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
            if quantidade:
                updates.append("quantidade= %s")
                params.append(quantidade)

            if not updates:
                raise ValueError("No fields provided for update.")

            update_query += ", ".join(updates) + " WHERE id = %s;"
            params.append(tycket_id)

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
    def delete_tycket(cls,tycket_id):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM tyckets WHERE id = %s;", (tycket_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
            
    @classmethod
    def get_by_id(cls,tycket_id):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, id_event,id_user, id_payment, status FROM tyckets WHERE id = %s;", (tycket_id,))
            #conn.commit()#Usado quando altera dados na tabela
            tycket = cursor.fetchone()
            if not tycket:
                return None
            return cls(*tycket)
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
            cursor.execute("SELECT id, id_event,id_user, id_order, status FROM tyckets WHERE id_user = %s;", (user_id,))
            #conn.commit()#Usado quando altera dados na tabela
            tyckets = cursor.fetchall()
            tycket_objects = []
            for tycket in tyckets:
                tycket_dict = {
                    'id': tycket[0],
                    'id_event': tycket[1],
                    'id_user': tycket[2],
                    'id_order': tycket[3],
                    'status': tycket[4]         
                }
                tycket_objects.append(tycket_dict)
            return tycket_objects  # Retorna uma lista de objetos
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
        
    
        
