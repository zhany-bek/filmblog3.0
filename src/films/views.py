from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Film
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from bs4 import BeautifulSoup
from django.core.files import File

import requests
import os, io

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid username or password."
            return render(request, 'films/login.html', {'error_message': error_message})

    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'films/login.html')

def logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def index(request):
    if request.method == 'POST':
        film_title = request.POST['title']
        url = f"https://www.imdb.com/find?q={film_title}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
        }
    
        # Send a GET request to the search URL with custom headers
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        matches = soup.find_all(string=lambda text: film_title.lower() in text.lower())
        

        return render(request, 'films/home.html', {
            'urls': matches
        })
    
    return render(request, 'films/home.html')
