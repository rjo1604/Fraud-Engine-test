### what is the flake.nix file?

The `flake.nix` file is for NixOS users.
To get a devshell with all dependencies installed, run:

```bash
nix develop
```

Non Nix users, install:
- python3 packages
  - flask
  - waitress
- vscode HTML LSP (optionally for code completions)

### Running

Execute the following to spin up the server:

```bash
python main.py
```

Now visit http://localhost:5000
