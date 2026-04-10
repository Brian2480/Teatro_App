from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


def strip_value(value):
    return value.strip() if value else value


class RegisterForm(FlaskForm):
    
    student=StringField(
        'Nombre Completo:',
        validators=[
            DataRequired(),
            Length(min=10, max=50)
        ],
        filters=[strip_value]
    )

    plantel=SelectField(
        'Selecciona Plantel', 
        validators=[DataRequired()], 
        coerce=int
    )

    grupo=SelectField(
        'Selecciona Plantel', 
        validators=[DataRequired()], 
        coerce=int
    )


    submit = SubmitField('Obtener QR')