import sqlite3
from typing import Optional

DB_PATH = "market_luminus.db"

def conectar() -> sqlite3.Connection:
    """Cria e retorna uma conexão com o banco, ativando foreign keys."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db() -> None:
    """Cria as tabelas necessárias se não existirem."""
    with conectar() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS cliente (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT,
            telefone TEXT
        );
        CREATE TABLE IF NOT EXISTS servico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT
        );
        CREATE TABLE IF NOT EXISTS pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            id_servico INTEGER NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES cliente(id),
            FOREIGN KEY (id_servico) REFERENCES servico(id)
        );
        """)

def cadastrar_cliente() -> None:
    print("\n--- CADASTRO DE CLIENTE ---")
    nome = input("Nome do cliente: ").strip()
    if not nome:
        print("Nome é obrigatório.")
        return
    email = input("Email: ").strip() or None
    telefone = input("Telefone: ").strip() or None

    try:
        with conectar() as conn:
            conn.execute(
                "INSERT INTO cliente (nome, email, telefone) VALUES (?, ?, ?)",
                (nome, email, telefone)
            )
        print("Cliente cadastrado com sucesso!")
    except sqlite3.Error as e:
        print("Erro ao cadastrar cliente:", e)

def listar_clientes() -> None:
    print("\n--- LISTA DE CLIENTES ---")
    try:
        with conectar() as conn:
            cursor = conn.execute("SELECT id, nome, email, telefone FROM cliente ORDER BY id")
            rows = cursor.fetchall()
            if not rows:
                print("Nenhum cliente cadastrado.")
                return
            for r in rows:
                print(f"ID: {r[0]} | Nome: {r[1]} | Email: {r[2] or '-'} | Telefone: {r[3] or '-'}")
    except sqlite3.Error as e:
        print("Erro ao listar clientes:", e)

def cadastrar_servico() -> None:
    print("\n--- CADASTRO DE SERVIÇO ---")
    nome = input("Nome do serviço: ").strip()
    if not nome:
        print("Nome do serviço é obrigatório.")
        return
    descricao = input("Descrição do serviço: ").strip() or None

    try:
        with conectar() as conn:
            conn.execute(
                "INSERT INTO servico (nome, descricao) VALUES (?, ?)",
                (nome, descricao)
            )
        print("Serviço cadastrado com sucesso!")
    except sqlite3.Error as e:
        print("Erro ao cadastrar serviço:", e)

def criar_pedido() -> None:
    print("\n--- CRIAR PEDIDO ---")
    raw_id_cliente = input("ID do cliente: ").strip()
    raw_id_servico = input("ID do serviço: ").strip()
    try:
        id_cliente = int(raw_id_cliente)
        id_servico = int(raw_id_servico)
    except ValueError:
        print("IDs devem ser números inteiros.")
        return

    try:
        with conectar() as conn:
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM cliente WHERE id = ?", (id_cliente,))
            if cur.fetchone() is None:
                print("Cliente não encontrado.")
                return
            cur.execute("SELECT 1 FROM servico WHERE id = ?", (id_servico,))
            if cur.fetchone() is None:
                print("Serviço não encontrado.")
                return

            status = "Em andamento"
            cur.execute(
                "INSERT INTO pedido (id_cliente, id_servico, status) VALUES (?, ?, ?)",
                (id_cliente, id_servico, status)
            )
        print("Pedido criado com sucesso!")
    except sqlite3.Error as e:
        print("Erro ao criar pedido:", e)

def menu() -> None:
    print("\n===== MARKET LUMINUS =====")
    print("1 - Cadastrar cliente")
    print("2 - Listar clientes")
    print("3 - Cadastrar serviço")
    print("4 - Criar pedido")
    print("0 - Sair")

def main() -> None:
    init_db()
    try:
        while True:
            menu()
            opcao = input("Escolha uma opção: ").strip()
            if opcao == "1":
                cadastrar_cliente()
            elif opcao == "2":
                listar_clientes()
            elif opcao == "3":
                cadastrar_servico()
            elif opcao == "4":
                criar_pedido()
            elif opcao == "0":
                print("Sistema encerrado.")
                break
            else:
                print("Opção inválida. Tente novamente.")
    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário.")

if __name__ == "__main__":
    main()
