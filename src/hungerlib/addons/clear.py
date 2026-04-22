import os
def clearTerminal():
    os.system("clear" if os.name == "posix" else "cls")