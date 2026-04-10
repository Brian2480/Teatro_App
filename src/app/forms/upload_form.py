from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

class FileForm(FlaskForm):

    file = FileField(
        'Selecciona el PDF',
        validators=[
            FileRequired(),
            FileAllowed(['pdf'], "Solo se aceptan archivos PDF")
        ]
    )

    submit = SubmitField('Subir')