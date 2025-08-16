from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from tradeDataModels import TradeData
from affirmationDataModels import AffirmationResponse

class AffirmationSchema(SQLAlchemyAutoSchema):
    class Meta:
        #model = TradeData
        models = [TradeData,AffirmationResponse]
        load_instance = True
        