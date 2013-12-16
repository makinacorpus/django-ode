nodejs:
  cmd.script:
    - source: salt://scripts/install_nodejs.sh
    - user: root
    - shell: /bin/bash
    - unless: "test -e /usr/bin/node"

less:
  cmd.run:
    - name: npm -g install less
    - unless: "test -e /usr/bin/lessc"

less:
  cmd.run:
    - name: npm -g install grunt-cli
    - unless: "test -e /usr/bin/grunt"
