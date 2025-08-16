from flask_sqlalchemy import SQLAlchemy
from extensions import db

class AffirmationResponse(db.Model):
    __tablename__ = 'affirmationresponse'  # existing table name
    Id = db.Column(db.Integer, primary_key=True)
    InsertionDate = db.Column(db.DateTime)
    KeyData = db.Column(db.String( 255))
    ValueData = db.Column(db.String(255))    
    Approve = db.Column(db.Boolean)
    Reject = db.Column(db.Boolean)  
    RejectComment = db.Column(db.String(1000))
    Comment = db.Column(db.String(1000))
    TradeId_PK = db.Column(db.Integer, db.ForeignKey('tradedata.id'))
    FinalResult = db.Column(db.String(100))
    UserName = db.Column(db.String(255))    
    UserEmail = db.Column(db.String(255))
    UpdatedDate = db.Column(db.DateTime)
