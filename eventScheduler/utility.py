def check_if_fields_are_missing(data, required_fields):
    missing_or_falsy_fields = [field for field in required_fields if data.get(field) is None]
    if missing_or_falsy_fields:
        error_message = f"The following fields are missing or empty: {', '.join(missing_or_falsy_fields)}."
        return {'message': error_message}
    return None
