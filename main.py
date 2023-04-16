from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import WebSocket

app = FastAPI()

# 静的ファイルへのルーティング
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    messages = [
        {"icon": "🙂", "text": "こんにちは！"},
        {"icon": "😆", "text": "こんにちは、私はロボットです。"},
        {"icon": "🥲", "text": "FastAPIを使って楽しくチャットしています。"},
        {"icon": "🤔", "text": "素晴らしい！ 私も楽しんでいます。"},
    ]

    return templates.TemplateResponse("index.html", {"request": request, "messages": messages})


@app.get("/get_message")
async def get_message():
    message = {"icon": "🤖", "text": "新しいテキスト"}
    return JSONResponse(message)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # WebSocket接続を確立
    await websocket.accept()

    # クライアントとの対話を繰り返します
    while True:
        # クライアントからのメッセージを受信
        data = await websocket.receive_text()

        # 大規模言語モデルでの処理（実際にはOpenAIやChatGPTなどのAPI呼び出し）
        response_content = "大規模言語モデルからの応答...: " + data

        # レスポンスをクライアントに送信
        await websocket.send_text(response_content)