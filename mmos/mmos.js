function loadSlider(maxNumberItems){
    
    let slider = document.getElementById('slider');
    
    noUiSlider.create(slider, {
        connect: true,
        start: [0,maxNumberItems],
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

    let temp = data.length

    let last_mmo = data[temp-1]
    let last_mmo_number = last_mmo.mmo_number

    loadSlider(Number(last_mmo_number));
    data.forEach(function(value,key){
        html += loadTemplate("mmo_template", data[key]);
        
        let characterArray = value["character_list"].split(" ");

        for(character of characterArray){
            character_list.add(character);
        }

        let contentTagArray = value["general_tag_list"].split(" ");

        for(tag of contentTagArray){
            content_tag_list.add(tag);
        }

        
    });
    document.getElementById("content").innerHTML = html;
}


async function fetch_mmo_json() {
    await fetch("../db/mmo.json")
        .then(response => response.json())
        .then(json => {
            console.log(json);
            mmo_json = json;
            load_mmo(mmo_json);
            load_modal_characters(character_list);
            load_modal_content_tag(content_tag_list);
        });
        
    }
    
function load_modal_characters(character_list){        
    let element = document.getElementById("modal-table-characters");

    let html = ""
    character_list.forEach(
        function(value){
            html += loadTemplate("table-row-template-content-tag",value);
        }
    )
    
    element.tbody.innerHTML = html;
}


function load_modal_content_tag(content_tag_list){        
    let element = document.getElementById("checkbox-content-tag");

    let html = ""
    content_tag_list.forEach(
        function(value){
            html += loadTemplate("checkbox-content-tag-template",value);
        }
    )
    
    element.innerHTML = html;

    console.log(content_tag_list);
}


let character_list = new Set();

let content_tag_list = new Set();

let mmo_json;

fetch_mmo_json();