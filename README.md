# 🐄 Calculadora de Nutrição Bovina

Ferramenta desenvolvida em Python para calcular a necessidade diária de matéria seca e o custo de alimentação de bovinos, com base no peso e categoria do animal. Suporta seleção de um ou dois ingredientes, com balanceamento automático de proteína pelo método do Quadrado de Pearson.

## 💡 Motivação

Projeto desenvolvido para unir conhecimento em Medicina Veterinária com programação em Python, aplicando conceitos reais de nutrição animal em uma ferramenta prática para o agronegócio.

## ⚙️ Funcionalidades

- Seleção de categoria animal (bezerro, novilha, vaca em lactação, vaca seca, touro)
- Cálculo da necessidade diária de matéria seca com base no peso vivo
- Suporte a **1 ou 2 ingredientes** por cálculo
- Balanceamento automático de proteína pelo **Quadrado de Pearson** quando dois ingredientes são combinados
- Seleção automática do ingrediente mais econômico quando ambos atendem à exigência proteica
- Fallback automático para o ingrediente mais proteico quando nenhum atende à exigência mínima
- Estimativa de custo diário e mensal
- Alerta quando a dieta não atinge a exigência proteica mínima da categoria

## 🐾 Categorias suportadas

| Categoria | % Matéria Seca | Proteína mínima |
|---|---|---|
| Bezerro (até 6 meses) | 3,0% | 16% |
| Novilha (7–18 meses) | 2,5% | 14% |
| Vaca em lactação | 3,5% | 18% |
| Vaca seca | 2,0% | 12% |
| Touro | 2,2% | 13% |

## 🌾 Alimentos disponíveis

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

# Execute o programa
python calculadora.py
```

## 📋 Exemplo de uso

```
=============================================
  🐄 CALCULADORA DE NUTRIÇÃO BOVINA
  Desenvolvido por: Davi Matos Rodrigues
=============================================

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

  Informe o peso do animal (kg): 550

=============================================
  TIPO DE ALIMENTO
=============================================
  [1] Milho grão
  [2] Farelo de soja
  [3] Silagem de milho
  [4] Feno de tifton
  [5] Capim-elefante
  [0] Finalizar seleção
=============================================
  Escolha o alimento: 2
  Escolha o alimento: 3

=============================================
  RESULTADO DO CÁLCULO
=============================================
  Animal     : Vaca em lactação
  Peso       : 550.0 kg
=============================================
  Matéria seca/dia : 19.25 kg
  Custo diário     : R$ 24.29
  Custo mensal     : R$ 728.71
  Peso de Farelo de soja : KG 5.57
  Peso de Silagem de milho : KG 13.68
=============================================
  ✅ Atende à exigência proteica mínima
=============================================
```

## 🛠️ Tecnologias

- Python 3 (sem dependências externas)

## 📚 Referências técnicas

- Nutrient Requirements of Beef Cattle — NRC
- Tabelas de exigências nutricionais para bovinos — Embrapa
- Método do Quadrado de Pearson para balanceamento de rações

## 👨‍💻 Autor

**Davi Matos Rodrigues**  
Estudante de Medicina Veterinária (UFPI) e ADS (Uninter)  
[GitHub](https://github.com/dmrodrigues-dev) · [LinkedIn](https://linkedin.com/in/seu-perfil)

---

> Projeto em desenvolvimento — novas funcionalidades em breve.