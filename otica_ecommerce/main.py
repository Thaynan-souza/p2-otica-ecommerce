from fastapi import FastAPI, Request, Form, responses, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from typing import Optional

from banco import (
    consultar_produtos, cadastrar_usuario, verificar_login, 
    adicionar_ao_carrinho, atualizar_quantidade, remover_do_carrinho, 
    esvaziar_carrinho, consultar_carrinho, finalizar_compra, consultar_historico
)

app = FastAPI(title="Ótica E-commerce")
app.mount("/static", StaticFiles(directory="static"), name="static")
paginas = Jinja2Templates(directory="paginas")

@app.get("/")
async def index(request: Request, usuario_logado: Optional[str] = Cookie(None)):
    produtos_bd = consultar_produtos()
    qtd_carrinho = len(consultar_carrinho(usuario_logado)) if usuario_logado else 0
    return paginas.TemplateResponse(request=request, name="index.html", context={"request": request, "produtos": produtos_bd, "usuario": usuario_logado, "qtd_carrinho": qtd_carrinho})

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

# --- ROTAS DO CARRINHO ---
@app.post("/adicionar")
async def adicionar_item(id_produto: int = Form(...), usuario_logado: Optional[str] = Cookie(None)):
    if not usuario_logado: return responses.RedirectResponse(url="/login", status_code=303)
    adicionar_ao_carrinho(usuario_logado, id_produto)
    return responses.RedirectResponse(url="/", status_code=303)

@app.get("/carrinho")
async def pagina_carrinho(request: Request, usuario_logado: Optional[str] = Cookie(None)):
    if not usuario_logado: return responses.RedirectResponse(url="/login", status_code=303)
    itens = consultar_carrinho(usuario_logado)
    total = sum(i['preco'] * i['quantidade'] for i in itens)
    return paginas.TemplateResponse(request=request, name="carrinho.html", context={"request": request, "usuario": usuario_logado, "itens": itens, "total": total})

@app.post("/carrinho/atualizar")
async def atualizar_carrinho(id_item: int = Form(...), acao: str = Form(...), usuario_logado: Optional[str] = Cookie(None)):
    if usuario_logado: atualizar_quantidade(id_item, acao)
    return responses.RedirectResponse(url="/carrinho", status_code=303)

@app.post("/carrinho/remover")
async def remover_carrinho(id_item: int = Form(...), usuario_logado: Optional[str] = Cookie(None)):
    if usuario_logado: remover_do_carrinho(id_item)
    return responses.RedirectResponse(url="/carrinho", status_code=303)

@app.post("/carrinho/esvaziar")
async def esvaziar(usuario_logado: Optional[str] = Cookie(None)):
    if usuario_logado: esvaziar_carrinho(usuario_logado)
    return responses.RedirectResponse(url="/carrinho", status_code=303)

# --- PAGAMENTO E HISTÓRICO ---
@app.get("/pagamento")
async def pagina_pagamento(request: Request, usuario_logado: Optional[str] = Cookie(None)):
    if not usuario_logado: return responses.RedirectResponse(url="/login", status_code=303)
    itens = consultar_carrinho(usuario_logado)
    total = sum(i['preco'] * i['quantidade'] for i in itens)
    return paginas.TemplateResponse(request=request, name="pagamento.html", context={"request": request, "usuario": usuario_logado, "total": total})

@app.post("/pagamento")
async def processar_pagamento(usuario_logado: Optional[str] = Cookie(None)):
    if usuario_logado: finalizar_compra(usuario_logado)
    return responses.RedirectResponse(url="/historico", status_code=303)

@app.get("/historico")
async def pagina_historico(request: Request, usuario_logado: Optional[str] = Cookie(None)):
    if not usuario_logado: return responses.RedirectResponse(url="/login", status_code=303)
    compras = consultar_historico(usuario_logado)
    return paginas.TemplateResponse(request=request, name="historico.html", context={"request": request, "usuario": usuario_logado, "compras": compras})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)