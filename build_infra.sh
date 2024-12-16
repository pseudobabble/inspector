set -e

python infrastructure/setup.py bdist_wheel && cp dist/infrastructure-1.0.0-py3-none-any.whl training-ucd/ && docker compose up -d --build training-ucd
