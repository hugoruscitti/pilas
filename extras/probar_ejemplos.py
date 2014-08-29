import sys
import subprocess
import os
import signal

path = os.path.join(os.path.dirname(__file__), "..")
os.chdir(path)

directorio_relativo = 'pilasengine/ejemplos/'


def esperar(segundos):
    #print "Esperando %d segundos:" %(segundos)

    for x in range(segundos):
        os.system('sleep 1s')
        #print ".",

    #print "listo"

def check_pid(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

def terminar(pid):
    os.kill(pid, signal.SIGKILL)



def probar_ejemplo(directorio_relativo, nombre):
    pid = subprocess.Popen([sys.executable, directorio_relativo + nombre]).pid
    esperar(5)

    print nombre,

    if check_pid(pid):
        terminar(pid)
        print "[OK]"
    else:
        print "ERROR"


scripts = [script for script in os.listdir(directorio_relativo)
        if script.endswith('.py') and '__' not in script and not script.startswith('.')
       ]

for x in scripts:
    probar_ejemplo(directorio_relativo, x)