function input_field_focus(n){
    document.getElementById(n).classList.add("input-field-focused")
}

document.body.addEventListener("click", function() {
    all_inps = document.body.querySelectorAll(".theme_input");
    input_field_focusout(all_inps[0].getAttribute('data-for-js2') , all_inps[0].getAttribute('data-for-js1'))
    console.log(8,all_inps[0].getAttribute('data-for-js2') , all_inps[0].getAttribute('data-for-js1'))

    for(i=0;i<=all_inps.length;i++) {

        input_field_focusout( all_inps[i].getAttribute('data-for-js2') , all_inps[i].getAttribute('data-for-js1'))
        console.log(i,all_inps[i].getAttribute("data-for-js2"), all_inps[i].getAttribute("data-for-js1"))
        break;
    }
})

// function input_field_focusout(n,m){
//     alert("Working")
//     var inp_value = document.getElementById(m).value;
//     if(inp_value == "" || inp_value == null){
//         document.getElementById(n).classList.remove("input-field-focused")
//     }
// }
