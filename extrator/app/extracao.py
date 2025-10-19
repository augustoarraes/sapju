from app.db import session
from app.schema import DocumentoEvento
from app.model import DocumentoModel
from datetime import datetime
import dotenv, os, pdftotext, json


class ExtracaoDocumento:

    def __init__(self, documento: DocumentoEvento):
        dotenv.load_dotenv(".env")
        self.dir_uploads = os.environ["DIR_UPLOAD"]
        self.documento = documento
        self.session = session
        self.documento_model = self.session.query(DocumentoModel).filter(DocumentoModel.documento_id==documento.documento_id).first()
        if not self.documento_model:
            self.update_status_documento("FALHA_NO_PROCESSAMENTO")
            print(f"Arquivo {self.documento.dict()} não existe!")
        print(f"Iniciando extração de {self.documento_model.as_dict()} ......")
        

    def update_status_documento(self, status):
        self.documento_model.status = status
        self.documento_model.data_atualizacao = datetime.now().strftime("%m-%d-%Y %H:%M:%S.%f")
        self.session.commit()
        print(f"{status} para extração de {self.documento.dict()}")

    
    def salva_texto_documento(self, texto):
        print(f"Finalizando extração de {self.documento.dict()} ......")
        self.documento_model.texto = texto
        self.documento_model.data_atualizacao = datetime.now().strftime("%m-%d-%Y %H:%M:%S.%f")
        self.session.commit()
        print(f"Extração salva de {self.documento.dict()}")
        self.storage_extracao()

    
    def storage_extracao(self):
        print(f"Armazenando a extração de {self.documento_model.as_dict()} ......")


    def extracao_documento(self):
        self.update_status_documento("EM_EXECUCAO")
        try:
            with open(f"{self.dir_uploads}/{self.documento_model.nome_documento}", "rb") as f:
                pdf = pdftotext.PDF(f)
                texto = "\n".join(pdf)
                self.salva_texto_documento( texto )
                self.update_status_documento("CONCLUIDA")
        except Exception as e:
            self.update_status_documento("FALHA_NO_PROCESSAMENTO")
            print(f"Erro na extração do arquivo {self.documento.dict()}: {e}")
        #return 1
