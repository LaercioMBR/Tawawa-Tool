

/* 
function replaceContent(){

    let reader = new FileReader();

    reader.readAsText("navbar.html");
    let temp = reader;
    alert(temp);
}

function replaceContent(){
    alert("teste string")    


}

let buttons = document.getElementsByClassName("nav-link");
let sections = document.getElementsByClassName("section");

for(let button of buttons){
    addListenersToDisplay(button)
}

function addListenersToDisplay(element){
    let element_id = element.id
    for(let section of sections){
        if(section.id.includes(element_id) ){
            element.addEventListener("click", event => {
                // alert(section.id)
                document.getElementById(section.id).style = "display:true";
            });
        }
    }
}


*/