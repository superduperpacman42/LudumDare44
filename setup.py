import cx_Freeze
import os
os.environ['TCL_LIBRARY'] = r'C:\Program Files\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Program Files\Python36\tcl\tk8.6'

executables = [cx_Freeze.Executable("Game.pyw", base = "Win32GUI")]
cx_Freeze.setup(
    name="Demonic Dealings",
    version = "1.0",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":['images/','audio/','bankgothic/','lcd-solid_lcd-solid']}},
    executables = executables

    )
