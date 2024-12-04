from crm_app.models import Client  # Import the Client model from crm_app
from .models import Poem, PoemStatistics, Category
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import requests
import json
import random
from django.http import JsonResponse
from django.conf import settings
import logging
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
logger = logging.getLogger(__name__)

# List of predefin
# Vue pour l'inscription des utilisateurs
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optionnel : Créer un client pour chaque utilisateur
            Client.objects.create(user=user)
            login(request, user)
            return redirect('generate_poetry')  # Rediriger vers la génération de poésie
    else:
        form = UserCreationForm()
    return render(request, 'textgen/signup.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            return render(request, 'textgen/login.html', {'error': 'Both fields are required.'})
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('generate_poetry')
        else:
            return render(request, 'textgen/login.html', {'error': 'Invalid credentials'})
    return render(request, 'textgen/login.html')


# List of predefined prompts or themes
predefined_prompts = [
    "A beautiful sunset over the ocean.",
    "A forest filled with whispers of ancient trees.",
    "A lonely star in the midnight sky.",
    "A flower blooming in the spring rain.",
    "The sound of waves crashing on a rocky shore.",
    "A dream that dances in the quiet night.",
    "The morning dew on a spider's web."
]

def generate_text(request):
    if request.method == 'GET':  # Change to GET request
        # Select a random prompt from the predefined list
        prompt = random.choice(predefined_prompts)

        # Define the OpenAI prompt to generate a poem
        prompt_content = f"""
        You are a poet. Please create a beautiful, creative poem based on the following prompt:

        {prompt}
        """

        # Define the API request URL and headers
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}"
        }

        data = {
            "model": "gpt-4",  # Using GPT-4 (or another available model)
            "messages": [
                {"role": "system", "content": "You are a poet."},
                {"role": "user", "content": prompt_content.strip()}
            ],
            "max_tokens": 150,  # Limit to a short poem
            "temperature": 0.7,  # Creative temperature for poetry
            "n": 1,  # Number of responses
            "stop": None
        }

        try:
            # Make the API request to OpenAI
            response = requests.post(url, headers=headers, data=json.dumps(data), timeout=60)
            response.raise_for_status()  # Raise an error for bad responses

            # Parse the OpenAI response
            response_json = response.json()
            poem_text = response_json['choices'][0]['message']['content'].strip()

            logger.info(f"Generated poem: {poem_text}")

            # Return the poem as a JSON response
            return JsonResponse({'poem': poem_text})

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            return JsonResponse({'error': f"Request error: {e}"}, status=500)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return JsonResponse({'error': f"JSON decode error: {e}"}, status=500)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return JsonResponse({'error': f"Unexpected error: {e}"}, status=500)

    # If not a GET request, return an error message
    return JsonResponse({'error': 'Invalid request method. Please use GET.'}, status=400)
def generate_poetry(request):
    if request.method == 'GET':  # Handle GET request
        # Ensure categories exist in the database
        create_default_categories()

        # Define a list of predefined categories
        categories = [
            "Nature", "Love", "Fantasy", "Adventure", "Mystery",
            "Horror", "Science Fiction", "Romance", "Comedy", "Tragedy"
        ]

        # Select a random prompt from the predefined list
        prompt = random.choice(predefined_prompts)

        # Get the client's preferred language
        client = request.user.client
        preferred_language = client.preferred_language

        # Randomly assign a category from the predefined list
        selected_category = random.choice(categories)

        # Define the OpenAI prompt to generate poetry, including language context and category
        prompt_content = f"""
        You are a poet. Please create a beautiful, creative poem based on the following prompt:

        {prompt}

        The poem should belong to the category of {selected_category}.
        """

        # Modify the language-based instructions
        if preferred_language == 'fr':
            prompt_content += "\n\nPlease write the poem in French."
        else:
            prompt_content += "\n\nPlease write the poem in English."

        # Define the API request URL and headers
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}"
        }

        data = {
            "model": "gpt-4",  # Using GPT-4 for generating the poem
            "messages": [
                {"role": "system", "content": "You are a poet."},
                {"role": "user", "content": prompt_content.strip()}
            ],
            "max_tokens": 150,  # Limit to a short poem
            "temperature": 0.7,  # Creative temperature for poetry
            "n": 1,  # Number of responses
            "stop": None
        }

        try:
            # Make the API request to OpenAI
            response = requests.post(url, headers=headers, data=json.dumps(data), timeout=60)
            response.raise_for_status()  # Raise an error for bad responses

            # Parse the OpenAI response
            response_json = response.json()
            poem_text = response_json['choices'][0]['message']['content'].strip()

            # Check if the selected category exists in the database
            try:
                category = Category.objects.get(name=selected_category)
            except Category.DoesNotExist:
                # Handle case where the category doesn't exist in the database
                logger.warning(f"Category '{selected_category}' does not exist. Assigning default category.")
                # Assign a fallback category (default or any category of your choice)
                category = Category.objects.get(name="Nature")  # Default category (e.g., Nature)

            # Ensure PoemStatistics exists for the category
            if not hasattr(category, 'statistics'):
                # Create PoemStatistics if it does not exist
                PoemStatistics.objects.get_or_create(category=category)

            # Save the poem to the database with the assigned category
            poem = Poem.objects.create(user=request.user, text=poem_text, language=preferred_language, category=category)

            # Update the statistics for the category
            poem.category.statistics.update_statistics()

            logger.info(f"Generated and saved poem in category {category.name}: {poem_text}")

            # Return the poem as a rendered HTML page
            return render(request, 'textgen/result.html', {
                'poem': poem_text,
                'language': preferred_language,
                'category': category.name,
                'error': None  # No error if the poem was generated successfully
            })

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            return render(request, 'textgen/result.html', {
                'poem': None,
                'error': f"Request error: {e}",
            })
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return render(request, 'textgen/result.html', {
                'poem': None,
                'error': f"JSON decode error: {e}",
            })
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return render(request, 'textgen/result.html', {
                'poem': None,
                'error': f"Unexpected error: {e}",
            })

    # If not a GET request, return an error message
    return JsonResponse({'error': 'Invalid request method. Please use GET.'}, status=400)

def create_default_categories():
    categories = [
        "Nature", "Love", "Fantasy", "Adventure", "Mystery",
        "Horror", "Science Fiction", "Romance", "Comedy", "Tragedy"
    ]

    for category in categories:
        # This will create the category if it doesn't exist or do nothing if it exists
        Category.objects.get_or_create(name=category, description=f"Category for {category} poems.")
def view_poems(request):
    # Get the poems associated with the logged-in user
    poems = Poem.objects.filter(user=request.user).order_by('-created_at').select_related('category')

    # For each poem, attach the number of poems in its category
    for poem in poems:
        if poem.category:
            # Ensure PoemStatistics exists for the category
            stats, created = PoemStatistics.objects.get_or_create(category=poem.category)
            stats.update_statistics()
            # Attach the number of poems to the poem instance
            poem.num_poems_in_category = stats.number_of_poems
        else:
            poem.num_poems_in_category = 0

    return render(request, 'textgen/poems_list.html', {
        'poems': poems,
    })
