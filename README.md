<div align="center">
  <a href="https://github.com/Lifearafter/URL_Shortener">
    <img src="docs/icons/page_icon.png" alt="Logo" width="400" height="186">
  </a>

  <h3 align="center">Minimalistic URL-Shortener</h3>

  <p align="center">
    A URL-Shortener without the extra BS
    <br />
    <a href="https://lifearafter.github.io/URL_Shortener"><strong>Website »</strong></a>
    <br />
    <br />
    <a href="https://nxihka4eoi.execute-api.us-east-1.amazonaws.com/dev/docs">API Docs</a>
    ·
    <a href="https://github.com/Lifearafter/URL_Shortener/issues">Report Bug</a>
    ·
    <a href="https://github.com/Lifearafter/URL_Shortener/issues">Request Feature</a>
  </p>
</div>

# URL Shortener - API and Website

<p style="font-size:17px">A <i>full-stack</i> project to implement a URL Shortener, using <b>FASTAPI</b> and <b>SQL Alchemy</b>. The Projects main purpose was to demonstrate the workings of a <i>Restful API</i>, and how it interacts with a <i>Relational Database</i> (MySQL). The website was a attempt at learning the workings of the <b>JavaScript DOM</b> and <b>CSS Styling</b>. The project is hosted on <b>AWS</b>, with a CI/CD pipeline from the github repository to AWS Services using <b>Github Actions</b>.</p>

<hr>

<br/>

## **API**

**API is temporarily hosted at https://nxihka4eoi.execute-api.us-east-1.amazonaws.com/dev**

> You can access the documentation to the API using https://nxihka4eoi.execute-api.us-east-1.amazonaws.com/dev/docs

> The API domain will change in the future, so plan accordingly

### **Endpoints**

1.  **GET**
    - `input` longURL
    - `returns` if exists <span style="color: #7879FF">True</span> - _URL_
    - `returns` if exists <span style = 'color: #7879FF'>False</span> - notfound msg
2.  **GET**
    - `input` shortURL
    - `returns` if exists <span style="color: #7879FF">True</span> - HTTP redirect
    - `returns` if exists <span style = 'color: #7879FF'>False</span> - notfound msg
3.  **POST**
    - `input` longURL
    - `returns` if exists <span style="color: #7879FF">True or False</span> - _URL_Model_
    - `returns` if no input - No Input Msg
4.  **DELETE**
    - `input` longURL
    - `returns` if exists <span style="color: #7879FF">True</span> - _URL_Model_.
    - `returns` if exists <span style="color: #7879FF">False</span> - No Input Msg

> All Users should be able to use Post and Delete Options for now.<br/>
> Things might change in the future.<br/>

### **Models**

_URL_ - Holds longURL, shortURL, date and time accessed</br>

- Extends Pydantic BaseModel </br>
- Response Model </br>

_Users_ - Holds user information for oauth purposes </br>

- Work still in progress
- May have a **one to many** relationship with URL model in the future</br>
- May also extend the Pydantic BaseModel
- Will be a Response Model
- Will have endpoints associated with it

### **OAuth2**

Normal Users - To keep track of which account has which shortened URLs associated with it. (Work in progress)

### **Shortener Algo**

Simply looks at the last digit of the most recent addition to the URL database, and adds the next digit or letter to it.</br>

If all have been exhausted the algorithm starts at another bit to the last addition, and that bit is 0.

> Only digits and lowercase letters <br/>

> Work in progress to add a table in the database that holds all the deleted or expired shortened urls. To make it so that the **API** will first look through this table to find a shortened URL, then will go and use the **Shortener Algo**

### **ORM - SQL Database**

Used a **MySQL** Database to hold all the tables for this app. <br/>
Mapped to it by using the **SQL Alchemy** Library in python using the **PymySQl** DBAPI for the purposes of connecting my mapped operations. <br/>

### **Hosting and CI/CD**

Used Github Actions, to Continuously Integrate and Deploy to my **AWS Lambda Function**. <br/>
The Database is a **AWS RDS** instance. </br>
Used the **AWS API Gateway** to map requests to my API to the Lambda Function.<br/>
**Unit Test** Coverage is at **92%**, some cases are untestable in normal circumstances.

<hr>
<br/>

## **Website**

Written using Javascript, HTML, and CSS. No Frameworks or external Libraries. <br/>
A simple manipulation of the DOM to display elements when needed after calls made to API.<br/>

You can visit my website for the URL Shortener, to test out its current functionality. <br/>
**https://lifearafter.github.io/URL_Shortener**

> The website domain will change in the future, and the ReadMe will reflect these changes.

<hr>

<br/>

## **Future Plans**

- Upgrade the Database so that on every use, if a shortened URL is not associated with a account/User than it is to be terminated (Deleted) after 5 days of no use.<br/>
- Add admin priveledges to delete users and accounts. <br/>
- Add ability to look previous shortened urls even without an account. <br/>
- Add ability to increase usage time of a shortened URL by a User.
- Migrate API and Website to personal domain.
- Add a Dockerfile for those who would like to replicated the URL-Shortener.
