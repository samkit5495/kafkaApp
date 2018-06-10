from mongoengine import *
from datetime import datetime


class User(Document):
    user_id = IntField(required=True)
    balance = FloatField(required=True)
    avg_transaction_amount = FloatField(required=True)
    stdev = FloatField(required=True)
    avg_monthly_balance = FloatField(required=True)

    
class Transaction(Document):
    user = ReferenceField(User,required=True)
    date = DateTimeField(required=True)
    amount = FloatField(required=True)
    alert = BooleanField(default=False)