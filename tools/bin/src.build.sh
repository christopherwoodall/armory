#! /usr/bin/env bash
set -e

PROJECT="armory"

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ] ; do SOURCE="$(readlink "$SOURCE")"; done
BDIR="$( cd -P "$( dirname "$SOURCE" )/../.." && pwd )"

pushd $BDIR

BUILD_TIME=`date -u '+%Y-%m-%d_%I:%M:%S%p'`
TAG="current"
REVISION="current"

if hash git 2>/dev/null && [ -e $BDIR/.git ]; then
  TAG=`git describe --always --abbrev=0`
  REVISION=`git rev-parse HEAD`
fi

# Should be tagged during build with the version hook
# echo "${TAG:1}" > $BDIR/VERSION.txt

popd

echo "VERSION file updated with tag: $TAG and revision: $REVISION"