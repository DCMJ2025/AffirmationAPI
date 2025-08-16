import os

class JWTConfig:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "mdMjRNpcpk6DqDtb9sFY4wkqtfjHVnEuV")
    JWT_ISSUER = os.getenv("JWT_ISSUER", "affirmation-api")
    JWT_EXPIRATION_SECONDS = int(os.getenv("JWT_EXPIRATION_SECONDS", 3000))  # 1 hour
