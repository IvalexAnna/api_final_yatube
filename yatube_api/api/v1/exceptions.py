from rest_framework.exceptions import APIException


class CustomPermissionDenied(APIException):
    status_code = 403
    default_detail = "У вас нет прав для выполнения этого действия."
    default_code = "permission_denied"
