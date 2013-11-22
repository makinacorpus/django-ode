nodejs:
  cmd.script:
    - source: salt://scripts/install_nodejs.sh
    - user: root
    - shell: /bin/bash
    - unless: "test -e /usr/local/bin/node"
