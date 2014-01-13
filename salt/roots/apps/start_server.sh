#!/bin/sh

ENV_DIR={{ env_dir }}
PROJECT_DIR={{ project_dir }}
. ${ENV_DIR}/bin/activate
cd ${PROJECT_DIR}
${ENV_DIR}/bin/circusctl restart || ${ENV_DIR}/bin/circusd --daemon ${PROJECT_DIR}/circus.ini
