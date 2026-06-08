function calcular(event) {
    event.preventDefault()

    const peso = document.getElementById('peso').value
    let categoria = document.querySelector('input[name="cat"]:checked')
    if (!categoria) {
            alert('Selcione uma categoria!')
            return
        }
    categoria = categoria.value
    let ingredientes = document.querySelectorAll('input[type="checkbox"]:checked')
    ingredientes = Array.from(ingredientes).map(checkbox => checkbox.value)
    if (ingredientes.length === 0) {
        alert('Selecione pelo menos um ingrediente')
        return
    }

    if (ingredientes.length > 2) {
        alert('Selecione no máximo dois ingredientes')
        return
    }


    fetch("http://localhost:5000/calcular", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            peso: peso,
            categoria: categoria,
            ingredientes: ingredientes

        })
    })
    .then(resposta => {
        if (!resposta.ok) {
            throw new Error('Erro ao calcular ração.');
        }
        return resposta.json()
    })
    .then(dados => {
        alert(dados.message)
        carregar_racoes()


    })
    .catch(erro => {
        alert(erro.message)
    })

}

function abrir_modal() {
    document.getElementById('modal-ingrediente').style.display = 'block'
}

function fechar_modal() {
    document.getElementById('modal-ingrediente').style.display = 'none'
}

function carregar_radios() {
    let div = document.getElementById('lista-categorias')
    div.innerHTML = ''
    
    fetch("http://localhost:5000/categorias",{
        method: "GET",
        headers: {'Content-Type': 'application/json'}
    })
    .then(resposta => {
        if (!resposta.ok) {
            throw new Error('Erro ao recuperar categorias')
        }
        return resposta.json()
    })
    .then(dados => {
        for (let categoria of dados) {

            let radio = document.createElement('label')
            radio.innerHTML = `<input type="radio" name="cat" class="categoria" value=${categoria.id}>${categoria.nome}`
            div.appendChild(radio)

        }
    })
}

function carregar_checkboxes() {
    let div = document.getElementById('lista-ingredientes')
    div.innerHTML = ''

    fetch("http://localhost:5000/ingredientes", {
        method: 'GET',
        headers: {'Content-Type': 'application/json'}
    })
    .then(resposta => {
        if (!resposta.ok) {
            throw new Error('Erro ao recuperar ingredientes')
        }
        return resposta.json()
    })
    .then(dados => {
        for (let ingrediente of dados) {

            let checkbox = document.createElement('label')
            checkbox.innerHTML = `<input type="checkbox" name="ingredientes" class="ingredientes" value=${ingrediente.id}>${ingrediente.nome}`
            div.appendChild(checkbox)

        }
    })

}

function carregar_racoes() {
    let tabela = document.getElementById('historico')
    tabela.innerHTML = `
        <tr>
            <th>Data</th>
            <th>Categoria</th>
            <th>Peso</th>
            <th>Ing. 1</th>
            <th>Kg Ing. 1</th>
            <th>Ing. 2</th>
            <th>Kg Ing. 2</th>
            <th>MS/Dia</th>
            <th>Custo Dia</th>
            <th>Custo Mês</th>
            <th>Atende PB</th>
        </tr>`

    fetch("http://localhost:5000/racoes", {
        method: 'GET',
        headers: {'Content-Type': 'application/json'}
    })
    .then(resposta => {
        if (!resposta.ok) {
            throw new Error('Erro ao recuperar rações')
        }
        return resposta.json()
    })
    .then(dados => {
        for (let racao of dados) {

            let linha = document.createElement('tr')
            linha.innerHTML = `
                <td>${racao.data}</td>
                <td>${racao.categoria}</td>
                <td>${racao.peso}</td>
                <td>${racao.ingrediente1}</td>
                <td>${racao.kgingrediente1}</td>
                <td>${racao.ingrediente2}</td>
                <td>${racao.kgingrediente2}</td>
                <td>${racao.materiaseca_dia}</td>
                <td>${racao.custodiario}</td>
                <td>${racao.customensal}</td>
                <td>${racao.atendeproteina ? 'Sim' : 'Não'}</td>
            `
            tabela.appendChild(linha)
        }
    })
}

function ingrediente() {
    const nome = document.getElementById('novo-nome').value
    const proteina = parseFloat(document.getElementById('nova-proteina').value)
    const preco = parseFloat(document.getElementById('novo-preco').value)

    if (!nome || isNaN(proteina) || isNaN(preco)) {
        alert('Preencha todos os campos!')
        return
    }

    fetch("http://localhost:5000/ingrediente", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            nome: nome,
            proteina: proteina,
            preco_kg: preco
        })

    })
    .then(resposta => {
        if (!resposta.ok) {
            throw new Error('Erro ao abir modal.')
        }
        return resposta.json()
    })
    .then(dados => {
        alert(dados.message)

        fechar_modal()

        carregar_checkboxes()
    })
    .catch(erro => {
        alert(erro.message)
    })

}


document.addEventListener('DOMContentLoaded', carregar_radios)
document.addEventListener('DOMContentLoaded', carregar_checkboxes)
document.addEventListener('DOMContentLoaded', carregar_racoes)