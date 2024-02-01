from rest_framework.response import Response
from rest_framework import status

def check_if_fields_are_missing(data,required_fields):
    missing_or_falsy_fields = [field for field in required_fields if not data.get(field)]
    if missing_or_falsy_fields:
        if len(missing_or_falsy_fields) == 1:
            error_message = f"{missing_or_falsy_fields[0]} is missing or empty."
        else:
            error_message = f"The following fields are missing or empty: {', '.join(missing_or_falsy_fields)}."
        return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
    return None