from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SelectField, SubmitField, FloatField, BooleanField
from wtforms.fields.core import BooleanField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import date

def fecha_por_debajo_de_hoy(formulario, campo):
    hoy = date.today()
    if campo.data > hoy:
        raise ValidationError('La fecha introducida no pude ser mayor que {}'.format(hoy))

class MovimientosForm(FlaskForm):
    fecha = DateField("Fecha", validators=[DataRequired(message="Insertar una fecha válida"), fecha_por_debajo_de_hoy]) #Datefield es una clase de wtforms
    concepto = StringField("Concepto", validators = [DataRequired(), Length(min=10)])
    categoria = SelectField("Categoria", choices=[('00', ''), ('SU', 'Supervivencia'), ('OV', 'Ocio/Vicio'),
                        ('CU', 'Cultura'), ('EX', 'Extras')])
    cantidad = FloatField("Cantidad", validators = [DataRequired()])
    esGasto = BooleanField("Es gasto")
    submit = SubmitField('Aceptar')

