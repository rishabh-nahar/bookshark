function input_field_focus(n){
    document.getElementById(n).classList.add("input-field-focused")
}
function input_field_focusout(n,m){
    var inp_value = document.getElementById(m).value;
    if(inp_value == ""){
        document.getElementById(n).classList.remove("input-field-focused")
    }
}