import importlib

try:
    jnius = importlib.import_module('jnius')
    autoclass = getattr(jnius, 'autoclass')
    cast = getattr(jnius, 'cast')
except Exception:
    # Lightweight stubs for development / static analysis so the module missing
    # doesn't raise import errors outside an Android environment.
    class _JniusDummy:
        def __init__(self, *args, **kwargs):
            pass
        def __getattr__(self, name):
            return self
        def __call__(self, *args, **kwargs):
            return self
    def autoclass(name):
        return _JniusDummy()
    def cast(typ, obj):
        return obj

def kirim_via_whatsapp(self, pesan):
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')

    intent = Intent()
    intent.setAction(Intent.ACTION_SEND)
    intent.setType("text/plain")
    intent.putExtra(Intent.EXTRA_TEXT, pesan)
    package = "com.whatsapp"
    intent.setPackage(package)

    currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
    currentActivity.startActivity(intent)
