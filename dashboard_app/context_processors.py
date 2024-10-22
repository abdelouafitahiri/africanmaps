from django.contrib.auth.models import User

def user_context(request):
    user = request.user
    return {
        'username': user.username if user.is_authenticated else 'Invité',
        'role': 'Administrateur' if user.is_staff else 'Utilisateur',
    }
