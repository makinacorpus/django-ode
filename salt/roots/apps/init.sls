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
            endpoint_port: {{ pillar['apps']['ode_frontend']['circus_port'] }}
            pubsub_endpoint_port: 55556
            stats_endpoint_port: 55557
            wsgi_application: django_ode.wsgi.application


api_circus_conf:
    file.managed:
        - name: /home/users/ode_api/ode/circus.ini
        - source: salt://apps/circus.ini
        - template: jinja
        - context:
            port: {{ pillar['apps']['ode_api']['port'] }}
            endpoint_port: {{ pillar['apps']['ode_api']['circus_port'] }}
            pubsub_endpoint_port: 56556
            stats_endpoint_port: 56557
            wsgi_application: wsgi.application


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
            admins: "{% for admin in pillar.get('admins', []) %}\"{{ admin["email"] }}\",{% endfor %}"


init_dependencies:
  cmd.run:
    - name: "npm install -g grunt"


init_frontend:
  cmd.run:
    - name: ". ../env/bin/activate
             && export DJANGO_SETTINGS_MODULE=django_ode.settings.local
	     && make production"
    - cwd: {{ pillar['apps']['ode_frontend']['project_dir'] }}
    - user: ode_frontend


init_api:
  cmd.run:
    - name: ". ../env/bin/activate
             && make production"
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
            circus_port: {{ config['circus_port'] }}


start_{{ app_name }}:
  cmd.run:
    - name: {{ config['project_dir'] }}/start_server.sh
    - user: {{ app_name }}
  cron.file:
    - name: salt://apps/crontab
    - user: {{ app_name }}
    - template: jinja
    - context:
        project_dir: {{ config['project_dir'] }}
        env_dir: {{ config['env_dir'] }}
        harvest: {{ app_name == 'ode_api' }}

{% endfor %}
