import openai
import time
import os
import gradio as gr
# from dotenv import load_dotenv, find_dotenv

#load_dotenv(find_dotenv())
key = os.getenv("OPENAI_API_KEY")

# Initialize the client
client = openai.OpenAI(
    api_key=key
)

file = client.files.retrieve(
    file_id="file-myOPkDcUdM7eIj9HOfRrl3DD"
)

assistant = client.beta.assistants.retrieve(
    assistant_id="asst_xq0jreBs6VfI91fK7FQ5CSQC"
)

thread = client.beta.threads.create()

def main(query):
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=query
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    while True:
        time.sleep(5)

        # Retrieve the run status
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

        # If run is completed, get messages
        if run_status.status == 'completed':
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            response = ""
            # Loop through messages and print content based on role
            for msg in messages.data:
                role = msg.role
                # Skip the first user message
                #TODO: Remove bandaid solution
                first_user_message = True
                if role == "user" and first_user_message:
                    first_user_message = False
                    continue
                content = msg.content[0].text.value
                response += f"{content}\n\n"
            return response+"\n\n"
        else:
            continue


iface = gr.Interface(fn=main, inputs="textbox", outputs="textbox", title="-old BETA").launch()
iface.launch()