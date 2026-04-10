from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.app.models.model import Grupo, Plantel
from src.app.extension import db


class ServiceError(Exception):
    pass

class GroupsService():

    @staticmethod
    def get_by_id(plantel_id):
        return db.session.get(Plantel, plantel_id)

    @staticmethod
    def save(nombre_plantel,lista_nombres_grupos):

        try:
            nuevo_plantel = Plantel(plantel=nombre_plantel)
            db.session.add(nuevo_plantel)

            db.session.flush()

            for nombre in lista_nombres_grupos:
                if nombre.strip(): 
                    nuevo_grupo = Grupo(
                        name_group=nombre,
                        plantel_id=nuevo_plantel.id
                    )
                    db.session.add(nuevo_grupo)

            db.session.commit()
            return True
        
        except SQLAlchemyError as e:
            db.session.rollback()
            print("\n" + "!"*30)
            print(f'__ERROR TECNICO__')
            print(f"Ubication: GroupsService.save")
            print(f'Description: {e}')
            print("!"*30 + "\n")
            raise ServiceError('ERROR: El nombre del plantel ya existe')
        
        except Exception as e:
            db.session.rollback()
            print("\n" + "!"*30)
            print('__ERROR INESPERADO__')
            print('Ubication: GroupsService.save')
            print(f'Description: {e}')
            print("!"*30 + "\n")
            raise ServiceError('ERROR: Algo salio mal al intentar registrar')
        
    @staticmethod
    def show():
        plantels = select(Plantel).options(joinedload(Plantel.grupos))
        result = db.session.execute(plantels).unique().scalars().all()

        return result

    @staticmethod
    def delete(plantel_id):
        try:
            plantel = db.session.get(Plantel, plantel_id)

            if not plantel:
                raise ServiceError("El palntel ya no existe")

            db.session.delete(plantel)
            db.session.commit()
            return True
        
        except SQLAlchemyError as e:
            db.session.rollback()
            print("\n" + "!"*30)
            print('__ERROR TECNICO__')
            print('Ubication: GroupsService.delete')
            print(f'Description: {e}')
            print("!"*30 + "\n")
            raise ServiceError('ERROR: No se pudo eliminar ')
        
        except Exception as e:
            db.session.rollback()
            print("\n" + "!"*30)
            print('__ERROR INESPERADO__')
            print('Ubication: GroupsService.delete')
            print(f'Description: {e}')
            print("!"*30 + "\n")
            raise ServiceError('ERROR: Algo salio mal al intentar eliminar')

    @staticmethod
    def update_groups(plantel_id, nuevo_nombre, lista_grupos):
        """
        Actualiza el nombre del plantel y sincroniza su lista de grupos.
        """
        # 1. Obtener el registro existente
        plantel = GroupsService.get_by_id(plantel_id)
        
        if not plantel:
            raise ServiceError("El plantel solicitado no existe en el sistema.")

        try:
            # 2. Actualizar datos básicos
            plantel.plantel = nuevo_nombre

            # 3. Sincronizar Grupos (Estrategia: Borrar y Reemplazar)
            # Primero eliminamos todos los grupos actuales vinculados a este plantel
            for grupo_viejo in plantel.grupos:
                db.session.delete(grupo_viejo)
            
            # Forzamos un flush para que los deletes se procesen antes de insertar los mismos nombres
            db.session.flush()

            # 4. Insertar los nuevos grupos recibidos del formulario
            for nombre_grupo in lista_grupos:
                if nombre_grupo and nombre_grupo.strip():
                    nuevo_grupo = Grupo(
                        name_group=nombre_grupo.strip(),
                        plantel_id=plantel.id
                    )
                    db.session.add(nuevo_grupo)

            # 5. Confirmar todos los cambios
            db.session.commit()
            return True

        except SQLAlchemyError as e:
            db.session.rollback()
            # Log de error técnico para el desarrollador
            print("\n" + "!"*30)
            print(f"__ERROR DE BASE DE DATOS EN UPDATE__")
            print(f"Location: GroupsService.update_groups")
            print(f"Description: {str(e)}")
            print("!"*30 + "\n")
            raise ServiceError("No se pudieron guardar los cambios en la base de datos.")

        except Exception as e:
            db.session.rollback()
            print(f"Error inesperado: {e}")
            raise ServiceError("Ocurrió un error inesperado al procesar la actualización.")