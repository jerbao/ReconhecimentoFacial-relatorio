import json
import os
from typing import Dict
from threading import Lock
import time

class Operador:
    json_lock = Lock()

    @staticmethod
    def arquivo_modificado(arquivo, ultima_modificacao):
        """
        Verifica se um arquivo foi modificado desde a última modificação registrada.

        Args:
            arquivo (str): O caminho para o arquivo.
            ultima_modificacao (float): O tempo da última modificação registrada.

        Returns:
            bool: True se o arquivo foi modificado, False caso contrário.
        """
        tempo_atual = os.path.getmtime(arquivo)
        if tempo_atual > ultima_modificacao:
            return True
        else:
            return False

    @staticmethod
    def abreJson(NomeArquivo: str) -> Dict:
        """
        Abre um arquivo JSON, verificando se foi modificado desde a última abertura.

        Args:
            NomeArquivo (str): O caminho para o arquivo JSON.

        Returns:
            dict: O objeto de dados JSON.
        """
        max_tentativas = 10  # Definir o número máximo de tentativas
        tentativas = 0
        while tentativas < max_tentativas:
            try:
                with open(NomeArquivo) as file:
                    data = json.load(file)
                    ultima_modificacao = os.path.getmtime(NomeArquivo)
                    while tentativas < max_tentativas:
                        if Operador.arquivo_modificado(NomeArquivo, ultima_modificacao):
                            print("Arquivo modificado. Reabrindo e enviando dados atualizados...")
                            time.sleep(1)  # Aguardar 1 segundo antes de tentar abrir novamente
                            break  # Sair do loop interno e tentar abrir novamente
                        else:
                            Operador.escreveJsonLocked(data, NomeArquivo)
                            return data

            except IOError:
                print(f'{NomeArquivo} não encontrado!')
                data = {}
                break  # Sair do loop principal

            except json.JSONDecodeError:
                print(f'Erro ao decodificar o JSON em {NomeArquivo}. Tentando novamente em 1 segundo...')
                time.sleep(1)  # Aguardar 1 segundo antes de tentar abrir novamente
                tentativas += 1

            except Exception as e:
                print(f'Erro ao abrir o arquivo {NomeArquivo}: {str(e)}. Tentando novamente em 1 segundo...')
                time.sleep(1)  # Aguardar 1 segundo antes de tentar abrir novamente
                tentativas += 1

        return data

    @staticmethod
    def escreveJson(Data: any, NomeArquivo: str) -> None:
        """
        Escreve dados em um arquivo JSON.

        Args:
            Data (any): Os dados a serem escritos.
            NomeArquivo (str): O caminho para o arquivo JSON.

        Returns:
            None
        """
        try:
            with open(NomeArquivo, 'w') as file:
                json.dump(Data, file, indent=4)

        except IOError:
            print(f'Não foi possível escrever no arquivo: {NomeArquivo}')

    @staticmethod
    def getDataLen(NomeArquivo: str) -> int:
        """
        Retorna o tamanho de um arquivo JSON em inteiro.

        Args:
            NomeArquivo (str): O caminho para o arquivo JSON.

        Returns:
            int: O tamanho do arquivo em inteiro.
        """
        data = Operador.abreJson(NomeArquivo)
        return len(data)

    @staticmethod
    def escreveJsonLocked(Data: any, NomeArquivo: str) -> None:
        """
        Escreve dados em um arquivo JSON com trava.

        Args:
            Data (any): Os dados a serem escritos.
            NomeArquivo (str): O caminho para o arquivo JSON.

        Returns:
            None
        """
        with Operador.json_lock:
            Operador.escreveJson(Data, NomeArquivo)
