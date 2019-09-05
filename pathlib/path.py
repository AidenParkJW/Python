import pathlib, datetime

print("{:30} : {}".format("pathlib.PurePath('.')"           , type(pathlib.PurePath("."))))
print("{:30} : {}".format("pathlib.PurePosixPath('.')"      , type(pathlib.PurePosixPath("."))))
print("{:30} : {}".format("pathlib.PureWindowsPath('.')"    , type(pathlib.PureWindowsPath("."))))

print()

print("{:30} : {}".format("pathlib.Path('.')"               , type(pathlib.Path("."))))
#print("{:30} : {}".format("pathlib.PosixPath('.')"         , type(pathlib.PosixPath("."))))
print("{:30} : {}".format("pathlib.WindowsPath('.')"        , type(pathlib.WindowsPath("."))))



_path = pathlib.Path(".")
print(_path.cwd())
print()

for _dir in _path.iterdir() :
    print("{} {:30} {:10} {:20} {}".format("D" if _dir.is_dir() else "F"
                                        , _dir.name
                                        , _dir.stat().st_size
                                        , datetime.datetime.fromtimestamp(_dir.stat().st_mtime).strftime("%Y/%m/%d %H:%M:%S")
                                        , _path.joinpath(_path.absolute(), _dir)))
