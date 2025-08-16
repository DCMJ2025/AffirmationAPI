from flask_sqlalchemy import SQLAlchemy
from extensions import db

#db = SQLAlchemy()

class TradeData(db.Model):
    __tablename__ = 'tradedata'  # existing table name
    id = db.Column(db.Integer, primary_key=True)
    insertDate = db.Column(db.DateTime)
    tradeEventDate = db.Column(db.DateTime)
    tradeRef = db.Column(db.String(20))
    amount = db.Column(db.Numeric(20, 10))
    baseEventType = db.Column(db.String(10))
    counterPartyName = db.Column(db.String(250))
    counterPartyEmail = db.Column(db.String(250))
    confirmationType = db.Column(db.String(50))
