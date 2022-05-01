   function input_field_focus(n){
        document.getElementById(n).classList.add("input-field-focused")
    }
    function input_field_focusout(n,m){
        var inp_value = document.getElementById(m).value;
        if(inp_value == ""){
            document.getElementById(n).classList.remove("input-field-focused")
        }
    }

    var pincode = document.getElementById("pincode_input");
    pincode.addEventListener("focusout",pincode_input)

    function pincode_input(){
        var pincode = document.getElementById("pincode_input").value;
        var api = "https://api.postalpincode.in/pincode/" + pincode

        fetch(api,{
            method: "GET"
        })
        .then((res) => {
            return res.json()
        })
        .then(data => {
            // console.log(data[0].PostOffice[0] , data[0].PostOffice[1] , data)
            document.getElementById("block_input").value = data[0].PostOffice[0].Name;
            document.getElementById("district_input").value = data[0].PostOffice[0].District;
            document.getElementById("state_input").value = data[0].PostOffice[0].State;
        })
        .catch((err) => {
            // console.log(err)
        })
    }