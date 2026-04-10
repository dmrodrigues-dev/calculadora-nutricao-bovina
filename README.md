# 🐄 Calculadora de Nutrição Bovina

Ferramenta desenvolvida em Python para calcular a necessidade diária de matéria seca e o custo de alimentação de bovinos, com base no peso e categoria do animal. Suporta seleção de um ou dois ingredientes, com balanceamento automático de proteína pelo método do Quadrado de Pearson.

## 💡 Motivação

Projeto desenvolvido para unir conhecimento em Medicina Veterinária com programação em Python, aplicando conceitos reais de nutrição animal em uma ferramenta prática para o agronegócio.

## ⚙️ Funcionalidades

- Histórico automático de cálculos salvo em CSV para consulta posterior
- Consulta de histórico pelo menu principal
- Possibilidade de cadastro de novos ingredientes no banco de ingredientes
- Banco de ingredientes salvo em CSV com 5 ingredientes padrões
- Seleção de categoria animal (bezerro, novilha, vaca em lactação, vaca seca, touro)
- Cálculo da necessidade diária de matéria seca com base no peso vivo
- Suporte a **1 ou 2 ingredientes** por cálculo
- Balanceamento automático de proteína pelo **Quadrado de Pearson** quando dois ingredientes são combinados
- Seleção automática do ingrediente mais econômico quando ambos atendem à exigência proteica
- Fallback automático para o ingrediente mais proteico quando nenhum atende à exigência mínima
- Estimativa de custo diário e mensal
- Alerta quando a dieta não atinge a exigência proteica mínima da categoria
- Registro de dados (data, categoria, peso, ingrediente 1, Kg ingrediente 1, ingrediente 2, Kg ingrediente 2, matéria seca/dia, custo diário, custo mensal e atende proteína) como nova linha no arquivo "arquivo.csv"

## 🐾 Categorias suportadas

| Categoria | % Matéria Seca | Proteína mínima |
|---|---|---|
| Bezerro (até 6 meses) | 3,0% | 16% |
| Novilha (7–18 meses) | 2,5% | 14% |
| Vaca em lactação | 3,5% | 18% |
| Vaca seca | 2,0% | 12% |
| Touro | 2,2% | 13% |

## 🌾 Alimentos padrões

| Alimento | Proteína (%) | Preço (R$/kg) |
|---|---|---|
| Milho grão | 8,5% | R$ 1,20 |
| Farelo de soja | 45,0% | R$ 3,50 |
| Silagem de milho | 7,0% | R$ 0,35 |
| Feno de tifton | 10,0% | R$ 1,80 |
| Capim-elefante | 9,0% | R$ 0,25 |

## 🔬 Método: Quadrado de Pearson

Quando dois ingredientes são selecionados com proteínas em lados opostos da exigência mínima, o programa utiliza o **Quadrado de Pearson** para calcular as proporções exatas de cada um, garantindo que a mistura atinja precisamente o nível proteico necessário.

```
     45% (farelo de soja)
          \    → 18 - 7 = 11 partes de farelo
    18%    ×
          /    → 45 - 18 = 27 partes de silagem
      7% (silagem de milho)
```

## 🚀 Como usar

**Pré-requisito:** Python 3.7 ou superior instalado.

```bash
# Clone o repositório
git clone https://github.com/dmrodrigues-dev/calculadora-nutricao-bovina.git

# Acesse a pasta
cd calculadora-nutricao-bovina

# Instale as bibliotecas do requirements.txt
pip install -r requirements.txt

# Execute o programa
python calculadora.py
```

## 📋 Exemplo de uso

```
=============================================
  🐄 CALCULADORA DE NUTRIÇÃO BOVINA
  Desenvolvido por: Davi Matos Rodrigues
=============================================
arquivo.csv não encontrado, criando arquivo...
Arquivo criado em arquivo.csv
ingredientes.csv não encontrado, criando arquivo...
Arquivo criado em ingredientes.csv

=============================================
  MENU PRINCIPAL
=============================================
  [1] Calcular Ração
  [2] Consultar Histórico
  [3] Cadastrar novo ingrediente
  [4] Sair
=============================================
  Escolha uma opção: 1

=============================================
  CATEGORIA DO ANIMAL
=============================================
  [1] Bezerro (até 6 meses)
  [2] Novilha (7-18 meses)
  [3] Vaca em lactação
  [4] Vaca seca
  [5] Touro
=============================================
  Escolha a categoria: 3
  Informe o peso do animal (kg): 400

=============================================
  TIPO DE ALIMENTO
=============================================
  [1] Milho grão
  [2] Farelo de soja
  [3] Silagem de milho
  [4] Feno de tifton
  [5] Capim-elefante
  [x] Terminar seleção
=============================================
  Escolha o alimento: 1
  Escolha o alimento: 2

=============================================
  RESULTADO DO CÁLCULO
=============================================
  Animal     : Vaca em lactação
  Peso       : 400.0 kg
=============================================
  Matéria seca/dia : 14.00 kg
  Custo diário     : R$ 25.18
  Custo mensal     : R$ 755.42
  Peso de Farelo de soja : KG 3.64
  Peso de Milho grão : KG 10.36
=============================================
  ✅ Atende à exigência proteica mínima
=============================================

  Pressione qualquer tecla para continuar: 

=============================================
  MENU PRINCIPAL
=============================================
  [1] Calcular Ração
  [2] Consultar Histórico
  [3] Cadastrar novo ingrediente
  [4] Sair
=============================================
  Escolha uma opção: 4

=============================================
  Fechando programa...
=============================================
```

## 🛠️ Tecnologias

- Python 3
- Biblioteca pandas

## 📚 Referências técnicas

- Nutrient Requirements of Beef Cattle — NRC
- Tabelas de exigências nutricionais para bovinos — Embrapa
- Método do Quadrado de Pearson para balanceamento de rações

## 👨‍💻 Autor

**Davi Matos Rodrigues**  
Estudante de Medicina Veterinária (UFPI) e ADS (Uninter)  
[GitHub](https://github.com/dmrodrigues-dev) · [LinkedIn](https://www.linkedin.com/in/davi-matos-rodrigues-057430268/)

---

> Projeto em desenvolvimento — novas funcionalidades em breve.