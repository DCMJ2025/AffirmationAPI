from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from tradeDataModels import TradeData

class AffirmationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TradeData
        load_instance = True
