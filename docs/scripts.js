var urltoapi = "https://nxihka4eoi.execute-api.us-east-1.amazonaws.com/dev"
var shortmainurl;

function inputButtonClick() {

    var longurl = document.getElementById("inputtext").value;
    
    if (longurl == "" || isValidURL(longurl) == false || isNotAPIredirect(longurl) == true) {
        alert("Please enter a valid input");
    }
    else {
        var url = urltoapi + "/url?long_url=" + longurl;
        var xhr = new XMLHttpRequest();
        xhr.open("GET", url, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4) {
                if(xhr.status == 200){
                    var response = xhr.responseText;
                    var json = JSON.parse(response);
                    var output = json.short_url;
                    shortmainurl = urltoapi+'/'+output;
                    document.getElementById("inputtext").value = shortmainurl;
                    showRedirectDiv();
                }
                else if (xhr.status == 404) {
                    var req = new XMLHttpRequest();
                    url = urltoapi + "/add?long_url=" + longurl;
                    req.open("POST", url, true);
                    req.onreadystatechange = function () {
                        if (req.readyState == 4) {
                            if (req.status == 200) {
                                var response = req.responseText;
                                var json = JSON.parse(response);
                                var output = json.short_url;
                                shortmainurl = urltoapi+'/'+output;
                                document.getElementById("inputtext").value = shortmainurl;
                                showRedirectDiv();
                            }
                            else {
                                alert("Error");
                            }
                        }
                    }
                    req.send();
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

function inputRedirect(){
    window.open(shortmainurl, '_blank');
    let redirectDiv = document.getElementById("redirectDiv");
    redirectDiv.style.display = "none";
}
function showRedirectDiv(){
    let redirectDiv = document.getElementById("redirectDiv");
    redirectDiv.style.display = "block";
}

function isValidURL(string) {
    var res = string.match(/(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/g);
    return (res !== null)
}

function isNotAPIredirect(string){
    var res = string.includes(urltoapi);
    return res;
}