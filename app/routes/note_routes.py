from flask import Blueprint, request, jsonify
from app.database import conectar_db

notes_bp = Blueprint("notes_bp", __name__)


@notes_bp.route('/notes', methods=['POST'])
def new_note():
    conexao = None
    cursor = None

    try:
        data = request.get_json()

        title = data.get("title")
        text = data.get("text")
        color = data.get("color", "")
        user_id = data.get("user_id")

        if not text or not user_id:
            return jsonify({
                "message": "Text and ID are mandatory"
            }), 400

        conexao = conectar_db()

        if not conexao:
            return jsonify({
                "message": "Error connecting to database"
            }), 500

        cursor = conexao.cursor()

        sql = """
            INSERT INTO notas (titulo, conteudo, cor, usuario_id)
            VALUES (%s, %s, %s, %s)
        """

        valores = (title, text, color, user_id)

        cursor.execute(sql, valores)
        conexao.commit()

        return jsonify({
            "message": "New note added successfully!",
            "id_nota": cursor.lastrowid
        }), 201

    except Exception as e:
        return jsonify({
            "message": "Erro interno",
            "detail": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()

@notes_bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_notes(notes_id):
    conexao = None
    cursor = None
    
    try:
    
        conexao = conectar_db()
        cursor = conexao.cursor()
       
        cursor.execute(
            """
            DELETE FROM notes
            WHERE id = %s
        """,
        (notes_id,)
       )
         
        conexao.commit()

        if cursor.rowcount == 0:
            return jsonify({
            "message": "Note not found"
        }), 404

        return jsonify({
        "message": "Nota excluída com sucesso!"
        }), 200
    
    except Exception as e:
        return jsonify({
            "message": "Erro interno",
            "detail": str(e)
        }), 500
    
    finally:
        if cursor:
            cursor.close()
        
        if conexao and conexao.is_connected():
            conexao.close()

@notes_bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    conexao = None
    cursor = None
    
    try:

        request_data = request.get_json()
        
        titulo = request_data.get("titulo")
        conteudo = request_data.get("conteudo")
        cor = request_data.get("cor", "#FFFFFF")


        conexao = conectar_db()
        cursor = conexao.cursor()
       
        cursor.execute(
            """
            UPDATE notes
            SET titulo = %s, conteudo = %s, cor = %s 
            WHERE id = %s
        """,
        (titulo, conteudo, cor, note_id)
       )
         
        conexao.commit()

        if cursor.rowcount == 0:
            return jsonify({
            "message": "Note not found"
        }), 404

        return jsonify({
        "message": "Nota atualizada com sucesso!"
        }), 200
    
    except Exception as e:
        return jsonify({
            "message": "Erro interno",
            "detail": str(e)
        }), 500
    
    finally:
        if cursor:
            cursor.close()
        
        if conexao and conexao.is_connected():
            conexao.close()




  








       

