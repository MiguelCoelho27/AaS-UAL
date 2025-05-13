import psycopg2
from psycopg2.extras import RealDictCursor
from decimal import Decimal

DB_CONFIG = {
    "dbname": "payment_db",
    "user": "admin",
    "password": "admin123",
    "host": "postgres-payments",
    "port": 5432
}

class Payment:
    def __init__(self, payment_id,id_tycket, status, form_pay, valor):
        self.id = payment_id
        self.id_tycket = id_tycket
        self.status = status
        self.valor = float(valor)
        self.form_pay = form_pay

    def to_dict(self):
        """Converte o evento em um dicionário."""
        return {
            "id": self.id,
            "id_tycket": self.id_tycket,
            "status": self.status,
            "valor": self.valor,
            "form_pay": self.form_pay
            
        }

    @staticmethod
    def get_db_connection():
        """Cria uma conexão com o banco de dados."""
        return psycopg2.connect(**DB_CONFIG)

    @classmethod
    def create(cls, status, valor, form_pay):
        """Cria um novo evento no banco de dados."""
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        try:
            valor = Decimal(valor)
            cursor.execute(
                "INSERT INTO payments ( status, valor,form_pay) VALUES ( %s, %s, %s) RETURNING id;",
                ( status, valor, form_pay)
            )
            payment_id = cursor.fetchone()[0]
            conn.commit()
            return payment_id
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
            cursor.execute("SELECT * FROM payments;")
            payments = cursor.fetchall()
            return payments
        except Exception as e:
            conn.rollback()  
            raise e
        finally:
            cursor.close()
            conn.close()
            

    @classmethod
    def update_payment(cls, payment_id, id_order=None, status=None, form_pay=None):
  
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        try:
          
            update_query = "UPDATE payments SET "
            updates = []
            params = []
            if id_order:
                updates.append("id_order = %s")
                params.append(id_order)
            if status:
                updates.append("status = %s")
                params.append(status)
            if form_pay:
                updates.append("form_pay = %s")
                params.append(form_pay)

            if not updates:
                raise ValueError("No fields provided for update.")

            update_query += ", ".join(updates) + " WHERE id = %s;"
            params.append(payment_id)

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
    def delete_payment(cls,payment_id):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM payments WHERE id = %s;", (payment_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
            
    @classmethod
    def get_by_id(cls,payment_id):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, id_tycket, status, valor, form_pay FROM payments WHERE id = %s;", (payment_id,))
            #conn.commit()#Usado quando altera dados na tabela
            payment = cursor.fetchone()
            if not payment:
                return None
            return cls(*payment)
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
        
    
        
