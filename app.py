from flask import Flask, jsonify, request
from flask_cors import CORS
from tradeDataModels import db, TradeData
from schemas import AffirmationSchema
from config import Config
from middleware import register_middlewares
from logUtils import setup_logger

from JWTconfig import JWTConfig
from JWTauth import create_token, verify_token



app = Flask(__name__)
app.config.from_object(Config)
app.config.from_object(JWTConfig)
CORS(app)

logger = setup_logger()
register_middlewares(app, logger)

# Initialize DB
db.init_app(app)

# Schemas
affirmations_schema = AffirmationSchema(many=True) # For lists
affirmation_schema = AffirmationSchema()           # For single objects


# ----------- Routes ------------

@app.route("/api/tradedata", methods=["GET"])
def get_trades():
    tradeData = TradeData.query.all()
    return jsonify(affirmations_schema.dump(tradeData))

@app.route("/api/tradedata/<int:id>", methods=["GET"])
def get_trade(id):
    tradeData = TradeData.query.get_or_404(id)
    return jsonify(affirmation_schema.dump(tradeData))

@app.route("/api/tradedata", methods=["POST"])
def create_trade():
    data = request.get_json()
    tradeData = affirmation_schema.load(data)
    db.session.add(tradeData)
    db.session.commit()
    return affirmation_schema.jsonify(tradeData), 201

@app.route("/api/tradedata/<int:trade_id>", methods=["PUT"])
def update_trade(trade_id):
    tradeData = TradeData.query.get_or_404(trade_id)
    data = request.get_json()
    for key, value in data.items():
        setattr(tradeData, key, value)
    db.session.commit()
    return affirmation_schema.jsonify(tradeData)

@app.route("/api/trades/<int:trade_id>", methods=["DELETE"])
def delete_trade(trade_id):
    trade = TradeData.query.get_or_404(trade_id)
    db.session.delete(trade)
    db.session.commit()
    return jsonify({"message": "Trade deleted"}), 200

# Issue JWT Token
@app.route("/api/token", methods=["POST"])
def issue_token():
    try:
        data = request.get_json()
        tradeID = data.get("tradeID")
        if not isinstance(tradeID, int):
            return jsonify({"error": "tradeID must be an integer"}), 400

        token = create_token(tradeID)
        return jsonify({"token": token})
    except Exception as e:
        print("Error in /api/token:", e)
        return jsonify({"error": str(e)}), 500

# Validate JWT Token
@app.route("/api/validate", methods=["POST"])
def validate_token():
    data = request.get_json()
    token = data.get("token")

    if not token:
        return jsonify({"error": "Token is required"}), 400

    result = verify_token(token)

    if isinstance(result, tuple):  # error
        return jsonify(result[0]), result[1]

    return jsonify({"decoded": result})


# ----------- Main ------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Only needed if creating tables manually
    app.run(debug=True)
