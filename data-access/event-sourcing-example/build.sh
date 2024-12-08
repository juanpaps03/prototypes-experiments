# Build project script

PROJECT=${PWD##*/}
echo "Running build for $PROJECT"

poetry env use $(which python3)
source "$(dirname $(poetry run which python3))/activate"
poetry install --sync

echo "Formatting code"
black . --exclude "/(\.eggs|\.git|\.hg|\.mypy_cache|\.nox|\.tox|\.venv|_build|buck-out|build|dist|bin|lib)/"

echo "Running mypy"
python3 -m mypy --install-types --non-interactive -p $PROJECT

echo "Running pytest"
python3 -m pytest -s

echo "Running behave"
python3 -m behave

poetry build