from flask import Flask, make_response, jsonify, request
import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='P@ssw0rd',
    database='CreateDatabase'
)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/livros', methods=['GET'])
def obter_livros():
    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM books')
    meus_livros = my_cursor.fetchall()

    return make_response(
        jsonify(
            mensagem = 'Lista de livros!',
            dados = meus_livros
        )
    )

@app.route('/livros', methods=['POST'])
def incluir_novo_livro():
    novo_livro = request.get_json()

    my_cursor = mydb.cursor()
    sql = f"INSERT INTO books (titulo, autor) VALUES ('{novo_livro['titulo']}', '{novo_livro['autor']}')"
    my_cursor.execute(sql)
    mydb.commit()

    return make_response(
        jsonify(
            mensagem = 'Novo livro cadastrado com sucesso!',
            dados = novo_livro
        )
    )

@app.route('/livros/<int:id>', methods=['GET'])
def obter_livro_por_id(id):

    my_cursor = mydb.cursor()
    sql = f"SELECT titulo, autor FROM books WHERE id={id}"
    my_cursor.execute(sql)
    result = my_cursor.fetchall()

    return make_response(
        jsonify(
            mensagem = 'Livro selecionado com sucesso!',
            dados = result
        )
    )

@app.route('/livros/<int:id>', methods=['PUT'])
def editar_livro_por_id(id):
    livro_atualizado = request.get_json()

    my_cursor = mydb.cursor()
    sql = "UPDATE books SET titulo = %s, autor = %s WHERE id = %s"
    val = (livro_atualizado['titulo'], livro_atualizado['autor'], id)
    my_cursor.execute(sql, val)
    mydb.commit()

    return make_response(
        jsonify(
            mensagem = 'Livro atualizado com sucesso!',
            dados = livro_atualizado
        )
    )

@app.route('/livros/<int:id>', methods=['DELETE'])
def excluir_livro(id):

    my_cursor = mydb.cursor()
    sql = f"DELETE FROM books WHERE id={id}"
    my_cursor.execute(sql)
    mydb.commit()

    return make_response(
        jsonify(
            mensagem = 'Livro excluido com sucesso!'
        ), 200
    )

app.run(port=5000, host='localhost', debug=True)