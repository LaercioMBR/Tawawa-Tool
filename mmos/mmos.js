function load_mmo_thead(json) {
    let table_head = document.getElementById('mmo_table_thead_tr')

    for( mmo_metadata in json ){
        let head = document.createElement("th")
        head.innerHTML = mmo_metadata
        table_head.appendChild(head)
    }
}

function load_mmo_tbody(json) {
    let table_body = document.getElementById('mmo_table_tbody')

    console.log("load mmo tbody JSON")
    console.log(json)
    console.log("typeof  JSON")
    console.log(typeof(json))

    let length = json.length
    console.log(length)
    console.log("length of json")

    for(i=0; i<= length; i++ ){
        let row = document.createElement("tr")

        for(key in json[i]){
            let tabledata = document.createElement("td")
            tabledata.innerHTML = json[i][key]
            row.appendChild(tabledata)
        }
        table_body.appendChild(row)
    }
}

function load_table(json){
    load_mmo_thead(json.meta)
    load_mmo_tbody(json.data)
}


function fetch_mmo_json(){
    fetch("../db/mmo.json")
        .then(response => response.json())
        .then(data => {
            console.log(data)
            load_table(data);     
        });        

}

fetch_mmo_json()