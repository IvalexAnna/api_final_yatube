from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее редактировать объект только его автору.
    Остальные пользователи могут только читать.
    """

    def has_permission(self, request, view):
        # Разрешить доступ для всех аутентифицированных пользователей
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Разрешить доступ на чтение для всех
        #if request.method in permissions.SAFE_METHODS:
            #return True
        # Разрешить редактирование только автору объекта
        return obj.author == request.user