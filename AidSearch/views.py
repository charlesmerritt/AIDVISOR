from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import openai
import os
import time
import json
from .models import User, Scholarship, Info
from .forms import CreateNewUserForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


def home(request):
    return render(request, 'AidSearch/index.html', )


@login_required
def history(request):
    return render(request, 'AidSearch/history.html')


@login_required
def myaccount(request):
    return render(request, 'AidSearch/myaccount.html')


@login_required
def resources(request):
    return render(request, 'AidSearch/resources.html')


@login_required
def saved(request):
    scholarships = Scholarship.objects.filter(user=request.user)
    return render(request, 'AidSearch/saved.html', {'scholarships': scholarships})


def register(request):
    return render()


@login_required
@require_http_methods(["POST"])
def save_scholarship(request):
    data = request.POST
    title = data.get('title')

    if title:
        Scholarship.objects.create(user=request.user, title=title)

    return redirect('/saved')


@login_required
@require_http_methods(["POST"])
def edit_user_details(request):
    # Assuming you're receiving a user ID and details to update as JSON
    user_id = request.POST.get('user_id')
    age = request.POST.get('age')
    gender = request.POST.get('gender')
    # Add more fields as necessary

    try:
        user_info = Info.objects.get(user_id=user_id)
        user_info.age = age if age is not None else user_info.age
        user_info.gender = gender if gender is not None else user_info.gender
        # Update more fields as necessary
        user_info.save()

        return JsonResponse({'status': 'success', 'message': 'User details updated successfully.'})
    except Info.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404)


@login_required
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
    if key is not None or "":
        print("Key found")
    else:
        print("Key not found, have you added the API key to your environment?")

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
