from django.core.exceptions import ValidationError

import jsonschema


def validate_polygon_points(value):
    try:
        jsonschema.validate(value, {
            "type": "array",
            "minItems": 4,
            "items": {
                "type": "array",
                "minItems": 2,
                "maxItems": 2,
                "prefixItems": [
                    {
                        "type": "number",
                        "minimum": -180,
                        "maximum":  180
                    },
                    {
                        "type": "number",
                        "minimum": -90,
                        "maximum":  90
                    }
                ]
            }
        })
    except jsonschema.exceptions.ValidationError:
        raise ValidationError('JSON is not of the form [[lon, lat], ...] with at least 4 items.')
