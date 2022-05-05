
function input_field_focus(n){
    document.getElementById(n).classList.add("input-field-focused")
}

function input_field_focusout(n,m){
    alert("working")
    var inp_value = document.getElementById(m).value;
    if(inp_value == ""){
        document.getElementById(n).classList.remove("input-field-focused")
    }
}

// document.body.addEventListener("click", function() {
//     all_inps = document.body.querySelectorAll(".theme_input");

//     for(i=0;i<=all_inps.length;i++) {
//         input_field_focusout( all_inps[i].getAttribute('data-for-js2') , all_inps[i].getAttribute('data-forjs1'))
//         console.log(i,all_inps[i].getAttribute("data-for-js2"), all_inps[i].getAttribute("data-forjs1"))
//     }
// })