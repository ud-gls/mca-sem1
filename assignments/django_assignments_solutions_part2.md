# Django Assignment Solutions: Part 2

## Solution for 6th qustion

### Step 1: Create the Django Project and App

Open your terminal and run the following commands:

```bash
# Create Django project
django-admin startproject task_manager

# Navigate to the project directory
cd task_manager

# Create Django app
python manage.py startapp tasks
```

### Step 2: Define the Task Model

#### `tasks/models.py`
```python
from django.db import models

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
```

### Step 3: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Implement Views and Templates

#### `tasks/views.py`
```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'tasks/task_detail.html', {'task': task})

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/create_task.html', {'form': form})

def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})

def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.completed = True
    task.save()
    return redirect('task_list')
```

#### `tasks/forms.py`
```python
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'completed']
```

#### `tasks/templates/tasks/task_list.html`
{% raw %}
```html
<!-- tasks/task_list.html -->
{% extends 'base.html' %}

{% block title %}Task List{% endblock %}

{% block content %}
  <h1>Task List</h1>
  <ul>
    {% for task in tasks %}
      <li>
        <a href="{% url 'task_detail' task.id %}">{{ task.title }}</a>
        {% if task.completed %}
          (Completed)
        {% endif %}
      </li>
    {% endfor %}
  </ul>
  <a href="{% url 'create_task' %}">Create New Task</a>
{% endblock %}
```

#### `tasks/templates/tasks/task_detail.html`
```html
<!-- tasks/task_detail.html -->
{% extends 'base.html' %}

{% block title %}{{ task.title }}{% endblock %}

{% block content %}
  <h1>{{ task.title }}</h1>
  <p>Description: {{ task.description }}</p>
  <p>Due Date: {{ task.due_date }}</p>
  <p>Priority: {{ task.priority }}</p>
  {% if task.completed %}
    <p>Status: Completed</p>
  {% else %}
    <a href="{% url 'edit_task' task.id %}">Edit Task</a>
    <a href="{% url 'complete_task' task.id %}">Mark as Completed</a>
  {% endif %}
{% endblock %}
```

#### `tasks/templates/tasks/create_task.html`
```html
<!-- tasks/create_task.html -->
{% extends 'base.html' %}

{% block title %}Create New Task{% endblock %}

{% block content %}
  <h1>Create New Task</h1>
  <form method="post" action="{% url 'create_task' %}">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Create Task</button>
  </form>
  <a href="{% url 'task_list' %}">Cancel</a>
{% endblock %}
```

#### `tasks/templates/tasks/edit_task.html`
```html
<!-- tasks/edit_task.html -->
{% extends 'base.html' %}

{% block title %}Edit Task: {{ task.title }}{% endblock %}

{% block content %}
  <h1>Edit Task: {{ task.title }}</h1>
  <form method="post" action="{% url 'edit_task' task.id %}">
    {% csrf_token %}
   

 {{ form.as_p }}
    <button type="submit">Save Changes</button>
  </form>
  <a href="{% url 'task_list' %}">Cancel</a>
{% endblock %}
```
{% endraw %}

### Step 5: Update the URLs

#### `tasks/urls.py`
```python
from django.urls import path
from .views import task_list, task_detail, create_task, edit_task, complete_task

urlpatterns = [
    path('', task_list, name='task_list'),
    path('<int:task_id>/', task_detail, name='task_detail'),
    path('create/', create_task, name='create_task'),
    path('<int:task_id>/edit/', edit_task, name='edit_task'),
    path('<int:task_id>/complete/', complete_task, name='complete_task'),
]
```

### Step 6: URL Routing

Configure the URLs in the main `urls.py` file of the project.

#### `task_manager/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),
]
```

### Step 7: Add Task Filtering and Categorization

#### Update `tasks/views.py`
Add views to filter and categorize tasks based on due date, priority, and completion status.

```python
# tasks/views.py

from django.shortcuts import render
from .models import Task

def filter_tasks(request, filter_type):
    if filter_type == 'completed':
        tasks = Task.objects.filter(completed=True)
        title = 'Completed Tasks'
    elif filter_type == 'high_priority':
        tasks = Task.objects.filter(priority='High', completed=False)
        title = 'High Priority Tasks'
    elif filter_type == 'due_soon':
        tasks = Task.objects.filter(due_date__lte='2023-12-31', completed=False)
        title = 'Tasks Due Soon'
    else:
        tasks = Task.objects.all()
        title = 'All Tasks'

    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'title': title})
```

#### Update `tasks/urls.py`
Add URLs for the new views.

```python
# tasks/urls.py

from django.urls import path
from .views import task_list, task_detail, create_task, edit_task, complete_task, filter_tasks

urlpatterns = [
    path('', task_list, name='task_list'),
    path('<int:task_id>/', task_detail, name='task_detail'),
    path('create/', create_task, name='create_task'),
    path('<int:task_id>/edit/', edit_task, name='edit_task'),
    path('<int:task_id>/complete/', complete_task, name='complete_task'),
    path('filter/<str:filter_type>/', filter_tasks, name='filter_tasks'),
]
```

#### Update `tasks/templates/tasks/task_list.html`
Modify the template to include links for filtering tasks.
{% raw %}
```html
<!-- tasks/task_list.html -->

{% extends 'base.html' %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
  <h1>{{ title }}</h1>
  <ul>
    {% for task in tasks %}
      <li>
        <a href="{% url 'task_detail' task.id %}">{{ task.title }}</a>
        {% if task.completed %}
          (Completed)
        {% endif %}
      </li>
    {% endfor %}
  </ul>
  <a href="{% url 'create_task' %}">Create New Task</a><br>
  <a href="{% url 'filter_tasks' 'all' %}">All Tasks</a>
  <a href="{% url 'filter_tasks' 'completed' %}">Completed Tasks</a>
  <a href="{% url 'filter_tasks' 'high_priority' %}">High Priority Tasks</a>
  <a href="{% url 'filter_tasks' 'due_soon' %}">Tasks Due Soon</a>
{% endblock %}
```
{% endraw %}

Now, you can filter tasks based on completion status, priority, and due date by clicking on the respective links.

### Step 8: Add Task Reminders

#### Update `tasks/models.py`
Add a new field for reminders to the `Task` model.

```python
# tasks/models.py

from django.db import models

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    completed = models.BooleanField(default=False)
    reminders = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
```

#### Update `tasks/forms.py`
Include the new field in the form.

```python
# tasks/forms.py

from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'completed', 'reminders']
```

#### Update `tasks/templates/tasks/create_task.html` and `tasks/templates/tasks/edit_task.html`
Include the new field in the task creation and editing forms.
{% raw %}
```html
<!-- tasks/create_task.html -->

{% extends 'base.html' %}

{% block title %}Create New Task{% endblock %}

{% block content %}
  <h1>Create New Task</h1>
  <form method="post" action="{% url 'create_task' %}">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Create Task</button>
  </form>
  <a href="{% url 'task_list' %}">Cancel</a>
{% endblock %}
```

```html
<!-- tasks/edit_task.html -->

{% extends 'base.html' %}

{% block title %}Edit Task: {{ task.title }}{% endblock %}

{% block content %}
  <h1>Edit Task: {{ task.title }}</h1>
  <form method="post" action="{% url 'edit_task' task.id %}">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save Changes</button>
  </form>
  <a href="{% url 'task_list' %}">Cancel</a>
{% endblock %}
```
{% endraw %}

## Solution for 7th qustion

### Step 1: Create the Django Project and App

Open your terminal and run the following commands:

```bash
# Create Django project
django-admin startproject photo_share

# Navigate to the project directory
cd photo_share

# Create Django app
python manage.py startapp photos
```

### Step 2: Define the Photo Model

#### `photos/models.py`
```python
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    caption = models.CharField(max_length=255)
    tags = models.CharField(max_length=255)

    def __str__(self):
        return self.caption

    def create_thumbnail(self):
        max_size = (300, 300)
        image = Image.open(self.image)
        image.thumbnail(max_size)
        thumbnail_io = BytesIO()
        image.save(thumbnail_io, 'JPEG', quality=85)
        thumbnail = InMemoryUploadedFile(
            thumbnail_io,
            None,
            f'{self.image.name.split(".")[0]}_thumb.jpg',
            'image/jpeg',
            thumbnail_io.tell,
            None
        )
        self.thumbnail.save(thumbnail.name, thumbnail)
```

### Step 3: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Implement Views and Templates

#### `photos/views.py`
```python
from django.shortcuts import render, redirect
from .models import Photo
from .forms import PhotoForm
from django.contrib.auth.decorators import login_required

@login_required
def photo_list(request, tag=None, username=None):
    photos = Photo.objects.all()

    if tag:
        photos = photos.filter(tags__icontains=tag)

    if username:
        user = User.objects.get(username=username)
        photos = photos.filter(user=user)

    return render(request, 'photos/photo_list.html', {'photos': photos, 'tag': tag, 'username': username})
```

#### `photos/forms.py`
```python
from django import forms
from .models import Photo

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption', 'tags']
```

#### `templates/base.html`
{% raw %}
```html
<!-- templates/base.html -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Photo Share{% endblock %}</title>
    <!-- Add your CSS styles or link to external stylesheets here -->
</head>
<body>

<nav>
    <ul>
        <li><a href="{% url 'photo_list' %}">All Photos</a></li>
        <li><a href="{% url 'photo_list_by_tag' 'landscape' %}">Filter by Landscape</a></li>
        <li><a href="{% url 'photo_list_by_tag' 'portrait' %}">Filter by Portrait</a></li>
        <!-- Add more navigation links as needed -->
        {% if user.is_authenticated %}
            <li><a href="{% url 'upload_photo' %}">Upload Photo</a></li>
            <li><a href="{% url 'photo_list_by_user' user.username %}">My Photos</a></li>
            <li><a href="{% url 'logout' %}">Logout</a></li>
        {% else %}
            <li><a href="{% url 'login' %}">Login</a></li>
            <li><a href="{% url 'signup' %}">Sign Up</a></li>
        {% endif %}
    </ul>
</nav>

{% block content %}
    <!-- The content of each page will go here -->
{% endblock %}

<!-- Add your JavaScript scripts or link to external scripts here -->
</body>
</html>
```

#### `photos/templates/photos/photo_list.html`
```html
<!-- photos/photo_list.html -->
{% extends 'base.html' %}

{% block title %}
  {% if tag %}
    Photos - Tag: {{ tag }}
  {% elif username %}
    Photos - User: {{ username }}
  {% else %}
    Photo List
  {% endif %}
{% endblock %}

{% block content %}
  <h1>Photo List</h1>
  {% if tag %}
    <p>Filtering by Tag: {{ tag }}</p>
  {% elif username %}
    <p>Filtering by User: {{ username }}</p>
  {% endif %}
  <ul>
    {% for photo in photos %}
      <li>
        <img src="{{ photo.thumbnail.url }}" alt="{{ photo.caption }}">
        <p>Caption: {{ photo.caption }}</p>
        <p>Tags: {{ photo.tags }}</p>
      </li>
    {% endfor %}
  </ul>
  <a href="{% url 'upload_photo' %}">Upload Photo</a>
  <br>
  <a href="{% url 'photo_list' %}">All Photos</a>
  <a href="{% url 'photo_list_by_tag' 'landscape' %}">Filter by Landscape</a>
  <a href="{% url 'photo_list_by_tag' 'portrait' %}">Filter by Portrait</a>
  <br>
  <a href="{% url 'photo_list_by_user' request.user.username %}">My Photos</a>
{% endblock %}
```
{% endraw %}

### Step 5: Update the URLs

#### `photos/urls.py`
```python
from django.urls import path
from .views import photo_list

urlpatterns = [
    path('', photo_list, name='photo_list'),
    path('tag/<str:tag>/', photo_list, name='photo_list_by_tag'),
    path('user/<str:username>/', photo_list, name='photo_list_by_user'),
]
```

### Step 6: Create the Upload Photo View

#### `photos/views.py`
```python
from django.shortcuts import render, redirect
from .models import Photo
from .forms import PhotoForm
from django.contrib.auth.decorators import login_required

@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            photo.create_thumbnail()
            return redirect('photo_list')
    else:
        form = PhotoForm()
    return render(request, 'photos/upload_photo.html', {'form': form})
```

#### `photos/templates/photos/upload_photo.html`
{% raw %}
```html
<!-- photos/upload_photo.html -->
{% extends 'base.html' %}

{% block title %}Upload Photo{% endblock %}

{% block content %}
  <h1>Upload Photo</h1>
  <form method="post" enctype="multipart/form-data" action="{% url 'upload_photo' %}">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Upload</

button>
  </form>
  <a href="{% url 'photo_list' %}">Back to Photo List</a>
{% endblock %}
```
{% endraw %}

### Step 7: Update the URLs

#### `photo_share/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('photos/', include('photos.urls')),
]
```

### Step 8: Configure Media Settings

Make sure to configure media settings in your `settings.py` for development:

#### `photo_share/settings.py`
```python
# ...

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Step 9: Implement Image Resizing and Thumbnails

For image resizing and thumbnails, you can use the `Pillow` library. Install it using:

```bash
pip install Pillow
```

#### Update `photos/models.py`
Add a method to generate a thumbnail.

```python
# photos/models.py

from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class Photo(models.Model):
    # ... (previous code)

    def create_thumbnail(self):
        max_size = (300, 300)
        image = Image.open(self.image)
        image.thumbnail(max_size)
        thumbnail_io = BytesIO()
        image.save(thumbnail_io, 'JPEG', quality=85)
        thumbnail = InMemoryUploadedFile(
            thumbnail_io,
            None,
            f'{self.image.name.split(".")[0]}_thumb.jpg',
            'image/jpeg',
            thumbnail_io.tell,
            None
        )
        self.thumbnail.save(thumbnail.name, thumbnail)
```

#### Update `photos/forms.py`
Include the thumbnail field in the form.

```python
# photos/forms.py

from django import forms
from .models import Photo

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption', 'tags']
```

#### Update `photos/views.py`
Call the `create_thumbnail` method after saving a photo.

```python
# photos/views.py

from django.shortcuts import render, redirect
from .models import Photo
from .forms import PhotoForm

@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            photo.create_thumbnail()
            return redirect('photo_list')
    else:
        form = PhotoForm()
    return render(request, 'photos/upload_photo.html', {'form': form})
```

#### Update `photos/templates/photos/photo_list.html`
Display the thumbnail.
{% raw %}
```html
<!-- photos/photo_list.html -->
{% extends 'base.html' %}

{% block title %}
  {% if tag %}
    Photos - Tag: {{ tag }}
  {% elif username %}
    Photos - User: {{ username }}
  {% else %}
    Photo List
  {% endif %}
{% endblock %}

{% block content %}
  <h1>Photo List</h1>
  {% if tag %}
    <p>Filtering by Tag: {{ tag }}</p>
  {% elif username %}
    <p>Filtering by User: {{ username }}</p>
  {% endif %}
  <ul>
    {% for photo in photos %}
      <li>
        <img src="{{ photo.thumbnail.url }}" alt="{{ photo.caption }}">
        <p>Caption: {{ photo.caption }}</p>
        <p>Tags: {{ photo.tags }}</p>
      </li>
    {% endfor %}
  </ul>
  <a href="{% url 'upload_photo' %}">Upload Photo</a>
  <br>
  <a href="{% url 'photo_list' %}">All Photos</a>
  <a href="{% url 'photo_list_by_tag' 'landscape' %}">Filter by Landscape</a>
  <a href="{% url 'photo_list_by_tag' 'portrait' %}">Filter by Portrait</a>
  <br>
  <a href="{% url 'photo_list_by_user' request.user.username %}">My Photos</a>
{% endblock %}
```
{% endraw %}

### Step 10: Run the Development Server

Run the development server to test your application:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/photos/` in your web browser to see the photo list.

## Solution for 8th qustion

Certainly! Let's go through the steps to create a Django project named "restaurant_booking" with three apps: "restaurants," "tables," and "reservations." We'll define models for Restaurant, Table, and Reservation with appropriate fields. Then, we'll implement views and templates to display a list of restaurants with menus and availability, allow users to search for restaurants based on location, cuisine, and date, and enable users to make reservations online and manage existing bookings.

### Step 1: Create the Django Project and Apps

```bash
# Create Django project
django-admin startproject restaurant_booking

# Navigate to the project directory
cd restaurant_booking

# Create Django apps
python manage.py startapp restaurants
python manage.py startapp tables
python manage.py startapp reservations
```

### Step 2: Define Models

#### `restaurants/models.py`
```python
from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    cuisine = models.CharField(max_length=50)
    menu = models.TextField()

    def __str__(self):
        return self.name
```

#### `tables/models.py`
```python
from django.db import models
from restaurants.models import Restaurant

class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    number = models.IntegerField()
    capacity = models.IntegerField()

    def __str__(self):
        return f"Table {self.number} at {self.restaurant.name}"
```

#### `reservations/models.py`
```python
from django.db import models
from restaurants.models import Restaurant
from tables.models import Table
from django.contrib.auth.models import User

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"Reservation for {self.user.username} at {self.restaurant.name}, Table {self.table.number} on {self.date} at {self.time}"
```

### Step 3: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Implement Views and Templates

#### `restaurants/views.py`
```python
from django.shortcuts import render
from .models import Restaurant

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurants/restaurant_list.html', {'restaurants': restaurants})
```

#### `tables/views.py`
```python
from django.shortcuts import render
from .models import Table

def table_list(request, restaurant_id):
    tables = Table.objects.filter(restaurant_id=restaurant_id)
    return render(request, 'tables/table_list.html', {'tables': tables})
```

#### `reservations/views.py`
```python
from django.shortcuts import render
from .models import Reservation

def reservation_list(request, user_id):
    reservations = Reservation.objects.filter(user_id=user_id)
    return render(request, 'reservations/reservation_list.html', {'reservations': reservations})
```

### Step 5: Implement Templates

#### `restaurants/templates/restaurants/restaurant_list.html`
{% raw %}
```html
<!-- restaurants/restaurant_list.html -->
{% extends 'base.html' %}

{% block title %}Restaurant List{% endblock %}

{% block content %}
  <h1>Restaurant List</h1>
  <ul>
    {% for restaurant in restaurants %}
      <li>
        <h2>{{ restaurant.name }}</h2>
        <p>Location: {{ restaurant.location }}</p>
        <p>Cuisine: {{ restaurant.cuisine }}</p>
        <p>Menu: {{ restaurant.menu }}</p>
        <a href="{% url 'table_list' restaurant.id %}">View Tables</a>
      </li>
    {% endfor %}
  </ul>
{% endblock %}
```

#### `tables/templates/tables/table_list.html`
```html
<!-- tables/table_list.html -->
{% extends 'base.html' %}

{% block title %}Table List{% endblock %}

{% block content %}
  <h1>Table List</h1>
  <ul>
    {% for table in tables %}
      <li>
        <h2>Table {{ table.number }}</h2>
        <p>Capacity: {{ table.capacity }}</p>
      </li>
    {% endfor %}
  </ul>
{% endblock %}
```

#### `reservations/templates/reservations/reservation_list.html`
```html
<!-- reservations/reservation_list.html -->
{% extends 'base.html' %}

{% block title %}Reservation List{% endblock %}

{% block content %}
  <h1>Reservation List</h1>
  <ul>
    {% for reservation in reservations %}
      <li>
        <h2>{{ reservation.restaurant.name }}</h2>
        <p>Table: {{ reservation.table.number }}</p>
        <p>Date: {{ reservation.date }}</p>
        <p>Time: {{ reservation.time }}</p>
      </li>
    {% endfor %}
  </ul>
{% endblock %}
```
{% endraw %}

### Step 6: Update URLs

#### `restaurant_booking/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('restaurants/', include('restaurants.urls')),
    path('tables/', include('tables.urls')),
    path('reservations/', include('reservations.urls')),
]
```

#### `restaurants/urls.py`
```python
from django.urls import path
from .views import restaurant_list

urlpatterns = [
    path('', restaurant_list, name='restaurant_list'),
]
```

#### `tables/urls.py`
```python
from django.urls import path
from .views import table_list

urlpatterns = [
    path('<int:restaurant_id>/', table_list, name='table_list'),
]
```

#### `reservations/urls.py`
```python
from django.urls import path
from .views import reservation_list

urlpatterns = [
    path('<int:user_id>/', reservation_list, name='reservation_list'),
]
```

### Step 7: Run the Development Server

Run the development server to test your application:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/restaurants/` in your web browser to see the list of restaurants.


## Solution for 9th qustion

### Step 1: Create the Django Project and Apps

```bash
# Create Django project
django-admin startproject restaurant_booking

# Navigate to the project directory
cd restaurant_booking

# Create Django apps
python manage.py startapp restaurants
python manage.py startapp tables
python manage.py startapp reservations
```

### Step 2: Define Models

#### `restaurants/models.py`
```python
from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    cuisine = models.CharField(max_length=50)
    menu = models.TextField()

    def __str__(self):
        return self.name
```

#### `tables/models.py`
```python
from django.db import models
from restaurants.models import Restaurant

class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    number = models.IntegerField()
    capacity = models.IntegerField()

    def __str__(self):
        return f"Table {self.number} at {self.restaurant.name}"
```

#### `reservations/models.py`
```python
from django.db import models
from restaurants.models import Restaurant
from tables.models import Table
from django.contrib.auth.models import User

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"Reservation for {self.user.username} at {self.restaurant.name}, Table {self.table.number} on {self.date} at {self.time}"
```

### Step 3: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Implement Views and Templates

#### `restaurants/views.py`
```python
from django.shortcuts import render
from .models import Restaurant

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurants/restaurant_list.html', {'restaurants': restaurants})
```

#### `tables/views.py`
```python
from django.shortcuts import render
from .models import Table

def table_list(request, restaurant_id):
    tables = Table.objects.filter(restaurant_id=restaurant_id)
    return render(request, 'tables/table_list.html', {'tables': tables})
```

#### `reservations/views.py`
```python
from django.shortcuts import render
from .models import Reservation

def reservation_list(request, user_id):
    reservations = Reservation.objects.filter(user_id=user_id)
    return render(request, 'reservations/reservation_list.html', {'reservations': reservations})
```

### Step 5: Implement Templates

#### `templates/base.html`
{% raw %}
```html
<!-- templates/base.html -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Restaurant Booking{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'css/styles.css' %}">
    <!-- Add your additional CSS styles or link to external stylesheets here -->
</head>
<body>

<nav>
    <ul>
        <li><a href="{% url 'restaurant_list' %}">All Restaurants</a></li>
        <li><a href="{% url 'search_restaurants' %}">Search Restaurants</a></li>
        <li><a href="{% url 'reservation_list' user_id=request.user.id %}">My Reservations</a></li>
        <!-- Add more navigation links as needed -->
        {% if user.is_authenticated %}
            <li><a href="{% url 'logout' %}">Logout</a></li>
        {% else %}
            <li><a href="{% url 'login' %}">Login</a></li>
            <li><a href="{% url 'signup' %}">Sign Up</a></li>
        {% endif %}
    </ul>
</nav>

{% if messages %}
    <div>
        {% for message in messages %}
            <p>{{ message }}</p>
        {% endfor %}
    </div>
{% endif %}

{% block content %}
    <!-- The content of each page will go here -->
{% endblock %}

<script src="{% static 'js/scripts.js' %}"></script>
<!-- Add your additional JavaScript scripts or link to external scripts here -->
</body>
</html>
```

In this template:

- The `{% block title %}Restaurant Booking{% endblock %}` is a placeholder for the page title. Each template that extends this base template can provide its own title within the `{% block title %}{% endblock %}` tags.

- The navigation links are included within a `<nav>` element. You can customize these links based on your application's requirements.

- The `{% if messages %}` block is included to display any Django messages. This is useful for displaying success messages, error messages, etc. You'll need to use the `messages` framework in your views to add messages.

- The `{% block content %}{% endblock %}` is a placeholder for the specific content of each page. Templates that extend this base template will override this block to provide their unique content.

#### `restaurants/templates/restaurants/restaurant_list.html`
```html
<!-- restaurants/restaurant_list.html -->
{% extends 'base.html' %}

{% block title %}Restaurant List{% endblock %}

{% block content %}
  <h1>Restaurant List</h1>
  <ul>
    {% for restaurant in restaurants %}
      <li>
        <h2>{{ restaurant.name }}</h2>
        <p>Location: {{ restaurant.location }}</p>
        <p>Cuisine: {{ restaurant.cuisine }}</p>
        <p>Menu: {{ restaurant.menu }}</p>
        <a href="{% url 'table_list' restaurant.id %}">View Tables</a>
      </li>
    {% endfor %}
  </ul>
{% endblock %}
```

#### `tables/templates/tables/table_list.html`
```html
<!-- tables/table_list.html -->
{% extends 'base.html' %}

{% block title %}Table List{% endblock %}

{% block content %}
  <h1>Table List</h1>
  <ul>
    {% for table in tables %}
      <li>
        <h2>Table {{ table.number }}</h2>
        <p>Capacity: {{ table.capacity }}</p>
      </li>
    {% endfor %}
  </ul>
{% endblock %}
```

#### `reservations/templates/reservations/reservation_list.html`
```html
<!-- reservations/reservation_list.html -->
{% extends 'base.html' %}

{% block title %}Reservation List{% endblock %}

{% block content %}
  <h1>Reservation List</h1>
  <ul>
    {% for reservation in reservations %}
      <li>
        <h2>{{ reservation.restaurant.name }}</h2>
        <p>Table: {{ reservation.table.number }}</p>
        <p>Date: {{ reservation.date }}</p>
        <p>Time: {{ reservation.time }}</p>
      </li>
    {% endfor %}
  </ul>
{% endblock %}
```
{% endraw %}

### Step 6: Update URLs

#### `restaurant_booking/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('restaurants/', include('restaurants.urls')),
    path('tables/', include('tables.urls')),
    path('reservations/', include('reservations.urls')),
]
```

#### `restaurants/urls.py`
```python
from django.urls import path
from .views import restaurant_list

urlpatterns = [
    path('', restaurant_list, name='restaurant_list'),
]
```

#### `tables/urls.py`
```python
from django.urls import path
from .views import table_list

urlpatterns = [
    path('<int:restaurant_id>/', table_list, name='table_list'),
]
```

#### `reservations/urls.py`
```python
from django.urls import path
from .views import reservation_list

urlpatterns = [
    path('<int:user_id>/', reservation_list, name='reservation_list'),
]
```

### Step 7: Run the Development Server

Run the development server to test your application:

```bash
python manage.py runserver
```

### Step 8: Update Views and Templates for Search and Reservation

#### `restaurants/views.py`
```python
from django.shortcuts import render
from .models import Restaurant

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurants/restaurant_list.html', {'restaurants': restaurants})

def search_restaurants(request):
    if request.method == 'GET':
        location = request.GET.get('location', '')
        cuisine = request.GET.get('cuisine', '')
        date = request.GET.get('date', '')

        restaurants = Restaurant.objects.filter(
            location__icontains=location,
            cuisine__icontains=cuisine,
        )

        # Additional filtering based on availability using the 'date' parameter

        return render(request, 'restaurants/search_results.html', {'restaurants': restaurants})
```

#### `restaurants/templates/restaurants/search_results.html`
{% raw %}
```html
<!-- restaurants/search_results.html -->
{% extends 'base.html' %}

{% block title %}Search Results{% endblock %}

{% block content %}
  <h1>Search Results</h1>
  <ul>
    {% for restaurant in restaurants %}
      <li>
        <h2>{{ restaurant.name }}</h2>
        <p>Location: {{ restaurant.location }}</p>
        <p>Cuisine: {{ restaurant.cuisine }}</p>
        <p>Menu: {{ restaurant.menu }}</p>
        <a href="{% url 'table_list' restaurant.id %}">View Tables</a>
      </li>
    {% endfor %}
  </ul>
{% endblock %}
```
{% endraw %}

#### `reservations/views.py`
```python
from django.shortcuts import render, redirect
from .models import Reservation
from .forms import ReservationForm
from django.contrib.auth.decorators import login_required

@login_required
def make_reservation(request, restaurant_id, table_id):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.restaurant_id = restaurant_id
            reservation.table_id = table_id
            reservation.save()
            return redirect('reservation_list', user_id=request.user.id)
    else:
        form = ReservationForm()
    return render(request, 'reservations/make_reservation.html', {'form': form})
```

#### `reservations/forms.py`
```python
from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'time']
```

#### `reservations/templates/reservations/make_reservation.html`
{% raw %}
```html
<!-- reservations/make_reservation.html -->
{% extends 'base.html' %}

{% block title %}Make Reservation{% endblock %}

{% block content %}
  <h1>Make Reservation</h1>
  <form method="post" action="">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Make Reservation</button>
  </form>
  <a href="{% url 'reservation_list' user_id=request.user.id %}">Back to Reservation List</a>
{% endblock %}
```
{% endraw %}

### Step 9: Update URLs

#### `restaurants/urls.py`
```python
from django.urls import path
from .views import restaurant_list, search_restaurants

urlpatterns = [
    path('', restaurant_list, name='restaurant_list'),
    path('search/', search_restaurants, name='search_restaurants'),
]
```

#### `reservations/urls.py`
```python
from django.urls import path
from .views import reservation_list, make_reservation

urlpatterns = [
    path('<int:user_id>/', reservation_list, name='reservation_list'),
    path('make/<int:restaurant_id>/<int:table_id>/', make_reservation, name='make_reservation'),
]
```

### Step 10: Update `base.html` for Navigation

#### `templates/base.html`
Add a link to the search page and the reservation list.
{% raw %}
```html
<!-- templates/base.html -->
<!-- ... (previous content) -->

<nav>
    <ul>
        <li><a href="{% url 'restaurant_list' %}">All Restaurants</a></li>
        <li><a href="{% url 'search_restaurants' %}">Search Restaurants</a></li>
        <li><a href="{% url 'reservation_list' user_id=request.user.id %}">My Reservations</a></li>
        <!-- ... (previous content) -->
    </ul>
</nav>

<!-- ... (remaining content) -->
```
{% endraw %}


### Step 11: Run the Development Server

Run the development server to test your application:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/restaurants/` in your web browser to see the list of restaurants. You can also try searching for restaurants and making reservations.

## Solution for 10th qustion

### Step 1: Create the Django Project and Apps

```bash
# Create Django project
django-admin startproject news_portal

# Navigate to the project directory
cd news_portal

# Create Django apps
python manage.py startapp articles
python manage.py startapp categories
python manage.py startapp authors
```

### Step 2: Define Models

#### `articles/models.py`
```python
from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
```

#### `categories/models.py`
```python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
```

#### `authors/models.py`
```python
from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self):
        return self.user.username
```

### Step 3: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Implement Views and Templates

#### `articles/views.py`
```python
from django.shortcuts import render, get_object_or_404
from .models import Article

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'articles/article_list.html', {'articles': articles})

def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'articles/article_detail.html', {'article': article})
```

#### `articles/templates/articles/article_list.html`
{% raw %}
```html
<!-- articles/article_list.html -->
{% extends 'base.html' %}

{% block title %}Latest News{% endblock %}

{% block content %}
  <h1>Latest News</h1>
  <ul>
    {% for article in articles %}
      <li>
        <h2><a href="{% url 'article_detail' article.id %}">{{ article.title }}</a></h2>
        <p>Category: {{ article.category.name }}</p>
        <p>Author: {{ article.author.username }}</p>
        <p>{{ article.content|truncatewords:50 }}</p>
      </li>
    {% endfor %}
  </ul>
{% endblock %}
```

#### `articles/templates/articles/article_detail.html`
```html
<!-- articles/article_detail.html -->
{% extends 'base.html' %}

{% block title %}{{ article.title }}{% endblock %}

{% block content %}
  <h1>{{ article.title }}</h1>
  <p>Category: {{ article.category.name }}</p>
  <p>Author: {{ article.author.username }}</p>
  <p>{{ article.content }}</p>
  <!-- Add comments section here -->
{% endblock %}
```
{% endraw %}

### Step 5: Update URLs

#### `news_portal/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
    # Add other app URLs here
]
```

#### `articles/urls.py`
```python
from django.urls import path
from .views import article_list, article_detail

urlpatterns = [
    path('', article_list, name='article_list'),
    path('<int:article_id>/', article_detail, name='article_detail'),
]
```

### Step 6: Create Templates for Registration and Login

Create the necessary templates for user registration and login.

#### `registration/templates/registration/signup.html`
{% raw %}
```html
<!-- registration/signup.html -->
{% extends 'base.html' %}

{% block title %}Sign Up{% endblock %}

{% block content %}
  <h1>Sign Up</h1>
  <form method="post" action="{% url 'signup' %}">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Sign Up</button>
  </form>
  <p>Already have an account? <a href="{% url 'login' %}">Log In</a></p>
{% endblock %}
```

#### `registration/templates/registration/login.html`
```html
<!-- registration/login.html -->
{% extends 'base.html' %}

{% block title %}Log In{% endblock %}

{% block content %}
  <h1>Log In</h1>
  <form method="post" action="{% url 'login' %}">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Log In</button>
  </form>
  <p>Don't have an account? <a href="{% url 'signup' %}">Sign Up</a></p>
{% endblock %}
```

### Step 7: Update `base.html` for Navigation and User Authentication

#### `templates/base.html`
Add links for user authentication.

```html
<!-- templates/base.html -->
<!-- ... (previous content) -->

<nav>
    <ul>
        <li><a href="{% url 'article_list' %}">Latest News</a></li>
        <!-- Add other navigation links as needed -->
        {% if user.is_authenticated %}


            <li><a href="{% url 'logout' %}">Logout</a></li>
            <li><a href="{% url 'profile' %}">My Profile</a></li>
        {% else %}
            <li><a href="{% url 'login' %}">Login</a></li>
            <li><a href="{% url 'signup' %}">Sign Up</a></li>
        {% endif %}
    </ul>
</nav>

<!-- ... (remaining content) -->
```
{% endraw %}

### Step 8: Update `settings.py` for User Authentication

In your `settings.py`, make sure you have the following configurations for user authentication:

```python
# settings.py

INSTALLED_APPS = [
    # ...
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # ...
]

# ...

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
```

### Step 9: Run the Development Server

Run the development server to test your application:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/articles/` in your web browser to see the list of latest news articles.

### Step 10: Implement Comments

#### `comments/models.py`
```python
from django.db import models
from django.contrib.auth.models import User
from articles.models import Article

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.article.title}"
```

#### `comments/views.py`
```python
from django.shortcuts import render, redirect
from .models import Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required

@login_required
def add_comment(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.article = article
            comment.save()
            return redirect('article_detail', article_id=article.id)
    else:
        form = CommentForm()

    return render(request, 'comments/add_comment.html', {'form': form})
```

#### `comments/forms.py`
```python
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
```

#### `comments/templates/comments/add_comment.html`
{% raw %}
```html
<!-- comments/add_comment.html -->
{% extends 'base.html' %}

{% block title %}Add Comment{% endblock %}

{% block content %}
  <h1>Add Comment</h1>
  <form method="post" action="{% url 'add_comment' article.id %}">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Add Comment</button>
  </form>
  <a href="{% url 'article_detail' article.id %}">Back to Article</a>
{% endblock %}
```
{% endraw %}

### Step 11: Update URLs

#### `comments/urls.py`
```python
from django.urls import path
from .views import add_comment

urlpatterns = [
    path('add/<int:article_id>/', add_comment, name='add_comment'),
]
```

#### `articles/urls.py`
```python
from django.urls import path
from .views import article_list, article_detail
from comments.views import add_comment

urlpatterns = [
    path('', article_list, name='article_list'),
    path('<int:article_id>/', article_detail, name='article_detail'),
    path('comments/', include('comments.urls')),
]
```

### Step 12: Create Templates for User Profile

#### `authors/views.py`
```python
from django.shortcuts import render
from .models import Author

def profile(request):
    author = Author.objects.get(user=request.user)
    return render(request, 'authors/profile.html', {'author': author})
```

#### `authors/templates/authors/profile.html`
{% raw %}
```html
<!-- authors/profile.html -->
{% extends 'base.html' %}

{% block title %}My Profile{% endblock %}

{% block content %}
  <h1>My Profile</h1>
  <p>Username: {{ user.username }}</p>
  <p>Bio: {{ author.bio }}</p>
{% endblock %}
```
{% endraw %}

### Step 13: Update URLs

#### `authors/urls.py`
```python
from django.urls import path
from .views import profile

urlpatterns = [
    path('profile/', profile, name='profile'),
]
```

#### `news_portal/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
    path('authors/', include('authors.urls')),
    path('comments/', include('comments.urls')),
    # Add other app URLs here
]
```

### Step 14: Run the Development Server

Run the development server to test your application:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/articles/` in your web browser to see the list of latest news articles. Log in or sign up to leave comments and view your profile.

### Step 15: Implement User Registration and Login

#### `registration/views.py`
```python
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('article_list')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('article_list')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('article_list')
```

#### `registration/urls.py`
```python
from django.urls import path
from .views import signup, user_login, user_logout

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
```

#### `templates/base.html`
Add links for user authentication.
{% raw %}
```html
<!-- templates/base.html -->
<!-- ... (previous content) -->

<nav>
    <ul>
        <li><a href="{% url 'article_list' %}">Latest News</a></li>
        <!-- Add other navigation links as needed -->
        {% if user.is_authenticated %}
            <li><a href="{% url 'logout' %}">Logout</a></li>
            <li><a href="{% url 'profile' %}">My Profile</a></li>
        {% else %}
            <li><a href="{% url 'login' %}">Login</a></li>
            <li><a href="{% url 'signup' %}">Sign Up</a></li>
        {% endif %}
    </ul>
</nav>

<!-- ... (remaining content) -->
```
{% endraw %}

### Step 16: Update URLs

#### `news_portal/urls.py`
Include the registration URLs.

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
    path('authors/', include('authors.urls')),
    path('comments/', include('comments.urls')),
    path('registration/', include('registration.urls')),
    # Add other app URLs here
]
```

### Step 17: Update `settings.py` for User Authentication

Ensure that the `AUTHENTICATION_BACKENDS` setting includes `'django.contrib.auth.backends.ModelBackend'`.

```python
# settings.py

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
```

### Step 18: Run the Development Server

Run the development server to test your application:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/articles/` in your web browser to see the list of latest news articles. You can now sign up, log in, and log out using the provided links in the navigation bar.


### Step 19: Display User-Specific Content

#### `articles/views.py`
Update the `article_list` view to show articles authored by the logged-in user.

```python
from django.shortcuts import render
from .models import Article
from django.contrib.auth.decorators import login_required

@login_required
def article_list(request):
    articles = Article.objects.filter(author=request.user)
    return render(request, 'articles/article_list.html', {'articles': articles})
```

### Step 20: Allow Users to Manage Their Articles

#### `articles/views.py`
Add views to create, update, and delete articles.

```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Article
from .forms import ArticleForm
from django.contrib.auth.decorators import login_required

@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_list')
    else:
        form = ArticleForm()

    return render(request, 'articles/create_article.html', {'form': form})

@login_required
def update_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id, author=request.user)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_list')
    else:
        form = ArticleForm(instance=article)

    return render(request, 'articles/update_article.html', {'form': form, 'article': article})

@login_required
def delete_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id, author=request.user)
    article.delete()
    return redirect('article_list')
```

#### `articles/urls.py`
Update the article URLs to include the new views.

```python
from django.urls import path
from .views import article_list, article_detail, create_article, update_article, delete_article

urlpatterns = [
    path('', article_list, name='article_list'),
    path('<int:article_id>/', article_detail, name='article_detail'),
    path('create/', create_article, name='create_article'),
    path('update/<int:article_id>/', update_article, name='update_article'),
    path('delete/<int:article_id>/', delete_article, name='delete_article'),
]
```

#### `articles/templates/articles/article_list.html`
Include links to create, update, and delete articles.
{% raw %}
```html
<!-- articles/article_list.html -->
{% extends 'base.html' %}

{% block title %}My Articles{% endblock %}

{% block content %}
  <h1>My Articles</h1>
  <ul>
    {% for article in articles %}
      <li>
        <h2><a href="{% url 'article_detail' article.id %}">{{ article.title }}</a></h2>
        <p>Category: {{ article.category.name }}</p>
        <p>{{ article.content|truncatewords:50 }}</p>
        <p>Published on: {{ article.pub_date }}</p>
        <a href="{% url 'update_article' article.id %}">Update</a>
        <a href="{% url 'delete_article' article.id %}">Delete</a>
      </li>
    {% endfor %}
  </ul>
  <a href="{% url 'create_article' %}">Create New Article</a>
{% endblock %}
```
{% endraw %}

### Step 21: Update `urls.py` for Articles

#### `news_portal/urls.py`
Update the URLs to include the article app URLs.

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
    path('authors/', include('authors.urls')),
    path('comments/', include('comments.urls')),
    path('registration/', include('registration.urls')),
    # Add other app URLs here
]
```

### Step 22: Run the Development Server

Run the development server to test your application:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/articles/` in your web browser to see the list of your articles. You can create, update, and delete articles if you are logged in.