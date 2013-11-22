less:
  cmd.run:
    - name: npm -g install less
    - unless: "test -e /usr/local/bin/lessc"
