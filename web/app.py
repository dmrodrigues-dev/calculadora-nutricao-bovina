from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
CORS(app)


# CONFIGURANDO SQLITE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calculadoranutricaobovina.db'

# Conexão com o banco
db = SQLAlchemy(app)

# Modelagem de tabelas
class Racao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    categoria = db.Column(db.String(25), nullable=False)
    peso = db.Column(db.Float, nullable=False)
    ingrediente1 = db.Column(db.String(50), nullable=False)
    kgingrediente1 = db.Column(db.Float, nullable=False)
    ingrediente2 = db.Column(db.String(50))
    kgingrediente2 = db.Column(db.Float)
    materiaseca_dia = db.Column(db.Float, nullable=False)
    custodiario = db.Column(db.Float, nullable=False)
    customensal = db.Column(db.Float, nullable=False)
    atendeproteina = db.Column(db.Boolean, nullable=False)

class Ingrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    proteina = db.Column(db.Float, nullable=False)
    preco_kg = db.Column(db.Float, nullable=False)
            
class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(25), nullable=False)
    percentual_ms = db.Column(db.Float, nullable=False)
    proteina_min = db.Column(db.Float, nullable=False)

# ABRINDO TERMINAL FLASK
with app.app_context():
    # Criando tabelas
    db.create_all()

    if Ingrediente.query.count() == 0: # Se não hover ingrediente
        INGREDIENTS = [{"nome": "Milho grão", "proteina": 8.5, "preco_kg": 1.20},
               {"nome": "Farelo de soja", "proteina": 45.0, "preco_kg": 3.50},
               {"nome": "Silagem de milho", "proteina": 7.0, "preco_kg": 0.35},
               {"nome": "Feno de tifton", "proteina": 10.0, "preco_kg": 1.80},
               {"nome": "Capim-elefante", "proteina": 9.0, "preco_kg": 0.25}]
               
        for ingrediente in INGREDIENTS: # Adicione o ingrediente da lista INGREDIENTS no db
            db.session.add(
                Ingrediente(
                    nome=ingrediente['nome'],
                    proteina=ingrediente['proteina'],
                    preco_kg=ingrediente['preco_kg']
                )
            )


    if Categoria.query.count() == 0:# Se não houver categoria
        CATEGORIAS = [{"nome": "Bezerro (até 6 meses)", "percentual_ms": 0.03, "proteina_min": 16},
              {"nome": "Novilha (7-18 meses)", "percentual_ms": 0.025, "proteina_min": 14},
              {"nome": "Vaca em lactação", "percentual_ms": 0.035, "proteina_min": 18},
              {"nome": "Vaca seca", "percentual_ms": 0.02, "proteina_min": 12},
              {"nome": "Touro", "percentual_ms": 0.022, "proteina_min": 13}]
        
        for categoria in CATEGORIAS: # Adicione a categoria da lista CATEGORIAS no db
            db.session.add(
                Categoria(
                    nome=categoria['nome'],
                    percentual_ms=categoria['percentual_ms'],
                    proteina_min=categoria['proteina_min']
                )
            )
              
    db.session.commit()


# Rota para recuperar categorias na base de dados
@app.route('/categorias', methods=['GET'])
def categorias():
    categorias = Categoria.query.all()
    lista_cat = [{'id':cat.id,'nome': cat.nome} for cat in categorias]

    return jsonify(lista_cat)


# Rota para recuperar ingredientes na base de dados
@app.route('/ingredientes', methods=['GET'])
def ingredientes():
    ingredientes = Ingrediente.query.all()
    lista_ing = [{'id': ing.id, 'nome': ing.nome} for ing in ingredientes]

    return jsonify(lista_ing)


# Rota para recuperar rações na base de dados
@app.route('/racoes', methods=['GET'])
def racoes():
    racoes = Racao.query.all()
    lista_rac = [{
        'data': rac.data.strftime('%d/%m/%Y'),
        'categoria': rac.categoria,
        'peso': rac.peso,
        'ingrediente1': rac.ingrediente1,
        'kgingrediente1': rac.kgingrediente1,
        'ingrediente2': rac.ingrediente2,
        'kgingrediente2': rac.kgingrediente2,
        'materiaseca_dia': rac.materiaseca_dia,
        'custodiario': rac.custodiario,
        'customensal': rac.customensal,
        'atendeproteina': rac.atendeproteina
    } for rac in racoes]

    return jsonify(lista_rac)


# Rota para calcular a ração
@app.route('/calcular', methods=['POST'])
def calcular():
    '''
    exemplo = {
    "peso": 400,
    "categoria": "Vaca em lactação",
    "ingredientes": ["Milho grão", "Farelo de soja"]
    }
    '''
    # Buscando dados do request
    dados = request.json

    # Dividindo dados do request
    peso = dados.get('peso')
    categoria = dados.get('categoria')
    ingredientes = dados.get('ingredientes')

    # Validando os dados brutos
    if not peso or not categoria or not ingredientes:
        return jsonify({'message': 'Dados inválidos!'}), 400

    # Ajustando dados
    peso = float(peso)
    categoria = db.session.get(Categoria, categoria)
    ingredientes = Ingrediente.query.filter( Ingrediente.id.in_(ingredientes) ).all()
    # ^-Filtra a tabela Ingrediente e seleciona todos que tenham o id dentro da lista ingredientes

    # Validando dados tratados
    if not (0 < peso < 2000) or not categoria or not (0 < len(ingredientes) < 3):
        return jsonify({'message': 'Dados inválidos!'}), 400
    
    # CALCULO DA RAÇÃO PROPRIAMENTE DITA

    # Definindo necessidades
    necessidade_ms = peso * categoria.percentual_ms
    necessidade_proteina = categoria.proteina_min

    # Se o usuário selecionou 2 ingredientes
    if len(ingredientes) == 2:
        # Separando o mais proteico do menos proteico
        maior_prot = max(ingredientes, key=lambda ing : ing.proteina)
        menor_prot = min(ingredientes, key=lambda ing : ing.proteina)

        # Se a proteina do mais proteico não satisfazer a necessidade
        if maior_prot.proteina < necessidade_proteina:
            custo_diario = maior_prot.preco_kg * necessidade_ms
            atende_proteina = False
            # O ingrediente mais proteico ocupa toda a ração
            peso_ing = [
                    {'nome': maior_prot.nome,
                     'peso': necessidade_ms},
                    {'nome': menor_prot.nome,
                     'peso': 0}
                ]

        # Se a proteina do menos proteico passar da necessidade    
        elif menor_prot.proteina >= necessidade_proteina:
            # Separa o mais caro do mais barato
            caro = max(ingredientes, key=lambda ing : ing.preco_kg)
            barato = min(ingredientes, key=lambda ing : ing.preco_kg)
            custo_diario = barato.preco_kg * necessidade_ms
            atende_proteina = True
            # O ingrediente mais barato ocupa toda a ração
            peso_ing = [
                {'nome': barato.nome,
                 'peso': necessidade_ms},
                {'nome': caro.nome,
                 'peso': 0}
            ]

        # Se um ingrediente passar da necessidade e outro não
        else:
            partes_maior_prot = necessidade_proteina - menor_prot.proteina
            partes_menor_prot = maior_prot.proteina - necessidade_proteina

            maior_prot_kg = necessidade_ms * ( partes_maior_prot / (partes_maior_prot + partes_menor_prot) )
            menor_prot_kg = necessidade_ms * ( partes_menor_prot / (partes_maior_prot + partes_menor_prot) )

            custo_diario = ( maior_prot_kg * maior_prot.preco_kg ) + ( menor_prot_kg * menor_prot.preco_kg )
            atende_proteina = True
            peso_ing = [
                {'nome': maior_prot.nome,
                 'peso': maior_prot_kg},
                {'nome': menor_prot.nome,
                 'peso': menor_prot_kg}
            ]

    # Se o usuário selecionou 1 ingrediente
    else:
        ing = ingredientes[0]
        custo_diario = necessidade_ms * ing.preco_kg
        atende_proteina = ing.proteina >= necessidade_proteina
        peso_ing = [
            {'nome': ing.nome,
             'peso': necessidade_ms}
        ]

    # Definindo custo mensal
    custo_mensal = custo_diario * 30
    
    # Criando e adicionando o objeto Racao com os dados obtidos
    racao = Racao(
        data= date.today(),
        categoria= categoria.nome,
        peso= peso,
        ingrediente1= peso_ing[0]['nome'],
        kgingrediente1= round(peso_ing[0]['peso'], 2),
        ingrediente2= peso_ing[1]["nome"] if len(peso_ing) > 1 else '-',
        kgingrediente2= round(peso_ing[1]['peso'], 2) if len(peso_ing) > 1 else 0,
        materiaseca_dia= round(necessidade_ms, 2),
        custodiario= round(custo_diario, 2),
        customensal= round(custo_mensal, 2),
        atendeproteina= atende_proteina
    )
    db.session.add(racao)
    db.session.commit() # Salvando no banco

    return jsonify({'message': 'Nova raçao adicionada.'})


# Rota para adicionar ingrediente
@app.route('/ingrediente', methods=['POST'])
def ingrediente():
    '''
    Exemplo:
    {
    "nome": "Palma forrageira",
    "proteina": 4.5,
    "preco_kg": 1.5
    }
    '''
    dados = request.json

    if not 'nome' in dados or not 'proteina' in dados or not 'preco_kg' in dados:
        return jsonify({'message': 'Dados inválidos.'}), 400
    
    ingrediente = Ingrediente(
        nome= dados.get('nome'),
        proteina= float(dados.get('proteina')),
        preco_kg= float(dados.get('preco_kg'))
    )
    db.session.add(ingrediente)
    db.session.commit()

    return jsonify({'message': 'Ingrediente adicionado.'})


if __name__ == '__main__':
    app.run(debug=True)
