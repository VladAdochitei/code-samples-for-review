# Form section
from flask_wtf import FlaskForm 
from wtforms import StringField, DecimalField, SelectField, SubmitField
from decimal import Decimal 
from wtforms.validators import InputRequired, NumberRange 
from flask_wtf.file import FileField, FileRequired, FileAllowed 
from app.models import Category
 
class NameForm(FlaskForm): 
    name = StringField('Name', validators=[InputRequired()])

class CategoryForm(NameForm): 
    submit = SubmitField("Submit")
 
class CategoryField(SelectField): 
    def iter_choices(self): 
        categories = [(c.id, c.name) for c in Category.query.all()] 
        for value, label in categories: 
            yield (value, label, self.coerce(value) == self.data) 
 
    def pre_validate(self, form): 
        for v, _ in [(c.id, c.name) for c in Category.query.all()]: 
            if self.data == v: 
                break 
        else: 
            raise ValueError(self.gettext('Not a valid choice')) 
 
class ProductForm(NameForm): 
    price = DecimalField('Price', validators=[InputRequired(), NumberRange(min=Decimal('0.0'))]) 
    category = CategoryField('Category', validators=[InputRequired()], coerce=int ) 
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField("Submit")

class CheckoutForm(FlaskForm):
    full_name = StringField('Full Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    city = StringField('City', validators=[InputRequired()])
    submit = SubmitField('Checkout')