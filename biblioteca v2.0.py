import sqlite3

# ==============================================================================
#   CRIAÇÃO   BANCO DE DADOS:
# ==============================================================================

conexao = sqlite3.connect("Biblioteca.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    autor TEXT NOT NULL,
    status TEXT NOT NULL
)
""")

conexao.commit()
conexao.close()

print("Tabela criada/verificada com sucesso!")

# ==============================================================================
#                  FUNÇÕES DO SISTEMA
# ==============================================================================

# --- 1. CADASTRAR LIVRO ---
def cadastrar_livro():
    nome = input("Nome do livro: ").lower().strip()
    autor = input("Nome do autor: ").lower().strip()
    status = "Disponivel"

    conexao = sqlite3.connect("Biblioteca.db")
    cursor = conexao.cursor()

    # Verifica se o livro já existe antes de adicionar
    cursor.execute("SELECT 1 FROM livros WHERE nome = ? AND autor = ?", (nome, autor))
    livro_existe = cursor.fetchone()

    if livro_existe:
        print(f"\n Erro: O livro '{nome.title()}' deste autor já está cadastrado!")
        conexao.close()
    else:
        # Se não existir, insere (o ID gera automático pelo AUTOINCREMENT)
        cursor.execute("""
        INSERT INTO livros (nome, autor, status)
        VALUES (?, ?, ?)
        """, (nome, autor, status))

        conexao.commit()
        conexao.close()
        print(f"\n✅ Livro '{nome.title()}' cadastrado com sucesso!")


# --- 2. BUSCAR LIVRO ---
def buscar_livro():
    buscar = input("Digite o nome do livro para buscar: ").lower().strip()

    conexao = sqlite3.connect("Biblioteca.db")
    cursor = conexao.cursor()

    # Busca parcial por nome (traz o ID também para o usuário saber qual usar)
    cursor.execute("SELECT id, nome, autor, status FROM livros WHERE nome LIKE ?", (f"%{buscar}%",))
    resultados = cursor.fetchall()
    conexao.close()

    if resultados:
        print(f"\n Livros encontrados com o termo '{buscar}':")
        for livro in resultados:
            # Exibe o ID na tela
            print(f"-  ID: {livro[0]} | Nome: {livro[1].title()} | Autor: {livro[2].title()} | Status: {livro[3]}")
    else:
        print(f"\n Nenhum livro encontrado com o nome '{buscar}'")  


# --- 3. EMPRESTAR LIVRO (PELO ID) ---
def emprestar_livro():
    id_livro = int(input("Digite o ID do livro que deseja pegar emprestado: "))

    conexao = sqlite3.connect("Biblioteca.db")
    cursor = conexao.cursor()

    # Busca o status e nome do livro pelo ID
    cursor.execute("SELECT status, nome FROM livros WHERE id = ?", (id_livro,))
    resultado = cursor.fetchone()

    if resultado is None:
        print(f"\n Erro: O ID '{id_livro}' não foi encontrado no sistema.")
    elif resultado[0] == "Emprestado":
        print(f"\n O livro '{resultado[1].title()}' já está emprestado no momento.")
    else:
        # Altera o status usando o ID como filtro
        cursor.execute("UPDATE livros SET status = 'Emprestado' WHERE id = ?", (id_livro,))
        conexao.commit()
        print(f"\n Sucesso! O livro '{resultado[1].title()}' foi emprestado.")

    conexao.close()


# --- 4. DEVOLVER LIVRO (PELO ID) ---
def devolver_livro():
    id_livro = int(input("Digite o ID do livro que deseja devolver: "))

    conexao = sqlite3.connect("Biblioteca.db")
    cursor = conexao.cursor()

    # Busca o status e nome do livro pelo ID
    cursor.execute("SELECT status, nome FROM livros WHERE id = ?", (id_livro,))
    resultado = cursor.fetchone()

    if resultado is None:
        print(f"\n Erro: O ID '{id_livro}' não foi encontrado no sistema.")
    elif resultado[0] == "Disponivel":
        print(f"\n O livro '{resultado[1].title()}' já consta como disponível no sistema.")
    else:
        # Atualiza o status de volta para Disponivel usando o ID
        cursor.execute("UPDATE livros SET status = 'Disponivel' WHERE id = ?", (id_livro,))
        conexao.commit()
        print(f"\n Sucesso! O livro '{resultado[1].title()}' foi devolvido.")   
    
    conexao.close()


# --- 5. REMOVER LIVRO (PELO ID) ---
def remover_livro():
    id_livro = int(input("Digite o ID do livro que deseja remover: "))

    conexao = sqlite3.connect("Biblioteca.db")
    cursor = conexao.cursor()

    # Verifica se existe pelo ID e pega o nome para o print
    cursor.execute("SELECT nome FROM livros WHERE id = ?", (id_livro,))
    resultado = cursor.fetchone()

    if resultado is None:
        print(f"\n ERRO: O ID '{id_livro}' não foi encontrado.")
    else:
        # Remove fisicamente a linha pelo ID
        cursor.execute("DELETE FROM livros WHERE id = ?", (id_livro,))
        conexao.commit()
        print(f"\n O Livro '{resultado[0].title()}' foi removido do sistema com sucesso!")
    
    conexao.close()


# --- 6. MOSTRAR LIVROS POR STATUS ---
def mostrar_livro_por_status():
    opcao = input("Deseja ver os livros disponiveis (1) ou Emprestados (2): ").strip()

    if opcao == "1":
        status_busca = "Disponivel"
    elif opcao == "2":
        status_busca = "Emprestado"
    else:
        print("\n Escolha uma opção válida")
        return

    conexao = sqlite3.connect("Biblioteca.db")
    cursor = conexao.cursor()

    # Busca também o ID
    cursor.execute("SELECT id, nome, autor FROM livros WHERE status = ?", (status_busca,))
    resultados = cursor.fetchall()
    conexao.close()

    if resultados:
        print(f"\n Livros com status '{status_busca}': ")
        for livro in resultados:
            print(f"-  ID: {livro[0]} | {livro[1].title()} (Autor: {livro[2].title()})")
    else:
        print(f"\n Nenhum livro encontrado com o status '{status_busca}'.")


# --- 7. HISTÓRICO / RELATÓRIO DA BIBLIOTECA ---
def historico_biblioteca():
    conexao = sqlite3.connect("Biblioteca.db")
    cursor = conexao.cursor()

    # Busca ID, nome, autor e status de tudo
    cursor.execute("SELECT id, nome, autor, status FROM livros")
    todos_livros = cursor.fetchall()
    conexao.close()

    if not todos_livros:
        print("\n A Biblioteca está vazia.")
        return

    total_livros = len(todos_livros)
    disponivel = 0
    emprestado = 0

    print("\n === RELATÓRIO DA BIBLIOTECA ===")
    for livro in todos_livros:
        id_banco, nome, autor, status = livro
        print(f" ID: {id_banco} | {nome.title()} | Autor: {autor.title()} | Status: {status}")

        if status == "Disponivel":
            disponivel += 1
        elif status == "Emprestado":
            emprestado += 1
            
    print("-" * 40)
    print(f" Resumo: Total: {total_livros} | Disponíveis: {disponivel} | Emprestados: {emprestado}")
    print("=" * 40)

def sair():
    print("Saindo...")




# ==============================================================================
#        MENU PRINCIPAL ( CONTROLE DE FLUXO )
# ==============================================================================

def menu():
    while True:
        print("\n=== MENU BIBLIOTECA ===")
        print("1. Cadastrar Livro")
        print("2. Buscar Livro")
        print("3. Emprestar Livro")
        print("4. Devolver Livro")
        print("5. Remover Livro")
        print("6. Mostrar por Status")
        print("7. Relatório Geral")
        print("0. Sair")
        
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_livro()
        elif opcao == "2":
            buscar_livro()
        elif opcao == "3":
            emprestar_livro()
        elif opcao == "4":
            devolver_livro()
        elif opcao == "5":
            remover_livro()
        elif opcao == "6":
            mostrar_livro_por_status()
        elif opcao == "7":
            historico_biblioteca()
        elif opcao == "0":
            sair()
            break
        else:
            print("\n Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()