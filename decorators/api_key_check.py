# -*- coding: utf-8 -*-
"""
"""

from functools import wraps
from flask import request

from flask_api_key.utils import get_ext_config

from flask_api_key.exceptions import LocationNotImplemented, AuthorizationHeaderMissing, WrongAuthHeaderType, HeaderMissingAPIKey, HeaderContainsExcessParts, InvalidAPIKey
from flask_api_key.api_key_manager import APIKeyManager
from flask_api_key.api_key import APIKey
from config import config
from models.metadata.metadata_models import Source

def api_key_check():
    def api_key_check_fn(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            cfg = get_ext_config()
            app_name = config["application"].get("app_name")
            # if not litterbux skip api check
            if app_name != Source.litterbux:
                return func(*args, **kwargs)
            
            auth = request.headers.get('X-API-KEY', None)
            if not auth:
                raise AuthorizationHeaderMissing()
            
            unverified_key = auth
            legit = APIKey().verify_key(unverified_key)
            if not legit:
                raise InvalidAPIKey()

            return func(*args, **kwargs)
            
        return decorated_function
    
    return api_key_check_fn
