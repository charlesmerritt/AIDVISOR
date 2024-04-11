from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import openai
import os
import time
import json
from dotenv import load_dotenv
from .models import User
from .forms import CreateNewUserForm


def home(request):
    return render(request, 'AidSearch/index.html', )


def history(request):
    return render(request, 'AidSearch/history.html')


def myaccount(request):
    return render(request, 'AidSearch/myaccount.html')


def resources(request):
    return render(request, 'AidSearch/resources.html')


def saved(request):
    return render(request, 'AidSearch/saved.html')


def create(request):
    form = CreateNewUserForm
    return render(request, 'AidSearch/create.html', {"form": form})

def register(request):
    return render()

@require_http_methods(["POST"])
def assistant_query(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    userInput = body['query']

    key = os.getenv("OPENAI_API_KEY")

    # Initialize the client
    client = openai.OpenAI(
        api_key=key
    )
    print(key)

    # TODO: Create context from user info
    file = client.files.retrieve(
        file_id="file-myOPkDcUdM7eIj9HOfRrl3DD"
    )
    if file is not None:
        print(file)
    else:
        print("No file found")

    assistant = client.beta.assistants.retrieve(
        assistant_id="asst_xq0jreBs6VfI91fK7FQ5CSQC"
    )
    if assistant is not None:
        print("assistant found")
        print(assistant)
    else:
        print("No assistant found")

    thread = client.beta.threads.create()
    print(thread)

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=userInput
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
            return JsonResponse({
                "message": messages.data[0].content[0].text.value
            })
            # Loop through messages and print content based on role
        #     for msg in messages.data:
        #         role = msg.role
        #         # Skip the first user message
        #         # TODO: Remove bandaid solution
        #         first_user_message = True
        #         if role == "user" and first_user_message:
        #             first_user_message = False
        #             continue
        #         content = msg.content[0].text.value
        #         response += f"{content}\n\n"
        #     return response + "\n\n"
        # else:
        #     continue
