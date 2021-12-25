from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from starlette import status
from app import models, schemas, database

from .config import settings

# login endpoint
OAuth2_schema = OAuth2PasswordBearer(tokenUrl="login")
#secret key
# Algo to use
# expiration time for token

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data : dict): # data is payload
    to_encode = data.copy()
    #chk time to expire token

    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm= ALGORITHM)

    return encoded_jwt

# verify access token
def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms = ALGORITHM)
        id = payload.get("user_id")
        name = payload.get("name")
  
        if id == None and name == None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception

    return token_data 

# when we wana test prod server or something we will have to change port and ip etc which 
# is qite a problem so we can cretea variable which changes as per environment
def get_current_User(token: str= Depends(OAuth2_schema), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not found validate credentials",
                             headers={"WWW-Authenticate":"Bearer"})

    token = verify_access_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user

