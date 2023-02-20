from passlib.context import CryptContext

pwd_context =  CryptContext(schemes=['bcrypt'], deprecated = 'auto')

def hashie(password:str):
    return pwd_context.hash(password)

def verify(new_pasword, hash_password):
    return pwd_context.verify(new_pasword, hash_password)