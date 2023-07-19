import multiprocessing, subprocess
from Modules.Lybrary.operador import Operador as op
from time import sleep


def executar_processo(numero):
    arquivo = f"./Modules/Processa{numero}.py"
    subprocess.run(["python3", arquivo])

if __name__ == '__main__':
    processos = []

    tamanho = op.getDataLen("./Modules/Archives/consumables.json")

    # Executar Processa de 1 a 12
    for i in range(1, tamanho+1):
        processo = multiprocessing.Process(target=executar_processo, args=(i,))
        processos.append(processo)
        processo.start()

    # Aguardar a conclusão de todos os processos
    for processo in processos:
        sleep(0.15)
        processo.join()
