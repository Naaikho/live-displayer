import os, sys
import shutil
import time
import colorama
colorama.init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint, colored
from threading import Thread

home = sys.path[0]
loop = bool()

def path(*arg):
    p = arg[0]
    i = 1
    while i < len(arg):
        p = os.path.join(p, arg[i])
        i += 1
    return p

if os.path.exists(path(home, "env")):
    shutil.rmtree(path(home, "env"))

def targetCpy(src, dst):
    tmp_cpy = ("import os, sys\n\n"+
    "sys.path[0] = \"{}\"\n".format(os.path.dirname(src))+
    "try:\n")
    with open(src, "r") as data:
        for tmp_line in data.readlines():
            tmp_cpy += "    " + tmp_line
    tmp_cpy += "\nexcept Exception as e:\n    print('error in the code . . .')\n    print(e)\ninput()"

    shutil.copytree(os.path.dirname(src), path(sys.path[0], "env"), ignore=shutil.ignore_patterns("*.md", ".git*", "__pycache__"))

    with open(dst, "w") as data:
        data.write(tmp_cpy)

def startSHowing(target, args):
    global loop

    loop = True
    TARGET_CPY = path(sys.path[0], "env", target.split("/")[-1])
    if os.path.exists(path(home, "env")):
        shutil.rmtree(path(home, "env"))
    targetCpy(target, TARGET_CPY)
    os.startfile(TARGET_CPY + " " + args)
    mtime = os.path.getmtime(target)
    while loop:
        if mtime != os.path.getmtime(target):
            os.system("TASKKILL /F /IM py.exe")
            if os.path.exists(path(home, "env")):
                shutil.rmtree(path(home, "env"))
            targetCpy(target, TARGET_CPY)
            os.startfile(TARGET_CPY + " " + args)
            mtime = os.path.getmtime(target)
            print("> ", end="")
        time.sleep(0.1)

while 1:
    cmmd = input("> ")

    if cmmd in ["help", "h", "aide", "?"] or cmmd == "":
        print(colored("target\n", "blue", attrs=["bold"])+
        " • Start the liveShower after choose the target file (.py).\n"+
        colored("stop\n", "blue", attrs=["bold"])+
        " • Stop the currently started target.")
        continue
    elif cmmd == "target":
        target = "/".join(input("target: ").split("\\"))
        if target.split(".")[-1] != "py":
            print("pls select a Python file (.py)")
            continue
        args = input("args: ")
        t = Thread(target=lambda: startSHowing(target, args))
        t.daemon = True
        t.start()
        continue
    elif cmmd == "stop":
        loop = False
        os.system("TASKKILL /F /IM py.exe")