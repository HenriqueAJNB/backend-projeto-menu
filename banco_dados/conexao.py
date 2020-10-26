import sqlite3


def cria_tabelas():
    """Cria o esquema de tabelas no banco de dados"""
    conn = sqlite3.connect(r"banco_dados\menu.db")
    with conn:
        conn.execute(
            """CREATE TABLE cliente(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            primeiro_nome TEXT,
                            ultimo_nome TEXT,
                            email TEXT);"""
        )

        conn.execute(
            """CREATE TABLE pedido(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            data TEXT,
                            status TEXT,
                            id_cliente INTEGER,
                            valor REAL,
                            FOREIGN KEY(id_cliente) REFERENCES cliente(id));"""
        )


# ............................ CLIENTE ..................................


def cadastra_cliente(primeiro_nome: str, ultimo_nome: str, email: str):
    """Cadastra um novo cliente no banco de dados"""

    cliente = (primeiro_nome, ultimo_nome, email)

    sql = """INSERT INTO cliente
        (primeiro_nome, ultimo_nome, email)
        VALUES (?,?,?)"""

    conn = sqlite3.connect(r"banco_dados\menu.db")
    with conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute(sql, cliente)


def consulta_cliente(id=None):
    """Consulta um cliente na base utilizando o id"""
    conn = sqlite3.connect(r"banco_dados\menu.db")
    with conn:
        cursor = conn.cursor()
        if not id:
            cursor.execute(f"SELECT * FROM cliente;")
            cliente = cursor.fetchall()
        else:
            cursor.execute(f"SELECT * FROM cliente WHERE id={id};")
            cliente = cursor.fetchall()

    clientes_dict = [
        {"id_cliente": id, "primeiro_nome": pn, "ultimo_nome": un, "e-mail": em}
        for (id, pn, un, em) in cliente
    ]

    return clientes_dict


def altera_cliente(id: int, primeiro_nome: str, ultimo_nome: str, email: str):
    """Altera as informações de um cliente utilizando o id como referência"""
    alteracoes = (primeiro_nome, ultimo_nome, email)
    conn = sqlite3.connect(r"banco_dados\menu.db")
    with conn:
        cursor = conn.cursor()

        sql = f"""UPDATE cliente
                  SET primeiro_nome = ?,
                    ultimo_nome = ?,
                    email = ?
                  WHERE id={id}"""
        cursor.execute(sql, alteracoes)


def remove_cliente(id: int):
    """Remove um cliente da base"""
    conn = sqlite3.connect(r"banco_dados\menu.db")
    with conn:
        cursor = conn.cursor()

        sql = f"""DELETE FROM cliente WHERE id={id};"""
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(sql)


# ............................ PEDIDO ..................................


def cadastra_pedido(data: str, status: str, id_cliente: int, valor: float):
    """Cadastra um novo pedido no bando de dados. Caso o id do cliente informado não esteja cadastrado, o código informará um erro."""
    pedido = (data, status, id_cliente, valor)
    conn = sqlite3.connect(r"banco_dados\menu.db")
    with conn:
        sql = """INSERT INTO pedido
            (data, status, id_cliente, valor)
            VALUES (?,?,?,?)"""

        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(sql, pedido)


def consulta_pedido(id_cliente=None, id_pedido=None):
    """Consulta todos os pedidos dabase de dados. Caso um id_cliente seja especificado, retorna os pedidos daquele cliente"""
    conn = sqlite3.connect(r"banco_dados\menu.db")
    with conn:
        cursor = conn.cursor()
        if id_cliente is None and id_pedido is None:
            cursor.execute(f"SELECT * FROM pedido;")

        elif id_cliente is not None and id_pedido is None:
            cursor.execute(f"SELECT * FROM pedido WHERE id_cliente={id_cliente};")

        elif id_cliente is None and id_pedido is not None:
            cursor.execute(f"SELECT * FROM pedido WHERE id={id_pedido};")

        pedidos = cursor.fetchall()
        pedidos_dict = pedidos_dict = [
            {
                "id_pedido": id,
                "data": dt,
                "status": st,
                "id_cliente": id_cli,
                "valor": vlr,
            }
            for (id, dt, st, id_cli, vlr) in pedidos
        ]

    return pedidos_dict


def altera_pedido(id: int, data: str, status: str, id_cliente: str, valor: float):
    """Altera as informações de um pedido"""
    alteracoes = (data, status, id_cliente, valor)
    conn = sqlite3.connect(r"banco_dados\menu.db")
    with conn:
        cursor = conn.cursor()

        sql = f"""UPDATE pedido
                  SET data = ?,
                    status = ?,
                    id_cliente = ?,
                    valor = ?
                  WHERE id={id}"""
        cursor.execute(sql, alteracoes)


def remove_pedido(id_pedido: int):
    conn = sqlite3.connect(r"banco_dados\menu.db")
    with conn:
        cursor = conn.cursor()

        sql = f"""DELETE FROM pedido WHERE id={id_pedido};"""
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(sql)
