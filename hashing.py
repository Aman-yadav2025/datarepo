#following code is not working due to library incampibilities

# from passlib.context import CryptContext

# pwd_cxt = CryptContext(schemes=["bcrypt"],deprecated = "auto")

# class Hash():
#     @staticmethod
#     def bcrypt(password:str):
#         return pwd_cxt.hash(password)

#updated code

import bcrypt

class Hash():
    @staticmethod
    def bcrypt(password: str):
        # bcrypt requires bytes, so we encode the password first
        pwd_bytes = password.encode('utf-8') #incode the password into binary so that function can understand it
        salt = bcrypt.gensalt() #make each binary code unique
        hashed_password = bcrypt.hashpw(pwd_bytes, salt)
        
        # Decode back to a normal string so SQLAlchemy can save it
        return hashed_password.decode('utf-8')