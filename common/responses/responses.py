from rest_framework.response import Response

def success_response(data : any = None, status_code : int =200):
    """Return a standardized success response."""
    return Response(
        {
            "is_ok": True,
            "error": "",
            "data": data,
        },
        status=status_code,
    )


def error_response(message : str, status_code : int =400):
    """Return a standardized error response."""
    return Response(
        {
            "is_ok": False,
            "error": message,
            "data": None,
        },
        status=status_code,
    )
