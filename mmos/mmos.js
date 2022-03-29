function loadSlider(maxNumberItems){
    
    let slider = document.getElementById('slider');
    
    noUiSlider.create(slider, {
        connect: true,
        start: [0,1000],
        range: {
            'min': 0,
            'max': maxNumberItems,
        },
        step: 1,
        behaviour: 'tap-drag',
        tooltips: true,
    
    });

}

function localtime(){
    let currentDate = Date();

    alert(currentDate);
}

function loadTemplate(template_id, data) {
    var template = document.getElementById(template_id).innerHTML;
    return eval('`' + template + '`');
}

function load_mmo(json) {
    let data = json.data;
    
    let html = "";

    loadSlider(json.data.length);
    data.forEach(function(value,key){
        html += loadTemplate("mmo_template", data[key]);
    });    
    document.getElementById("content").innerHTML = html;
}


function fetch_mmo_json() {
    fetch("../db/mmo.json")
        .then(response => response.json())
        .then(json => {
            console.log(json)
            load_mmo(json);
        });

}

fetch_mmo_json()