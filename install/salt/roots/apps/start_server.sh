#!/bin/sh

ENV_DIR="/home/users/ode_frontend/env"
PROJECT_DIR="/home/users/ode_frontend/django_ode"
. ${ENV_DIR}/bin/activate
cd ${PROJECT_DIR}
${ENV_DIR}/bin/circusd --daemon ${PROJECT_DIR}/circus.ini
