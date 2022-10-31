from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    
    def bcrypt(password):
        return pwd_context.hash(password)
    
    def verify(plain, hashed):
        return pwd_context.verify(plain, hashed)