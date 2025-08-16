from flask import Flask, jsonify, request
from flask_cors import CORS
from affirmationDataModels import AffirmationResponse
from sqlUtilities import call_add_affirmation_response
from tradeDataModels import  TradeData
from tradeDetailsDataModels import TradeDetails
from datetime import datetime
from schemas import AffirmationSchema
from config import Config
from middleware import register_middlewares
from logUtils import setup_logger
from JWTconfig import JWTConfig
from JWTauth import create_token, verify_token
from extensions import db
import json
from SendEmail import send_email

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

@app.route("/api/sendemail", methods=["POST"])
def sendemail():
    data = request.get_json()
    send_email(data['subject'], data['to_email'], data['html_content_body'])
    return "Email Sent", 201

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


@app.route('/api/insert', methods=['POST'])
def insert_affirmation():
    data = request.get_json()
    
    if not data or 'tradeID' not in data:
        return jsonify({"error": "Missing 'tradeID' in request"}), 400

    trade_id = data['tradeID']

    try:
        call_add_affirmation_response(trade_id)
        return jsonify({"message": f"Stored procedure executed for tradeID {trade_id}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/affirmations/<int:trade_id>', methods=['GET'])
def get_affirmations_by_trade_id(trade_id):
    try:
        responses = AffirmationResponse.query.filter_by(TradeId_PK=trade_id).all()
        result = []

        for row in responses:
            result.append({
                "Id": row.Id,
                "InsertionDate": row.InsertionDate.strftime("%Y-%m-%d %H:%M:%S") if row.InsertionDate else None,
                "KeyData": row.KeyData,
                "ValueData": row.ValueData,
                "Approve": bool(row.Approve),
                "Reject": bool(row.Reject),
                "RejectComment": row.RejectComment,
                "Comment": row.Comment,
                "TradeId_PK": row.TradeId_PK,
                "FinalResult": str(row.FinalResult),
                "UserName": row.UserName,
                "UserEmail": row.UserEmail,
                "UpdatedDate": row.UpdatedDate.strftime("%Y-%m-%d %H:%M:%S") if row.UpdatedDate else None
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/update-affirmations', methods=['POST'])
def update_affirmation_responses():
    data = request.get_json()
    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of updates"}), 400

    try:
        for item in data:
            row_id = item.get("Id")
            if not row_id:
                continue  # or handle missing Id

            # Fetch the existing row
            response = AffirmationResponse.query.get(row_id)
            if not response:
                continue  # or collect missing rows

            # Update only provided fields
            for field in ["Approve", "Reject", "RejectComment", "Comment", "UserName", "UserEmail","FinalResult"]:
                if field in item:
                    setattr(response, field, item[field])

        db.session.commit()
        return jsonify({"message": "Updates applied successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/tradedetails', methods=['POST'])
def add_trade():
    raw_data = request.get_json()
    data = json.loads(raw_data)
    try:
        trade = TradeDetails(
            insertiondate=datetime.utcnow(),  # override default
            tradeid=data.get('tradeid'),
            version=data.get('version'),
            Confirmation=data.get('Confirmation'),
            Nominal=data.get('Nominal'),
            Ccy=data.get('Ccy'),
            Sccy=data.get('Sccy'),
            SecurityData=data.get('SecurityData'),
            EventData=data.get('EventData'),
            Eventtype=data.get('Eventtype'),
            Productcategory=data.get('Productcategory'),
            Product=data.get('Product'),
            Asset=data.get('Asset'),
            Rate=data.get('Rate'),
            TD=data.get('TD'),
            OED=data.get('OED'),
            Cptycode=data.get('Cptycode'),
            CptyName=data.get('CptyName'),
            Party1=data.get('Party1'),
            Party2=data.get('Party2'),
            Party2email=data.get('Party2email'),
            Region=data.get('Region')
        )

        db.session.add(trade)
        db.session.commit()

        return jsonify({
            "message": "Trade inserted successfully",
            "trade_id": trade.ID
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



# ----------- Main ------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Only needed if creating tables manually
    app.run(debug=True)
