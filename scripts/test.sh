#!/usr/bin/env bash

set -e
set -x

bash ./scripts/lint.sh
coverage run --source=poetry_version_plugin,tests -m pytest "${@}"
coverage combine
coverage xml
