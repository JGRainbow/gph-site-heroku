from .base import *

DEBUG = False

IS_TEST = False

# Used for constructing URLs; include the protocol and trailing
# slash (e.g. 'https://galacticpuzzlehunt.com/')
DOMAIN = 'FIXME'

# List of places you're serving from, e.g.
# ['galacticpuzzlehunt.com', 'gph.example.com']; or just ['*']
ALLOWED_HOSTS = ['*']

# Google Analytics
GA_CODE = '''
<script>
  /* FIXME */
</script>
'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dcq49ipe4g98kd',
        'USER': 'fqvqdqmgeggofq',
        'PASSWORD': '50405005308eb6a0186d7d89fee482f0dcac5c2b62f95d4886a339b4a0c334c3',
        'HOST': 'ec2-34-250-252-161.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
    }
}