import unicodedata
from flask import Blueprint, render_template, url_for, redirect, request, flash, jsonify

from src.app.services import FileService, GroupsService, PublicService, ServiceError
from src.app.forms.register_form import RegisterForm

bp = Blueprint('public',__name__)


def normalizar_texto(texto):
    if not texto:
        return ""
    # 1. Convertir a mayúsculas y quitar espacios extra
    texto = texto.upper().strip()
    # 2. Descomponer caracteres con acentos (á -> a + ´)
    texto = unicodedata.normalize('NFD', texto)
    # 3. Filtrar solo los caracteres que no sean acentos (non-spacing marks)
    texto = "".join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/information')
def information():
    return render_template('info.html')

@bp.route('/questionnaries')
def questionnaries():
    questionnaries = FileService.get_all()
    return render_template('questionnaries.html', questionnaries=questionnaries)

@bp.route('/register', methods=['GET', 'POST'])
def register_view():
    form = RegisterForm()
    # Cargamos los planteles para la primera vista
    form.plantel.choices = PublicService.get_all_plantels_choices() # type: ignore
    form.grupo.choices = [(0, "-- Selecciona un plantel primero --")]
    return render_template('register.html', form=form)

@bp.route('/process_register', methods=['POST'])
def process_register():

    form = RegisterForm()
    
    # 1. RECONSTRUCCIÓN: Necesaria para que WTForms pueda validar los IDs enviados
    form.plantel.choices = PublicService.get_all_plantels_choices() # type: ignore
    
    plantel_id = int(request.form.get('plantel', 0))
    form.grupo.choices = PublicService.get_groups_for_selection(plantel_id)# type: ignore

    # 2. VALIDACIÓN
    if form.validate_on_submit():
        # Traducimos los IDs a Strings
        student_name = normalizar_texto(form.student.data)
        campus_str = next((name for val, name, *_ in form.plantel.choices if val == form.plantel.data), "N/A")
        group_str = next((name for val, name, *_ in form.grupo.choices if val == form.grupo.data), "N/A")

        try:
            # 3. GUARDADO Y QR
            new_register = PublicService.save_register_with_qr(student_name, campus_str, group_str)
            return redirect(url_for('public.my_qr', reg_id=new_register.id))
        
        except ServiceError as e:
            flash(str(e), 'danger')
        
        except Exception as e:
            flash(str(e), 'danger')
            
    return render_template('register.html', form=form)

@bp.route('/download/my_qr/<int:reg_id>')
def my_qr(reg_id):
    registro = PublicService.get_register_by_id(reg_id)
    return render_template('myqr.html', registro=registro)

# La ruta para el JavaScript sigue existiendo para la parte dinámica del cliente
@bp.route('/get_groups_by_plantel/<int:plantel_id>')
def get_groups_by_plantel(plantel_id):
    # Reutilizamos el servicio para el JSON
    grupos = PublicService.get_groups_for_selection(plantel_id)
    # Convertimos las tuplas (id, nombre) a diccionarios para el JS
    return jsonify([{"id": g[0], "name": g[1]} for g in grupos])
