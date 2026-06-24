from fastapi import Depends,HTTPException,status
import jwt 
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import UTC, UTC, datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from app import schemas, database, models
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
#SECRET_KEY
#ALgorith
#Expiration time

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93fce93a4778152c33e8618ddc10"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 90        

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=str(id))
    except ExpiredSignatureError:
        raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credentials_exception)
    db_user = db.query(models.User).filter(models.User.id == token.id).first()
    print("Hi mini")
    return db_user