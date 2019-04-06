var el = x => document.getElementById(x);

function showPicker(inputId) { el('file-input').click(); }

function showPicked(input) {
    el('upload-label').innerHTML = input.files[0].name;
    var reader = new FileReader();
    reader.onload = function (e) {
        el('image-picked').src = e.target.result;
        el('image-picked').className = '';
    }
    reader.readAsDataURL(input.files[0]);
}

function chooseClass(clazz, img_id){
    el('analyze-button').innerHTML = 'Reporting...';
    var xhr = new XMLHttpRequest();
    var loc = window.location
    xhr.open('POST', `${loc.protocol}//${loc.hostname}:${loc.port}/report`, true);
	xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onerror = function() {alert (xhr.responseText);}
    xhr.onload = function(e) {
        el('analyze-button').innerHTML = 'Analyze';
		el('result-buttons').style.visibility = "hidden";
    }

	var report = {
		'img_id' : img_id,
		'class' : clazz
	}
    xhr.send(JSON.stringify(report));
}

function createButtons(response){
	buttons = '';
	for (const clazz of response.classes){
        buttons += `<button class='choose-class-button' type='button'
			onclick='chooseClass("${clazz}", "${response.img_id}")'>${clazz}</button>`
	}
	return buttons;
}

function analyze() {
    var uploadFiles = el('file-input').files;
    if (uploadFiles.length != 1) alert('Please select 1 file to analyze!');

    el('analyze-button').innerHTML = 'Analyzing...';
    var xhr = new XMLHttpRequest();
    var loc = window.location
    xhr.open('POST', `${loc.protocol}//${loc.hostname}:${loc.port}/analyze`, true);
    xhr.onerror = function() {alert (xhr.responseText);}
    xhr.onload = function(e) {
        if (this.readyState === 4) {
            var response = JSON.parse(e.target.responseText);
            el('result-label').innerHTML = `Result = ${response['result']}`;
			el('result-buttons').innerHTML = createButtons(response);
			el('result-buttons').style.visibility = 'visible';
        }
        el('analyze-button').innerHTML = 'Analyze';
    }

    var fileData = new FormData();
    fileData.append('file', uploadFiles[0]);
    xhr.send(fileData);
}

