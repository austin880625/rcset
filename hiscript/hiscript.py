#!/usr/bin/env python3

import sys
import stat
import os
import curses

class HiscRunException(Exception):
    def __init__(self, cmd):
        self.cmd = cmd

class HiscSaveException(Exception):
    pass

def saveSelectionTemp(select, cmds):
    with open("/tmp/hiscript_script.sh", "w") as f:
        f.write("#!/usr/bin/env bash\n\n")
        for i, cmd in enumerate(cmds):
            if i >= len(select):
                break
            if select[i] == 1:
                f.write(cmd[1])
                f.write("\n")

    st = os.stat('/tmp/hiscript_script.sh')
    os.chmod('/tmp/hiscript_script.sh', st.st_mode | stat.S_IEXEC)

def copyScript():
    exist = True
    i = 0
    while exist == True:
        i += 1
        savePath = "~/.local/bin/hiscript.%d" % (i)
        exist = os.path.isfile(savePath)
    newPath = input("input save path(%s):" % savePath)
    if newPath.strip() != '':
        savePath = newPath
    os.system("cp /tmp/hiscript_script.sh %s" % (savePath))

def main(scr, cmds):
    maxcur = len(cmds) - 1
    while len(cmds[maxcur]) < 2:
        maxcur -= 1
        if maxcur == 0:
            break

    c = 'q'

    y, x = scr.getmaxyx()
    cur = maxcur
    start = cur - (y-1)
    select = [0] * (maxcur + 1)

    while True:
        y, x = scr.getmaxyx()
        scr.clear()
        l = len(str(cur))
        start = max(start, 0)
        end = min(start + y, maxcur)
        
        for i in range(start, end):
            if i == cur:
                scr.standout()
            if select[i] == 1:
                scr.addstr(i-start, 0, "*")

            scr.addstr(i-start, 6, cmds[i][1])
            scr.standend()

        scr.refresh()
        c = scr.getch()
        if c == ord('q') or c == ord('w') or c == ord('t'):
            break
        elif c == ord('r'):
            raise HiscRunException(cmds[cur][1])
        elif c == ord('k'):
            if cur > 0:
                cur -= 1
            if cur < start + 5 and start > 0:
                start -= 1
        elif c == ord('j'):
            if cur < maxcur:
                cur += 1
            if cur > end - 5 and end < maxcur:
                start += 1
        elif c == ord(' '):
            select[cur] = 1 - select[cur]

    if c == ord('w'):
        saveSelectionTemp(select, cmds)
        raise HiscSaveException()
    if c == ord('t'):
        saveSelectionTemp(select, cmds)

if __name__ == '__main__':
    if sys.argv[2] == 'c':
        lines = open("/tmp/hiscript", "r").read().split('\n')
        cmds = [line.split(None, 1) for line in lines]

        try:
            curses.wrapper(main, cmds)
        except HiscRunException as e:
            print(e.cmd)
            os.system(e.cmd)
        except HiscSaveException as e:
            copyScript()
    elif sys.argv[2] == 'e':
        os.system("vim /tmp/hiscript_script.sh")
    elif sys.argv[2] == 'r':
        os.system("/tmp/hiscript_script.sh")
    elif sys.argv[2] == 'w':
        copyScript()
