from flask import Flask
from view import event_blueprint
import psycopg2

# Configuração do banco de dados
DB_CONFIG = {
    "dbname": "event_db",
    "user": "admin",
    "password": "admin123",
    "host": "postgres-events",
    "port": 5432,
}

def initialize_database():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS events (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        price DECIMAL(10, 2) NOT NULL,
        vagas INT NOT NULL,
        date_time TIMESTAMP NOT NULL,
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
        print("Tabela 'events' inicializada com sucesso.")
    except Exception as e:
        print(f"Erro ao inicializar a tabela: {e}")

# Instância do Flask
app = Flask(__name__)

# Registro do blueprint
app.register_blueprint(event_blueprint)

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True, host='0.0.0.0', port=5000)
