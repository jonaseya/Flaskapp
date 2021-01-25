
from re import error
import re
from flask import Flask,render_template,url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import redirect, validate_arguments
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, form
from wtforms.fields.core import DateField, DateTimeField, DecimalField, IntegerField
from wtforms.validators import DataRequired, InputRequired, Length, AnyOf, ValidationError
from wtforms.fields.html5 import DateTimeLocalField



app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)



def length(min=-1, max=-1):
    message = 'Must be between %d and %d numbers long.' % (min, max)

    def _length(form, field):
        l = field.data and len(str(field.data)) or 0
        if l < min or max != -1 and l > max:
            raise ValidationError(message)

    return _length



class PaymentForm(FlaskForm): 
    card_holder = StringField('card_holder', validators=[InputRequired(), length(max= 50)]) 
    card_number = IntegerField('card_number', validators=[InputRequired('Credit Card number is required!'),length(min=13, max=16)]) 
    expiration_date =  DateTimeField('expiration_date', format='%Y/%m/%d', validators=[InputRequired()])
    security_code = StringField('security_code', validators=[InputRequired('Credit Card number is required!'),length(min=1, max=3)])
    amount = DecimalField('amount', validators=[InputRequired(),length(min=1)])


class ConformationForm(FlaskForm):
    pass
    
class Todo(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    card_holder = db.Column(db.String, default=0)
    card_number = db.Column(db.Integer, default = 0)
    expiration_date = db.Column(db.Integer,default = 0)
    security_code = db.Column(db.Integer,default = 0)
    amount = db.Column(db.Integer,default = 0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
     
    def __repr__(self):
        return '<Task %r>' %self.id








@app.route('/', methods=['GET','POST'])
def form():
    form = PaymentForm()
    card_holder = request.form.get(' card_holder')
    card_number = request.form.get('card_number')
    expiration_date = request.form.get('expiration_date')
    security_code = request.form.get('security_code')
    amount = request.form.get('amount')
    if form.validate_on_submit():
        new_task = Todo(
                card_holder=card_holder,
                card_number=card_number,
                expiration_date = expiration_date,
                security_code=security_code,
                amount=amount)
        db.session.add(new_task)
        db.session.commit() # save to db
        if float(amount) < 20:
                return cheap_payment_gateway()
        elif 20 < float(amount)<  500:
                return expensive_payment_gateway()
        elif float(amount) > 500:
                return premium_payment_gateway()    
    
    return render_template('form.html', form = form)
    
@app.route('/paynow', methods=['GET','POST'])
def cheap_payment_gateway():
    if request.method == 'GET':
         return "Your payment Has been processed through CheapPaymentGateway"
    return render_template ('paynow.html' )


@app.route('/expensive', methods=['GET','POST'])
def expensive_payment_gateway():
    if request.method == 'GET':
         return "Your payment Has been processed through ExpensivePaymentGateway"
    return render_template ('expensive.html' )

@app.route('/premium', methods=['GET','POST'])    
def premium_payment_gateway():
    if request.method == 'GET':
         return "Your payment Has been processed through PremiumPaymentGateway"
    return render_template ('premium.html' )
    


if __name__=='__main__':
    app.run(debug=True)



