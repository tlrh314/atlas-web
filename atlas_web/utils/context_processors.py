from django.conf import settings


def settings_context(_request):
    """
    Note that context_processors are processed before every response. Not that if you want
    to make a variable available in every template, then you can pass the variable here
    instead of passing that variable to every template individually via the relevant view.
    """
    return {"DEBUG": settings.DEBUG}
