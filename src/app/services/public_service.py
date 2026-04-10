import cloudinary.uploader
import io
from PIL import Image
import qrcode
from sqlalchemy.exc import SQLAlchemyError
import uuid

from src.app.services import GroupsService
from src.app.models.model import Registro
from src.app.extension import db


class ServiceError(Exception):
    pass


class PublicService:

    @staticmethod
    def get_register_by_id(id_register):
        return db.session.get(Registro, id_register)

    @staticmethod
    def get_groups_for_selection(plantel_id):
        """Devuelve una lista de tuplas (id, nombre) para WTForms o diccionarios para JSON."""
        plantel = GroupsService.get_by_id(plantel_id)
        if not plantel:
            return []
        return [(g.id, g.name_group) for g in plantel.grupos]

    @staticmethod
    def get_all_plantels_choices():
        """Devuelve los planteles listos para el SelectField."""
        plantels = GroupsService.show()
        choices = [(p.id, p.plantel) for p in plantels]
        choices.insert(0, (0, "-- Selecciona Plantel --"))
        return choices
    
    @staticmethod
    def save_register_with_qr(student,campus,group):
        public_id = None
        try:
            # 1. Crear la información del QR
            datos_qr = f"Alumno: {student}\nPlantel: {campus}\nGrupo: {group}"
            
            # 2. Generar el QR con la librería
            img = qrcode.make(datos_qr)

            # 3. GUARDAR EN MEMORIA (BytesIO)
            # Esto evita crear archivos temporales en tu computadora
            buffer = io.BytesIO()
            img.save(buffer, "PNG")
            buffer.seek(0) # Regresar al inicio del archivo virtual

            unique_id = uuid.uuid4().hex[:3]
            nombre_archivo = f"qr_{student.replace(' ', '_')}_{unique_id}"

            # 4. SUBIR A CLOUDINARY
            upload_result = cloudinary.uploader.upload(
                buffer,
                folder="my_qrs",
                public_id=nombre_archivo,
                overwrite=False
            )

            # 5. OBTENER URL Y GUARDAR EN DB
            url_final = upload_result.get('secure_url')
            
            nuevo_registro = Registro(
                student=student,
                campus=campus,
                group=group,
                qr_url=url_final,
                qr_public_id=upload_result.get('public_id')
            )

            db.session.add(nuevo_registro)
            db.session.commit()

            return nuevo_registro
        
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
            print("\n" + "!"*30)
            print('__ERROR INESPERADO__')
            print('Ubication: PublicService.save_register')
            print(f'Description: {e}')
            print("!"*30 + "\n")
            raise ServiceError('ERROR: No se pudo crear el qr')
