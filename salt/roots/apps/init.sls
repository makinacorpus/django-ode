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
        - user: ode_frontend
        - group: ode_frontend
        - mode: 600

initapp:
  cmd.run:
    - name: ". ../env/bin/activate
             && python manage.py syncdb --settings=django_ode.settings.local --noinput
             && python manage.py collectstatic --settings=django_ode.settings.local --noinput"
    - cwd: /home/users/ode_frontend/django_ode
    - user: ode_frontend

start_script:
    file.managed:
        - name: /home/users/ode_frontend/django_ode/start_server.sh
        - source: salt://apps/start_server.sh
        - template: jinja
        - user: ode_frontend
        - group: ode_frontend
        - mode: 744

start_circus:
  cmd.run:
    - name: /home/users/ode_frontend/django_ode/start_server.sh
    - user: ode_frontend
  cron.file:
    - name: salt://apps/crontab
    - user: ode_frontend
