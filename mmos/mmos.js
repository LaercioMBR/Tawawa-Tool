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

    alert(temp)
    let last_mmo = data[temp-1]
    let last_mmo_number = last_mmo.mmo_number

    loadSlider(Number(last_mmo_number));
    data.forEach(function(value,key){
        html += loadTemplate("mmo_template", data[key]);
        
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
            character_list = mmo_json["unique_character_list"];
            load_modal_characters(character_list);
            content_tag_list = mmo_json["unique_tag_list"];
            load_modal_content_tag(content_tag_list);
        });
        
    }
    
function load_modal_characters(character_list){        
    
    let html = ""
    
    alert(character_list)
    character_list.forEach(
        function(value){
            html += loadTemplate("table-row-template-character-tag",value);
        }
    )
    
    document.getElementById("modal-table-characters-tbody").innerHTML = html;
    
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

let character_list;

let content_tag_list;

let mmo_json;

fetch_mmo_json();