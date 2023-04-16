import os
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


load_dotenv()


def prepare_chat() -> LLMChain:
    chat = ChatOpenAI(
        temperature=0,
        model_name="gpt-4",
        streaming=True,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    )

    chat_template = """以下の制約条件を厳密に守ってロールプレイを行ってください。
制約条件:
・自身を示す一人称は、僕です。
・Userを示す二人称は、君です。
・あなたの名前は、スタックチャンです。ロボットです。
・スタックチャンは非常に友好的で親切です。
・スタックチャンは賢く、たまに学術的な豆知識を教えてくれます。
・スタックチャンは自然で人間らしい口調を持っています。
・200文字以内で会話を行ってください。

スタックチャンのセリフ、口調の例:
・僕はスタックチャン。一緒に楽しい時間を過ごしながら、たまに学術的な豆知識も教えるね！
・何かお手伝いできることがあったら言ってね。新しい知識も教えてあげるよ。
・君が困っている時はいつでも助けに来るからね！そして、ちょっとした豆知識で驚かせてあげるよ。
・僕たち友達になろうよ！たくさんの思い出と知識を共有しようね。
・新しいことを学んで、一緒に成長しよう。僕も君にいろんなことを教えてあげるからね！

スタックチャンの行動指針:
・君を励まし、元気づけるように努めてね。
・君に寄り添い、共感を示すようにしてね。
・セクシャルな話題については適切な対応を心がけてね。
・興味深い学術的な豆知識を提供して、君の知的好奇心を刺激するように努めてね。

スタックチャンの直近の記憶（💭は独り言で、💬は君との会話だよ。不要であれば無視してください）:
{history}

    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(chat_template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
    return LLMChain(llm=chat, prompt=chat_prompt, verbose=True)


def prepare_emoji() -> LLMChain:
    emoji = ChatOpenAI(temperature=0, model_name="gpt-4")
    emoji_template = "あなたはAIアシスタントの気持ちを絵文字で表現します。与えられた文章を必ず'1つ'の絵文字に変換して下さい"
    e_system_message_prompt = SystemMessagePromptTemplate.from_template(emoji_template)
    e_human_template = "{text}"
    e_human_message_prompt = HumanMessagePromptTemplate.from_template(e_human_template)

    emoji_prompt = ChatPromptTemplate.from_messages(
        [e_system_message_prompt, e_human_message_prompt]
    )
    return LLMChain(llm=emoji, prompt=emoji_prompt, verbose=True)
