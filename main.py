'''
This is the entrypoint of the app
'''
import json

from flask import Flask
from flask import request

from .validator import validate
from .risk_profile import RiskProfileCalculator

app = Flask(__name__)


@app.route('/', methods=['POST'])
def risk():
    data = json.loads(request.data)
    errors = validate(data)
    if errors:
        return {'errors': errors}, 400
    return RiskProfileCalculator(data).calculate()
