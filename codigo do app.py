import tkinter as tk
from tkinter import messagebox
import sqlite3

# ======================
# CONFIGURAÇÕES INICIAIS
# ======================
root = tk.Tk()
root.title("Marketing Luminus")
root.geometry("1100x650")
root.configure(bg="#0f0f0f")

# ======================
# FUNÇÕES
# ======================
def tela_em_construcao(nome):
    messagebox.showinfo(
        "Market Luminus",
        f"A tela '{nome}' está em desenvolvimento.\n\nSistema em evolução."
    )

# ======================
# BANCO DE DADOS (BASE)
# ======================
conn = sqlite3.connect("market_luminus.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT
)
""")

conn.commit()

# ======================
# CORES
# ======================
PRETO = "#0f0f0f"
DOURADO = "#d4af37"
BRANCO = "#ffffff"
CINZA = "#1a1a1a"

# ======================
# MENU LATERAL
# ======================
menu = tk.Frame(root, bg=PRETO, width=220)
menu.pack(side="left", fill="y")

tk.Label(
    menu,
    text="Luminus",
    bg=PRETO,
    fg=DOURADO,
    font=("Arial", 18, "bold")
).pack(pady=30)

def botao_menu(texto):
    return tk.Button(
        menu,
        text=texto,
        bg=PRETO,
        fg=BRANCO,
        activebackground=DOURADO,
        activeforeground=PRETO,
        relief="solid",
        borderwidth=1,
        command=lambda: tela_em_construcao(texto)
    )

botao_menu("Dashboard").pack(fill="x", pady=5, padx=15)
botao_menu("Leads").pack(fill="x", pady=5, padx=15)
botao_menu("Conteúdo").pack(fill="x", pady=5, padx=15)
botao_menu("Calendário").pack(fill="x", pady=5, padx=15)
botao_menu("Feedbacks").pack(fill="x", pady=5, padx=15)

# ======================
# ÁREA PRINCIPAL
# ======================
main = tk.Frame(root, bg=CINZA)
main.pack(expand=True, fill="both")

# TÍTULO
tk.Label(
    main,
    text="Marketing Luminus",
    bg=CINZA,
    fg=DOURADO,
    font=("Arial", 26, "bold")
).pack(pady=20)

tk.Label(
    main,
    text="Bem-vindo(a), administrador",
    bg=CINZA,
    fg=BRANCO,
    font=("Arial", 12)
).pack(pady=5)

# ======================
# CARDS (BOTÕES GRANDES)
# ======================
cards = tk.Frame(main, bg=CINZA)
cards.pack(pady=40)

def card(texto):
    return tk.Button(
        cards,
        text=texto,
        width=22,
        height=5,
        bg=BRANCO,
        fg=PRETO,
        relief="solid",
        borderwidth=2,
        highlightbackground=DOURADO,
        command=lambda: tela_em_construcao(texto)
    )

card("Clientes").grid(row=0, column=0, padx=20, pady=20)
card("Campanhas").grid(row=0, column=1, padx=20, pady=20)
card("Pedidos").grid(row=0, column=2, padx=20, pady=20)

card("Agenda").grid(row=1, column=0, padx=20, pady=20)
card("Feedbacks").grid(row=1, column=1, padx=20, pady=20)
card("Conteúdos").grid(row=1, column=2, padx=20, pady=20)

# ======================
# RODAR SISTEMA
# ======================
root.mainloop()

