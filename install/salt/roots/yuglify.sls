yuglify:
  cmd.run:
    - name: npm -g install yuglify
    - unless: "test -e /usr/local/bin/yuglify"
