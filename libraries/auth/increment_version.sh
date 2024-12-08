if [ $1 ]; then
  if ! poetry version $1
  then
    echo "Wrong option, use: patch, minor, major, prepatch, preminor, premajor, prerelease."
  fi
  exit 16
else
  poetry version patch
fi
