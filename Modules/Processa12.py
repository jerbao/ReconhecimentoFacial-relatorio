import cv2, os
from time import sleep
from deepface import DeepFace
from Lybrary.operador import Operador as op

def processaImagem() -> None:
    """
        Função que compara imagens recebidas com o banco de dados de imagens

        Entradas:
            Nenhuma

        Saídas:
            Nenhuma
    """

    img1 = cv2.imread(data[nomeProcesso]["FotoComparar"])
    img2 = cv2.imread(data[nomeProcesso]["ImagemBanco"])
    if DeepFace.verify(img1_path = img1,img2_path = img2,model_name=data[nomeProcesso]["modeloIA"])['verified']:
        nomeArquivo = os.path.basename(data[nomeProcesso]["ImagemBanco"])
        todoNome = os.path.splitext(nomeArquivo)[0]
        cache.append(todoNome.split('-')[0])
        op.escreveJsonLocked(cache, "Modules/Archives/cache.json")
        
    data[nomeProcesso] = ""
    op.escreveJsonLocked(data, "Modules/Archives/consumables.json")

while True:
    data = op.abreJson("Modules/Archives/consumables.json")
    cache = op.abreJson("Modules/Archives/cache.json")
    nomeProcesso = (os.path.basename(__file__)).split('.')[0]
    if not data[nomeProcesso] == "":
        processaImagem()
        sleep(0.5)
    else:
        sleep(1)