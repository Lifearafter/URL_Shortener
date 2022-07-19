## API Design

### Operations

1.  **GET**
    - `input` longURL
    - `returns` if exists <span style="color: #7879FF">True</span> - _URL_
    - `returns` if exists <span style = 'color: #7879FF'>False</span> - notfound msg
2.  **GET**
    - `input` shortURL
    - `returns` HTTP redirect
3.  **POST**
    - `input` longURL
    - `returns` if no input - No Input Msg
    - `returns` if input - _URL_Model_
4.  **DELETE**
    - `input` longURL <span style="color: #7879FF">Optional</span>
    - `input` shortURL <span style="color: #7879FF">Optional</span>
    - `returns` if no input - No Input Msg
    - `returns` deletion complete msg and _URL_Model_.

> **Side Note** - All HTTP operations return a status code, execpt for the redirect endpoint.

### Models

_URL_ - Holds longURL, shortURL, date and time accessed</br>

- Extends Pydantic BaseModel </br>
- Response Model </br>

### OAuth2

Admin Users - For deletion to work an admin must perform the operation after login
No sign-up feature

### Shortener Algo

Simply looks at the last digit of the most recent addition to the URL database, and adds the next digit or letter to it.</br>
If all have been exhausted the algorithm starts at another bit to the last addition, and that bit is 0.
