var urltoapi = "https://nxihka4eoi.execute-api.us-east-1.amazonaws.com/dev"

function inputButtonClick() {

    var x = document.getElementById("inputtext").value;
    
    if (x == "") {
        alert("Please enter a valid input");
    }
    else {
        var url = urltoapi + "/url?long_url=" + x;
        var  xhr = new XMLHttpRequest();
        xhr.open("GET", url, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4) {
                if(xhr.status == 200){
                    var response = xhr.responseText;
                    var json = JSON.parse(response);
                    var output = json.short_url;
                    document.getElementById("inputtext").value = urltoapi+'/'+output;
                }
                else{
                    var response = JSON.parse(xhr.responseText);
                    document.getElementById("inputtext").value = response.message;
                    
                }
            }
        }
        xhr.send();
    }
}