import os
import mysql.connector
from dotenv import load_dotenv

def conectar_db():
   try:
      conexao = mysql.connector.connect(
         host=os.getenv('DB_HOST'),
         port=os.getenv('DB_PORT'),
         user=os.getenv('DB_USER'),
         password=os.getenv('DB_PASSWORD'),
         database=os.getenv('DB_NAME')
      )
      return conexao
   except mysql.connector.error as err:
      print(f"Erro ao conectar ao banco de dados: {err}")
      return None