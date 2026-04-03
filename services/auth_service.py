"""Serviço de autenticação JWT."""
from datetime import datetime, timedelta
from typing import Optional
import bcrypt
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from core.config import settings
from models.nutricionista import Nutricionista


class AuthService:
    """Serviço de autenticação com JWT."""

    def __init__(self, db: Session):
        """
        Inicializa o serviço de auth.
        
        Args:
            db: Sessão do banco de dados
        """
        self.db = db

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Faz hash de uma senha.
        
        Args:
            password: Senha em texto plano
            
        Returns:
            Hash da senha
        """
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifica se uma senha corresponde ao hash.
        
        Args:
            plain_password: Senha em texto plano
            hashed_password: Hash armazenado
            
        Returns:
            True se a senha corresponde, False caso contrário
        """
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def create_access_token(
        self, 
        nutricionista_id: int, 
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Cria um token JWT.
        
        Args:
            nutricionista_id: ID do nutricionista
            expires_delta: Tempo de expiração customizado
            
        Returns:
            Token JWT
        """
        to_encode = {"sub": str(nutricionista_id)}

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )

        return encoded_jwt

    def verify_token(self, token: str) -> Optional[int]:
        """
        Verifica um token JWT e retorna o ID do usuário.
        
        Args:
            token: Token JWT
            
        Returns:
            ID do nutricionista ou None se inválido
        """
        try:
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=[settings.ALGORITHM]
            )
            nutricionista_id: str = payload.get("sub")
            
            if nutricionista_id is None:
                return None
                
            return int(nutricionista_id)
            
        except JWTError:
            return None

    def get_nutricionista_by_email(self, email: str) -> Optional[Nutricionista]:
        """
        Obtém um nutricionista pelo email.
        
        Args:
            email: Email do nutricionista
            
        Returns:
            Nutricionista ou None
        """
        return self.db.query(Nutricionista).filter(
            Nutricionista.email == email
        ).first()

    def authenticate_nutricionista(
        self, 
        email: str, 
        password: str
    ) -> Optional[Nutricionista]:
        """
        Autentica um nutricionista com email e senha.
        
        Args:
            email: Email do nutricionista
            password: Senha em texto plano
            
        Returns:
            Nutricionista se autenticado, None caso contrário
        """
        nutricionista = self.get_nutricionista_by_email(email)

        if not nutricionista:
            return None

        if not self.verify_password(password, nutricionista.senha_hash):
            return None

        return nutricionista
