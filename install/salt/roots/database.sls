database:
  postgres_database.present:
    - name: ode
    - encoding: utf8
    - template: template0
    - owner: ode
