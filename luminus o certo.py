import sqlite3

# =====================================
# CONEXÃO COM O BANCO
# =====================================
def conectar():
    return sqlite3.connect("market_luminus.db")

# =====================================
# CADASTRAR CLIENTE
# =====================================
def cadastrar_cliente():
    print("\n--- CADASTRO DE CLIENTE ---")
    nome = input("Nome: ")
    email = input("Email: ")
    telefone = input("Telefone: ")

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO cliente (nome, email, telefone)
            VALUES (?, ?, ?)
        """, (nome, email, telefone))

        conn.commit()
        conn.close()
        print("Cliente cadastrado com sucesso!")

    except Exception as erro:
        print("Erro:", erro)

# =====================================
# LISTAR CLIENTES
# =====================================
def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome FROM cliente")
    clientes = cursor.fetchall()

    if not clientes:
        print("Nenhum cliente cadastrado.")
    else:
        for c in clientes:
            print(f"{c[0]} - {c[1]}")

    conn.close()

# =====================================
# CADASTRAR SERVIÇO
# =====================================
def cadastrar_servico():
    print("\n--- CADASTRO DE SERVIÇO ---")
    nome = input("Nome do serviço: ")
    descricao = input("Descrição: ")

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO servico (nome, descricao)
            VALUES (?, ?)
        """, (nome, descricao))

        conn.commit()
        conn.close()
        print("Serviço cadastrado com sucesso!")

    except Exception as erro:
        print("Erro:", erro)

# =====================================
# LISTAR SERVIÇOS
# =====================================
def listar_servicos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome FROM servico")
    servicos = cursor.fetchall()

    if not servicos:
        print("Nenhum serviço cadastrado.")
    else:
        for s in servicos:
            print(f"{s[0]} - {s[1]}")

    conn.close()

# =====================================
# CRIAR PEDIDO
# =====================================
def criar_pedido():
    print("\n--- CRIAR PEDIDO ---")

    print("\nClientes:")
    listar_clientes()
    id_cliente = input("ID do cliente: ")

    print("\nServiços:")
    listar_servicos()
    id_servico = input("ID do serviço: ")

    status = "Em andamento"

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO pedido (id_cliente, id_servico, status)
            VALUES (?, ?, ?)
        """, (id_cliente, id_servico, status))

        conn.commit()
        conn.close()
        print("Pedido criado com sucesso!")

    except Exception as erro:
        print("Erro:", erro)

# =====================================
# LISTAR PEDIDOS
# =====================================
def listar_pedidos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT pedido.id,
               cliente.nome,
               servico.nome,
               pedido.status
        FROM pedido
        JOIN cliente ON pedido.id_cliente = cliente.id
        JOIN servico ON pedido.id_servico = servico.id
    """)

    pedidos = cursor.fetchall()

    if not pedidos:
        print("Nenhum pedido cadastrado.")
    else:
        for p in pedidos:
            print(f"Pedido {p[0]} | Cliente: {p[1]} | Serviço: {p[2]} | Status: {p[3]}")

    conn.close()

# =====================================
# ALTERAR STATUS DO PEDIDO
# =====================================
def alterar_status_pedido():
    print("\n--- ALTERAR STATUS ---")

    listar_pedidos()
    id_pedido = input("\nID do pedido: ")

    print("1 - Em andamento")
    print("2 - Concluído")
    opcao = input("Novo status: ")

    if opcao == "1":
        status = "Em andamento"
    elif opcao == "2":
        status = "Concluído"
    else:
        print("Opção inválida.")
        return

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE pedido
            SET status = ?
            WHERE id = ?
        """, (status, id_pedido))

        conn.commit()
        conn.close()
        print("Status atualizado!")

    except Exception as erro:
        print("Erro:", erro)

# =====================================
# MENU
# =====================================
def menu():
    print("\n===== MARKET LUMINUS =====")
    print("1 - Cadastrar cliente")
    print("2 - Listar clientes")
    print("3 - Cadastrar serviço")
    print("4 - Criar pedido")
    print("5 - Listar pedidos")
    print("6 - Alterar status do pedido")
    print("0 - Sair")

# =====================================
# PROGRAMA PRINCIPAL
# =====================================
while True:
    menu()
    opcao = input("Escolha: ")

    if opcao == "1":
        cadastrar_cliente()
    elif opcao == "2":
        listar_clientes()
    elif opcao == "3":
        cadastrar_servico()
    elif opcao == "4":
        criar_pedido()
    elif opcao == "5":
        listar_pedidos()
    elif opcao == "6":
        alterar_status_pedido()
    elif opcao == "0":
        print("Sistema encerrado.")
        break
    else:
        print("Opção inválida.")
