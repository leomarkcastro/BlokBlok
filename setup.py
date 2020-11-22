import cx_Freeze
import os

game_folder = os.path.dirname(__file__)   
#music_folder = os.path.join(game_folder, 'music')

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(game_folder):
    for file in f:
        files.append(os.path.join(r, file))




executables = [cx_Freeze.Executable("START.py")]

cx_Freeze.setup(
    name="Blok_Blok",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":files}},
    executables = executables

    )
