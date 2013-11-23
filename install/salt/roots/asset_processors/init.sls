nodejs:
  cmd.script:
    - source: salt://scripts/install_nodejs.sh
    - user: root
    - shell: /bin/bash
    - unless: "test -e /usr/local/bin/node"

less:
  cmd.run:
    - name: npm -g install less
    - unless: "test -e /usr/local/bin/lessc"

yuglify:
  cmd.run:
    - name: npm -g install yuglify
    - unless: "test -e /usr/local/bin/yuglify"
