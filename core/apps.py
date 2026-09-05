from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    
    def ready(self):
        """
        Import signals when Django starts
        """
        try:
            # Import activity logging signals
            import core.activity_logging  # noqa
            print("[OK] Activity logging signals loaded successfully")
        except Exception as e:
            print(f"[ERROR] Error loading activity logging signals: {e}")