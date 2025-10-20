import os
from django.apps import AppConfig

class HangarinConfig(AppConfig):
    name = 'hangarin'
    verbose_name = 'Hangarin'

    def ready(self):
        # Create/update the django.contrib.sites Site row matching SITE_ID after apps are loaded.
        # This is safe: it will silently skip if the DB/migrations aren't ready.
        try:
            from django.conf import settings
            from django.contrib.sites.models import Site
            from django.db.utils import OperationalError, ProgrammingError

            site_id = getattr(settings, 'SITE_ID', 1)
            site_domain = os.environ.get('SITE_DOMAIN') or (settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost:8000')
            site_name = os.environ.get('SITE_NAME', 'Hangarin')

            Site.objects.update_or_create(pk=site_id, defaults={'domain': site_domain, 'name': site_name})
        except (OperationalError, ProgrammingError, Exception):
            # DB not ready or other error — skip. After running migrations you can re-check the Site.
            pass


