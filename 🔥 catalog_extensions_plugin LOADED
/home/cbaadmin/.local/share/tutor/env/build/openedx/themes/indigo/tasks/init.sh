# Assign themes only if no other theme exists yet
./manage.py lms shell -c "
import sys
from django.contrib.sites.models import Site
def assign_theme(domain):
    site, _ = Site.objects.get_or_create(domain=domain)
    if not site.themes.exists():
        site.themes.create(theme_dir_name='indigo')

assign_theme('www.myopenedx.com')
assign_theme('www.myopenedx.com')
assign_theme('www.myopenedx.com:8000')
assign_theme('studio.www.myopenedx.com')
assign_theme('studio.www.myopenedx.com:8001')
"