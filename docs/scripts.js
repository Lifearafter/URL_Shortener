const URL_TO_API = "https://nxihka4eoi.execute-api.us-east-1.amazonaws.com/dev"
var shortURL;

var inputURL = document.getElementById("inputtext");
inputURL.addEventListener("keypress", function(event){
    if(event.key == "Enter"){
        inputButtonClick()
    }
});

function inputButtonClick() {

    let longURL = document.getElementById("inputtext").value;
    
    if (longURL == "" || isValidURL(longURL) == false || isNotAPIredirect(longURL) == true) {
        alert("Please enter a valid input");
    }
    else {
        let apiCall = URL_TO_API + "/url?long_url=" + longURL;
        let mainReq = new XMLHttpRequest();
        mainReq.open("GET", apiCall, true);
        mainReq.onreadystatechange = function () {
            if (mainReq.readyState == 4) {
                if(mainReq.status == 200){
                    let response = mainReq.responseText;
                    let jsonOut = JSON.parse(response);
                    let formattedOut = jsonOut.short_url;
                    shortURL = URL_TO_API+'/'+formattedOut;
                    document.getElementById("inputtext").value = shortURL;

                    let inputURL = document.getElementById("inputtext");
                    inputURL.style.marginLeft= "14.5vh";

                    showRedirectDiv();
                    showCopyButton();
                }
                else if (mainReq.status == 404) {
                    let alternateReq = new XMLHttpRequest();
                    apiCall = URL_TO_API + "/add?long_url=" + longURL;
                    alternateReq.open("POST", apiCall, true);
                    alternateReq.onreadystatechange = function () {
                        if (alternateReq.readyState == 4) {
                            if (alternateReq.status == 200) {
                                let response = alternateReq.responseText;
                                let json = JSON.parse(response);
                                let formattedOut = json.short_url;
                                shortURL = URL_TO_API+'/'+formattedOut;
                                document.getElementById("inputtext").value = shortURL;
                                showRedirectDiv();
                                showCopyButton();
                            }
                            else {
                                alert("Error");
                            }
                        }
                    }
                    alternateReq.send();
                }
                else{
                    let response = JSON.parse(mainReq.responseText);
                    document.getElementById("inputtext").value = response.message;
                }
            }
        }
        mainReq.send();
    }
}

function inputRedirect(){
    window.open(shortURL, '_blank');
    
    let redirectDiv = document.getElementById("redirectDiv");
    redirectDiv.style.display = "none";
}
function showRedirectDiv(){
    let redirectDiv = document.getElementById("redirectDiv");
    redirectDiv.style.display = "block";
}
function showCopyButton(){
    let copyButton = document.getElementById("copybutton")
    copyButton.style.display = "block";
}

function isValidURL(string) {
    let validMatch = string.match(/(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/g);
    return (validMatch !== null)
}

function isNotAPIredirect(string){
    let preventNestedRedirects = string.includes(URL_TO_API);
    return preventNestedRedirects;
}

function copyClear(){
    let urlInputBar = document.getElementById('inputtext')
    navigator.clipboard.writeText(urlInputBar.value);
    urlInputBar.value = '';

    let copyButton = document.getElementById('copybutton')
    copyButton.style.display = "none";

    let redirectDiv = document.getElementById('redirectDiv')
    redirectDiv.style.display = "none";

    let inputURL = document.getElementById("inputtext");
    inputURL.style.marginLeft= "0vh";
}