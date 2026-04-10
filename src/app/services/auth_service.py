from flask_login import login_user
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.app.extension import db
from src.app.models.model import User


class ServiceError(Exception):
    pass

class AuthService():
    @staticmethod
    def validation(username, password):
        try:
            
            stmt = select(User).where(User.username == username)
            user = db.session.scalar(stmt)

            if user and user.check_password(password):
                login_user(user)
                return True

            raise ServiceError('ERROR: Usuario o Contraseña Invalidos')
        
        except ServiceError:
            raise
        
        except SQLAlchemyError as e:
            db.session.rollback()
            print('__ERROR TECNICO__')
            print('Ubication: AuthService.validation')
            print('Description: {e}')
            raise ServiceError('ERROR: Usuario o Contraseña Invalidos')

        except Exception as e:
            print(f"__ERROR INESPERADO: {e}__")
            raise ServiceError("Ocurrió un error inesperado en el servidor")