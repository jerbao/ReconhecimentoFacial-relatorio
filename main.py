from time import sleep
from Modules.Lybrary.executor import Executor as exc

"""

    file -> main.py
    
"""


while True:
    sleep(0.15)
    exc.enviaJson("./Images/todasFotos/putin-1.jpg")

