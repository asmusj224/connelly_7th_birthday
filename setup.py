import cx_Freeze

executables = [cx_Freeze.Executable('main.py')]

cx_Freeze.setup(
    name="Crossy",
    options={"build_exe": {"packages": ["pygame"], "include_files": ["background.png", "enemy.png", "player.png", "treasure.png"]}},
    executables = executables
)