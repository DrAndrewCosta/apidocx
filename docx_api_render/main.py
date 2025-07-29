
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from docx import Document
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMPLATE_DIR = "templates"

class DadosLaudo(BaseModel):
    paciente: str
    corpo: str
    conclusao: str
    solicitante: str = ""
    data: str

@app.post("/gerar-laudo")
def gerar_laudo(dados: DadosLaudo):
    try:
        # Seleciona template padrão
        template_path = os.path.join(TEMPLATE_DIR, "2025 ABDOME TOTAL.docx")
        if not os.path.exists(template_path):
            raise HTTPException(status_code=500, detail="Template não encontrado.")

        doc = Document(template_path)

        # Substituições
        for p in doc.paragraphs:
            if "{PACIENTE}" in p.text:
                p.text = p.text.replace("{PACIENTE}", dados.paciente)
            if "{DATA}" in p.text:
                p.text = p.text.replace("{DATA}", dados.data)
            if "{SOLICITANTE}" in p.text:
                p.text = p.text.replace("{SOLICITANTE}", dados.solicitante)
            if "{CORPO}" in p.text:
                p.text = p.text.replace("{CORPO}", dados.corpo)
            if "{CONCLUSAO}" in p.text:
                p.text = p.text.replace("{CONCLUSAO}", dados.conclusao)

        filename = f"laudo_{uuid.uuid4().hex[:8]}.docx"
        output_path = os.path.join("outputs", filename)
        os.makedirs("outputs", exist_ok=True)
        doc.save(output_path)

        return FileResponse(output_path, filename=filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
