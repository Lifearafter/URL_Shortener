const URL_TO_API = "https://nxihka4eoi.execute-api.us-east-1.amazonaws.com/dev";
var shortURL;

let apiColdCall = URL_TO_API + "/url?long_url=" + "google.com";
let coldReq = new XMLHttpRequest();
coldReq.open("GET", apiColdCall, true);
coldReq.send();

let inputURL = document.getElementById("inputtext");
inputURL.addEventListener("keypress", (event) => {
  if (event.key == "Enter") {
    inputButtonClick();
  }
});

let urlCard = document.getElementById("card");
urlCard.addEventListener("click", () => {
  navigator.clipboard.writeText(shortURL);
  urlInputBar.value = "";
});

function inputButtonClick() {
  let urlEle = document.getElementById("inputtext");
  longURL = urlEle.value;

  if (
    longURL == "" ||
    isValidURL(longURL) == false ||
    isNotAPIredirect(longURL) == true
  ) {
    alert("Please enter a valid input");
  } else {
    let apiCall = URL_TO_API + "/add?long_url=" + longURL;
    let mainReq = new XMLHttpRequest();
    mainReq.onreadystatechange = () => {
      if (mainReq.readyState == 4 && mainReq.status == 200) {
        let response = mainReq.responseText;
        let jsonOut = JSON.parse(response);
        let formattedOut = jsonOut.short_url;
        shortURL = URL_TO_API + "/" + formattedOut;

        urlEle.value = shortURL;
        urlEle.style.marginLeft = "8.6vh";

        showRedirectDiv();
        showCopyButton();
        showShortUrl();
      }
    };
    mainReq.open("POST", apiCall, true);
    mainReq.send();
  }
}

function inputRedirect() {
  window.open(shortURL, "_blank");

  let redirectDiv = document.getElementById("redirectDiv");
  redirectDiv.style.display = "none";
}
function showRedirectDiv() {
  let redirectDiv = document.getElementById("redirectDiv");
  redirectDiv.style.display = "block";
}
function showCopyButton() {
  let copyButton = document.getElementById("copybutton");
  copyButton.style.display = "block";
}

function isValidURL(string) {
  let validMatch = string.match(
    /(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/g
  );
  return validMatch !== null;
}

function isNotAPIredirect(string) {
  let preventNestedRedirects = string.includes(URL_TO_API);
  return preventNestedRedirects;
}

function copyClear() {
  let urlInputBar = document.getElementById("inputtext");
  navigator.clipboard.writeText(shortURL);
  urlInputBar.value = "";

  let copyButton = document.getElementById("copybutton");
  copyButton.style.display = "none";

  let redirectDiv = document.getElementById("redirectDiv");
  redirectDiv.style.display = "none";

  let inputURL = document.getElementById("inputtext");
  inputURL.style.marginLeft = "0vh";
}

function showShortUrl() {
  let eleUrl = document.getElementById("card");
  eleUrl.style.display = "block";

  let eleName = document.getElementById("headingcard");
  eleName.style.display = "block";

  let eleDate = document.getElementById("datecard");
  eleDate.style.display = "block";

  var currentDate = new Date();

  eleName.innerHTML = "Short URL";
  eleUrl.innerHTML = shortURL;
  eleDate.innerHTML =
    currentDate.getMonth() +
    1 +
    "/" +
    currentDate.getDate() +
    "/" +
    currentDate.getFullYear();
}
