from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# 静的ファイルへのルーティング
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    messages = [
        {"icon": "🙂", "text": "こんにちは！"},
        {"icon": "🤖", "text": "こんにちは、私はロボットです。"},
        {"icon": "🙂", "text": "FastAPIを使って楽しくチャットしています。"},
        {"icon": "🤖", "text": "素晴らしい！ 私も楽しんでいます。"},
        {"icon": "🙂", "text": "こんにちは！"},
        {"icon": "🤖", "text": "こんにちは、私はロボットです。"},
        {"icon": "🙂", "text": "FastAPIを使って楽しくチャットしています。"},
        {"icon": "🤖", "text": "素晴らしい！ 私も楽しんでいます。"},
        {"icon": "🙂", "text": "こんにちは！"},
        {"icon": "🤖", "text": "こんにちは、私はロボットです。"},
        {"icon": "🙂", "text": "FastAPIを使って楽しくチャットしています。"},
        {"icon": "🤖", "text": "素晴らしい！ 私も楽しんでいます。"},
    ]

    return templates.TemplateResponse("index.html", {"request": request, "messages": messages})
