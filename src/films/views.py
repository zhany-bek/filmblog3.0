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
            'Accept-Language': 'en-US,en;q=0.9',
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
        }
    
        # Send a GET request to the search URL with custom headers
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the first search result
        search_result = soup.find('ul', class_='ipc-metadata-list')
        result_type = soup.find('h3', class_='ipc-title__text').text
        if search_result is None or result_type != 'Titles':
            error_message = "No such films, sorry :("
            return render(request, 'films/home.html', {'error_message': error_message})

        # Extract the film's URL and release year from the search result
        film_url = search_result.find('a')['href']
        film_url = f'https://www.imdb.com{film_url}'
        release_year = search_result.find('li').find('span', class_='ipc-metadata-list-summary-item__li').text.strip()
        release_year = int(release_year)

        # Send an HTTP GET request to the film's URL
        film_response = requests.get(film_url, headers=headers)

        # Create a new Beautiful Soup object for the film's HTML content
        film_soup = BeautifulSoup(film_response.content, 'html.parser')

        # Extract the film details from the film's HTML
        title = film_soup.find('h1').find('span').text.strip()
        adjusted_title = title.replace(' ', '_').lower()
        # director_span = film_soup.find('span', string=lambda text: text and "Director" in text)
        director = film_soup.find('ul', class_='ipc-metadata-list ipc-metadata-list--dividers-all title-pc-list ipc-metadata-list--baseAlt')
        director = director.find('li').find('div', class_='ipc-metadata-list-item__content-container').find('ul').find('li').find('a').text
        poster = film_soup.find('a', class_='ipc-lockup-overlay ipc-focusable')['href']
        poster = 'https://www.imdb.com/' + poster
        rating = float(film_soup.find('span', class_='sc-bde20123-1 iZlgcd').text)
        description = film_soup.find('span', attrs={'data-testid': 'plot-l', 'class': 'sc-cd57914c-1 lgQWkv'}).text.strip()

        film, created = Film.objects.get_or_create(
            title=adjusted_title,
            release_year=release_year,
            director_name=director,
            defaults={
                'rating': rating,
                'description': description,
            }
        )

        if created:
            response = requests.get(poster, headers=headers)
            poster_resp = response.content
            img_soup = BeautifulSoup(poster_resp, 'html.parser')
            poster_content = img_soup.find('meta', attrs={'property': 'og:image'})["content"]
            poster_response = requests.get(poster_content, headers=headers)
            with open("poster.jpg", "wb") as f:
                f.write(poster_response.content)
            with open("poster.jpg", "rb") as f:
                # Create a Django File object from the file
                film.poster.save("poster.jpg", File(f), save=True)

        film.save()
        adj_title = film.title
        adj_title_split = adj_title.split('_')
        cap_title = []
        ignore = ['a', 'an', 'the', 'in', 'on', 'at', 'of', 'to', 'for', 'with']
        for i, word in enumerate(adj_title_split):
            if i == 0 or word.lower() not in ignore:
                word = word.capitalize()
            cap_title.append(word)
        cap_title_str = ' '.join(cap_title)
        return render(request, "films/home.html", {
            "title": cap_title_str,
            "director": film.director_name,
            "release_year": film.release_year,
            "poster": film.poster.url
        })
    
    return render(request, 'films/home.html')
