from typing import Optional
from urllib import request
from fastapi import FastAPI, HTTPException, Request, Depends, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from models.models import Modelo, Montadora
from persistence.database import get_db
from persistence.montadora_repository import MontadoraRepository
from persistence.modelo_repository import ModeloRepository  # Alterado aqui

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

montadora_repository = MontadoraRepository()
modelo_repository = ModeloRepository()  # Alterado aqui

# Rotas para Montadoras
@app.get('/montadoras_list')
def montadora_list(request: Request, nome: str = None, pais: str = None, db: Session = Depends(get_db)):
    montadoras = montadora_repository.get_all(db, nome=nome, pais=pais)
    total_montadoras = len(montadoras)  
    return templates.TemplateResponse('montadora_list.html', {
        'montadoras': montadoras,
        'total_montadoras': total_montadoras, 
        'request': request
    })

@app.get('/montadoras_form')
def montadora_form(request: Request):
    return templates.TemplateResponse('montadora_form.html', {'request': request})


@app.post('/montadora_save')
def montadora_save(
    request: Request,
    nome: str = Form(...),
    pais: str = Form(...),
    ano: int = Form(...),
    db: Session = Depends(get_db)
):
    montadora = Montadora(nome=nome, pais=pais, ano_fundacao=ano)
    montadora_repository.save(db, montadora)
    return RedirectResponse('/montadoras_list', status_code=303)

@app.get('/montadoras_edit/{id}')
def montadora_edit(request: Request, id: str, db: Session = Depends(get_db)):
    montadora = montadora_repository.get_by_id(db, id)
    if not montadora:
        return templates.TemplateResponse('404.html', {'request': request}, status_code=404)
    return templates.TemplateResponse('montadora_form.html', {'montadora': montadora, 'request': request})

@app.post('/montadora_update/{id}')
def montadora_update(id: str, nome: str = Form(...), pais: str = Form(...), ano: int = Form(...), db: Session = Depends(get_db)):
    montadora = montadora_repository.get_by_id(db, id)

    if montadora:
        montadora.nome = nome
        montadora.pais = pais
        montadora.ano_fundacao = ano

        montadora_repository.update(db, montadora)  # Mantido como montadora
        return RedirectResponse('/montadoras_list', status_code=303)

    return RedirectResponse('/montadoras_list', status_code=404)

@app.post('/montadora_delete/{id}')
def montadora_delete(id: str, db: Session = Depends(get_db)):
    montadora_repository.delete(db, id)
    return RedirectResponse('/montadoras_list', status_code=303)

@app.get('/montadora_save_txt')
def salvar_dados_em_arquivo(db: Session = Depends(get_db)):
    montadoras = montadora_repository.get_all(db) 
    with open('montadoras.txt', 'w') as file:
        for montadora in montadoras:
            linha = f"{montadora.nome};{montadora.pais};{montadora.ano_fundacao}\n" 
            file.write(linha)
    return RedirectResponse('/montadoras_list', status_code=303)

@app.get("/montadora/{montadora_id}/modelos_list")
def modelos_list(montadora_id: str, request: Request, db: Session = Depends(get_db)):
    montadora = db.query(Montadora).filter(Montadora.id == montadora_id).first()
    modelos = db.query(Modelo).filter(Modelo.montadora_id == montadora_id).all()  # Alterado aqui
    
    return templates.TemplateResponse("modelos_list.html", {"request": request, "montadora": montadora, "modelos": modelos})

@app.get('/modelo_form/{montadora_id}')
@app.get('/modelo_form/{montadora_id}/{modelo_id: int = None}')
def modelo_form(request: Request, montadora_id: str, modelo_id: Optional[int] = None, db: Session = Depends(get_db)):
    # Busque a montadora pelo ID
    montadora = db.query(Montadora).filter(Montadora.id == montadora_id).first()
    if not montadora:
        raise HTTPException(status_code=404, detail="Montadora não encontrada")

    modelo = None  # Inicializa como None, assume que estamos adicionando um novo modelo

    # Se um modelo_id for fornecido, busque o modelo correspondente
    if modelo_id is not None:
        modelo = db.query(Modelo).filter(Modelo.id == modelo_id, Modelo.montadora_id == montadora_id).first()
        if not modelo:
            raise HTTPException(status_code=404, detail="Modelo não encontrado")

    return templates.TemplateResponse('modelo_form.html', {
        'request': request,
        'montadora_id': montadora_id,
        'montadora': montadora,
        'modelo': modelo  # Esta linha pode ser None se for um novo modelo
    })


@app.post('/modelo_save')
def modelo_save(
    request: Request,
    nome: str = Form(...),
    montadora_id: str = Form(...),
    valor_referencia: float = Form(...),
    motorizacao: float = Form(...),
    turbo: bool = Form(...),
    automatico: bool = Form(...),
    db: Session = Depends(get_db)
):
    try:
        modelo = Modelo(
            nome=nome,
            montadora_id=montadora_id,
            valor_referencia=valor_referencia,
            motorizacao=motorizacao,
            turbo=turbo,
            automatico=automatico
        )
        
        modelo_repository.save(db, modelo)
        return RedirectResponse(f'/montadora/{montadora_id}/modelos_list', status_code=303)
    except Exception as e:
        return {"error": str(e)}  # Retorna o erro como resposta JSON

@app.post('/modelos_delete/{modelo_id}')
def modelos_delete(modelo_id: str, db: Session = Depends(get_db)):
    # Obtém o modelo antes de deletá-lo
    modelo = modelo_repository.get_by_id(db, modelo_id)
    if modelo is None:
        return {"error": "Modelo não encontrado."}
    
    montadora_id = modelo.montadora_id  # Armazena o montadora_id antes da deleção

    # Deleta o modelo
    modelo_repository.delete(db, modelo_id)

    # Redireciona de volta para a lista de modelos da montadora associada
    return RedirectResponse(f'/montadora/{montadora_id}/modelos_list', status_code=303)


@app.get('/modelos_edit/{modelo_id}')
def modelos_edit(request: Request, modelo_id: str, db: Session = Depends(get_db)):
    modelo = modelo_repository.get_by_id(db, modelo_id)
    if modelo is None:
        return {"error": "Modelo não encontrado."}
    return templates.TemplateResponse('modelo_form.html', {'request': request, 'modelo': modelo, 'montadora_id': modelo.montadora_id})


@app.post('/modelo_update/{modelo_id}')
def modelo_update(
    modelo_id: str,
    request: Request,
    nome: str = Form(...),
    valor_referencia: float = Form(...),
    motorizacao: str = Form(...),
    turbo: bool = Form(...),
    automatico: bool = Form(...),
    db: Session = Depends(get_db)
):
    # Validação da motorização
    try:
        motorizacao_float = float(motorizacao)
    except ValueError:
        return {"error": "Motorização deve ser um número válido."}

    # Obtendo o modelo existente
    modelo_existente = modelo_repository.get_by_id(db, modelo_id)
    if not modelo_existente:
        return {"error": "Modelo não encontrado."}

    # Atualizando as informações do modelo
    modelo_existente.nome = nome
    modelo_existente.valor_referencia = valor_referencia
    modelo_existente.motorizacao = motorizacao_float
    modelo_existente.turbo = turbo
    modelo_existente.automatico = automatico

    # Chamando a função de atualização
    modelo_repository.update(db, modelo_existente)

    return RedirectResponse(f'/montadora/{modelo_existente.montadora_id}/modelos_list', status_code=303)


