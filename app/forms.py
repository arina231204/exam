from flask_wtf import FlaskForm
import wtforms as ws

from app import app, Employee, User


class EmployeeForm(FlaskForm):
    fullname = ws.StringField('ФИО', validators=[ws.validators.DataRequired(), ])
    phone = ws.StringField('Номер телефона', validators=[ws.validators.DataRequired(),
                                                      ws.validators.Length(min=13, max=13)])
    short_info = ws.TextAreaField('Краткая инф. о кандидате')
    experience =  ws.IntegerField('Опыт', validators=[ws.validators.DataRequired(),])
    preferred_position = ws.StringField('Предпочитаемая позиция')
    submit = ws.SubmitField('Сохранить')
    username = ws.SelectField(User)

    def validate(self):

        if not super().validate():
            return False

        error_counter = 0

        names_split = self.fullname.data.split()
        if len(names_split) == 1:
            self.fullname.errors.append('В фио не должно быть 1 слово')
            error_counter += 1


        if error_counter == 0:
            return True
        else:
            return False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_choices = []
        with app.app_context():
            for user in User.query.all():
                self.user_choices.append((user.username, user.username))

        self._fields['username'].choices = self.user_choices



class UserForm(FlaskForm):
    username = ws.StringField('Имя пользователя', validators=[ws.validators.DataRequired(),
                                                              ws.validators.Length(min=4, max=20)])
    password = ws.PasswordField('Пароль', validators=[ws.validators.DataRequired(),
                                                      ws.validators.Length(min=8, max=24)])