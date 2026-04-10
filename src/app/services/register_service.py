import cloudinary.uploader
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from openpyxl import Workbook

from src.app.models.model import Registro
from src.app.extension import db

class ServiceError(Exception):
    pass


class RegisterService():
    
    @staticmethod
    def get_all():
        try:
            stmt = select(Registro)
            result = db.session.execute(stmt).scalars().all()
            return result

        except SQLAlchemyError as e:
            print('__ERROR TECNICO__')
            print('Ubication: RegisterService.get_all()')
            print(f'Description: {e}')
            raise ServiceError("ERROR: No se pudieron obtener los datos")
    
    @staticmethod
    def delete_all():
        try:

            db.session.execute(delete(Registro))
            db.session.commit()
            return True
        
        except SQLAlchemyError as e:
            db.session.rollback()
            print('__ERROR TECNICO__')
            print('Ubication: RegisterService.get_all()')
            print(f'Description: {e}')
            raise ServiceError("ERROR: Los datos no se eliminaron")

        
        except Exception as e:
            db.session.rollback()
            print('__ERROR INESPERADO__')
            print('Ubication: RegisterService.get_all()')
            print(f'Description: {e}')
            raise ServiceError("ERROR: Ocurrió un fallo inesperado al intentar limpiar los datos.")
        
    @staticmethod
    def download_excel():

        try:
        
            # Obteniendo todos los datos de la base de datos
            stmt = select(Registro)
            registros = db.session.scalars(stmt).all()

            # Creando un archivo excel instanciando un objeto de la clase Workbook
            wb = Workbook()

            # Activar una hoja
            sheet = wb.active
            assert sheet is not None

            # Crear encabezado
            sheet.append(["ALUMNO","PLANTEL","GRUPO",])

            # Agregar el dato a la siguiente fila
            for r in registros:
                sheet.append([r.student,r.campus,r.group])

            # Guardar el archivo temporalmente en memoria
            from io import BytesIO
            output = BytesIO()
            wb.save(output)
            output.seek(0)

            return output
        
        except SQLAlchemyError as e:
            db.session.rollback()
            print('__ERROR TECNICO__')
            print('Ubication: RegisterService.download_excel()')
            print(f'Description: {e}')
            raise ServiceError('ERROR: No se encontraron datos')
    
        except Exception as e:
            db.session.rollback()
            print('__ERROR INESPERADO__')
            print('Ubication: RegisterService.download_excel()')
            print(f'Description: {e}')
            raise ServiceError('ERROR: No se pudo crear el Excel')
