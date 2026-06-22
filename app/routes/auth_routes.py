from flask import Blueprint, app, request, jsonify
from flask_cors import CORS
import mysql.connector
import bcrypt
import jwt as pyjwt
import datetime

from app.database import conectar_db


auth_bp = Blueprint('auth', __name__)
CORS(auth_bp)


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        senha = data.get("senha")

        if not email or not senha:
            return jsonify({"mensagem": "Email e senha são obrigatórios", "status": "erro"}), 400

        conexao = conectar_db()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({"mensagem": "Usuário não encontrado", "status": "erro"}), 404

        senha_hash = usuario["senha"].encode("utf-8")

        if not bcrypt.checkpw(senha.encode("utf-8"), senha_hash):
            return jsonify({"mensagem": "Senha incorreta", "status": "erro"}), 401

     
        token = pyjwt.encode({
            "email": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({
            "mensagem": "Login realizado com sucesso!",
            "token": token,
            "status": "sucesso"
        }), 200

    except Exception as e:
        return jsonify({"mensagem": "Erro ao fazer login", "detalhe": str(e)}), 500

    finally:
        cursor.close()
        conexao.close()


@auth_bp.route('/cadastrarnovo', methods=['POST'])
def cadastrar_novo():
    conexao = None  # Inicializa como None
    cursor = None   # Inicializa como None
    try:
        data = request.get_json()
        email = data.get("email")
        senha = data.get("senha")
        repet = data.get("repet")

        if not email or not senha or not repet:
            return jsonify({"mensagem": "Preencha todos os campos", "status": "erro"}), 400

        if senha != repet:
            return jsonify({"mensagem": "As senhas não coincidem", "status": "erro"}), 400

        conexao = conectar_db() # Agora 'conexao' é definida
        cursor = conexao.cursor() # Agora 'cursor' é definido

        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"mensagem": "Email já cadastrado", "status": "erro"}), 409

        senha_hash = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())

        cursor.execute("INSERT INTO usuarios (email, senha) VALUES (%s, %s)", (email, senha_hash))
        conexao.commit()

        return jsonify({"mensagem": "Usuário criado com sucesso!", "status": "sucesso"}), 201

    except mysql.connector.Error as err:
        # É uma boa prática capturar erros de DB separadamente
        return jsonify({"mensagem": "Erro de banco de dados", "detalhe": str(err)}), 500
    except Exception as e:
        # Captura todos os outros erros (como request.get_json() falhando)
        return jsonify({"mensagem": "Erro interno ao criar usuário", "detalhe": str(e)}), 500

    finally:
        # VERIFICAÇÃO DE SEGURANÇA:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()


@auth_bp.route('/recuperarsenha', methods=['POST'])
def recuperar_senha():
    try:
        data = request.get_json()
        email = data.get("email")

        if not email:
            return jsonify({"mensagem": "Email não fornecido", "status": "erro"}), 400

        conexao = conectar_db()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({"mensagem": "Usuário não encontrado", "status": "erro"}), 404

        # Aqui você poderia gerar uma nova senha ou enviar email (exemplo simplificado)
        nova_senha = "nova123"
        nova_hash = bcrypt.hashpw(nova_senha.encode("utf-8"), bcrypt.gensalt())

        cursor.execute("UPDATE usuarios SET senha = %s WHERE email = %s", (nova_hash, email))
        conexao.commit()

        return jsonify({
            "mensagem": f"Senha redefinida para '{nova_senha}' (exemplo — não faça isso em produção)",
            "status": "sucesso"
        }), 200

    except Exception as e:
        return jsonify({"mensagem": "Erro ao redefinir senha", "detalhe": str(e)}), 500

    finally:
        cursor.close()
        conexao.close()

# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)
