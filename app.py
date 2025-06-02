
import os
import psycopg2
from flask import Flask, request, jsonify
from datetime import datetime

def conexao_bd():
    conexao = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        dbname=os.getenv('DB_NAME'),
        port=os.getenv('DB_PORT')
    )
    return conexao

app = Flask(__name__)

@app.route('/registrar', methods=['POST'])
def registrar():
    try:
        dados = request.get_json()
        mapa = dados.get('mapa')
        placa = dados.get('placa')
        data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conexao = conexao_bd()
        cursor = conexao.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mapas_rotas (
                id SERIAL PRIMARY KEY,
                mapa TEXT,
                placa TEXT,
                data_registro TIMESTAMP
            )
        ''')
        conexao.commit()

        cursor.execute(
            'INSERT INTO mapas_rotas (mapa, placa, data_registro) VALUES (%s, %s, %s)',
            (mapa, placa, data)
        )
        conexao.commit()

        return jsonify({'msg': 'Registro salvo com sucesso'})
    except Exception as e:
        print(f'Erro: {e}')
        return jsonify({'erro': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexao' in locals():
            conexao.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
