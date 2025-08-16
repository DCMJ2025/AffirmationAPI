from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from extensions import db
from sqlalchemy import text

def call_add_affirmation_response(trade_id):
    try:
        with db.engine.begin() as conn:
            conn.execute(text("CALL AddAffirmationResponse(:tradeID)"),{"tradeID": trade_id})
    except Exception as e:
        print("Error calling stored procedure:", e)