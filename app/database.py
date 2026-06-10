from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

try:
    conexao = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )

    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios;")

    for linha in cursor.fetchall():
        print(linha)

except mysql.connector.Error as err:
    print(f"Erro ao conectar ou consultar o banco: {err}")

finally:
    if conexao.is_connected():
        cursor.close()
        conexao.close()
        print("Conexão encerrada.")