postgresql:
  pkg.installed

database_user:
    postgres_user.present:
        - name: {{ pillar['database']['username'] }}
        - password: {{ pillar['database']['password'] }}
        - require:
            - pkg: postgresql

database:
    postgres_database.present:
        - name: {{ pillar['database']['name'] }}
        - encoding: utf8
        - template: template0
        - owner: {{ pillar['database']['username'] }}
        - require:
            - postgres_user: database_user
