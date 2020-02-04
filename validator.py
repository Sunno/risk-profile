import jsonschema


SCHEMA = {
    'type': 'object',
    'required': [
        'age',
        'dependents',
        'house',
        'income',
        'marital_status',
        'risk_questions',
        'vehicle'
    ],
    'properties': {
        'age': {'type': 'integer', 'minimum': 0},
        'dependents': {'type': 'integer', 'minimum': 0},
        'house': {
            'type': ['object'],
            'properties': {
                'ownership_status': {
                    'type': 'string',
                    'enum': ['owned', 'mortgaged']
                }
            }
        },
        'income': {'type': 'integer', 'minimum': 0},
        'marital_status': {'type': 'string'},
        'risk_questions': {
            'type': 'array',
            'maxItems': 3,
            'minItems': 3
        },
        'vehicle': {
            'type': 'object',
            'properties': {
                'year': {'type': 'integer'}
            }
        }
    }
}


def validate(data):
    """
    Returns errors if any
    """
    validator = jsonschema.Draft7Validator(SCHEMA)

    errors = [error.message for error in validator.iter_errors(data)]
    if not errors:
        # here we validate if risk questions is a proper array
        for item in data['risk_questions']:
            if item not in [True, False, 0, 1]:
                errors.append(
                    "'risk_questions' only allow true, false, 0 or 1 values")
                break
    return errors
