from fastapi import FastAPI, HTTPException, Request, Depends, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from models.models import Montadora, Veiculo
from persistence.database import get_db
from persistence.montadora_repository import MontadoraRepository
from persistence.veiculo_repository import VeiculoRepository
from uuid import UUID

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

montadora_repository = MontadoraRepository()
veiculo_repository = VeiculoRepository() 

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

from fastapi.responses import RedirectResponse
from fastapi import Form, Depends
from sqlalchemy.orm import Session
import uuid

@app.post('/montadora_update/{id}')
def montadora_update(id: uuid.UUID, nome: str = Form(...), pais: str = Form(...), ano: int = Form(...), db: Session = Depends(get_db)):
    montadora = montadora_repository.get_by_id(db, id)

    if montadora:
        montadora.nome = nome
        montadora.pais = pais
        montadora.ano_fundacao = ano

        montadora_repository.update(db, id, montadora)
        return RedirectResponse('/montadoras_list', status_code=303)

    return RedirectResponse('/montadoras_list', status_code=404)


@app.post('/montadora_delete/{id}')
def montadora_delete(id: str, db: Session = Depends(get_db)):
    montadora_repository.delete(db, id)
    return RedirectResponse('/montadoras_list', status_code=303)

@app.get('/veiculos_list')
def veiculo_list(request: Request, db: Session = Depends(get_db)):
    veiculos = veiculo_repository.get_all(db)
    return templates.TemplateResponse('veiculo_list.html', {'veiculos': veiculos, 'request': request})

@app.get('/veiculo_form')
def veiculo_form(request: Request, db: Session = Depends(get_db)):
    montadoras = montadora_repository.get_all(db)
    return templates.TemplateResponse('veiculo_form.html', {'request': request, 'montadoras': montadoras})

@app.post('/veiculo_save')
def veiculo_save(
    request: Request,
    nome: str = Form(...),
    montadora_id: str = Form(...),
    valor_referencia: float = Form(...), 
    motorizacao: float = Form(...),
    turbo: bool = Form(...),
    automatico: bool = Form(...),
    db: Session = Depends(get_db)
):
    veiculo = Veiculo(
        nome=nome,
        montadora_id=montadora_id,
        valor_referencia=valor_referencia,
        motorizacao=motorizacao,
        turbo=turbo,
        automatico=automatico
    )
    veiculo_repository.save(db, veiculo)
    return RedirectResponse('/veiculos_list', status_code=303)

@app.get('/veiculo_edit/{id}')
def veiculo_edit(request: Request, id: str, db: Session = Depends(get_db)):
    veiculo = veiculo_repository.get_by_id(db, id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    
    montadoras = montadora_repository.get_all(db)
    return templates.TemplateResponse('veiculo_form.html', {'veiculo': veiculo, 'montadoras': montadoras, 'request': request})

@app.post('/veiculo_update/{id}')
def veiculo_update(
    id: str,
    nome: str = Form(...),
    montadora_id: str = Form(...),
    valor_referencia: float = Form(...), 
    motorizacao: float = Form(...),
    turbo: bool = Form(...),
    automatico: bool = Form(...),
    db: Session = Depends(get_db)
):
    veiculo = veiculo_repository.get_by_id(db, id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")

    veiculo.nome = nome
    veiculo.montadora_id = montadora_id
    veiculo.valor_referencia = valor_referencia
    veiculo.motorizacao = motorizacao
    veiculo.turbo = turbo
    veiculo.automatico = automatico

    veiculo_repository.update(db, veiculo)
    return RedirectResponse('/veiculos_list', status_code=303)

@app.post('/veiculo_delete/{id}')
def veiculo_delete(id: str, db: Session = Depends(get_db)):
    veiculo_repository.delete(db, id)
    return RedirectResponse('/veiculos_list', status_code=303)

@app.get('/montadora_save_txt')
def salvar_dados_em_arquivo(db: Session = Depends(get_db)):
    montadoras = montadora_repository.get_all(db) 
    with open('montadoras.txt', 'w') as file:
        for montadora in montadoras:
            linha = f"{montadora.nome};{montadora.pais};{montadora.ano_fundacao}\n" 
            file.write(linha)
    return RedirectResponse('/montadoras_list', status_code=303)