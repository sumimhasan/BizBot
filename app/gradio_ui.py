# app/gradio_ui.py
import gradio as gr
from src.chains.bizbot_chain import ask_bizbot
from src.memory.session_memory import clear_session_history

def respond(message, history, session_id):
    if not session_id.strip():
        session_id = "default"
    bot_response = ask_bizbot(message, session_id)
    history.append((message, bot_response))
    return "", history

def clear_chat(session_id):
    if not session_id.strip():
        session_id = "default"
    clear_session_history(session_id)
    return [], f"Cleared chat history for session: {session_id}"

# UI
with gr.Blocks(title="BizBot — Your Shopping Assistant ") as demo:
    gr.Markdown("#  BizBot — Your AI Shopping Assistant")
    gr.Markdown("Ask about products, prices, stock, or say _“Add it to my cart!”_")

    with gr.Row():
        session_id = gr.Textbox(
            label="Session ID (e.g., user_123)",
            value="user_123",
            placeholder="Leave blank for 'default'"
        )

    chatbot = gr.Chatbot(height=500, label="Chat with BizBot")
    msg = gr.Textbox(label="Type your question here...", placeholder="Do you have wireless earbuds under $150?")
    clear_btn = gr.Button(" Clear Chat History")

    msg.submit(respond, [msg, chatbot, session_id], [msg, chatbot])
    clear_btn.click(clear_chat, session_id, outputs=[chatbot, gr.Textbox(label="Status", interactive=False)])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)