"""Точка входа приложения ПЗ №5 «Шаблоны в FastAPI»."""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

from todo import todo_router

app = FastAPI(
    title="PetProjectUUST",
    description="Todo-приложение с шаблонами Jinja2 из ПЗ №5",
    version="3.0.0",
)

templates = Jinja2Templates(directory="templates/")


def _render_error(request: Request, status_code: int, detail):
    """Браузеру отдаём HTML-страницу, а JSON-API — прежний JSON-ответ."""
    if "text/html" in request.headers.get("accept", ""):
        return templates.TemplateResponse(
            request,
            "error.html",
            {"status_code": status_code, "detail": detail},
            status_code=status_code,
        )
    return JSONResponse({"detail": detail}, status_code=status_code)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return _render_error(request, exc.status_code, exc.detail)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return _render_error(
        request,
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        "Некорректные данные запроса.",
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return _render_error(
        request,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "Внутренняя ошибка сервера. Попробуйте позже.",
    )


@app.get("/")
async def welcome() -> dict:
    return {"message": "Hello World, Фатихов А.Д.!"}


app.include_router(todo_router)