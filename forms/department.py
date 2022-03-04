from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    title = StringField("Title of Departments", validators=[DataRequired()])
    chief = IntegerField("Chief id", validators=[DataRequired()])
    members = StringField("Members")
    email = EmailField("Departments Email", validators=[DataRequired()])
    submit = SubmitField("Submit")