from flask import request
import time
#import logging

def register_middlewares(app, logger):
    @app.before_request
    def before_request_func():
        request.start_time = time.time()

    @app.after_request
    def after_request_func(response):
        duration = time.time() - request.start_time
        logger.info(f"{request.method} {request.path} {response.status_code} {duration:.4f}s")
        return response

    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.exception(f"Unhandled Exception: {str(e)}")
        return {"error": "Internal Server Error"}, 500