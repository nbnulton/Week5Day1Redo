from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired, EqualTo, ValidationError
from .models import User

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('Password')])
    submit = SubmitField('Register')

            # MUST BE LIKE THIS VALIDATE_FIELDNAME
    def validate_email(form, field):                                # give only the first result returns one user object
        same_email_user = User.query.filter_by(email = field.data).first()
                            # SELECT * FROM user WHERE email = ???
                            # filter_by always gives list
        if same_email_user:
            raise ValidationError("Email is already in use")