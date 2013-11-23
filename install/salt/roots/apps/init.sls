{% for app_name, config in pillar.get('apps', {}).items() %}

{{ app_name }}_repository:
    git.latest:
        - name: {{ config['repository'] }}
        - target: /home/users/{{ app_name }}/{{ config['target'] }}
        - user: {{ app_name }}

/home/users/{{ app_name }}/env:
    virtualenv.managed:
        - no_site_packages: True
        - user: {{ app_name }}
        - requirements: /home/users/{{ app_name }}/{{ config['target'] }}/requirements.txt

{% endfor %}

circus.ini:
    file.managed:
        - name: /home/users/ode_frontend/django_ode/circus.ini
        - source: salt://apps/circus.ini
        - template: jinja

ode_frontend_settings:
    file.managed:
        - name: /home/users/ode_frontend/django_ode/django_ode/settings/local.py
        - source: salt://apps/local_settings.py
        - template: jinja
