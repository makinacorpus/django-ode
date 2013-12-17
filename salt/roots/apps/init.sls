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


frontend_circus_conf:
    file.managed:
        - name: /home/users/ode_frontend/django_ode/circus.ini
        - source: salt://apps/circus.ini
        - template: jinja
        - context:
            port: {{ pillar['apps']['ode_frontend']['port'] }}
            endpoint_port: 5555
            pubsub_endpoint_port: 5556
            stats_endpoint_port: 5557


api_circus_conf:
    file.managed:
        - name: /home/users/ode_api/ode/circus.ini
        - source: salt://apps/circus.ini
        - template: jinja
        - context:
            port: {{ pillar['apps']['ode_api']['port'] }}
            endpoint_port: 6555
            pubsub_endpoint_port: 6556
            stats_endpoint_port: 6557


frontend_settings:
    file.managed:
        - name: {{ pillar['apps']['ode_frontend']['project_dir'] }}/django_ode/settings/local.py
        - source: salt://apps/local_settings.py
        - template: jinja
        - user: ode_frontend
        - group: ode_frontend
        - mode: 600


api_settings:
    file.managed:
        - name: {{ pillar['apps']['ode_api']['project_dir'] }}/production.ini
        - source: salt://apps/production.ini
        - template: jinja
        - user: ode_api
        - group: ode_api
        - mode: 600
        - context:
            database: {{ pillar['database'] }}


init_frontend:
  cmd.run:
    - name: ". ../env/bin/activate
             && npm install
             && grunt
             && export DJANGO_SETTINGS_MODULE=django_ode.settings.local
             && python manage.py syncdb --noinput
             && python manage.py collectstatic --noinput
             && python manage.py compilemessages -l fr"
    - cwd: {{ pillar['apps']['ode_frontend']['project_dir'] }}
    - user: ode_frontend


init_api:
  cmd.run:
    - name: ". ../env/bin/activate
             && python setup.py develop
	     && ../env/bin/initialize_ode_db production.ini
             && python setup.py compile_catalog -l fr"
    - cwd: {{ pillar['apps']['ode_api']['project_dir'] }}
    - user: ode_api


{% for app_name, config in pillar.get('apps', {}).items() %}

{{ app_name }}_start_script:
    file.managed:
        - name: {{ config['project_dir'] }}/start_server.sh
        - source: salt://apps/start_server.sh
        - template: jinja
        - mode: 744
        - user: {{ app_name }}
        - group: {{ app_name }}
        - context:
            env_dir: {{ config['env_dir'] }}
            project_dir: {{ config['project_dir'] }}


start_{{ app_name }}:
  cmd.run:
    - name: {{ config['project_dir'] }}/start_server.sh
    - user: {{ app_name }}
  cron.file:
    - name: salt://apps/crontab
    - user: {{ app_name }}
    - context:
        project_dir: {{ config['project_dir'] }}

{% endfor %}
