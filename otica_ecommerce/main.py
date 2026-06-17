from fastapi import FastAPI, Request, Form, responses, Cookie
from fastapi.templating import Jinja2Templates
import uvicorn
from typing import Optional

# Importamos todas as funções do banco.py
from banco import (
    consultar_produtos, cadastrar_usuario, verificar_login, 
    adicionar_ao_carrinho, consultar_carrinho, finalizar_compra, consultar_historico
)

app = FastAPI(title="Ótica E-commerce")
paginas = Jinja2Templates(directory="paginas")

# --- VITRINE PRINCIPAL ---
@app.get("/")
async def index(request: Request, usuario_logado: Optional[str] = Cookie(None)):
    produtos_bd = consultar_produtos()
    qtd_carrinho = 0
    if usuario_logado:
        qtd_carrinho = len(consultar_carrinho(usuario_logado))
        
    contexto = {"request": request, "produtos": produtos_bd, "usuario": usuario_logado, "qtd_carrinho": qtd_carrinho}
    return paginas.TemplateResponse(request=request, name="index.html", context=contexto)

# --- AUTENTICAÇÃO ---
@app.get("/login")
async def login_page(request: Request):
    return paginas.TemplateResponse(request=request, name="login.html", context={"request": request})

@app.post("/login")
async def login_handler(request: Request, username: str = Form(...), password: str = Form(...), action: str = Form(...)):
    if action == "cadastrar":
        if cadastrar_usuario(username, password):
            return paginas.TemplateResponse(request=request, name="login.html", context={"request": request, "sucesso_msg": "Conta criada! Faça login."})
        return paginas.TemplateResponse(request=request, name="login.html", context={"request": request, "erro_msg": "Erro ao cadastrar."})
    elif action == "entrar":
        if verificar_login(username, password):
            resposta = responses.RedirectResponse(url="/", status_code=303)
            resposta.set_cookie(key="usuario_logado", value=username)
            return resposta
        return paginas.TemplateResponse(request=request, name="login.html", context={"request": request, "erro_msg": "Usuário ou senha incorretos."})

@app.get("/logout")
async def logout():
    resposta = responses.RedirectResponse(url="/", status_code=303)
    resposta.delete_cookie("usuario_logado")
    return resposta

# --- CARRINHO ---
@app.post("/adicionar")
async def adicionar_item(id_produto: int = Form(...), usuario_logado: Optional[str] = Cookie(None)):
    if not usuario_logado:
        return responses.RedirectResponse(url="/login", status_code=303)
    adicionar_ao_carrinho(usuario_logado, id_produto)
    return responses.RedirectResponse(url="/", status_code=303)

@app.get("/carrinho")
async def pagina_carrinho(request: Request, usuario_logado: Optional[str] = Cookie(None)):
    if not usuario_logado:
        return responses.RedirectResponse(url="/login", status_code=303)
    itens = consultar_carrinho(usuario_logado)
    total = sum(i['preco'] for i in itens)
    return paginas.TemplateResponse(request=request, name="carrinho.html", context={"request": request, "usuario": usuario_logado, "itens": itens, "total": total})

# --- PAGAMENTO (ITEM 6) ---
@app.get("/pagamento")
async def pagina_pagamento(request: Request, usuario_logado: Optional[str] = Cookie(None)):
    if not usuario_logado:
        return responses.RedirectResponse(url="/login", status_code=303)
    itens = consultar_carrinho(usuario_logado)
    total = sum(i['preco'] for i in itens)
    return paginas.TemplateResponse(request=request, name="pagamento.html", context={"request": request, "usuario": usuario_logado, "total": total})

@app.post("/pagamento")
async def processar_pagamento(usuario_logado: Optional[str] = Cookie(None)):
    if usuario_logado:
        finalizar_compra(usuario_logado) # Transfere os produtos para o histórico e limpa o carrinho
    return responses.RedirectResponse(url="/historico", status_code=303)

# --- HISTÓRICO DE PEDIDOS (ITEM 7) ---
@app.get("/historico")
async def pagina_historico(request: Request, usuario_logado: Optional[str] = Cookie(None)):
    if not usuario_logado:
        return responses.RedirectResponse(url="/login", status_code=303)
    compras = consultar_historico(usuario_logado)
    return paginas.TemplateResponse(request=request, name="historico.html", context={"request": request, "usuario": usuario_logado, "compras": compras})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)