# Build project script

PROJECT=${PWD##*/}
echo "Running build for $PROJECT"


poetry env use $(which python3)
source "$(dirname $(poetry run which python3))/activate"
poetry install --sync

poetry build