const API_URL = "https://nxihka4eoi.execute-api.us-east-1.amazonaws.com/dev"
let output_url = '';

function inputButtonClick() {

    const shorturl = document.getElementById("inputtext").value;
    
    if (shorturl == "" || isValidURL(shorturl) == false || isNotAPIredirect(shorturl) == true) {
        alert("Please enter a valid input");
    }
    else {
        const xhr_request_url = API_URL + "/url?shorturl=" + shorturl;
        const xhr = new XMLHttpRequest();
        xhr.open("GET", xhr_request_url, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4) {
                if(xhr.status == 200){
                    const response = xhr.responseText;
                    const json = JSON.parse(response);
                    const output = json.longurl;
                    output_url = API_URL+'/'+output;
                    document.getElementById("inputtext").value = output_url;
                    showRedirectDiv();
                }
                else if (xhr.status == 404) {
                    let req = new XMLHttpRequest();
                    xhr_request_url = API_URL + "/add?long_url=" + shorturl;
                    req.open("POST", xhr_request_url, true);
                    req.onreadystatechange = function () {
                        if (req.readyState == 4) {
                            if (req.status == 200) {
                                const response = req.responseText;
                                const json = JSON.parse(response);
                                const output = json.longurl;
                                output_url = API_URL+'/'+output;
                                document.getElementById("inputtext").value = output_url;
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
                    const response = JSON.parse(xhr.responseText);
                    document.getElementById("inputtext").value = response.message;
                }
            }
        }
        xhr.send();
    }
}

function inputRedirect(){
    window.open(output_url, '_blank');
    const redirectDiv = document.getElementById("redirectDiv");
    redirectDiv.style.display = "none";
}

function showRedirectDiv(){
    const redirectDiv = document.getElementById("redirectDiv");
    redirectDiv.style.display = "block";
}

function isValidURL(string) {
    return null !== string.match(/(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/g);
}

function isNotAPIredirect(string){
    return string.includes(API_URL);
}