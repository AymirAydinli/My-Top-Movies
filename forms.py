from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, URLField
from wtforms.validators import DataRequired


class MovieEditForm(FlaskForm):
    rating = SelectField('Rating', validators=[DataRequired()], choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    review = StringField('Review', validators=[DataRequired()])
    submit = SubmitField(label='Update')


class MovieAddForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField(label='Add Movie')
