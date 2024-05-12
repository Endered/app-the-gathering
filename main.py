import sys
import json

with open(sys.argv[1]) as f:
    js = f.read()

obj = json.loads(js)

packages = [ "coreutils" ]
bins = []

for package, uses in obj["dependencies"].items():
    packages.append(package)
    for use in uses:
        binary_name = use["binary-name"]
        if "alternate-name" in use:
            alternate_name = use["alternate-name"]
        else:
            alternate_name = binary_name
        bins.append((package, binary_name, alternate_name))

packages = list(set(packages))

print("let")
print("pkgs = import <nixpkgs> {};")
print("p = pkgs.hello;")
print("drv = pkgs.stdenv.mkDerivation {")
print("name = \"hey\";")
packages_str = " ".join(packages)
print(f"buildInputs = with pkgs; [ {packages_str} ];")
print("unpackPhase = \"true\";")
print("buildPhase = ''")
print("echo '#!/bin/bash' >> app-the-gathering-temporary-file")
print("echo 'x=$(${pkgs.coreutils}/bin/basename \"$ARGV0\")' >> app-the-gathering-temporary-file")
for (package, binary_name, alternate_name) in bins:
    print(f"MATCH_NUM=$(find ${{pkgs.{package}}}/bin -name '{binary_name}' -printf 'find\\n' -type f | wc -l)")
    print(f"find ${{pkgs.{package}}}/bin -name '{binary_name}' -printf 'find\\n' -type f")
    print('echo a"$MATCH_NUM"a')
    print("if [ $MATCH_NUM != 1 ]; then")
    print("echo Invalid binary_name or alternate_name was supplied >&2")
    print("exit 1")
    print("fi")
    print(f"TMP=\"$(find ${{pkgs.{package}}}/bin -name '{binary_name}' | xargs readlink -f)\"")
    print(f"echo 'if [ $x = {alternate_name} ]; then' >> app-the-gathering-temporary-file")
    print("echo 'unset ARGV0' >> app-the-gathering-temporary-file")
    print("echo 'unset x' >> app-the-gathering-temporary-file")
    print("echo 'unset MATCH_NUM' >> app-the-gathering-temporary-file")
    print("echo 'unset TMP' >> app-the-gathering-temporary-file")
    print(f"echo \"exec -a {binary_name} '$TMP'\" '$@' >> app-the-gathering-temporary-file")
    print("echo 'fi' >> app-the-gathering-temporary-file")
print("echo 'if [ \"$1\" = '\"'\"--softlink\"'\"' ]; then' >> app-the-gathering-temporary-file")
for (_, _, name) in bins:
    print(f"echo '${{pkgs.coreutils}}/bin/ln -s $ARGV0 {name}' >> app-the-gathering-temporary-file")
print("echo 'exit' >> app-the-gathering-temporary-file")
print("echo 'fi' >> app-the-gathering-temporary-file")
print("echo 'echo please call with --softlink for make softlinks' >> app-the-gathering-temporary-file")
print("chmod u+x app-the-gathering-temporary-file")
print("'';")
print("installPhase = ''")
print("mkdir -p $out/bin")
print("cp app-the-gathering-temporary-file $out/bin")
print("'';")
print("};")
print("in {")
print("type = \"app\";")
print("program = \"${drv}/bin/app-the-gathering-temporary-file\";")
print("}")
