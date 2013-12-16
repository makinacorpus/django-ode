nginx:           # ID declaration
  pkg:                # state declaration
    - installed       # function declaration
  service:
    - running
    - watch:
      - pkg: nginx
      - file: /etc/nginx/nginx.conf

nginx.conf:
  file.managed:
    - name: /etc/nginx/nginx.conf
    - source: salt://nginx/nginx.conf
    - template: jinja
