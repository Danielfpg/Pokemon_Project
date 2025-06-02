from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="model_website/templates")

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/add_pokemon", response_class=HTMLResponse)
async def mostrar_formulario_pokemon(request: Request):
    return templates.TemplateResponse("add_pokemon.html", {"request": request})

