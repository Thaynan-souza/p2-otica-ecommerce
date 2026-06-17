import mysql.connector
from mysql.connector import Error

def conectar_banco():
    """Estabelece a conexão com o banco de dados da ótica."""
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='otica_bd',
            port='3306'
        )
        if conexao.is_connected():
            return conexao
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def consultar_produtos():
    """Busca todos os produtos cadastrados no banco de dados[cite: 43]."""
    conexao = conectar_banco()
    if conexao:
        try:
            # dictionary=True faz o Python retornar os dados com os nomes das colunas (nome, preco, etc)
            # Isso vai facilitar MUITO a nossa vida na hora de jogar pro HTML (Jinja2) depois!
            cursor = conexao.cursor(dictionary=True) 
            cursor.execute("SELECT * FROM produto")
            produtos = cursor.fetchall()
            return produtos
        except Error as e:
            print(f"Erro ao consultar produtos: {e}")
            return []
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()
    return []
def cadastrar_usuario(nome, senha):
    """Insere um novo usuário no banco de dados."""
    conexao = conectar_banco()
    if conexao:
        try:
            cursor = conexao.cursor()
            sql = "INSERT INTO usuario (nome, senha) VALUES (%s, %s)"
            cursor.execute(sql, (nome, senha))
            conexao.commit()
            return True
        except Error as e:
            print(f"Erro ao cadastrar usuário: {e}")
            return False
        finally:
            cursor.close()
            conexao.close()
    return False

def verificar_login(nome, senha):
    """Verifica se o usuário e a senha existem e batem no banco de dados."""
    conexao = conectar_banco()
    if conexao:
        try:
            cursor = conexao.cursor(dictionary=True)
            sql = "SELECT * FROM usuario WHERE nome = %s AND senha = %s"
            cursor.execute(sql, (nome, senha))
            usuario = cursor.fetchone() # Traz apenas 1 resultado
            return usuario # Retorna os dados se achou, ou None se não achou
        except Error as e:
            print(f"Erro ao verificar login: {e}")
            return None
        finally:
            cursor.close()
            conexao.close()
    return None
def adicionar_ao_carrinho(usuario, cod_produto):
    """Insere um produto no carrinho do usuário logado."""
    conexao = conectar_banco()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO carrinho (usuario, cod_produto) VALUES (%s, %s)", (usuario, cod_produto))
            conexao.commit()
            return True
        except Error as e:
            print(f"Erro ao adicionar ao carrinho: {e}")
        finally:
            cursor.close()
            conexao.close()
    return False

def consultar_carrinho(usuario):
    """Busca todos os produtos que estão no carrinho do usuário."""
    conexao = conectar_banco()
    if conexao:
        try:
            cursor = conexao.cursor(dictionary=True)
            # O JOIN une a tabela carrinho com a tabela produto para pegarmos o nome e o preço
            sql = """
                SELECT p.cod_produto, p.nome, p.preco, c.id_item 
                FROM carrinho c
                JOIN produto p ON c.cod_produto = p.cod_produto
                WHERE c.usuario = %s
            """
            cursor.execute(sql, (usuario,))
            return cursor.fetchall()
        except Error as e:
            print(f"Erro ao consultar carrinho: {e}")
        finally:
            cursor.close()
            conexao.close()
    return []

def finalizar_compra(usuario):
    """Transfere os itens do carrinho para a tabela de pedidos e limpa o carrinho."""
    conexao = conectar_banco()
    if conexao:
        try:
            cursor = conexao.cursor(dictionary=True)
            
            # 1. Procura os itens atuais do carrinho do utilizador
            sql_buscar = """
                SELECT p.nome, p.preco 
                FROM carrinho c
                JOIN produto p ON c.cod_produto = p.cod_produto
                WHERE c.usuario = %s
            """
            cursor.execute(sql_buscar, (usuario,))
            itens = cursor.fetchall()
            
            if not itens:
                return False # Carrinho vazio
            
            # 2. Transfere cada item para a tabela de pedidos
            cursor_inserir = conexao.cursor()
            sql_inserir = "INSERT INTO pedido (usuario, nome_produto, preco) VALUES (%s, %s, %s)"
            for item in itens:
                cursor_inserir.execute(sql_inserir, (usuario, item['nome'], item['preco']))
            
            # 3. Limpa o carrinho do utilizador
            sql_limpar = "DELETE FROM carrinho WHERE usuario = %s"
            cursor_inserir.execute(sql_limpar, (usuario,))
            
            conexao.commit()
            cursor_inserir.close()
            return True
        except Error as e:
            print(f"Erro ao finalizar compra: {e}")
        finally:
            cursor.close()
            conexao.close()
    return False

def consultar_historico(usuario):
    """Procura o histórico de compras de um utilizador específico."""
    conexao = conectar_banco()
    if conexao:
        try:
            cursor = conexao.cursor(dictionary=True)
            sql = "SELECT * FROM pedido WHERE usuario = %s ORDER BY data_pedido DESC"
            cursor.execute(sql, (usuario,))
            return cursor.fetchall()
        except Error as e:
            print(f"Erro ao consultar histórico: {e}")
        finally:
            cursor.close()
            conexao.close()
    return []

# Teste rápido: Isso só roda se você executar este arquivo diretamente
if __name__ == "__main__":
    produtos_otica = consultar_produtos()
    print("--- Produtos cadastrados na Ótica ---")
    for p in produtos_otica:
        print(f"ID: {p['cod_produto']} | {p['nome']} | R$ {p['preco']:.2f} | Estoque: {p['estoque']}")