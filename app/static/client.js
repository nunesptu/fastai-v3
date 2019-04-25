var el = x => document.getElementById(x);

function create_table(response){

    var result = response['classe']

    var rows = ""
    response["probs"].forEach(tuple => {
        var clazz = tuple[0]
        var percent = parseFloat(tuple[1] * 100 ).toFixed(4)+"%"
        var css = ''

        if (clazz === result){
            css = 'class=result'
        }

        rows += `<tr ${css}><td>${clazz}</td><td>${percent}</td></tr>\n`
    })

    return `<table class='center'><thead><tr><td>Classe</td><td>Probabilidade</td></tr></thead><tbody>${rows}</tbody></table>`
}

function analyze() {
    el('analyze-button').innerHTML = 'Analisando...';
    var xhr = new XMLHttpRequest();
    var loc = window.location;
    xhr.open('POST', `${loc.protocol}//${loc.hostname}:${loc.port}/analyze`, true);
    xhr.onerror = function() {alert (xhr.responseText);}
    xhr.onload = function(e) {
        if (this.readyState === 4) {
            var response = JSON.parse(e.target.responseText);
            el('result-label').innerHTML = create_table(response);
        }
        el('analyze-button').innerHTML = 'Analisar';
    }

    var formData = new FormData();
    formData.append('input_text', el('input_text').value);
    xhr.send(formData);
}

