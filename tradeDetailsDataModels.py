from flask_sqlalchemy import SQLAlchemy
from extensions import db
from datetime import datetime
 

class TradeDetails(db.Model):
    __tablename__ = 'tradedetails'
    ID = db.Column(db.Integer, primary_key=True)
    insertiondate = db.Column(db.DateTime, default=datetime.utcnow)
    tradeid = db.Column(db.String(50))
    version = db.Column(db.Integer)
    Confirmation = db.Column(db.String(50))
    Nominal = db.Column(db.BigInteger)
    Ccy = db.Column(db.String(10))
    Sccy = db.Column(db.String(10))
    SecurityData = db.Column(db.String(50))
    EventData = db.Column(db.String(50))
    Eventtype = db.Column(db.String(50))
    Productcategory = db.Column(db.String(50))
    Product = db.Column(db.String(50))
    Asset = db.Column(db.String(50))
    Rate = db.Column(db.Float)
    TD = db.Column(db.DateTime)
    OED = db.Column(db.DateTime)
    Cptycode = db.Column(db.String(50))
    CptyName = db.Column(db.String(100))
    Party1 = db.Column(db.String(50))
    Party2 = db.Column(db.String(50))
    Party2email = db.Column(db.String(100))
    Region = db.Column(db.String(50))