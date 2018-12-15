from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextAreaField, IntegerField
from wtforms.validators import DataRequired

# Kullanıcı giriş formu

class LoginForm(Form):
    email = StringField("Email", validators=[validators.Email(message="Lütfen Geçerli Bir Email Adresi Girin")])
    password = PasswordField("Parola", validators=[validators.DataRequired(message="Lütfen Bu Alanı Doldurun")])

# Kullanıcı kayıt formu

class RegisterForm(Form):
    email = StringField("Email", validators=[validators.Email(message="Lütfen Geçerli Bir Email Adresi Girin")])
    password = PasswordField("Parola", validators=[
        validators.DataRequired(message="Lütfen Bu Alanı Doldurun"),
        validators.EqualTo(fieldname="confirm", message="Parolalarınız Uyuşmuyor")
    ])
    confirm = PasswordField("Parola Doğrula", validators=[validators.DataRequired(message="Lütfen Bu Alanı Doldurun")])

# Müşteri kayıt formu

class CustomerForm(Form):
    name = StringField("Ad", validators=[validators.Length(min=3, max=25), validators.DataRequired(message="Lütfen Bu Alanı Doldurun")])
    email = StringField("Email", validators=[validators.Email(message="Lütfen Geçerli Bir Email Adresi Girin")])
    tel = IntegerField("Telefon", validators=[validators.DataRequired(message="Lütfen Bu Alanı Doldurun")])