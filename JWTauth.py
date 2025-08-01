import jwt
import datetime
from flask import current_app



def create_token(tradeID: int):
    now = datetime.datetime.now()
    exp = now + datetime.timedelta(seconds= current_app.config['JWT_EXPIRATION_SECONDS'])

    payload = {
        "sub":  str(tradeID),
        "iss": current_app.config["JWT_ISSUER"],
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp())
    }

    print("Payload:", payload)

    token = jwt.encode(
        payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256"
    )
    print("Token:", token)

    return token

def verify_token(token: str):
    print("Current UTC at verify:", datetime.datetime.utcnow())
    try:
        decoded = jwt.decode(
            token,
            current_app.config["JWT_SECRET_KEY"],
            algorithms=["HS256"],
            issuer=current_app.config["JWT_ISSUER"]
            #leeway=600  # allow 60 seconds clock skew
        )
        return decoded
    except jwt.ExpiredSignatureError as e:
        print("ExpiredSignatureError:", e)
        return {"error": "Token has expired"}, 401
    except jwt.InvalidTokenError as e:
        print("InvalidTokenError:", e)
        return {"error": "Invalid token"}, 401


