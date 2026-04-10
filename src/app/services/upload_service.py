import cloudinary.uploader
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename

from src.app.extension import db
from src.app.models.model import File

class ServiceError(Exception):
    pass


class FileService:
    @staticmethod
    def upload_files(file_data):
        public_id = None
        try:

            clean_name = secure_filename(file_data.filename).rsplit('.', 1)[0]

            upload_result = cloudinary.uploader.upload(
                file=file_data,
                public_id=clean_name,
                resourse_type='auto',
                folder='my_questionnairs'
            )

            public_id = upload_result['public_id']
            secure_url = upload_result['secure_url']

            new_upload = File(
                file_name=clean_name,
                pdf_url=secure_url,
                pdf_public_id=public_id
            )

            db.session.add(new_upload)
            db.session.commit()

            return new_upload

        except SQLAlchemyError as e:
            db.session.rollback()
            if public_id:
                cloudinary.uploader.destroy(public_id)

            print("\n" + "!"*30)
            print(f'__ERROR TECNICO__')
            print(f"Ubication: FileService.upload_files")
            print(f'Description: {e}')
            print("!"*30 + "\n")
            raise ServiceError(f'ERROR: url no guardada en la base de datos')

        except Exception as e:
            db.session.rollback()
            print(f'ERROR INESPERADO: {e}')
            print("\n" + "!"*30)
            print(f'__ERROR INESPERADO__')
            print(f"Ubication: FileService.upload_files")
            print(f'Description: {e}')
            print("!"*30 + "\n")
            raise ServiceError(f'ERROR: No se pudo subir el archivo')
    
    @staticmethod
    def delete_files(file_id):

        file_object = db.session.get(File, file_id)

        if not file_object:
            raise ServiceError("El archivo no existe en la base de datos.")

        public_id_to_delete = file_object.pdf_public_id

        try:

            cloudinary.uploader.destroy(public_id_to_delete)

            db.session.delete(file_object)
            db.session.commit()

            return True
        
        except SQLAlchemyError as e:
            db.session.rollback()
            print("\n" + "!"*30)
            print(f'__ERROR TECNICO__')
            print(f"Ubication: FileService.delete_files")
            print(f'Description: {e}')
            print("!"*30 + "\n")
            raise ServiceError(f'ERROR: No se pudo eliminar de la base de datos')
        
        except Exception as e:
            db.session.rollback()
            print("\n" + "!"*30)
            print(f'__ERROR INESPERADO__')
            print(f"Ubication: FileService.delete_files")
            print(f'Description: {e}')
            print("!"*30 + "\n")
            raise ServiceError(f'ERROR: No se pudo eliminar de cloudinary')

    @staticmethod
    def get_all():
        try:
            stmt = select(File)
            return db.session.scalars(stmt).all()

        except Exception as e:
            raise ServiceError("ERROR: No se pudo obtener la lista")
