from typing import Optional
from fastapi import FastAPI, HTTPException, Request, Depends, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from models.models import Modelo, Montadora, Veiculo
from persistence.database import get_db
from persistence.montadora_repository import MontadoraRepository
from persistence.modelo_repository import ModeloRepository
from persistence.veiculo_repository import VeiculoRepository
from fastapi import APIRouter
import os


app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

montadora_repository = MontadoraRepository()
modelo_repository = ModeloRepository()
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

@app.post('/montadora_update/{id}')
def montadora_update(id: str, nome: str = Form(...), pais: str = Form(...), ano: int = Form(...), db: Session = Depends(get_db)):
    montadora = montadora_repository.get_by_id(db, id)

    if montadora:
        montadora.nome = nome
        montadora.pais = pais
        montadora.ano_fundacao = ano
        montadora_repository.update(db, montadora)
        return RedirectResponse('/montadoras_list', status_code=303)

    return RedirectResponse('/montadoras_list', status_code=404)

@app.post('/montadora_delete/{id}')
def montadora_delete(id: str, db: Session = Depends(get_db)):
    montadora_repository.delete(db, id)
    return RedirectResponse('/montadoras_list', status_code=303)

@app.get('/montadora_save_txt')
def salvar_dados_em_arquivo(db: Session = Depends(get_db)):
    data_folder = 'data'
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    montadoras = montadora_repository.get_all(db)
    montadoras_file_path = os.path.join(data_folder, 'montadoras.txt')
    
    with open(montadoras_file_path, 'w') as file:
        for montadora in montadoras:
            linha = f"{montadora.nome};{montadora.pais};{montadora.ano_fundacao}\n"
            file.write(linha)

    modelos = modelo_repository.get_all(db)
    modelos_file_path = os.path.join(data_folder, 'modelos.txt')

    with open(modelos_file_path, 'w') as file:
        for modelo in modelos:
            linha = f"{modelo.nome};{modelo.valor_referencia};{modelo.motorizacao};{modelo.turbo};{modelo.automatico}\n"
            file.write(linha)

    return RedirectResponse('/montadoras_list', status_code=303)

@app.get("/montadora/{montadora_id}/modelos_list")
def modelos_list(montadora_id: str, request: Request, db: Session = Depends(get_db)):
    montadora = db.query(Montadora).filter(Montadora.id == montadora_id).first()
    modelos = db.query(Modelo).filter(Modelo.montadora_id == montadora_id).all()
    
    return templates.TemplateResponse("modelos_list.html", {"request": request, "montadora": montadora, "modelos": modelos})

@app.get('/modelo_form/{montadora_id}')
@app.get('/modelo_form/{montadora_id}/{modelo_id}')
def modelo_form(request: Request, montadora_id: str, modelo_id: Optional[str] = None, db: Session = Depends(get_db)):
    montadora = db.query(Montadora).filter(Montadora.id == montadora_id).first()
    if not montadora:
        raise HTTPException(status_code=404, detail="Montadora não encontrada")

    modelo = None
    if modelo_id:
        modelo = db.query(Modelo).filter(Modelo.id == modelo_id, Modelo.montadora_id == montadora_id).first()
        if not modelo:
            raise HTTPException(status_code=404, detail="Modelo não encontrado")

    return templates.TemplateResponse('modelo_form.html', {
        'request': request,
        'montadora_id': montadora_id,
        'montadora': montadora,
        'modelo': modelo  
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
        return {"error": str(e)}

@app.post('/modelos_delete/{modelo_id}')
def modelos_delete(modelo_id: str, db: Session = Depends(get_db)):
    modelo = modelo_repository.get_by_id(db, modelo_id)
    if modelo is None:
        return {"error": "Modelo não encontrado."}
    
    montadora_id = modelo.montadora_id 
    modelo_repository.delete(db, modelo_id)
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
    motorizacao: float = Form(...),
    turbo: bool = Form(...),
    automatico: bool = Form(...),
    db: Session = Depends(get_db)
):
    modelo_existente = modelo_repository.get_by_id(db, modelo_id)
    if not modelo_existente:
        return {"error": "Modelo não encontrado."}

    modelo_existente.nome = nome
    modelo_existente.valor_referencia = valor_referencia
    modelo_existente.motorizacao = motorizacao
    modelo_existente.turbo = turbo
    modelo_existente.automatico = automatico

    modelo_repository.update(db, modelo_existente)
    return RedirectResponse(f'/montadora/{modelo_existente.montadora_id}/modelos_list', status_code=303)

# Inicializa o roteador para veículos
router = APIRouter()

# Rota para renderizar o formulário de criação de veículo
@app.get("/veiculo_form/{modelo_id}")
def veiculo_form(modelo_id: str, request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("veiculo_form.html", {"request": request, "modelo_id": modelo_id})

# Rota para criar um novo veículo e depois redirecionar para a lista de veículos
@app.post("/veiculo_create/")
def veiculo_create(
    modelo_id: str = Form(...),
    cor: str = Form(...),
    ano_fabricacao: int = Form(...),
    ano_modelo: int = Form(...),
    valor: float = Form(...),
    placa: str = Form(...),
    vendido: Optional[bool] = Form(False),
    db: Session = Depends(get_db)
):
    try:
        novo_veiculo = Veiculo(
            modelo_id=modelo_id,
            cor=cor,
            ano_fabricacao=ano_fabricacao,
            ano_modelo=ano_modelo,
            valor=valor,
            placa=placa,
            vendido=vendido
        )
        db.add(novo_veiculo)
        db.commit()
        return RedirectResponse(url=f"/modelo/{modelo_id}/veiculos_list", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

# Rota para listar veículos
@app.get("/modelo/{modelo_id}/veiculos_list")
def veiculos_list(
    modelo_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    modelo = db.query(Modelo).filter(Modelo.id == modelo_id).first()
    if modelo is None:
        raise HTTPException(status_code=404, detail="Modelo não encontrado")

    # Inicia a consulta para veículos
    query = db.query(Veiculo).filter(Veiculo.modelo_id == modelo_id)

    # Captura os parâmetros de filtro da requisição
    cor = request.query_params.get("cor")
    ano_fabricacao = request.query_params.get("ano_fabricacao")
    ano_modelo = request.query_params.get("ano_modelo")
    valor = request.query_params.get("valor")
    placa = request.query_params.get("placa")
    vendido = request.query_params.get("vendido")

    # Adiciona filtros à consulta se os parâmetros foram fornecidos
    if cor:
        query = query.filter(Veiculo.cor.ilike(f"%{cor}%"))  # Busca parcial para cor
    if ano_fabricacao:
        query = query.filter(Veiculo.ano_fabricacao == ano_fabricacao)
    if ano_modelo:
        query = query.filter(Veiculo.ano_modelo == ano_modelo)
    if valor:
        query = query.filter(Veiculo.valor == valor)
    if placa:
        query = query.filter(Veiculo.placa.ilike(f"%{placa}%"))  # Busca parcial para placa
    if vendido is not None:  # verifica se o parâmetro é fornecido
        query = query.filter(Veiculo.vendido == (vendido == 'true'))

    # Executa a consulta e obtém a lista de veículos
    veiculos = query.all()

    return templates.TemplateResponse(
        "veiculos_list.html",
        {
            "request": request,
            "modelo": modelo,
            "veiculos": veiculos
        }
    )


# Editar veículo
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

router = APIRouter()

# Editar veículo
@router.get('/veiculo_edit/{veiculo_id}')
def veiculo_edit(request: Request, veiculo_id: str, db: Session = Depends(get_db)):
    veiculo = veiculo_repository.get_by_id(db, veiculo_id)
    if veiculo is None:
        raise HTTPException(status_code=404, detail="Veículo não encontrado.")
    
    return templates.TemplateResponse('veiculo_form.html', {
        'request': request, 
        'veiculo': veiculo, 
        'modelo_id': veiculo.modelo_id
    })

# Atualizar veículo
@app.post('/veiculo_update/{veiculo_id}')
def veiculo_update(
    veiculo_id: str,
    request: Request,
    cor: str = Form(...),
    ano_fabricacao: int = Form(...),
    ano_modelo: int = Form(...),
    valor: float = Form(...),
    placa: str = Form(...),
    vendido: bool = Form(...),
    modelo_id: str = Form(...),
    db: Session = Depends(get_db)
):
    veiculo_existente = veiculo_repository.get_by_id(db, veiculo_id)
    if not veiculo_existente:
        return {"error": "Veículo não encontrado."}

    # Atualiza os dados do veículo existente
    veiculo_existente.cor = cor
    veiculo_existente.ano_fabricacao = ano_fabricacao
    veiculo_existente.ano_modelo = ano_modelo
    veiculo_existente.valor = valor
    veiculo_existente.placa = placa
    veiculo_existente.vendido = vendido
    veiculo_existente.modelo_id = modelo_id  # Se o veículo tem uma relação com um modelo

    veiculo_repository.update(db, veiculo_existente)

    return RedirectResponse(f'/montadora/{veiculo_existente.montadora_id}/veiculos_list', status_code=303)


# Deletar veículo
@router.post('/veiculo_delete/{veiculo_id}')
def veiculo_delete(veiculo_id: str, db: Session = Depends(get_db)):
    veiculo = veiculo_repository.get_by_id(db, veiculo_id)
    if veiculo is None:
        raise HTTPException(status_code=404, detail="Veículo não encontrado.")

    modelo_id = veiculo.modelo_id
    veiculo_repository.delete(db, veiculo_id)

    return RedirectResponse(f'/modelo/{modelo_id}/veiculos_list', status_code=303)


# Adiciona o roteador à aplicação FastAPI
app.include_router(router)