import os
from sqlite3.dbapi2 import IntegrityError

from flask import Flask, request
from flask.json import jsonify

from banco_dados.conexao import (
    altera_cliente,
    altera_pedido,
    cadastra_cliente,
    cadastra_pedido,
    consulta_cliente,
    consulta_pedido,
    cria_tabelas,
    remove_cliente,
    remove_pedido,
)

app = Flask(__name__)


# - - - - - - - - - - - - /clientes - - - - - - - - - - - -
# GET
@app.route("/clientes", methods=["GET"])
def get_clientes():
    """Lista todos os clientes da base"""
    clientes = consulta_cliente()
    if len(clientes) == 0:
        return jsonify({"Clientes": "nao há clientes cadastrados"}), 200
    return jsonify({"Clientes": clientes}), 200


# POST
@app.route("/clientes", methods=["POST"])
def post_clientes():
    """
    Insere um cliente na base
    ...
    Formato de entrada:
    {
        "email": "e-mail",
        "primeiro_nome": "prim_nome",
        "ultimo_nome": "ult_nome"
    }
    """
    if not request.json:
        return jsonify({"Erro": "Nenhum dado informado"}), 400

    if "primeiro_nome" not in request.json:
        return jsonify({"Erro": "Primeiro nome nao encontrado"}), 400

    if "ultimo_nome" not in request.json:
        return jsonify({"Erro": "Último nome nao encontrado!"}), 400

    if "email" not in request.json:
        return jsonify({"Erro": "Email nao encontrado!"}), 400

    cadastra_cliente(
        request.json["primeiro_nome"],
        request.json["ultimo_nome"],
        request.json["email"],
    )
    return jsonify({"status": "sucesso"}), 200


# - - - - - - - - - - - - /cliente/id_cliente - - - - - - - - - - - -
# GET
@app.route("/cliente/<int:id_cliente>", methods=["GET"])
def get_cliente(id_cliente):
    """Consulta um cliente através do id, trazendo todos os pedidos relacionados à ele"""
    cliente = consulta_cliente(id_cliente)
    pedidos = consulta_pedido(id_cliente)

    if cliente is not None and len(pedidos) != 0:
        return (
            jsonify(
                {f"cliente_{id_cliente}": cliente, "pedidos_relacionados": pedidos}
            ),
            200,
        )
    elif cliente is not None and len(pedidos) == 0:
        return (
            jsonify(
                {
                    f"cliente_{id_cliente}": cliente,
                    "pedidos_relacionados": "sem pedido registrado",
                }
            ),
            200,
        )
    else:
        return jsonify({"Erro": "id nao encontrado"}), 400


# PUT
@app.route("/cliente/<int:id_cliente>", methods=["PUT"])
def put_cliente(id_cliente):
    """Altera cliente através do id"""

    if not request.json:
        return jsonify({"Erro": "Nenhum dado informado!"}), 400

    if "primeiro_nome" not in request.json:
        return jsonify({"Erro": "Primeiro nome nao encontrado"}), 400

    if "ultimo_nome" not in request.json:
        return jsonify({"Erro": "Último nome nao encontrado"}), 400

    if "email" not in request.json:
        return jsonify({"Erro": "E-mail nome nao encontrado"}), 400

    altera_cliente(
        id_cliente,
        request.json["primeiro_nome"],
        request.json["ultimo_nome"],
        request.json["email"],
    )

    return jsonify({"status": "sucesso"}), 200


# DELETE
@app.route("/cliente/<int:id_cliente>", methods=["DELETE"])
def delete_cliente(id_cliente):
    """Deleta um cliente da base.
    nao pode haver pedidos relacionados para nao gerar erro de integridade no banco de dados.
    """
    try:
        remove_cliente(id_cliente)
        return jsonify({"status": "sucesso"}), 200
    except IntegrityError:
        return (
            jsonify(
                {
                    "Erro ao remover": "Cliente com pedido cadastrado na base",
                    "Pedidos cadastrados": consulta_pedido(id_cliente),
                }
            ),
            400,
        )


# - - - - - - - - - - - - /pedidos - - - - - - - - - - - -
# GET
@app.route("/pedidos", methods=["GET"])
def get_pedidos():
    """Lista todos os pedidos na base"""
    pedidos = consulta_pedido()
    if len(pedidos) == 0:
        return jsonify({"Pedidos": "Nao ha pedidos registrados"}), 200
    else:
        return jsonify({"Pedidos": pedidos}), 200


# POST
@app.route("/pedidos", methods=["POST"])
def post_pedido():
    """
    Insere um pedido na base
    ...
    Formato de entrada:
    {
        "data": "22/05/1990",
        "status": "ok",
        "id_cliente": 5,
        "valor": 50
    }
    """
    if not request.json:
        return jsonify({"Erro": "Nenhum dado informado"}), 400

    if "data" not in request.json:
        return jsonify({"Erro": "Data nome nao encontrado"}), 400

    if "status" not in request.json:
        return jsonify({"Erro": "Status nao encontrado!"}), 400

    if "id_cliente" not in request.json:
        return jsonify({"Erro": "Id do cliente nao encontrado!"}), 400

    if "valor" not in request.json:
        return jsonify({"Erro": "Valor nao encontrado!"}), 400

    try:
        cadastra_pedido(
            request.json["data"],
            request.json["status"],
            request.json["id_cliente"],
            request.json["valor"],
        )
        return jsonify({"status": "sucesso"}), 200
    except IntegrityError:
        return jsonify({"Erro": "Id do cliente nao cadastrado"}), 400


# - - - - - - - - - - - - /pedidos/id_pedido - - - - - - - - - - - -
# GET
@app.route("/pedido/<int:id_pedido>", methods=["GET"])
def get_pedido(id_pedido):
    """Consulta um pedido na base"""
    pedido = consulta_pedido(id_pedido=id_pedido)
    if len(pedido) == 0:
        return jsonify({"Erro": "Id nao encontrado"}), 400
    return jsonify(pedido), 200


# PUT
@app.route("/pedido/<int:id_pedido>", methods=["PUT"])
def put_pedido(id_pedido):
    """Altera um pedido através do id"""

    if not request.json:
        return jsonify({"Erro": "Nenhum dado informado!"}), 400

    if "data" not in request.json:
        return jsonify({"Erro": "Data nao encontrada!"}), 400

    if "status" not in request.json:
        return jsonify({"Erro": "Status nao encontrado!"}), 400

    if "id_cliente" not in request.json:
        return jsonify({"Erro": "id do cliente nao encontrado!"}), 400

    if "valor" not in request.json:
        return jsonify({"Erro": "valor nao encontrado!"}), 400

    altera_pedido(
        id_pedido,
        request.json["data"],
        request.json["status"],
        request.json["id_cliente"],
        request.json["valor"],
    )

    return jsonify({"status": "sucesso"}), 200


# DELETE
@app.route("/pedido/<int:id_pedido>", methods=["DELETE"])
def delete_pedido(id_pedido):
    """Deleta um pedido"""
    remove_pedido(id_pedido)
    return jsonify({"status": "sucesso"}), 200


if __name__ == "__main__":
    if not os.path.exists(r"banco_dados\menu.db"):
        cria_tabelas()
    app.run(debug=True)
