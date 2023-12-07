import gradio as gr
from openai import OpenAI
import openai
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler 
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory 
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain


load_dotenv()
open_api_key = os.getenv("api_key")
os.environ['OPENAI_API_KEY'] = open_api_key

# 템플릿 설정 - 영어로 설정하는 것이 정확도 및 속도에서 더 좋은 성능을 발휘합니다.
system_ai_en = "You are an artificial intelligence assistant, and you should be able to respond to various topics such as reading PDFs, summarizing documents, managing schedules, providing weather information, searching for the shortest route, and conducting web searches. Please respond briefly in Korean."
system_ai_ko= "당신은 인공지능 비서야, pdf 읽기, 문서요약하기, 일정 관리, 날씨, 최단경로 검색, 웹 검색 등 다양한 내용에 답변할 수 있어야해"
system_setting = SystemMessagePromptTemplate.from_template(system_ai_en)

# 프롬프트 설정
prompt = ChatPromptTemplate.from_messages([
    system_setting,                                           # 역할부여
    MessagesPlaceholder(variable_name="HeyMate"),              # 메모리 저장소 설정. ConversationBufferMemory의 memory_key 와 동일하게 설정
    HumanMessagePromptTemplate.from_template("{master_user}"), # 사용자 메시지 injection
])

# 메모리 설정
memory = ConversationBufferWindowMemory(memory_key="HeyMate", 
                                  ai_prefix="AI 비서 HeyMate",
                                  human_prefix="사용자",
                                  return_messages=True,
                                  k=10)
# llm 모델 정의
chatgpt = ChatOpenAI(
    temperature=0.3,
    max_tokens=2048,
    model_name="gpt-3.5-turbo"
    ) 

# llmchain 정의
def init_conversation():
    conversation = LLMChain(
        llm=chatgpt,   # LLM
        prompt=prompt, # Prompt
        verbose=True,  # True 로 설정시 로그 출력
        memory=memory  # 메모리
    )
    return conversation

# conversation 시작
conversation = init_conversation()

# 챗봇 gpt api 사용
def conversation_gr(input_text, chat_history):
    answer = conversation({"master_user": input_text})
    ai_answer = answer['text']
    chat_history.append((input_text, ai_answer))
    print(chat_history)
    print(memory)
    return input_text, chat_history

# 챗봇 초기화 
def reset_chatbot(input_text, chat_history):
    global memory
    chat_init = [[None, '안녕하세요 AI 인공지능 비서 HeyMate 입니다. 무엇이든 시켜만 주세요']]
    memory.clear() # 메모리 초기화
    return input_text, chat_init


## 그라디오 만들기
with gr.Blocks(theme=gr.themes.Default()) as app: 
    with gr.Tab("AI 인공지능 비서"):
        with gr.Column():
            chatbot = gr.Chatbot(
                value = [
                    [None, "안녕하세요 AI 인공지능 비서 HeyMate 입니다. 무엇이든 시켜만 주세요"]
                ],
                show_label="AI HeyMate"
            )
            with gr.Group():
                with gr.Row():
                    msg = gr.Textbox(elem_id="input-text",
                        lines=1,
                        placeholder="채팅 입력창",
                        container="무엇이든 물어보세요",
                        scale=8
                    )
                    clearbtn=gr.ClearButton([msg], scale=1)
                    submit_btn = gr.Button(
                        value="보내기",
                        scale=2,
                        visible="primary",
                    )
                    submit_btn.click(conversation_gr, [msg, chatbot], [msg, chatbot])

            with gr.Row(): 
                gr.Button(value="되돌리기 ↩️") 
                initbtn = gr.Button(value="초기화 🔄️")
                initbtn.click(reset_chatbot, [msg, chatbot], [msg, chatbot]) 

    with gr.Tab("PDF 처리"):
        pass
    with gr.Tab("자동모드"):
        pass

app.launch(debug=True)