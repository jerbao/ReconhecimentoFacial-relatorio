import os
from time import sleep
from threading import Lock
from Modules.Lybrary.operador import Operador as op
from abc import ABC, abstractmethod

"""

    file -> executor.py
    
"""


class Executor(ABC): 
    """Classe responsável por gerir os processas"""
    
    historico_imagens = set()
    json_lock = Lock()
    ImagensBD = './Images/todasFotos'
    consumables = "./Modules/Archives/consumables.json"

    def __init__(self) -> None:
        """A classe Executor não deve ser instanciada"""
        pass
    
    @staticmethod
    @abstractmethod
    def obterProximaImagem() -> str:
        """
        Método auxiliar para obter a próxima imagem disponível em ImagensBD.

        Saídas:
            str - Caminho completo para a próxima imagem disponível.
            None - Caso não haja mais imagens disponíveis.
        """
        for diretorio, subpastas, arquivos in os.walk(Executor.ImagensBD):
            sleep(0.02)
            for arquivo in arquivos:
                sleep(0.02)
                imagemBanco = os.path.join(diretorio, arquivo)
                if imagemBanco not in Executor.historico_imagens:
                    Executor.historico_imagens.add(imagemBanco)
                    return imagemBanco
        sleep(0.01)
        return None
    
    @staticmethod
    @abstractmethod
    def enviaJson(FotoComparar: str) -> None:
        """
        Método que encaminha a imagem para processamento

        Entradas:
            FotoComparar : str

        Saídas:
            None
        """
        data = op.abreJson(Executor.consumables)
        sleep(0.02)
        processas_disponiveis = [i for i in range(1, len(data)+1) if data[f"Processa{i}"] == ""]
        sleep(0.02)
        for i in processas_disponiveis:
            imagemBanco = Executor.obterProximaImagem()
            sleep(0.02)
            if imagemBanco is not None:
                with Executor.json_lock:
                    data = op.abreJson(Executor.consumables)
                    sleep(0.02)
                    if data[f"Processa{i}"] == "":
                        sleep(0.02)
                        data[f"Processa{i}"] = {
                            "FotoComparar": FotoComparar,
                            "ImagemBanco": imagemBanco,
                            "modeloIA": "Facenet",
                        }
                        op.escreveJson(data, Executor.consumables)
                        sleep(0.05)

    @staticmethod
    @abstractmethod
    def extendsJson() -> None:
        """
            Método que extende a quantidade de processas

            Entradas:
                Nenhuma

            Saídas:
                Nenhuma
        """

        data = op.abreJson(Executor.consumables)

        data[f"Processa{len(data)+1}"] = ""

        op.escreveJson(data, Executor.consumables)

    @staticmethod
    @abstractmethod
    def resumsJson(NomeProcesso:str) -> None:
        """
            Método que resume a quantidade de processas

            Entradas:
                Nenhuma

            Saídas:
                Nenhuma
        """

        data = op.abreJson(Executor.consumables)

        if NomeProcesso in data.keys():
            del data[NomeProcesso]
            op.escreveJson(data, Executor.consumables)
        else:
            print(f"O processo {NomeProcesso} não está na lista de processos.")