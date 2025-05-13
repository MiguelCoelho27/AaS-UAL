from flask import Blueprint, request, jsonify
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



# Criação do blueprint
user_blueprint = Blueprint('users', __name__)

# Rotas
@user_blueprint.route('/users', methods=['POST'])
def create_user():
    """Cria um novo usuário."""
    data = request.json
    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Invalid input"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING id;",
            (data['name'], data['email'], data['password'])
        )
        user_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({"id": user_id, "name": data['name'], "email": data['email']}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


@user_blueprint.route('/users', methods=['GET'])
def get_users():
    """Retorna todos os usuários."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT id, name, email, created_at FROM users;")
        users = cursor.fetchall()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
        
@user_blueprint.route('/users/<int:id_user>', methods=['GET'])
def get_user_by_id():
    id_user = id_user
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT id, name, email, FROM users WHERE id = %s;", (id_user))
        user = cursor.fetchone()
        return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
        
@user_blueprint.route('/users/login', methods=['GET'])
def get_user_by_email_password():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    # Valida se os campos necessários estão presentes
    if not email or not password:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        # Query corrigida
        cursor.execute(
            "SELECT id, name, email FROM users WHERE email = %s AND password = %s;",
            (email, password)
        )
        user = cursor.fetchone()
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"error": "Usuário não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()