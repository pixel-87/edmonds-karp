{
  pkgs,
  mkShell,
  ...
}:
mkShell {
  packages = with pkgs; [
    python3
    uv
    
    # System dependencies for Manim
    ffmpeg
    cairo
    pango
    pkg-config
    
    # Build tools
    ninja
    meson
  ];

  env = {
    LD_LIBRARY_PATH = "${pkgs.cairo}/lib:${pkgs.pango}/lib:${pkgs.glib}/lib:${pkgs.stdenv.cc.cc.lib}/lib";
  };

  shellHook = ''
    echo "Environment ready with uv. Run 'uv sync' to install dependencies."
  '';
}