from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SelectField, SubmitField, FloatField, BooleanField
from wtforms.fields.core import BooleanField
from wtforms.validators import DataRequired, Length

class MovimientosForm(FlaskForm):
    fecha = DateField("Fecha", validators=[DataRequired()]) #Datefield es una clase de wtforms
    concepto = StringField("Concepto", validators = [DataRequired(), Length(min=10)])
    categoria = SelectField("Categoria", choices=[('SU', 'Supervivencia'), ('OV', 'Ocio/Vicio'),
                        ('CU', 'Cultura'), ('EX', 'Extras')])
    cantidad = FloatField("Cantidad", validators = [DataRequired()])
    esGasto = BooleanField("Es gasto")
    submit = SubmitField('Aceptar')

