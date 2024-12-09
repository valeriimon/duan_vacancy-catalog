from django.http import HttpRequest

from user.models import UserRole


class Utils:
    @staticmethod
    def html_context(request: HttpRequest, context = {}):
        auth_user = None
        if request.user.is_authenticated:
            auth_user = {
                'email': request.user.email,
                'username': request.user.username,
                'role': str(UserRole.EMPLOYER) if request.user.is_employer() else str(UserRole.JOB_SEEKER)
            }
        return {
            'auth_user': auth_user,
            **context
        }