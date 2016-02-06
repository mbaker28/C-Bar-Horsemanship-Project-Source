import sys, os
cwd = os.getcwd()
sys.path.append(cwd)
sys.path.append(cwd + '/cb_info_db')

INTERP = os.path.expanduser("~/db.cbarhorsemanship.org/env/bin/python")

if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0,'$HOME/db.cbarhorsemanship.org/env/bin')
sys.path.insert(0,'$HOME/db.cbarhorsemanship.org/env/lib/python3.5/site-packages/django')
sys.path.insert(0,'$HOME/db.cbarhorsemanship.org/env/lib/python3.5/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = "cb_info_db.settings"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
