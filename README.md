# GSB FastAPI workshop

## Tools
* [VSCode](https://code.visualstudio.com/download)
* [python](https://www.python.org/downloads/)
* [Postman](https://www.postman.com/downloads/)

## Python ENV
* config python env
    `python -m venv env`
* Activate env
    `.\env\Scripts\activate`
    
## Cli in use
* For create python env `python3 -m venv env`
* `uvicorn main:app --reload`

## libraries in use
* `pip install "fastapi[all]"`
* `pip install sqlmodel`
* `pip install "python-jose[cryptography]"`
* `pip install "passlib[bcrypt]"`
* `pip install python-decouple`
* `pip install pytest`
* gen secret-key `openssl rand -hex 32`


## Ref

* [SQLModel](https://sqlmodel.tiangolo.com/)
* [Oauth](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
* [Unit test](https://www.fastapitutorial.com/blog/unit-testing-in-fastapi/)
* [Unit test2](https://medium.com/fastapi-tutorials/testing-fastapi-endpoints-f7e78f09b7b6)


## Note
> Use SQLAlchemy==1.4.34

> windows update pip `python -m pip install --upgrade pip`

> fix windows permission put this in powershell `Set-ExecutionPolicy RemoteSigned`
