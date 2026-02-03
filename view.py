from flask import Flask, jsonify, request
from main import app, con

@app.route('/livro', methods=['GET'])
def livro():
    try:
        cur= con.cursor()
        cur.execute('SELECT id_livro, titulo, autor, ano_publicacao FROM livros')
        livros = cur.fetchall()

        livros_lis = []

        for livro in livros:
            livros_lis.append({
                'id_livro': livro[0],
                'titulo': livro[1],
                'autor': livro[2],
                'ano_publicacao': livro[3]
            })
        return jsonify(mensagem='Lista de Livros', livros=livros_lis)
    except Exception as e:
        return jsonify(mensagem=f"Erro ao consultar banco de dados: {e}"), 500
    finally:
        cur.close()






@app.route('/criar_livro', methods=['POST'])
def criar_livro():
        data = request.get_json()


        titulo = data.get('titulo')
        autor = data.get('autor')
        ano_publicacao = data.get('ano_publicacao')

        try:

            cur = con.cursor()
            cur.execute("SELECT 1 FROM livros WHERE titulo = ? ", (titulo,))
            if cur.fetchone():
                return jsonify({"error": "Livro já cadastrado"}), 400
            cur.execute("INSERT INTO livros (titulo, autor, ano_publicacao) VALUES (?,?,?)",
                                                        (titulo, autor, ano_publicacao))



            con.commit()


            return jsonify({
                'message': 'Livro cadastrado com sucesso!',
                'livro': {
                    'titulo': titulo,
                    'autor': autor,
                    'ano_publicacao': ano_publicacao
                }
            }),201



        except Exception as e:
            return jsonify(mensagem=f"Erro ao consultar banco de dados: {e}"), 500
        finally:
            cur.close()

