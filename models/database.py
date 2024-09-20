import mysql.connector
import os
from dotenv import  load_dotenv

# Carrega os valores das credenciais
load_dotenv()

def conectar_banco_de_dados():
    try:
        host = os.getenv('DB_HOST')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        database = os.getenv('DB_NAME')
        port = int(os.getenv('DB_PORT'))

        cnx = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )

        return cnx
    except mysql.connector.Error as err:
        print("Erro ao conectar ao banco de dados: {}".format(err))
        return None


def criar_tabela_usuario(cnx):
    cursor = cnx.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT PRIMARY KEY AUTO_INCREMENT,
            usuario VARCHAR(255) NOT NULL,
            senha VARCHAR(255) NOT NULL
        );
    ''')
    cnx.commit()
    cursor.close()

def inserir_usuario(cnx, usuario):
    cursor = cnx.cursor()
    cursor.execute('''
        INSERT INTO usuarios (usuario, senha)
        VALUES (%s, %s);
    ''', (usuario.usuario, usuario.senha))
    cnx.commit()
    cursor.close()

# Função para consultar o usuário no banco de dados
def consultar_usuario(cnx, usuario, senha):
    cursor = cnx.cursor()
    cursor.execute('''
        SELECT * FROM usuarios WHERE usuario = %s AND senha = %s;
    ''', (usuario, senha))
    result = cursor.fetchone()
    cursor.close()
    return result