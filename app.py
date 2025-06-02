import psycopg2
from flask import Flask, request, jsonify
from datetime import datetime

# Conexão com o banco PostgreSQL (Render)
def conexao_bd():
    conexao = psycopg2.connect(
        host='dpg-d0v1po95pdvs7381bdhg-a.oregon-postgres.render.com',
        port='5432',
        database='meudb_5hu3',
        user='meudb_5hu3_user',
        password='Oe392lgWTjk9d37jPZCqTXmTKBqioWrt'
    )
    return conexao

# Criação da tabela, se não existir
def criar_tabela():
    try:
        conexao = conexao_bd()
        cursor = conexao.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mapas_rotas (
                id SERIAL PRIMARY KEY,
                mapa VARCHAR(255) NOT NULL,
                placa VARCHAR(50) NOT NULL,
                data_registro TIMESTAMP NOT NULL
            )
        ''')
        conexao.commit()
        cursor.close()
        conexao.close()
        print("Tabela verificada/criada com sucesso.")
    except Exception as e:
        print(f'Erro ao criar tabela: {e}')

# Inicializa o Flask e a tabela
app = Flask(__name__)
criar_tabela()

@app.route('/registrar', methods=['POST'])
def registrar():
    try:
        dados = request.get_json()
        mapa = dados.get('mapa')
        placa = dados.get('placa')
        data = datetime.now()

        conexao = conexao_bd()
        cursor = conexao.cursor()
        query = 'INSERT INTO mapas_rotas (mapa, placa, data_registro) VALUES (%s, %s, %s)'
        cursor.execute(query, (mapa, placa, data))
        conexao.commit()

        return jsonify({'msg': '1'})
    except Exception as e:
        print(f'Erro: {e}')
        return jsonify({'erro': str(e)})
    finally:
        try:
            cursor.close()
            conexao.close()
        except:
            pass

if __name__ == '__main__':
    app.run(debug=True)
