database:
    username: ode
    name: ode
    password: <secret password>


apps:
    ode_frontend:
        repository: https://github.com/makinacorpus/django-ode
        target: django_ode
        port: 8001
        circus_port: 55555
        project_dir: /home/users/ode_frontend/django_ode
        env_dir: /home/users/ode_frontend/env
        static_root: /home/users/ode_frontend/static/
        secret_key: <secret key>
    ode_api:
        project_dir: /home/users/ode_api/ode
        env_dir: /home/users/ode_api/env
        repository: https://github.com/makinacorpus/ODE
        target: ode
        port: 8002
        circus_port: 56555

server_name: <production server>

default_from_email: <from email address>

admins:
    - name: Alex Marandon
      email: <admin email address>


allowed_hosts:
    - localhost
    - <production server>

moderator_emails:
    - <moderator email adress>
