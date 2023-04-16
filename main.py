from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import WebSocket

from utils.save_load_json import load_data_from_json, save_data_to_json
from utils.prompt_prepare import prepare_chat, prepare_emoji

chat_chain = prepare_chat()
emoji_chain = prepare_emoji()

app = FastAPI()

# 静的ファイルへのルーティング
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    messages = load_data_from_json()

    return templates.TemplateResponse(
        "index.html", {"request": request, "messages": messages}
    )


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # WebSocket接続を確立
    await websocket.accept()

    # クライアントとの対話を繰り返します
    while True:
        # クライアントからのメッセージを受信
        data = await websocket.receive_text()

        # 大規模言語モデルでの処理（実際にはOpenAIやChatGPTなどのAPI呼び出し）
        response_content = chat_chain.run(history=load_data_from_json(), text=data)
        response = {
            "emoji": "💬",
            "ai_chat": response_content,
            "human_chat": data,
        }
        save_data_to_json(response)
        # レスポンスをクライアントに送信
        await websocket.send_json(response)
