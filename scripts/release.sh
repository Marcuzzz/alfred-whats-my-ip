#!/bin/bash

BUNDLEID=$(plutil -extract bundleid raw -o - ./info.plist)
NAME=${BUNDLEID##*.}

VERSION=${1:-$(poetry version --short)}

FILENAME="$NAME.v$VERSION.alfredworkflow"

poetry version $VERSION
plutil -replace version -string $VERSION info.plist

echo "NAME: $NAME"
echo "BUNDLE ID: $BUNDLEID"
echo "CURRENT VERSION: v$(poetry version --short)"
echo "NEW VERSION: v$VERSION"
echo


# echo "Testing workflow..."
# echo

# PYTHONPATH=src poetry run python3 -m unittest discover -s tests
# RESULT=$?

# if [ $RESULT != 0 ]; then
#   echo "⚠️  TESTS FAILED"
#   exit $RESULT
# fi


echo "Building binaries..."
echo
./scripts/build.sh > /dev/null
echo


echo "Building release..."
echo
mkdir releases 2> /dev/null
zip "releases/$FILENAME" -r dist img *.png info.plist
echo

echo "Released $NAME v$VERSION"
echo " * releases/$FILENAME"
echo

echo "Opening new release"
open "./releases/$FILENAME"

####### Upload release to GitHub #########
####### install github cli separately ####

if [ "$1" ]; then
    # Create a new release...
    gh release create "v$VERSION" "./releases/$FILENAME" --notes "Released $NAME v$VERSION"
fi