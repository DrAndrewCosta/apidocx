from docx import Document
from datetime import datetime

def inserir_laudo_completo(template_path, saida_path, texto_laudo, ponto_insercao="Exame realizado com"):
    doc = Document(template_path)
    encontrou_ponto = False

    # Criar lista temporária de parágrafos
    novos_paragrafos = []
    for linha in texto_laudo.split("\n"):
        novos_paragrafos.append(linha.strip())

    # Inserir após o ponto de referência
    for i, par in enumerate(doc.paragraphs):
        if ponto_insercao.lower() in par.text.lower():
            encontrou_ponto = True
            insert_index = i + 1
            for linha in novos_paragrafos:
                doc.paragraphs.insert(insert_index, doc.add_paragraph(linha))
                insert_index += 1
            break

    if not encontrou_ponto:
        raise ValueError("Ponto de inserção não encontrado no template.")

    doc.save(saida_path)

# EXEMPLO DE USO
texto_gerado = """João da Silva
29/07/2025

Fígado com contornos regulares, sem alterações significativas.
Vesícula biliar sem cálculos ou espessamento parietal.
...
Os achados ecográficos sugerem:
• Exame sem alterações."""

inserir_laudo_completo(
    template_path="templates/2025 ABDOME TOTAL.docx",
    saida_path="laudos/Joao_Silva.docx",
    texto_laudo=texto_gerado
)
