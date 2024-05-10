#!/bin/sh
#
NA_EXE="$1"

export NA_EXE

nix bundle --impure --bundler "$(dirname "$0")/nix-appimage" \
    --expr "$(python3 main.py $@)"
#'
#	let
#		p = with import <nixpkgs> {}; '"$NA_EXE"';
#	in {
#		type = "app";
#		program = "${p}/bin/'$NA_EXE'";
#	}
#	'

