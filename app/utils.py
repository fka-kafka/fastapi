from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'])


def hasher(password: str):
    """ 
    Hashes the user password.
    """    
    
    hashed = pwd_context.hash(password)
    return hashed


def verifier(password: str, hashed_pwd: str):
    """ 
    Verifies password authenticity to allow for token provision.
    """
    
    verified = pwd_context.verify(password, hashed_pwd)
    return verified