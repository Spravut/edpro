# main/context_processors.py

def user_role(request):
    if request.user.is_authenticated:
        is_tutor = hasattr(request.user, 'tutor_profile')
    else:
        is_tutor = False
    return {'is_tutor': is_tutor}