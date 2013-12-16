/home/users:
  file.directory:
    - makedirs: True

{% for app_name, config in pillar.get('apps', {}).items() %}
{{ app_name }}_user:
  user.present:
    - name: {{ app_name }}
    - home: /home/users/{{ app_name }}
    - shell: /bin/bash
  require:
    - directory: /home/users
{% endfor %}
