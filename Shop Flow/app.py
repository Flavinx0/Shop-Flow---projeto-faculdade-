from flask import Flask, render_template, request, redirect, url_for, session
from models.admin import Admin
from models.cliente import Cliente
from models.produto import Produto
from models.pedido import Pedido
from models.carrinho import Carrinho

app = Flask(__name__)
app.secret_key = "shopflow2026"

# ==================== DADOS EM MEMÓRIA ====================

admins = [
    Admin("Administrador", "admin@shopflow.com", "admin123")
]

clientes = []
produtos = [
    Produto(1, "Camiseta Básica", "Camiseta 100% algodão", 49.90, "Roupas", 50),
    Produto(2, "Calça Jeans", "Calça jeans slim fit", 129.90, "Roupas", 30),
    Produto(3, "Tênis Esportivo", "Tênis para corrida", 199.90, "Calçados", 20),
]
pedidos = []
carrinhos = {}

# ==================== ROTAS GERAIS ====================

@app.route("/")
def index():
    return render_template("index.html")

# ==================== ROTAS ADMIN ====================

@app.route("/admin/login", methods=["GET", "POST"])
def login_admin():
    erro = None
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        for admin in admins:
            if admin.get_email() == email and admin.get_senha() == senha:
                session["admin"] = email
                session["tipo"] = "admin"
                return redirect(url_for("dashboard_admin"))
        erro = "Email ou senha incorretos!"
    return render_template("login_admin.html", erro=erro)

@app.route("/admin/dashboard")
def dashboard_admin():
    if "admin" not in session:
        return redirect(url_for("login_admin"))
    admin = next((a for a in admins if a.get_email() == session["admin"]), None)
    return render_template("dashboard_admin.html", admin=admin, menu=admin.exibir_menu())

@app.route("/admin/produtos")
def admin_produtos():
    if "admin" not in session:
        return redirect(url_for("login_admin"))
    return render_template("admin_produtos.html", produtos=produtos)

@app.route("/admin/produtos/novo", methods=["GET", "POST"])
def admin_novo_produto():
    if "admin" not in session:
        return redirect(url_for("login_admin"))
    if request.method == "POST":
        novo_id = len(produtos) + 1
        p = Produto(
            novo_id,
            request.form["nome"],
            request.form["descricao"],
            float(request.form["preco"]),
            request.form["categoria"],
            int(request.form["estoque"])
        )
        produtos.append(p)
        return redirect(url_for("admin_produtos"))
    return render_template("admin_novo_produto.html")

@app.route("/admin/produtos/remover/<int:id>")
def admin_remover_produto(id):
    if "admin" not in session:
        return redirect(url_for("login_admin"))
    global produtos
    produtos = [p for p in produtos if p.get_id() != id]
    return redirect(url_for("admin_produtos"))

@app.route("/admin/pedidos")
def admin_pedidos():
    if "admin" not in session:
        return redirect(url_for("login_admin"))
    return render_template("admin_pedidos.html", pedidos=pedidos)

@app.route("/admin/pedidos/status/<int:id>", methods=["POST"])
def admin_atualizar_status(id):
    if "admin" not in session:
        return redirect(url_for("login_admin"))
    pedido = next((p for p in pedidos if p.get_id() == id), None)
    if pedido:
        pedido.atualizar_status(request.form["status"])
    return redirect(url_for("admin_pedidos"))

@app.route("/admin/admins")
def admin_admins():
    if "admin" not in session:
        return redirect(url_for("login_admin"))
    return render_template("admin_admins.html", admins=admins)

@app.route("/admin/admins/novo", methods=["GET", "POST"])
def admin_novo_admin():
    if "admin" not in session:
        return redirect(url_for("login_admin"))
    erro = None
    if request.method == "POST":
        email = request.form["email"]
        if any(a.get_email() == email for a in admins):
            erro = "Esse email já está cadastrado!"
        else:
            novo = Admin(request.form["nome"], email, request.form["senha"])
            admins.append(novo)
            return redirect(url_for("admin_admins"))
    return render_template("admin_novo_admin.html", erro=erro)

@app.route("/admin/logout")
def logout_admin():
    session.pop("admin", None)
    session.pop("tipo", None)
    return redirect(url_for("login_admin"))

# ==================== ROTAS CLIENTE ====================

@app.route("/cliente/cadastro", methods=["GET", "POST"])
def cadastro_cliente():
    erro = None
    if request.method == "POST":
        email = request.form["email"]
        if any(c.get_email() == email for c in clientes):
            erro = "Esse email já está cadastrado!"
        else:
            novo = Cliente(
                request.form["nome"],
                email,
                request.form["senha"],
                request.form["cpf"],
                request.form["endereco"]
            )
            clientes.append(novo)
            return redirect(url_for("login_cliente"))
    return render_template("cadastro_cliente.html", erro=erro)

@app.route("/cliente/login", methods=["GET", "POST"])
def login_cliente():
    erro = None
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        for cliente in clientes:
            if cliente.get_email() == email and cliente.get_senha() == senha:
                session["cliente"] = email
                session["tipo"] = "cliente"
                return redirect(url_for("dashboard_cliente"))
        erro = "Email ou senha incorretos!"
    return render_template("login_cliente.html", erro=erro)

@app.route("/cliente/dashboard")
def dashboard_cliente():
    if "cliente" not in session:
        return redirect(url_for("login_cliente"))
    cliente = next((c for c in clientes if c.get_email() == session["cliente"]), None)
    return render_template("dashboard_cliente.html", cliente=cliente, menu=cliente.exibir_menu())

@app.route("/cliente/produtos")
def cliente_produtos():
    if "cliente" not in session:
        return redirect(url_for("login_cliente"))
    return render_template("cliente_produtos.html", produtos=produtos)

@app.route("/cliente/carrinho")
def cliente_carrinho():
    if "cliente" not in session:
        return redirect(url_for("login_cliente"))
    email = session["cliente"]
    carrinho = carrinhos.get(email, None)
    dados = carrinho.to_dict() if carrinho else {"itens": [], "total": 0}
    return render_template("cliente_carrinho.html", carrinho=dados)

@app.route("/cliente/carrinho/adicionar/<int:id>")
def adicionar_carrinho(id):
    if "cliente" not in session:
        return redirect(url_for("login_cliente"))
    email = session["cliente"]
    cliente = next((c for c in clientes if c.get_email() == email), None)
    produto = next((p for p in produtos if p.get_id() == id), None)
    if email not in carrinhos:
        carrinhos[email] = Carrinho(cliente)
    carrinhos[email].adicionar_item(produto)
    return redirect(url_for("cliente_carrinho"))

@app.route("/cliente/carrinho/remover/<int:id>")
def remover_carrinho(id):
    if "cliente" not in session:
        return redirect(url_for("login_cliente"))
    email = session["cliente"]
    if email in carrinhos:
        carrinhos[email].remover_item(id)
    return redirect(url_for("cliente_carrinho"))

@app.route("/cliente/finalizar", methods=["POST"])
def finalizar_pedido():
    if "cliente" not in session:
        return redirect(url_for("login_cliente"))
    email = session["cliente"]
    cliente = next((c for c in clientes if c.get_email() == email), None)
    carrinho = carrinhos.get(email)
    if not carrinho or carrinho.esta_vazio():
        return redirect(url_for("cliente_carrinho"))
    pedido = Pedido(cliente)
    for item in carrinho.get_itens().values():
        pedido.adicionar_item(item["produto"], item["quantidade"])
    pedidos.append(pedido)
    carrinhos[email].limpar()
    return redirect(url_for("cliente_pedidos"))

@app.route("/cliente/pedidos")
def cliente_pedidos():
    if "cliente" not in session:
        return redirect(url_for("login_cliente"))
    email = session["cliente"]
    meus_pedidos = [p for p in pedidos if p.get_cliente().get_email() == email]
    return render_template("cliente_pedidos.html", pedidos=meus_pedidos)

@app.route("/cliente/logout")
def logout_cliente():
    session.pop("cliente", None)
    session.pop("tipo", None)
    return redirect(url_for("login_cliente"))

# ==================== INICIAR SERVIDOR ====================

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000, use_reloader=False)