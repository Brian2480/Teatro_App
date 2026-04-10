from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required

from src.app.services import FileService, GroupsService, ServiceError, RegisterService
from src.app.forms.upload_form import FileForm
from src.app.extension import db

bp = Blueprint('admin_panel', __name__, url_prefix='/admin_panel')


@bp.route('/registers')
@login_required
def show_registers():
    try:

        registers = RegisterService.get_all()
        return render_template('admin/registers.html', registers=registers)

    except ServiceError as e:
        flash(str(e), 'danger' )
        return render_template('admin/registers.html', registers=[])


@bp.route('/delete/registers', methods=['POST'])
@login_required
def delete_registers():
    try: 
        RegisterService.delete_all()
    
    except ServiceError as e:
        flash(str(e), 'danger')
    
    return redirect(url_for('admin_panel.show_registers'))


@bp.route('/show/groups')
@login_required
def show_groups():
    plantels = GroupsService.show()
    return render_template('admin/groups.html', plantels=plantels)


@bp.route('/save/groups', methods=['POST'])
@login_required
def save_groups():
    
    nombre_plantel = request.form.get('plantel')
    lista_nombres_grupos = request.form.getlist('name_group[]')

    try:

        GroupsService.save(
            nombre_plantel=nombre_plantel,
            lista_nombres_grupos=lista_nombres_grupos
            )
        
        flash('Registro exitoso', 'success')
        return redirect(url_for('admin_panel.show_groups'))
        
    except ServiceError as e:
        flash(str(e), 'danger')
        return render_template('admin/groups.html')


@bp.route('/delete/groups/<int:plantel_id>', methods=['POST'])
@login_required
def delete_groups(plantel_id):
    try:
        GroupsService.delete(plantel_id=plantel_id)
        flash('Plantel eliminado','success')

        return redirect(url_for('admin_panel.show_groups'))
    
    except ServiceError as e:
        flash(str(e), 'danger')
        return redirect(url_for('admin_panel.show_groups'))


@bp.route('/upload/files', methods=['GET','POST'])
@login_required
def upload_files():
    form = FileForm()
    questionnaries = FileService.get_all()

    if form.validate_on_submit():
        
        pdf_file = form.file.data

        try:
            FileService.upload_files(file_data=pdf_file)
            flash("!Archivo subido exitosamente¡", 'success')
            return redirect(url_for('admin_panel.upload_files'))
        
        except ServiceError as e:
            flash(str(e), 'danger')
            return redirect(url_for('admin_panel.upload_files'))

    return render_template('admin/upload.html', form=form, files=questionnaries)


@bp.route('/delete/files/<int:file_id>', methods=['POST'])
@login_required
def delete_files(file_id):

    try:
        FileService.delete_files(file_id=file_id)
        flash(f"Eliminado con exito",'success')

    except ServiceError as e:
        flash(str(e), 'danger')
    
    return redirect(url_for('admin_panel.upload_files'))


@bp.route('/edit/groups/<int:plantel_id>', methods=['GET', 'POST'])
@login_required
def edit_groups(plantel_id):
    # La ruta le pregunta al servicio, no a la DB directamente
    plantel = GroupsService.get_by_id(plantel_id)
    
    if not plantel:
        flash("Plantel no encontrado", "danger")
        return redirect(url_for('admin_panel.show_groups'))

    if request.method == 'POST':
        nuevo_nombre = request.form.get('plantel')
        lista_grupos = request.form.getlist('name_group[]')
        
        try:
            GroupsService.update_groups(plantel_id, nuevo_nombre, lista_grupos)
            flash("¡Actualizado con éxito!", "success")
            return redirect(url_for('admin_panel.show_groups'))
        
        except ServiceError as e:
            flash(str(e), "danger")

    return render_template('admin/edit.html', plantel=plantel)


@bp.route('/download/table')
@login_required
def download_table():
    try:

        excel_data = RegisterService.download_excel()
        
        return send_file(
            excel_data,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='Registro_Alumnos.xlsx'
        )
    
    except ServiceError as e:
        flash(str(e), 'danger')
    
    return render_template('si.html')
