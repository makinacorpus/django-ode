/home/users:
  file.directory:
    - makedirs: True

ode_user:
  user.present:
    - name: ode
    - home: /home/users/ode
  require:
    - directory: /home/users
