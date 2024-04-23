import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os
import time

print(os.environ)
print("Gradio Version: " + gr.__version__)

key = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    api_key=key
)


# Chatbot demo with multimodal input (text, markdown, LaTeX, code blocks, image, audio, & video).
# Shows support for streaming text.

# Define the initial instruction or context for the chatbot
initial_context = [
    ("You are a helpful and knowledgeable financial aid assistant called AIDVISOR, you must refer to yourself as AIDVISOR. Your purpose is to help direct students and others towards financial aid resources. You should be specific in your responses when providing resources and give links whenever you can.", None)
]

def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)


def add_text(history, text):
    history = history + [(text, None)]
    return history, gr.Textbox(value="", interactive=False)


def add_file(history, file):
    history = history + [((file.name,), None)]
    return history


def bot(history):
    # Get the last user input from the history
    prompt = history[-1][0]

    # Combine the initial instructions with the user's prompt
    full_prompt = initial_context[0][0] + "\n" + prompt

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": initial_context[0][0]},
            {"role": "user", "content": prompt},
        ]
    )

    # Convert the response object to a dictionary
    response_data = response.model_dump()
    response_text = response_data['choices'][0]['message']['content']

    history[-1][1] = ""
    for character in response_text:
        history[-1][1] += character
        time.sleep(0.005)  # You might want to adjust or remove the delay for instant response
        yield history


with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        label="AIDVISOR",
        elem_id="chatbot",
        bubble_full_width=False,
        avatar_images=(None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),
    )

    with gr.Row():
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter, or upload an image",
            container=False,
        )
        btn = gr.UploadButton("📁", file_types=["image", "video", "audio"])

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        bot, chatbot, chatbot, api_name="bot_response"
    )
    txt_msg.then(lambda: gr.Textbox(interactive=True), None, [txt], queue=False)
    file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=False).then(
        bot, chatbot, chatbot
    )

    chatbot.like(print_like_dislike, None, None)

demo.queue()
demo.launch(
    share=True
)
