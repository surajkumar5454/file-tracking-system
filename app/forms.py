from wtforms import Form, StringField, TextAreaField, SelectField, DecimalField, PasswordField
from wtforms.validators import DataRequired, NumberRange

class LoginForm(Form):
    username = SelectField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class ProposalForm(Form):
    file_number = StringField('File Number', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    department = StringField('Department', validators=[DataRequired()])
    estimated_cost = DecimalField('Estimated Cost', validators=[DataRequired(), NumberRange(min=0)])
    priority = SelectField('Priority', choices=[
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], default='normal') 