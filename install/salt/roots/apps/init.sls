{% for app_name, config in pillar.get('apps', {}).items() %}

{{ app_name }}_repository:
    git.latest:
        - name: {{ config['repository'] }}
        - target: /home/users/{{ app_name }}/{{ config['target'] }}
        - user: {{ app_name }}

/home/users/{{ app_name }}/env:
    virtualenv.managed:
        - no_site_packages: True
        - runas: {{ app_name }}
        - requirements: /home/users/{{ app_name }}/{{ config['target'] }}/requirements.txt

{% endfor %}
