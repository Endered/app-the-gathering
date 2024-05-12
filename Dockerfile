FROM ghcr.io/nixos/nix

WORKDIR /workdir/

COPY ./main.py main.sh /workdir/
COPY ./nix-appimage /workdir/nix-appimage

RUN nix-env -iA nixpkgs.busybox nixpkgs.python3 && \
    nix --extra-experimental-features 'nix-command flakes' bundle --impure --bundler /workdir/nix-appimage nixpkgs#hello

RUN nix-shell -p busybox --run \
  'sed -i ./main.sh -e "s/bundle/--extra-experimental-features '"'"'nix-command flakes'"'"' bundle/"'

CMD [ "./main.sh", "/src/apps.json" ]