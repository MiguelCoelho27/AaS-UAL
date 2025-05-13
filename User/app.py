from flask import Flask
from controller import user_blueprint
import psycopg2
from psycopg2.extras import RealDictCursor

# Configuração do banco de dados
DB_CONFIG = {
    "dbname": "user_db",
    "user": "admin",
    "password": "admin123",
    "host": "postgres-users",
    "port": 5432,
}

def get_db_connection():
    """Função para obter conexão com o banco de dados."""
    return psycopg2.connect(**DB_CONFIG)

def initialize_database():
    """Inicializa o banco de dados criando a tabela 'users'."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(150) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
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
        print("Tabela 'users' inicializada com sucesso.")
    except Exception as e:
        print(f"Erro ao inicializar a tabela: {e}")
# Instância do Flask
app = Flask(__name__)

# Registro do blueprint
app.register_blueprint(user_blueprint)

if __name__ == "__main__":
    # Inicializa o banco de dados e inicia o servidor
    initialize_database()
    app.run(host="0.0.0.0", port=5003)
