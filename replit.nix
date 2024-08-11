{ pkgs }: {
  deps = [
    pkgs.python310Full
    pkgs.ffmpeg
    pkgs.libopus
    pkgs.nodejs
  ];
}