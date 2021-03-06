#!/usr/bin/env python
#-*- coding: UTF-8 -*-

"""
Este es un script que busca actualizar el repositorio en que se halla
aprovechando git. Debe funcionar en GNU/Linux y en Windows, especialmente en
este último donde es más probable que el entorno esté incompleto o
desactualizado.
"""

from Queue import Queue, Empty
from src.autopipe import red, blue, green
from src.executables import get_paths
from src.downloader import downloader
from subprocess import Popen, PIPE, STARTUPINFO, SW_HIDE, STARTF_USESHOWWINDOW
from threading  import Thread
import os
import sys
import webbrowser

REPO_URL = "git://github.com/pointtonull/golsoft.git"
GIT_INSTALLER = ("https://msysgit.googlecode.com/files/"
    "msysGit-fullinstall-1.7.9-preview20120201.exe")


def enqueue_output(out, queue):
    for line in iter(out.read, ''):
        queue.put(line)
    out.close()


def non_blocking_proc(command):
    sys.stderr.write("» Launch: %s\n" % (" ".join(command)).lower(), "blue")
    info = STARTUPINFO()
    info.dwFlags |= STARTF_USESHOWWINDOW
    info.wShowWindow = SW_HIDE

    proc = Popen(command, stdout=PIPE, stderr=PIPE, bufsize=1,
        close_fds=False, startupinfo=info)

    stdout_queue = Queue()
    stdout = Thread(target=enqueue_output, args=(proc.stdout,
        stdout_queue))
    stdout.daemon = True
    stdout.start()

    stderr_queue = Queue()
    stderr = Thread(target=enqueue_output, args=(proc.stderr,
        stderr_queue))
    stderr.daemon = True
    stderr.start()

    while proc.poll() is None:

        try:
            line = stdout_queue.get_nowait()
        except Empty:
            pass
        else:
            sys.stdout.write("    " + line)

        try:
            line = stderr_queue.get_nowait()
        except Empty:
            pass
        else:
            sys.stderr.write("    " + line)

    return proc.returncode


def check_module(name, module):
    sys.stdout.write("    Cheking %s: " % name, "blue")
    try:
        module = __import__(module)
        print "pass"
        return module
    except ImportError:
        sys.stderr.write("fail\n")
        return False


def execute(path):
    sys.stderr.write("""***     Executing installer\n"""
        """***     execute & retry\n""")
    return non_blocking_proc([path])


def download(url, destpath=None):
    sys.stderr.write("""        Fetching installer\n"""
        """        execute & retry\n""")
    if destpath is None:
        destdir = "tools"
        filename = os.path.basename(url)
        destpath = os.path.join(destdir, filename)
    downloader(url, destpath)
    return non_blocking_proc([destpath])


def easy_install(module):
    easy_install_paths = get_paths("easy_install")
    command = [easy_install_paths[0], module]
    non_blocking_proc(command)


def pip_install(module):
    pip_paths = get_paths(r"pip")
    command = [pip_paths[0], "install", module]
    non_blocking_proc(command)


def main():
    "The main routine"

    blue("Verifing git: ")
    git_paths = get_paths(r"cmd\git")
    if git_paths:
        print("pass")
    else:
        red("fail\n")
        download(GIT_INSTALLER, "git-setup.exe")
        return 1

    blue("Verifing valid repository: ")
    if os.path.isdir(".git"):
        print("pass")
    else:
        red("fail\n")
        blue("Attempting to clone the repository at the current location\n"
            "\n\nThis may take some time depending on pool size and the speed"
            "of the connection.\n")
        non_blocking_proc([git_paths[0], "clone", REPO_URL])
        blue("""\n\nMust execute "update.pyw" inside the new dir.\n""")
        return

    commands = (
        [git_paths[0], "stash"],
        [git_paths[0], "fetch", "-v"],
        [git_paths[0], "rebase", "-v"]
    )

    for command in commands:
        non_blocking_proc(command)

    methods = {
        "executable" : execute,
        "easy_install" : easy_install,
        "download" : download,
        "pip" : pip_install
    }

    blue("\nTesting dependencies:\n")
    lines = (line.strip().split(";") for line in open("dependencies.txt")
        if not line.startswith("#"))
    for name, module, method, argument in lines:
        if not check_module(name, module):
            methods[method](argument)


if __name__ == "__main__":
    exit(main())
