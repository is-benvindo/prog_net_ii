from fastapi import FastAPI, Request, Depends, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from models import Montadora
from persistence.database import get_db
from persistence.montadora_repository import MontadoraRepository
from view_models import InputMontadora

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

repository = MontadoraRepository()

# Rotas
@app.get('/montadoras_list')
def montadora_list(request: Request, nome: str = None, pais: str = None, db: Session = Depends(get_db)):
    montadoras = repository.get_all(db, nome=nome, pais=pais)
    return templates.TemplateResponse('montadora_list.html', {'montadoras': montadoras, 'request': request})

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
    repository.save(db, montadora)
    return RedirectResponse('/montadoras_list', status_code=303)

@app.get('/montadoras_edit/{id}')
def montadora_edit(request: Request, id: str, db: Session = Depends(get_db)):
    print(f"ID recebido para edição: {id}")
    montadora = repository.get_by_id(db, id)
    if not montadora:
        print(f"Montadora não encontrada com ID {id}")
        return templates.TemplateResponse('404.html', {'request': request}, status_code=404)
    return templates.TemplateResponse('montadora_form.html', {'montadora': montadora, 'request': request})

@app.post('/montadora_update/{id}')
def montadora_update(id: str, nome: str = Form(...), pais: str = Form(...), ano: int = Form(...), db: Session = Depends(get_db)):
    print(f"ID recebido para atualização: {id}")
    print(f"Nome: {nome}, País: {pais}, Ano: {ano}")
    
    montadora = repository.get_by_id(db, id)
    if montadora:
        montadora.nome = nome
        montadora.pais = pais
        montadora.ano_fundacao = ano
        repository.update(db, montadora)
        print(f"Montadora atualizada: {montadora}")
    else:
        print(f"Montadora com ID {id} não encontrada.")
        
    return RedirectResponse('/montadoras_list', status_code=303)



@app.post('/montadora_delete/{id}')
def montadora_delete(id: str, db: Session = Depends(get_db)):
    repository.delete(db, id)
    return RedirectResponse('/montadoras_list', status_code=303)