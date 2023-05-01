import sqlite3
from flask import Flask, jsonify, Request

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/registros', methods=['GET'])
def get_registros():
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM registros')
    registros = cursor.fetchall()

    registros_json = []
    for registro in registros:
        registro_json = {'id': registro[0], 'ID': registro[1], 'Modelo': registro[2], 'N de fabricação': registro[3]}
        registros_json.append(registro_json)

    conn.close()

    return jsonify(registros_json)


@app.route('/cadastrar', methods=['POST'])
def cadastrar():

    id = Request.form['ID']
    modelo = Request.form['Modelo']
    fabricação = Request.form['N de fabricação']

    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO registros (ID, Modelo, N de fabricação) VALUES (?, ?, ?)', (id, modelo, fabricação))
    conn.commit()

    conn.close()

    return 'Registro cadastrado com sucesso!'


@app.route('/registros/<campo>/<valor>', methods=['DELETE'])
def excluir_registro(campo, valor):

    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM registros WHERE {campo}=?", (valor,))
    conn.commit()

    if cursor.rowcount == 0:
        return jsonify({'message': 'Registro não encontrado.'}), 404

    conn.close()

    return jsonify({'message': 'Registro excluído com sucesso.'}), 200


if __name__ == '__main__':
    app.run()
