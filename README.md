# 👓 Ótica Visão Clara - E-commerce

Este é um projeto completo de E-commerce para uma ótica, desenvolvido com **Python (FastAPI)** no backend, **MariaDB/MySQL** como banco de dados e renderização de páginas no servidor com **Jinja2**.

O sistema permite o cadastro de usuários com criptografia de senhas, navegação na vitrine de produtos, gestão completa de carrinho de compras (com verificação de estoque) e simulação de checkout financeiro.

---

## 🚀 Funcionalidades Principais

* **Catálogo de Produtos:** Vitrine dinâmica consumindo dados em tempo real do banco de dados.
* **Autenticação Segura:** Login e registro de usuários com senhas criptografadas nativamente via `bcrypt`.
* **Carrinho de Compras:** Adição, remoção, alteração de quantidades e esvaziamento total, com validação inteligente de estoque.
* **Checkout Simulado:** Tela de pagamento com opções de Pix, Boleto e Cartão de Crédito.
* **Gestão de Estoque:** Baixa automática de produtos no banco após finalização da compra.
* **Histórico de Compras:** Painel individual para o usuário consultar seus pedidos anteriores.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3.x, FastAPI, Uvicorn
* **Frontend:** HTML5, CSS3 Modular (sem uso de frameworks), Jinja2 Templates
* **Banco de Dados:** MariaDB / MySQL (Driver: `mysql-connector-python`)
* **Segurança:** Bcrypt (Hashing de senhas)

---

## ⚙️ Pré-requisitos e Instalação

Para rodar este projeto em ambiente de desenvolvimento CODESPACE, siga as instruções abaixo:

1. Verifique se o Banco de Dados está rodando
O Codespaces não inicia o MySQL/MariaDB automaticamente a cada abertura.

No terminal do VS Code, digite:

sudo service mariadb start

Se aparecer uma mensagem confirmando que o serviço iniciou, estamos prontos.

2. Certifique-se de que as dependências estão instaladas

Como o Codespaces pode recriar o ambiente, é bom garantir que as bibliotecas necessárias estão lá:

pip install fastapi uvicorn jinja2 mysql-connector-python bcrypt python-multipart

3. Suba o servidor

Agora, basta rodar o comando:

cd otica_ecommerce python -m uvicorn main:app --reload

Para rodar este projeto na sua máquina local ou ambiente de desenvolvimento, siga as instruções abaixo:

### Clonar o repositório
```
git clone [https://github.com/SeuUsuario/p2-otica-ecommerce.git](https://github.com/SeuUsuario/p2-otica-ecommerce.git)
cd p2-otica-ecommerce/otica_ecommerce

2. Instalar as dependências do Python
O projeto exige algumas bibliotecas externas para rodar o servidor, conectar ao banco e processar formulários. Execute o comando abaixo no seu terminal:


pip install fastapi uvicorn jinja2 mysql-connector-python bcrypt python-multipart

3. Configurar o Banco de Dados
Certifique-se de ter um servidor MySQL ou MariaDB rodando na sua máquina.

Execute o script SQL (fornecido junto ao projeto) no  gerenciador de banco de dados (ex: SQLTools, DBeaver, phpMyAdmin) para criar o banco otica_bd, as tabelas produto, usuario, carrinho, pedido e popular os produtos iniciais.

Abra o arquivo banco.py e verifique se as credenciais de conexão batem com o seu ambiente local:

# No arquivo banco.py:
conexao = mysql.connector.connect(
    host='localhost', 
    user='root',       # Altere se necessário
    password='root',   # Altere se necessário
    database='otica_bd', 
    port='3306'
)

▶️ Como Executar a Aplicação
Com as dependências instaladas e o banco configurado, inicie o servidor web com o Uvicorn executando o comando abaixo no terminal:


python -m uvicorn main:app --reload

O servidor estará rodando no endereço local: http://127.0.0.1:8000. Basta abrir este link no seu navegador para acessar a loja!

📁 Estrutura do Projeto

otica_ecommerce/
├── main.py          # Arquivo principal (Rotas da API e FastAPI)
├── banco.py         # Funções de Banco de Dados e Criptografia (Bcrypt)
├── static/          # Arquivos CSS modulares
│   ├── index.css
│   ├── carrinho.css
│   ├── pagamento.css
│   ├── login.css
│   └── historico.css
└── paginas/         # Templates HTML (Jinja2)
    ├── index.html
    ├── carrinho.html
    ├── pagamento.html
    ├── login.html
    └── historico.html
