python3:
  cmd.script:
    - source: salt://scripts/install_python3.3.sh
    - user: root
    - shell: /bin/bash
    - unless: "test -e /usr/local/bin/python3.3"
