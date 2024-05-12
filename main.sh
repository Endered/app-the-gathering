#!/bin/sh
#

if [ "$#" -lt 1 ]; then
    echo Please specify input json file!
    exit 1
fi

output=$(dirname $1)/gather.AppImage

if [ "$#" -ge 2 ]; then
    output="$2"
fi

nix bundle --impure --bundler "$(dirname "$0")/nix-appimage" \
    --expr "$(python3 main.py $1)"

find -name 'app-the-gathering-temporary-file*' | xargs -Ixxx bash -c "cp xxx $output; chmod u+w $output; rm xxx"
