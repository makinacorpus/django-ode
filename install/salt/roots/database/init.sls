postgresql:
  pkg.installed

{% for app_name, config in pillar.get('apps', {}).items() %}
{{ app_name }}_database_user:
    postgres_user.present:
        - name: {{ app_name }}
        - password: {{ config['dbpassword'] }}
        - require:
            - pkg: postgresql

{{ app_name }}_database:
  postgres_database.present:
    - name: {{ app_name }}
    - encoding: utf8
    - template: template0
    - owner: {{ app_name }}
    - require:
        - postgres_user: {{ app_name }}_database_user
{% endfor %}
