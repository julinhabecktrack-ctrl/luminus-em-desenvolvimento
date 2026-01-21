import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ===============================
# CONEXÃO E CRIAÇÃO DO BANCO
# ===============================
def conectar():
    return sqlite3.connect("market_luminus.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cliente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedido (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER,
        status TEXT,
        FOREIGN KEY (id_cliente) REFERENCES cliente(id)
    )
    """)

    conn.commit()
    conn.close()

# ===============================
# FUNÇÕES DO SISTEMA
# ===============================
def cadastrar_cliente():
    nome = entry_nome.get()
    email = entry_email.get()

    if nome == "" or email == "":
        messagebox.showerror("Erro", "Preencha todos os campos")
        return

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cliente (nome, email) VALUES (?, ?)",
        (nome, email)
    )
    conn.commit()
    conn.close()

    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)

    messagebox.showinfo("Sucesso", "Cliente cadastrado!")
    listar_clientes()

def listar_clientes():
    for item in tree_clientes.get_children():
        tree_clientes.delete(item)

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cliente")
    clientes = cursor.fetchall()
    conn.close()

    for c in clientes:
        tree_clientes.insert("", tk.END, values=c)

def criar_pedido():
    cliente_id = entry_cliente_id.get()
    status = combo_status.get()

    if cliente_id == "" or status == "":
        messagebox.showerror("Erro", "Informe ID do cliente e status")
        return

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO pedido (id_cliente, status) VALUES (?, ?)",
        (cliente_id, status)
    )
    conn.commit()
    conn.close()

    entry_cliente_id.delete(0, tk.END)
    messagebox.showinfo("Sucesso", "Pedido criado!")
    listar_pedidos()

def listar_pedidos():
    for item in tree_pedidos.get_children():
        tree_pedidos.delete(item)

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pedido.id, cliente.nome, pedido.status
        FROM pedido
        JOIN cliente ON pedido.id_cliente = cliente.id
    """)
    pedidos = cursor.fetchall()
    conn.close()

    for p in pedidos:
        tree_pedidos.insert("", tk.END, values=p)

# ===============================
# INTERFACE TKINTER
# ===============================
criar_tabelas()

root = tk.Tk()
root.title("Market Luminus")
root.geometry("900x600")
root.configure(bg="black")

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background="white", foreground="black")

titulo = tk.Label(
    root,
    text="MARKET LUMINUS",
    font=("Arial", 20, "bold"),
    fg="gold",
    bg="black"
)
titulo.pack(pady=10)

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# ===============================
# ABA CLIENTES
# ===============================
frame_clientes = tk.Frame(notebook, bg="black")
notebook.add(frame_clientes, text="Clientes")

tk.Label(frame_clientes, text="Nome:", fg="white", bg="black").pack()
entry_nome = tk.Entry(frame_clientes)
entry_nome.pack()

tk.Label(frame_clientes, text="Email:", fg="white", bg="black").pack()
entry_email = tk.Entry(frame_clientes)
entry_email.pack()

tk.Button(
    frame_clientes,
    text="Cadastrar Cliente",
    bg="gold",
    command=cadastrar_cliente
).pack(pady=10)

tree_clientes = ttk.Treeview(
    frame_clientes,
    columns=("ID", "Nome", "Email"),
    show="headings"
)
tree_clientes.heading("ID", text="ID")
tree_clientes.heading("Nome", text="Nome")
tree_clientes.heading("Email", text="Email")
tree_clientes.pack(expand=True, fill="both")

# ===============================
# ABA PEDIDOS
# ===============================
frame_pedidos = tk.Frame(notebook, bg="black")
notebook.add(frame_pedidos, text="Pedidos")

tk.Label(frame_pedidos, text="ID do Cliente:", fg="white", bg="black").pack()
entry_cliente_id = tk.Entry(frame_pedidos)
entry_cliente_id.pack()

tk.Label(frame_pedidos, text="Status:", fg="white", bg="black").pack()
combo_status = ttk.Combobox(
    frame_pedidos,
    values=["Pendente", "Em andamento", "Concluído"]
)
combo_status.pack()

tk.Button(
    frame_pedidos,
    text="Criar Pedido",
    bg="gold",
    command=criar_pedido
).pack(pady=10)

tree_pedidos = ttk.Treeview(
    frame_pedidos,
    columns=("ID Pedido", "Cliente", "Status"),
    show="headings"
)
tree_pedidos.heading("ID Pedido", text="ID Pedido")
tree_pedidos.heading("Cliente", text="Cliente")
tree_pedidos.heading("Status", text="Status")
tree_pedidos.pack(expand=True, fill="both")

listar_clientes()
listar_pedidos()

root.mainloop()

