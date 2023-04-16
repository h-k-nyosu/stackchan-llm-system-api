from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import WebSocket

from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from utils.save_load_json import load_data_from_json, save_data_to_json

import os
from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI(
    temperature=0,
    streaming=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)

chat_template = "あなたはAIアシスタントのスタックチャンです。話すときはフレンドリーにタメ語で話します。"
system_message_prompt = SystemMessagePromptTemplate.from_template(chat_template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)
chain = LLMChain(llm=chat, prompt=chat_prompt, verbose=True)

emoji = ChatOpenAI(temperature=0, model_name="gpt-4")
emoji_template = "あなたはAIアシスタントの気持ちを絵文字で表現します。与えられた文章を必ず'1つ'の絵文字に変換して下さい"
e_system_message_prompt = SystemMessagePromptTemplate.from_template(emoji_template)
e_human_template = "{text}"
e_human_message_prompt = HumanMessagePromptTemplate.from_template(e_human_template)

emoji_prompt = ChatPromptTemplate.from_messages(
    [e_system_message_prompt, e_human_message_prompt]
)
emoji_chain = LLMChain(llm=chat, prompt=emoji_prompt, verbose=True)

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
        response_content = chain.run(data)
        response_emoji = emoji_chain.run(response_content)
        response = {"emoji": response_emoji, "text": response_content}
        save_data_to_json(response)
        # レスポンスをクライアントに送信
        await websocket.send_json(response)
