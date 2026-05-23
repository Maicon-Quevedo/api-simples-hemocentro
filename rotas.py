from flask import Flask, request, jsonify
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def carregar(arq):
    with open(arq , 'r') as f:
        return json.load(f)
    
def salvar(arq, dados):
    with open(arq, 'w') as f:
        json.dump(dados, f, indent=4)

@app.get('/doadores/cpf/<cpf>') 
def get_doadores_por_cpf(cpf):
    doadores =carregar('doadores.json')

    for doador in doadores["doadores"]:
        if doador.get('cpf') == cpf:
            return jsonify(doador), 200
    return jsonify({"mensagem": "doador não encontrado"}), 404

@app.get('/doadores/id/<id>') 
def get_doadores_por_id(id):
    doadores =carregar('doadores.json')
    id=int(id)
    for doador in doadores["doadores"]:
        if doador.get('id') == id:
            return jsonify(doador), 200
    return jsonify({"mensagem": "doador não encontrado"}), 404

@app.get('/bolsas/id/<id>')
def get_bolsas_por_id(id):
    bolsas =carregar('bolsas_sangues.json')
    id=int(id)
    for bolsa in bolsas["bolsas_sangues"]:
        if bolsa.get('id') == id:
            return jsonify(bolsa), 200
    return jsonify({"mensagem": "bolsa não encontrado"}), 404

@app.put('/bolsas/<int:id>')
def atualizar(id):
    bolsas = carregar('bolsas_sangues.json')
    dados = request.json
    for bolsa in bolsas["bolsas_sangues"]:
        if bolsa.get('id') == id:
            bolsa.update(dados)
            salvar('bolsas_sangues.json', bolsas)
            return jsonify({"mensagem": "ok"}), 200
    return jsonify({"mensagem": "não encontrado"}), 404

@app.post('/login')
def login():
    dados=request.json
    email=dados.get('email')
    senha=dados.get('senha')

    campos_obrigatorios = ['email', 'senha']
    for campo in campos_obrigatorios: 
        if not dados.get(campo): 
            return jsonify({"mensagem": f"o campo '{campo}' é obrigatorio"}), 400
        
    campos_string = ['email', 'senha']
    for campo in campos_string:
        verificar=dados.get(campo)
        if not isinstance(verificar, str):
            return jsonify({"mensagem": f"o campo '{campo}' é do tipo string"}), 400

    with open('usuarios.json', 'r') as f:
        usuarios = json.load(f)

    usuario=next((u for u in usuarios["usuarios"] if u["email"]==email and u["senha"]==senha), None)

    if not usuario:
        return jsonify({"mensagem": "email ou senha incorretos"}), 401

    return jsonify({
        "mensagem": "login realizado com sucesso!",
        "nome": usuario["nome"],
        "tipo_sanguineo": usuario["tipo_sanguineo"]
    }), 200

@app.post('/bolsas')
def criar_bolsa():
    dados=request.json

    campos_obrigatorios = ['id', 'tipo_sanguineo', 'quantidade', 'volume_ml', 'volume_total_ml', 'local_armazenamento', 'status', 'temperatura']
    for campo in campos_obrigatorios:
        if not dados.get(campo):
            return jsonify({"mensagem": f"o campo '{campo}' é obrigatorio"}), 400
        
    campos_string = ['tipo_sanguineo', 'local_armazenamento', 'status']
    for campo in campos_string:
        verificar=dados.get(campo)
        if not isinstance(verificar, str):
            return jsonify({"mensagem": f"o campo '{campo}' é do tipo string"}), 400
        
    campos_inteiro = ['id', 'quantidade', 'volume_ml', 'volume_total_ml']
    for campo in campos_inteiro:
        verificar=dados.get(campo)
        if not isinstance(verificar, int):
            return jsonify({"mensagem": f"o campo '{campo}' é do tipo inteiro"}), 400

    if not dados.get('tipo_sanguineo'):
        return jsonify({"mensagem": "Campo tipo obrigatorio"}), 400

    with open('bolsas_sangues.json', 'r') as f:
        bolsas = json.load(f)

    bolsas["bolsas_sangues"].append(dados)

    with open('bolsas_sangues.json', 'w') as f:
        json.dump(bolsas, f, indent=4)

    resposta = {
        "mensagem": "Bolsa cadastrada com sucesso!"
    }

    return jsonify(resposta), 201

@app.get("/bolsas")
def buscar_bolsas():
    with open("bolsas_sangues.json", "r") as f:
        dados=json.load(f)
    bolsas=dados["bolsas_sangues"]
    resposta=[]
    for bolsa in bolsas:
        resposta.append({
            "Tipo Sanguineo": bolsa["tipo_sanguineo"],
            "Quantidade ": bolsa["quantidade"],
            "Volume Total": f'{bolsa["volume_total_ml"]}ml',
            "Local armazenado": bolsa["local_armazenamento"],
            "Temperatura de Armazenamento": f'{bolsa["temperatura"]}ºC',
            "Status": bolsa["status"]
        })
    return jsonify(resposta)

@app.get("/bolsas/<tipo>")
def BolsasPorTipo(tipo):
    with open("bolsas_sangues.json", "r") as f:
        dados = json.load(f)
    bolsas = dados["bolsas_sangues"]
    for bolsa in bolsas:
        if bolsa["tipo_sanguineo"]==tipo:
            return jsonify(bolsa), 200
    return jsonify({"erro": "tipo sanguíneo não encontrado"}), 404

@app.post('/doadores')
def criar_doador():
    dados = request.json

    campos_obrigatorios = ['id', 'nome', 'cpf', 'idade', 'peso', 'altura', 'genero', 'tipo_sanguineo', 'cidade', 'telefone']
    for campo in campos_obrigatorios:
        if not dados.get(campo):
            return jsonify({"mensagem": f"o campo '{campo}' é obrigatorio"}), 400
    
    campos_string = ['nome', 'cpf', 'genero', 'tipo_sanguineo', 'cidade', 'telefone']
    for campo in campos_string:
        verificar=dados.get(campo)
        if not isinstance(verificar, str):
            return jsonify({"mensagem": f"o campo '{campo}' é do tipo string"}), 400

    campos_inteiros = ['id', 'idade']
    for campo in campos_inteiros:
        verificar=dados.get(campo)
        if not isinstance(verificar, int):
            return jsonify({"mensagem": f"o campo '{campo}' é do tipo inteiro"}), 400

    campos_float = ['peso', 'altura']
    for campo in campos_float:
        verificar=dados.get(campo)
        if not isinstance(verificar, float):
            return jsonify({"mensagem": f"o campo '{campo}' é do tipo float"}), 400

    with open('doadores.json', 'r') as f:
        doadores = json.load(f)
    
    doadores["doadores"].append(dados)

    with open('doadores.json', 'w') as f:
        json.dump(doadores, f, indent=4)

    resposta = {
        "mensagem": "doador cadastrado com sucesso!"
    }

    return jsonify(resposta), 201

@app.get("/doadores")
def listar_doadores():
    with open("doadores.json", "r") as f:
        dados=json.load(f)
    doadores=dados["doadores"]
    resposta=[]
    for doador in doadores:
        resposta.append({
            "Nome": doador["nome"],
            "Tipo Sanguineo": doador["tipo_sanguineo"],
            "Idade ": doador["idade"],
            "Peso": f'{doador["peso"]}kg',
            "Altura": f'{doador["altura"]}m',
            "Genero": doador["genero"],
            "Cidade": doador["cidade"],
            "Contato": doador["telefone"]
        })
    return jsonify(resposta)

@app.get("/doadores/<tiposangue>")
def buscar_doador_tiposangue(tiposangue):
    tiposangue = tiposangue.replace(' ', '+')
    with open("doadores.json", "r") as f:
        dados=json.load(f)

    doadores =[d for d in dados["doadores"] if d["tipo_sanguineo"]==tiposangue]
    
    if not doadores:
        return jsonify({"mensagem": "Esse tipo sanguineo nao existe, ou não há doadores desse tipo"}), 404
    
    resposta = []
    for doador in doadores:
        resposta.append({
            "Nome": doador["nome"],
            "Tipo Sanguineo": doador["tipo_sanguineo"],
            "Idade": doador["idade"],
            "Peso": f'{doador["peso"]}kg',
            "Altura": f'{doador["altura"]}m',
            "Genero": doador["genero"],
            "Cidade": doador["cidade"],
            "Contato": doador["telefone"]
        })
    return jsonify(resposta), 200

app.run(debug=True)