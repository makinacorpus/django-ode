#!/bin/sh

ENV_DIR={{ env_dir }}
PROJECT_DIR={{ project_dir }}
. ${ENV_DIR}/bin/activate
cd ${PROJECT_DIR}

#${ENV_DIR}/bin/circusctl quit --waiting || echo No circusd running
if ${ENV_DIR}/bin/circusctl --endpoint tcp://127.0.0.1:{{ circus_port }} status
then
    ${ENV_DIR}/bin/circusctl --endpoint tcp://127.0.0.1:{{ circus_port }} restart
else
    ${ENV_DIR}/bin/circusd --daemon ${PROJECT_DIR}/circus.ini
fi