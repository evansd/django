from django.conf import settings
from django.core.management.commands.runserver import (
    Command as RunserverCommand,
)


WHITENOISE_PATH = 'whitenoise.middleware.WhiteNoiseMiddleware'


class Command(RunserverCommand):
    help = "Starts a lightweight Web server for development and also serves static files."

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--nostatic', action="store_false", dest='use_static_handler',
            help='Tells Django to NOT automatically serve static files at STATIC_URL.',
        )
        parser.add_argument(
            '--insecure', action="store_true", dest='insecure_serving',
            help='Allows serving static files even if DEBUG is False.',
        )

    def get_handler(self, *args, **options):
        """
        If static files should be served, inject WhiteNoise into the middleware
        list if it's not already present. Otherwise do nothing and return the
        default handler.
        """
        use_static_handler = options['use_static_handler']
        insecure_serving = options['insecure_serving']
        if use_static_handler and (settings.DEBUG or insecure_serving):
            if WHITENOISE_PATH not in settings.MIDDLEWARE:
                settings.WHITENOISE_USE_FINDERS = True
                settings.WHITENOISE_AUTOREFRESH = True
                settings.MIDDLEWARE.insert(0, WHITENOISE_PATH)
        return super().get_handler(*args, **options)
