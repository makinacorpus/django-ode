{% for app_name, config in pillar.get('apps', {}).items() %}
{{ app_name }}_repository:
    git.latest:
        - name: {{ config['repository'] }}
        - target: /home/users/{{ app_name }}/{{ config['target'] }}
        - user: {{ app_name }}
{% endfor %}
