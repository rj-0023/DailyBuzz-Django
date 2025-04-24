from django.shortcuts import render, redirect,  HttpResponseRedirect
from django.urls import reverse
from .models import TodoList
from newsapi import NewsApiClient
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import python_weather
import asyncio
from dotenv import load_dotenv
import os
from rest_framework import viewsets
from .serializers import TodoSerializer
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    return render(request, "home.html")

@login_required
def tasks(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        city = data.get('city', 'Unknown')
        async def fetch_weather(city_name) -> None:

        # Declare the client. The measuring unit used defaults to the metric system (celcius, km/h, etc.)
            async with python_weather.Client(unit=python_weather.METRIC) as client:

                # Fetch a weather forecast from a city.
                weather = await client.get(city_name)
                return {
                        'temp': weather.temperature,
                        'description': str(weather.kind)
                    }
        try:
            weather_data = asyncio.run(fetch_weather(city))
        except Exception as e:
            print("Weather fetch error:", e)
            weather_data = {
                'temp': 'N/A',
                'description': 'Unavailable'
            }
        return JsonResponse({
            'city': city,
            'temperature': weather_data['temp'],
            'sky_text': weather_data['description'],
        })    
    todos = TodoList.objects.filter(user=request.user)
    news = get_news()
    return render(request, "tasks.html", {"todos": todos, "news": news})

@login_required
def create_task(request):
    if request.method=="POST":
        task_name = request.POST.get("task")
        to_be_completed = request.POST.get("to_be_completed")

        TodoList.objects.create(user=request.user,
                                task=task_name,
                                to_be_completed = to_be_completed)
        return redirect("tasks")
    return render(request, "create_task.html")

@login_required
def update_task(request, id):
    task = TodoList.objects.get(id=id)
    
    if request.method == "POST":
        task_name = request.POST.get("task")
        to_be_completed = request.POST.get("to_be_completed")
        is_completed = request.POST.get('completed') == 'on'
        
        task.task_name = task_name
        task.to_be_completed = to_be_completed
        task.completed = is_completed
        task.save()
        return redirect("tasks")
    return render(request, "update_task.html", {"task":task})

@login_required
def delete_task(request, id):
    task = TodoList.objects.get(id=id)
    task.delete()
    return redirect('tasks')

def get_news():
    load_dotenv()  
    api_key = os.getenv("API_KEY")
    news_api = NewsApiClient(api_key=api_key)

    # /v2/top-headlines
    top_headlines = news_api.get_top_headlines(
                                            language='en',
                                            country='us')
    print(len(top_headlines["articles"]))
    return top_headlines["articles"]


class TodoViewSet(viewsets.ModelViewSet):
    queryset = TodoList.objects.all()
    serializer_class = TodoSerializer



def user_register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tasks')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form':form})



def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')


@csrf_exempt
@login_required
def voice_to_task(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get("text", "")
            if not text:
                return JsonResponse({"error": "No text provided"}, status=400)

            # Import and use your model inference
            from .gemini import your_model_inference
            result = your_model_inference(text)
            print(result)
            if result["intent"] == "create_task":
                from .models import TodoList
                TodoList.objects.create(
                    user=request.user,
                    task=result["task"],
                    to_be_completed=result["datetime"]
                )
                
                return JsonResponse({"status": "success", "task": result["task"]})
            else:
                return JsonResponse({"status": "ignored", "reason": "Unsupported intent"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid method"}, status=405)
