import mysql.connector
import os
import smtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Carrega as variáveis de ambiente
load_dotenv()

def conectar_banco_de_dados():
    """Conecta ao banco de dados usando variáveis de ambiente para credenciais."""
    try:
        cnx = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=int(os.getenv('DB_PORT'))
        )
        return cnx
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None

def criar_tabela_usuario(cnx):
    """Cria a tabela de usuários, incluindo email e status premium."""
    cursor = cnx.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT PRIMARY KEY AUTO_INCREMENT,
            usuario VARCHAR(255) NOT NULL,
            senha VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            premium BOOLEAN DEFAULT FALSE
        );
    ''')
    cnx.commit()
    cursor.close()

def inserir_usuario(cnx, usuario, senha, email, premium=False):
    """Insere um novo usuário no banco de dados."""
    cursor = cnx.cursor()
    cursor.execute('''
        INSERT INTO usuarios (usuario, senha, email, premium)
        VALUES (%s, %s, %s, %s);
    ''', (usuario, senha, email, premium))
    cnx.commit()
    cursor.close()

def consultar_usuario(cnx, usuario, senha):
    """Consulta se o usuário existe no banco de dados com a senha fornecida."""
    cursor = cnx.cursor()
    cursor.execute('''
        SELECT id, email, premium FROM usuarios WHERE usuario = %s AND senha = %s;
    ''', (usuario, senha))
    result = cursor.fetchone()
    cursor.close()
    return result

def verifica_nome_usuario(cnx, usuario):
    """Verifica se o nome de usuário já existe no banco de dados."""
    cursor = cnx.cursor()
    cursor.execute('''
        SELECT COUNT(1) FROM usuarios WHERE usuario = %s;
    ''', (usuario,))
    existe = cursor.fetchone()[0] > 0
    cursor.close()
    return existe

def definir_premium(cnx, usuario_id, status):
    """Define o status premium de um usuário pelo seu ID."""
    cursor = cnx.cursor()
    cursor.execute('''
        UPDATE usuarios SET premium = %s WHERE id = %s;
    ''', (status, usuario_id))
    cnx.commit()
    cursor.close()

def enviar_notificacao(email_destino, assunto, mensagem):
    """Envia uma notificação por email para o usuário especificado."""
    try:
        smtp_host = os.getenv('SMTP_HOST')
        smtp_port = int(os.getenv('SMTP_PORT'))
        remetente_email = os.getenv('SMTP_EMAIL')
        remetente_senha = os.getenv('SMTP_PASSWORD')

        msg = MIMEMultipart()
        msg['From'] = remetente_email
        msg['To'] = email_destino
        msg['Subject'] = assunto
        msg.attach(MIMEText(mensagem, 'plain'))

        # Envia o email
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(remetente_email, remetente_senha)
            server.sendmail(remetente_email, email_destino, msg.as_string())

        print(f"Notificação enviada para {email_destino}")

    except Exception as e:
        print(f"Erro ao enviar notificação: {e}")

# Exemplo de uso
if __name__ == "__main__":
    cnx = conectar_banco_de_dados()

    if cnx:
        criar_tabela_usuario(cnx)

        if not verifica_nome_usuario(cnx, "usuario_exemplo"):
            inserir_usuario(cnx, "usuario_exemplo", "senha123", "email@exemplo.com", premium=True)

        usuario_info = consultar_usuario(cnx, "usuario_exemplo", "senha123")
        if usuario_info:
            usuario_id, email, premium = usuario_info
            print(f"Usuário encontrado: ID={usuario_id}, Email={email}, Premium={premium}")

            enviar_notificacao(email, "Bem-vindo!", "Olá, obrigado por se registrar em nosso aplicativo!")

        definir_premium(cnx, usuario_id, False)

        cnx.close()
