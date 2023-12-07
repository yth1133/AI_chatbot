import gradio as gr


def respond(message, chat_history):  # 채팅봇의 응답을 처리하는 함수를 정의합니다.
    bot_message = message + "안녕"
    chat_history.append((message, bot_message))  # 채팅 기록에 사용자의 메시지와 봇의 응답을 추가합니다.

    return "", chat_history  # 수정된 채팅 기록을 반환합니다.

with gr.Blocks() as demo:  # gr.Blocks()를 사용하여 인터페이스를 생성합니다.
    chatbot = gr.Chatbot(label="채팅창")  # '채팅창'이라는 레이블을 가진 채팅봇 컴포넌트를 생성합니다.
    msg = gr.Textbox(label="입력")  # '입력'이라는 레이블을 가진 텍스트박스를 생성합니다.
    clear = gr.Button("초기화")  # '초기화'라는 레이블을 가진 버튼을 생성합니다.

    msg.submit(respond, [msg, chatbot], [msg, chatbot])  # 텍스트박스에 메시지를 입력하고 제출하면 respond 함수가 호출되도록 합니다.
    clear.click(lambda: None, None, chatbot, queue=False)  # '초기화' 버튼을 클릭하면 채팅 기록을 초기화합니다.

demo.launch(debug=True) 