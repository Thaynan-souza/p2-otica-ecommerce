import mysql.connector
from mysql.connector import Error

def conectar_banco():
    try:
        conexao = mysql.connector.connect(host='localhost', user='root', password='root', database='otica_bd', port='3306')
        if conexao.is_connected(): return conexao
    except Error as e: print(f"Erro: {e}")
    return None

def consultar_produtos():
    conexao = conectar_banco()
    if conexao:
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT * FROM produto")
            return cursor.fetchall()
        finally: cursor.close(); conexao.close()
    return []

def cadastrar_usuario(nome, senha):
    conexao = conectar_banco()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO usuario (nome, senha) VALUES (%s, %s)", (nome, senha))
            conexao.commit()
            return True
        except: return False
        finally: cursor.close(); conexao.close()
    return False

def verificar_login(nome, senha):
    conexao = conectar_banco()
    if conexao:
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuario WHERE nome = %s AND senha = %s", (nome, senha))
            return cursor.fetchone()
        finally: cursor.close(); conexao.close()
    return None

# --- NOVAS FUNÇÕES DO CARRINHO E STOCK ---

def adicionar_ao_carrinho(usuario, cod_produto):
    conexao = conectar_banco()
    if conexao:
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT id_item, quantidade FROM carrinho WHERE usuario = %s AND cod_produto = %s", (usuario, cod_produto))
            item = cursor.fetchone()
            cursor.execute("SELECT estoque FROM produto WHERE cod_produto = %s", (cod_produto,))
            produto = cursor.fetchone()
            
            if item:
                if produto['estoque'] > item['quantidade']:
                    cursor.execute("UPDATE carrinho SET quantidade = quantidade + 1 WHERE id_item = %s", (item['id_item'],))
            else:
                if produto['estoque'] > 0:
                    cursor.execute("INSERT INTO carrinho (usuario, cod_produto, quantidade) VALUES (%s, %s, 1)", (usuario, cod_produto))
            conexao.commit()
            return True
        finally: cursor.close(); conexao.close()
    return False

def atualizar_quantidade(id_item, acao):
    conexao = conectar_banco()
    if conexao:
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT c.quantidade, p.estoque FROM carrinho c JOIN produto p ON c.cod_produto = p.cod_produto WHERE c.id_item = %s", (id_item,))
            dados = cursor.fetchone()
            if dados:
                if acao == 'aumentar' and dados['estoque'] > dados['quantidade']:
                    cursor.execute("UPDATE carrinho SET quantidade = quantidade + 1 WHERE id_item = %s", (id_item,))
                elif acao == 'diminuir' and dados['quantidade'] > 1:
                    cursor.execute("UPDATE carrinho SET quantidade = quantidade - 1 WHERE id_item = %s", (id_item,))
            conexao.commit()
        finally: cursor.close(); conexao.close()

def remover_do_carrinho(id_item):
    conexao = conectar_banco()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM carrinho WHERE id_item = %s", (id_item,))
            conexao.commit()
        finally: cursor.close(); conexao.close()

def esvaziar_carrinho(usuario):
    conexao = conectar_banco()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM carrinho WHERE usuario = %s", (usuario,))
            conexao.commit()
        finally: cursor.close(); conexao.close()

def consultar_carrinho(usuario):
    conexao = conectar_banco()
    if conexao:
        try:
            cursor = conexao.cursor(dictionary=True)
            sql = "SELECT p.cod_produto, p.nome, p.preco, c.id_item, c.quantidade FROM carrinho c JOIN produto p ON c.cod_produto = p.cod_produto WHERE c.usuario = %s"
            cursor.execute(sql, (usuario,))
            return cursor.fetchall()
        finally: cursor.close(); conexao.close()
    return []

def finalizar_compra(usuario):
    conexao = conectar_banco()
    if conexao:
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT p.cod_produto, p.nome, p.preco, c.quantidade FROM carrinho c JOIN produto p ON c.cod_produto = p.cod_produto WHERE c.usuario = %s", (usuario,))
            itens = cursor.fetchall()
            
            if not itens: return False
            
            cursor_inserir = conexao.cursor()
            for item in itens:
                preco_total_item = item['preco'] * item['quantidade']
                nome_formatado = f"{item['quantidade']}x {item['nome']}"
                cursor_inserir.execute("INSERT INTO pedido (usuario, nome_produto, preco) VALUES (%s, %s, %s)", (usuario, nome_formatado, preco_total_item))
                
                # REQUISITO DA PROVA: DAR BAIXA NO STOCK
                cursor_inserir.execute("UPDATE produto SET estoque = estoque - %s WHERE cod_produto = %s", (item['quantidade'], item['cod_produto']))
                
            cursor_inserir.execute("DELETE FROM carrinho WHERE usuario = %s", (usuario,))
            conexao.commit()
            return True
        finally: cursor.close(); conexao.close()
    return False

def consultar_historico(usuario):
    conexao = conectar_banco()
    if conexao:
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT * FROM pedido WHERE usuario = %s ORDER BY data_pedido DESC", (usuario,))
            return cursor.fetchall()
        finally: cursor.close(); conexao.close()
    return []