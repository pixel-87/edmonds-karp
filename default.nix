{ lib, python3Packages, ... }:
python3Packages.buildPythonApplication {
  pname = "example-python";
  version = "0.0.1";

  src = ./.;

  # If you are using poetry, you can use the following configuration
  # pyproject = true;
  # build-system = [ python3Packages.poetry-core ];

  dependencies = with python3Packages; [
    manim
    networkx
  ];

  nativeCheckInputs = [ python3Packages.pytestCheckHook ];

  meta = {
    description = "A report, code, an animation for the Edmonds-Karp Algorithm";
    homepage = "https://github.com/pixel-87/edmonds-karp";
    license = lib.licenses.gpl3Plus;
    maintainers = with lib.maintainers; [ ];
  };
}
