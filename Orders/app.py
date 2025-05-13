from flask import Flask
from view import order_blueprint
import psycopg2

# Configuração do banco de dados
DB_CONFIG = {
    "dbname": "order_db",
    "user": "admin",
    "password": "admin123",
    "host": "postgres-orders",
    "port": 5432,
}

def initialize_database():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        status VARCHAR(100) NOT NULL,
        id_event INT NOT NULL,
        id_user INT NOT NULL,
        id_payment INT ,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
    );
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
        conn.close()
        print("Tabela 'orders' inicializada com sucesso.")
    except Exception as e:
        print(f"Erro ao inicializar a tabela: {e}")

# Instância do Flask
app = Flask(__name__)

# Registro do blueprint
app.register_blueprint(order_blueprint)

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True, host='0.0.0.0', port=5004)
