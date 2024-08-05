{
  description = "devshell for github:rjo1604/fraud-engine-test";

  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem
      (system:
        let pkgs = nixpkgs.legacyPackages.${system}; in
        {
          devShells.default = pkgs.mkShell {
            packages = with pkgs;
            [
              vscode-langservers-extracted
              (python311.withPackages(ps: with ps; [
                flask
                waitress
                # add more python stuff here
              ]))
            ];
          };
        }
      );
}
