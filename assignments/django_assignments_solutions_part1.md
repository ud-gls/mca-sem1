# Django Assignment Solutions: Part 1

## Solution for 1st qustion

### Step 1: Create the Django Project and Apps

Open your terminal and run the following commands:

```bash
# Create Django project
django-admin startproject ecommerce

# Navigate to the project directory
cd ecommerce

# Create Django apps
python manage.py startapp products
python manage.py startapp cart
python manage.py startapp orders
```

### Step 2: Define Models

#### `products/models.py`
```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
```

#### `cart/models.py`
```python
from django.db import models
from products.models import Product

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
```

#### `orders/models.py`
```python
from django.db import models
from products.models import Product

class Order(models.Model):
    items = models.ManyToManyField(Product, through='OrderItem')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id}"
```

#### `orders/models.py`
```python
from django.db import models
from products.models import Product
from orders.models import Order

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
```

### Step 3: Implement Views and Templates

#### `products/views.py`
```python
from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})
```

#### `cart/views.py`
```python
from django.shortcuts import render, redirect
from .models import CartItem
from products.models import Product

def view_cart(request):
    cart_items = CartItem.objects.all()
    return render(request, 'cart/view_cart.html', {'cart_items': cart_items})

def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)

    # Check if item is already in the cart
    existing_item = CartItem.objects.filter(product=product).first()

    if existing_item:
        existing_item.quantity += 1
        existing_item.save()
    else:
        new_item = CartItem(product=product, quantity=1)
        new_item.save()

    return redirect('view_cart')
```

#### `orders/views.py`
```python
from django.shortcuts import render, redirect
from .models import Order, OrderItem
from cart.models import CartItem
from products.models import Product

def create_order(request):
    if request.method == 'POST':
        # Capture user information
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')

        # Create a new order
        order = Order(name=name, email=email, address=address, total_price=0)
        order.save()

        # Retrieve items from the cart and create order items
        cart_items = CartItem.objects.all()

        for item in cart_items:
            order_item = OrderItem(order=order, product=item.product, quantity=item.quantity)
            order_item.save()

            # Update total price of the order
            order.total_price += item.product.price * item.quantity
            order.save()

        # Clear the cart
        CartItem.objects.all().delete()

        return render(request, 'orders/order_confirmation.html', {'order': order})

    return render(request, 'orders/create_order.html')
```

### Step 4: Create Templates

#### `products/templates/products/product_list.html`
{% raw %}
```html
<!-- products/product_list.html -->
{% extends 'base.html' %}

{% block title %}Product List{% endblock %}

{% block content %}
  <h1>Product List</h1>
  <ul>
    {% for product in products %}
      <li>
        <strong>{{ product.name }}</strong><br>
        Description: {{ product.description }}<br>
        Price: ${{ product.price }}<br>
        <a href="{% url 'add_to_cart' product.id %}">Add to Cart</a>
      </li>
    {% endfor %}
  </ul>
{% endblock %}
```
#### `cart/templates/cart/view_cart.html`
```html
<!-- cart/view_cart.html -->
{% extends 'base.html' %}

{% block title %}View Cart{% endblock %}

{% block content %}
  <h1>Your Cart</h1>
  <ul>
    {% for item in cart_items %}
      <li>
        <strong>{{ item.product.name }}</strong><br>
        Quantity: {{ item.quantity }}<br>
        <!-- Add quantity adjustment form here -->
      </li>
    {% endfor %}
  </ul>
  <a href="{% url 'product_list' %}">Continue Shopping</a>
{% endblock %}
```

#### `orders/templates/orders/create_order.html`
```html
<!-- orders/create_order.html -->
{% extends 'base.html' %}

{% block title %}Create Order{% endblock %}

{% block content %}
  <h1>Create Your Order</h1>
  <form method="post" action="{% url 'create_order' %}">
    {% csrf_token %}
    <label for="name">Name:</label>
    <input type="text" id="name" name="name" required><br>
    <label for="email">Email:</label>
    <input type="email" id="email" name="email" required><br>
    <label for="address">Address:</label>
    <textarea id="address" name="address" required></textarea><br>
    <input type="submit" value="Place Order">
  </form>
  <a href="{% url 'view_cart' %}">View Cart</a>
{% endblock %}
```

#### `orders/templates/orders/order_confirmation.html`
```html
<!-- orders/order_confirmation.html -->
{% extends 'base.html' %}

{% block title %}Order Confirmation{% endblock %}

{% block content %}
  <h1>Order Confirmation</h1>
  <p>Your order ({{ order }}) has been placed successfully!</p>
  <p>Total Price: ${{ order.total_price }}</p>
  <a href="{% url 'product_list' %}">Continue Shopping</a>
{% endblock %}
```
{% endraw %}

### Step 5: URL Routing

Configure the URLs in `urls.py` files of each app and the main project.

#### `ecommerce/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
]
```

#### `products/urls.py`
```python
from django.urls import path
from .views import product_list

urlpatterns = [
    path('', product_list, name='product_list'),
]
```

#### `cart/urls.py`
```python
from django.urls import path
from .views import view_cart, add_to_cart

urlpatterns = [
    path('', view_cart, name='view_cart'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
]
```

#### `orders/urls.py`
```python
from django.urls import path
from .views import create_order

urlpatterns = [
    path('create/', create_order, name='create_order'),
]
```

### Step 6: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Run the Development Server

```bash
python manage.py runserver
```



Visit `http://127.0.0.1:8000/products/` to see the list of products, `http://127.0.0.1:8000/cart/` to view the cart, and `http://127.0.0.1:8000/orders/create/` to create an order.


## Solution for 2nd qustion

### Step 1: Create the Django Project and App

Open your terminal and run the following commands:

```bash
# Create Django project
django-admin startproject blog

# Navigate to the project directory
cd blog

# Create Django app
python manage.py startapp posts
```

### Step 2: Define Model and Run Migrations

#### `posts/models.py`
```python
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

#### Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Implement CRUD Operations in the Admin Interface

#### `posts/admin.py`
```python
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date')
    search_fields = ('title', 'content')
    list_filter = ('author', 'pub_date')
```

### Step 3: Create Forms for Post Creation and Editing

#### `posts/forms.py`
```python
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
```

### Step 5: Create Views and Templates

#### `posts/views.py`
```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def post_list(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 5)  # Show 5 posts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'posts/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})

def post_create(request):
    form_title = 'Create Post'
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form, 'form_title': form_title})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form_title = 'Edit Post'
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_form.html', {'form': form, 'form_title': form_title})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
```

#### `posts/urls.py`
```python
from django.urls import path
from .views import post_list, post_detail, post_create, post_edit, post_delete

urlpatterns = [
    path('', post_list, name='post_list'),
    path('<int:pk>/', post_detail, name='post_detail'),
    path('create/', post_create, name='post_create'),
    path('<int:pk>/edit/', post_edit, name='post_edit'),
    path('<int:pk>/delete/', post_delete, name='post_delete'),
]
```

#### `templates/base.html`
{% raw %}
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Default Title{% endblock %}</title>
</head>
<body>
    <nav>
        <ul>
            <li><a href="{% url 'post_list' %}">Home</a></li>
            <li><a href="{% url 'post_create' %}">Create Post</a></li>
        </ul>
    </nav>
    {% block content %}
    {% endblock %}
</body>
</html>
```

#### `posts/templates/posts/post_list.html`
```html
<!-- posts/post_list.html -->
{% extends 'base.html' %}

{% block title %}Post List{% endblock %}

{% block content %}
  <h1>Blog Posts</h1>
  {% for post in posts %}
    <div>
      <h2><a href="{% url 'post_detail' pk=post.pk %}">{{ post.title }}</a></h2>
      <p>{{ post.author }} | {{ post.pub_date }}</p>
      <p>{{ post.content }}</p>
      {% if request.user == post.author %}
        <a href="{% url 'post_edit' pk=post.pk %}">Edit</a>
        <a href="{% url 'post_delete' pk=post.pk %}">Delete</a>
      {% endif %}
    </div>
  {% endfor %}

  <div class="pagination">
    <!-- Pagination links as before -->
  </div>
{% endblock %}
```

#### `posts/templates/posts/post_detail.html`
```html
<!-- posts/post_detail.html -->
{% extends 'base.html' %}

{% block title %}{{ post.title }}{% endblock %}

{% block content %}
  <h1>{{ post.title }}</h1>
  <p>{{ post.author }} | {{ post.pub_date }}</p>
  <p>{{ post.content }}</p>
  {% if request.user == post.author %}
    <a href="{% url 'post_edit' pk=post.pk %}">Edit</a>
    <a href="{% url 'post_delete' pk=post.pk %}">Delete</a>
  {% endif %}
  <a href="{% url 'post_list' %}">Back to Post List</a>
{% endblock %}
```

#### `posts/templates/posts/post_form.html`
```html
<!-- posts/post_form.html -->
{% extends 'base.html' %}

{% block title %}{{ form_title }}{% endblock %}

{% block content %}
  <h1>{{ form_title }}</h1>
  <form method="post" action="{% url 'post_create' %}">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Save">
  </form>
  <a href="{% url 'post_list' %}">Cancel</a>
{% endblock %}
```
{% endraw %}

### Step 6: URL Routing (Continued)

Configure the URLs in the `urls.py` file of the `posts` app.

#### `blog/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
]
```

### Step 7: Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/posts/` to see the list of blog posts, `http://127.0.0.1:8000/posts/create/` to create a new post, and explore other views based on the URLs defined in the `urls.py` file.


## Solution for 3rd qustion


### Step 1: Create the Django Project and Apps

Open your terminal and run the following commands:

```bash
# Create Django project
django-admin startproject movie_recommender

# Navigate to the project directory
cd movie_recommender

# Create Django apps
python manage.py startapp movies
python manage.py startapp ratings
python manage.py startapp recommendations
```

### Step 2: Define Models and Run Migrations

#### `movies/models.py`
```python
from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
```

#### `ratings/models.py`
```python
from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    def __str__(self):
        return f"{self.user.username} rated {self.movie.title} with {self.rating}"
```

#### `recommendations/models.py`
```python
from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    predicted_rating = models.FloatField()

    def __str__(self):
        return f"{self.user.username} recommends {self.movie.title} with predicted rating {self.predicted_rating}"
```

#### Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Implement Views and Templates

#### `movies/views.py`
```python
from django.shortcuts import render
from .models import Movie

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})
```

#### `ratings/views.py`
```python
from django.shortcuts import render, redirect
from .models import Rating
from movies.models import Movie
from django.contrib.auth.decorators import login_required

@login_required
def rate_movie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)

    if request.method == 'POST':
        rating_value = int(request.POST.get('rating'))
        Rating.objects.create(user=request.user, movie=movie, rating=rating_value)

    return redirect('movie_list')
```

#### `recommendations/views.py`
```python
from django.shortcuts import render
from .models import Recommendation

def recommended_movies(request):
    user_recommendations = Recommendation.objects.filter(user=request.user)
    return render(request, 'recommendations/recommended_movies.html', {'recommendations': user_recommendations})
```

### Step 4: Create Templates

#### `movies/templates/movies/movie_list.html`
{% raw %}
```html
<!-- movies/movie_list.html -->
{% extends 'base.html' %}

{% block title %}Movie List{% endblock %}

{% block content %}
  <h1>Movie List</h1>
  <ul>
    {% for movie in movies %}
      <li>{{ movie.title }} - <a href="{% url 'rate_movie' movie.id %}">Rate</a></li>
    {% endfor %}
  </ul>
{% endblock %}
```

#### `recommendations/templates/recommendations/recommended_movies.html`
```html
<!-- recommendations/recommended_movies.html -->
{% extends 'base.html' %}

{% block title %}Recommended Movies{% endblock %}

{% block content %}
  <h1>Recommended Movies</h1>
  <ul>
    {% for recommendation in recommendations %}
      <li>{{ recommendation.movie.title }} - Predicted Rating: {{ recommendation.predicted_rating }}</li>
    {% endfor %}
  </ul>
{% endblock %}
```
{% endraw %}

### Step 5: URL Routing

Configure the URLs in `urls.py` files of each app and the main project.

#### `movie_recommender/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', include('movies.urls')),
    path('ratings/', include('ratings.urls')),
    path('recommendations/', include('recommendations.urls')),
]
```

#### `movies/urls.py`
```python
from django.urls import path
from .views import movie_list

urlpatterns = [
    path('', movie_list, name='movie_list'),
]
```

#### `ratings/urls.py`
```python
from django.urls import path
from .views import rate_movie

urlpatterns = [
    path('<int:movie_id>/', rate_movie, name='rate_movie'),
]
```

#### `recommendations/urls.py`
```python
from django.urls import path
from .views import recommended_movies

urlpatterns = [
    path('', recommended_movies, name='recommended_movies'),
]
```

### Step 6: Update `settings.py`

#### `movie_recommender/settings.py`
```python
# ...
LOGIN_REDIRECT_URL = '/movies/'  # Redirect to movie list after login
# ...
```

### Step 7: Update `base.html` Template for Login/Logout Links

#### `templates/base.html`
{% raw %}
```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <

meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Default Title{% endblock %}</title>
</head>
<body>
    <nav>
        <ul>
            <li><a href="{% url 'movie_list' %}">Movies</a></li>
            <li><a href="{% url 'recommended_movies' %}">Recommended Movies</a></li>
            {% if user.is_authenticated %}
              <li><a href="{% url 'logout' %}">Logout</a></li>
            {% else %}
              <li><a href="{% url 'login' %}">Login</a></li>
            {% endif %}
        </ul>
    </nav>
    {% block content %}
    {% endblock %}
</body>
</html>
```
{% endraw %}

### Step 8: Update `settings.py` for Authentication

In your `settings.py` file, make sure you have the authentication-related configurations set up correctly. Add the following to enable authentication and redirect users to the login page:

#### `movie_recommender/settings.py`
```python
# ...

# Authentication settings
LOGIN_URL = '/login/'

# ...
```

### Step 9: Create Authentication Views and Templates

You can use Django's built-in authentication views and templates to handle user authentication. Update the `urls.py` in the main project and create a `templates/registration` directory for authentication templates.

#### `movie_recommender/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', include('movies.urls')),
    path('ratings/', include('ratings.urls')),
    path('recommendations/', include('recommendations.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Add authentication URLs
]
```

### Step 10: Update `base.html` for Authentication Links

#### `templates/base.html`
{% raw %}
```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Default Title{% endblock %}</title>
</head>
<body>
    <nav>
        <ul>
            <li><a href="{% url 'movie_list' %}">Movies</a></li>
            <li><a href="{% url 'recommended_movies' %}">Recommended Movies</a></li>
            {% if user.is_authenticated %}
              <li><a href="{% url 'logout' %}">Logout</a></li>
            {% else %}
              <li><a href="{% url 'login' %}">Login</a></li>
              <li><a href="{% url 'register' %}">Register</a></li>
            {% endif %}
        </ul>
    </nav>
    {% block content %}
    {% endblock %}
</body>
</html>
```
{% endraw %}

### Step 11: Create Registration View and Template

Create a `registration` app to handle user registration. Run the following commands:

```bash
python manage.py startapp registration
```

#### `registration/views.py`
```python
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movie_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
```

#### `registration/urls.py`
```python
from django.urls import path
from .views import register

urlpatterns = [
    path('register/', register, name='register'),
]
```

#### `registration/templates/registration/register.html`
{% raw %}
```html
<!-- registration/register.html -->
{% extends 'base.html' %}

{% block title %}Register{% endblock %}

{% block content %}
  <h1>Register</h1>
  <form method="post" action="{% url 'register' %}">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Register">
  </form>
  <a href="{% url 'login' %}">Already have an account? Login here.</a>
{% endblock %}
```
{% endraw %}

#### Update `urls.py` in the main project to include registration URLs:

#### `movie_recommender/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', include('movies.urls')),
    path('ratings/', include('ratings.urls')),
    path('recommendations/', include('recommendations.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('registration.urls')),  # Include registration URLs
]
```

### Step 12: Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/movies/` to see the list of movies, `http://127.0.0.1:8000/ratings/1/` to rate a movie, and `http://127.0.0.1:8000/recommendations/` to see recommended movies. You can also visit `http://127.0.0.1:8000/accounts/register/` to register a new user.


## Solution for 4th qustion

### Step 1: Create the Django Project and Apps

Open your terminal and run the following commands:

```bash
# Create Django project
django-admin startproject social_network

# Navigate to the project directory
cd social_network

# Create Django apps
python manage.py startapp users
python manage.py startapp posts
python manage.py startapp profiles
```

### Step 2: Define Models and Run Migrations

#### `users/models.py`
```python
from django.db import models
from django.contrib.auth.models import User as DjangoUser

class Profile(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True)
    interests = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username
```

#### `posts/models.py`
```python
from django.db import models
from users.models import Profile

class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.user.username} - {self.created_at}"
```

#### Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Implement CRUD Operations in the Admin Interface

#### `users/admin.py`
```python
from django.contrib import admin
from .models import Profile

admin.site.register(Profile)
```

#### `posts/admin.py`
```python
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

### Step 4: Create Views and Templates

#### `users/views.py`
```python
from django.shortcuts import render, get_object_or_404
from .models import Profile

def user_profile(request, username):
    user_profile = get_object_or_404(Profile, user__username=username)
    return render(request, 'users/user_profile.html', {'user_profile': user_profile})
```

#### `posts/views.py`
```python
from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from users.models import Profile
from django.contrib.auth.decorators import login_required

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.profile
            post.save()
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})
```

#### `profiles/views.py`
```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Relationship
from users.models import Profile

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username).profile
    Relationship.objects.create(from_user=request.user.profile, to_user=user_to_follow)
    return redirect('user_profile', username=username)
```

### Step 5: Create Templates

#### `users/templates/users/user_profile.html`
{% raw %}
```html
<!-- users/user_profile.html -->
{% extends 'base.html' %}

{% block title %}{{ user_profile.user.username }}{% endblock %}

{% block content %}
  <h1>{{ user_profile.user.username }}</h1>
  {% if user_profile.profile_picture %}
    <img src="{{ user_profile.profile_picture.url }}" alt="Profile Picture">
  {% endif %}
  <p>Bio: {{ user_profile.bio }}</p>
  <p>Interests: {{ user_profile.interests }}</p>

  {% if user != user_profile.user %}
    {% if not user_profile.user in user.profile.following.all %}
      <a href="{% url 'follow_user' username=user_profile.user.username %}">Follow</a>
    {% endif %}
  {% endif %}

  <h2>Posts</h2>
  {% for post in user_profile.user.post_set.all %}
    <div>
      <p>{{ post.text }}</p>
      {% if post.image %}
        <img src="{{ post.image.url }}" alt="Post Image">
      {% endif %}
      {% if post.link %}
        <a href="{{ post.link }}" target="_blank">{{ post.link }}</a>
      {% endif %}
    </div>
  {% endfor %}
{% endblock %}
```

#### `posts/templates/posts/create_post.html`
```html
<!-- posts/create_post.html -->
{% extends 'base.html' %}

{% block title %}Create Post{% endblock %}

{% block content %}
  <h1>Create Post</h1>
  <form method="post" action="{% url 'create_post' %}" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Post">
  </form>
  <a href="{% url 'feed' %}">Back to Feed</a>
{% endblock %}
```
{% endraw %}

### Step 6: URL Routing

Configure the URLs in `urls.py` files of each app and the main project.

#### `social_network/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('posts/', include('posts.urls')),
    path('profiles/', include('profiles.urls')),
]
```

#### `users/urls.py`
```python
from django.urls import path
from .views import user_profile

urlpatterns = [
    path('<str:username>/', user_profile, name='user_profile'),
]
```

#### `posts/urls.py`
```python
from django.urls import path
from .views import create_post

urlpatterns = [
    path('create/', create_post, name='create_post'),
]
```

#### `profiles/urls.py`
```python
from django.urls import path
from .views import follow_user

urlpatterns = [
    path('follow/<str:username>/', follow_user, name='follow_user'),
]
```

### Step 7: Update `base.html` for Navigation

#### `templates/base.html`
{% raw %}
```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Default Title{% endblock %}</title>
</head>
<body>
    <nav>
        <ul>
            <li><a href="{% url 'feed' %}">Feed</a></li>
            <li><a href="{% url '

create_post' %}">Create Post</a></li>
            {% if user.is_authenticated %}
              <li><a href="{% url 'user_profile' username=user.username %}">Profile</a></li>
              <li><a href="{% url 'logout' %}">Logout</a></li>
            {% else %}
              <li><a href="{% url 'login' %}">Login</a></li>
              <li><a href="{% url 'register' %}">Register</a></li>
            {% endif %}
        </ul>
    </nav>
    {% block content %}
    {% endblock %}
</body>
</html>
```
{% endraw %}

### Step 8: Implement a Feed and Search Feature

#### `posts/views.py`
```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Post
from users.models import Profile, Relationship

@login_required
def feed(request):
    user = request.user.profile
    following = user.following.all()
    posts = Post.objects.filter(author__in=following).order_by('-created_at')
    return render(request, 'posts/feed.html', {'posts': posts})
```

#### `posts/templates/posts/feed.html`
{% raw %}
```html
<!-- posts/feed.html -->
{% extends 'base.html' %}

{% block title %}Feed{% endblock %}

{% block content %}
  <h1>Feed</h1>
  {% for post in posts %}
    <div>
      <p>{{ post.text }}</p>
      {% if post.image %}
        <img src="{{ post.image.url }}" alt="Post Image">
      {% endif %}
      {% if post.link %}
        <a href="{{ post.link }}" target="_blank">{{ post.link }}</a>
      {% endif %}
      <p>Posted by: <a href="{% url 'user_profile' username=post.author.user.username %}">{{ post.author.user.username }}</a></p>
      <p>Created at: {{ post.created_at }}</p>
    </div>
  {% endfor %}
{% endblock %}
```
{% endraw %}

#### `profiles/views.py`
```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Relationship
from users.models import Profile

@login_required
def search(request):
    query = request.GET.get('q')
    users = Profile.objects.filter(user__username__icontains=query)
    posts = Post.objects.filter(text__icontains=query)
    return render(request, 'profiles/search_results.html', {'users': users, 'posts': posts, 'query': query})
```

#### `profiles/templates/profiles/search_results.html`
{% raw %}
```html
<!-- profiles/search_results.html -->
{% extends 'base.html' %}

{% block title %}Search Results{% endblock %}

{% block content %}
  <h1>Search Results for "{{ query }}"</h1>

  <h2>Users</h2>
  {% for user in users %}
    <p><a href="{% url 'user_profile' username=user.user.username %}">{{ user.user.username }}</a></p>
  {% endfor %}

  <h2>Posts</h2>
  {% for post in posts %}
    <div>
      <p>{{ post.text }}</p>
      {% if post.image %}
        <img src="{{ post.image.url }}" alt="Post Image">
      {% endif %}
      {% if post.link %}
        <a href="{{ post.link }}" target="_blank">{{ post.link }}</a>
      {% endif %}
      <p>Posted by: <a href="{% url 'user_profile' username=post.author.user.username %}">{{ post.author.user.username }}</a></p>
      <p>Created at: {{ post.created_at }}</p>
    </div>
  {% endfor %}
{% endblock %}
```
{% endraw %}

#### `profiles/urls.py`
```python
from django.urls import path
from .views import search

urlpatterns = [
    path('search/', search, name='search_results'),
]
```

#### Update `urls.py` in the main project to include search URLs:

#### `social_network/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('posts/', include('posts.urls')),
    path('profiles/', include('profiles.urls')),
]
```

### Step 9: Update the Navigation Bar in `base.html`

#### `templates/base.html`
{% raw %}
```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Default Title{% endblock %}</title>
</head>
<body>
    <nav>
        <ul>
            <li><a href="{% url 'feed' %}">Feed</a></li>
            <li><a href="{% url 'create_post' %}">Create Post</a></li>
            <li><a href="{% url 'search_results' %}">Search</a></li>
            {% if user.is_authenticated %}
              <li><a href="{% url 'user_profile' username=user.username %}">Profile</a></li>
              <li><a href="{% url 'logout' %}">Logout</a></li>
            {% else %}
              <li><a href="{% url 'login' %}">Login</a></li>
              <li><a href="{% url 'register' %}">Register</a></li>
            {% endif %}
        </ul>
    </nav>
    {% block content %}
    {% endblock %}
</body>
</html>
```
{% endraw %}

### Step 10: Update `posts/urls.py` for Feed URL

#### `posts/urls.py`
```python
from django.urls import path
from .views import create_post, feed

urlpatterns = [
    path('create/', create_post, name='create_post'),
    path('feed/', feed, name='feed'),
]
```

### Step 11: Update `profiles/urls.py` for Search URL

#### `profiles/urls.py`
```python
from django.urls import path
from .views import follow_user, search

urlpatterns = [
    path('follow/<str:username>/', follow_user, name='follow_user'),
    path('search/', search, name='search_results'),
]
```

### Step 12: Update `users/urls.py` for User Profile URL

#### `users/urls.py`
```python
from django.urls import path
from .views import user_profile

urlpatterns = [
    path('<str:username>/', user_profile, name='user_profile'),
]
```

### Step 13: Implement the Follow and Unfollow Features

#### `profiles/views.py`
```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Relationship
from users.models import Profile

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(Profile, user__username=username)

    # Check if the relationship already exists
    relationship, created = Relationship.objects.get_or_create(from_user=request.user.profile, to_user=user_to_follow)

    if not created:
        # If the relationship already exists, delete it (unfollow)
        relationship.delete()

    return redirect('user_profile', username=username)
```

### Step 14: Update `profiles/urls.py` for Follow and Unfollow URLs

#### `profiles/urls.py`
```python
from django.urls import path
from .views import follow_user

urlpatterns = [
    path('follow/<str:username>/', follow_user, name='follow_user'),
]
```

### Step 15: Update the User Profile Template

#### `users/templates/users/user_profile.html`
{% raw %}
```html
<!-- users/user_profile.html -->
{% extends 'base.html' %}

{% block title %}{{ user_profile.user.username }}{% endblock %}

{% block content %}
  <h1>{{ user_profile.user.username }}</h1>
  {% if user_profile.profile_picture %}
    <img src="{{ user_profile.profile_picture.url }}" alt="Profile Picture">
  {% endif %}
  <p>Bio: {{ user_profile.bio }}</p>
  <p>Interests: {{ user_profile.interests }}</p>

  {% if user != user_profile.user %}
    {% if not user_profile.user in user.profile.following.all %}
      <a href="{% url 'follow_user' username=user_profile.user.username %}">Follow</a>
    {% else %}
      <a href="{% url 'follow_user' username=user_profile.user.username %}">Unfollow</a>
    {% endif %}
  {% endif %}

  <h2>Posts</h2>
  {% for post in user_profile.user.post_set.all %}
    <div>
      <p>{{ post.text }}</p>
      {% if post.image %}
        <img src="{{ post.image.url }}" alt="Post Image">
      {% endif %}
      {% if post.link %}
        <a href="{{ post.link }}" target="_blank">{{ post.link }}</a>
      {% endif %}
    </div>
  {% endfor %}
{% endblock %}
```
{% endraw %}

## Solution for 5th qustion


### Step 1: Create the Django Project and Apps

Open your terminal and run the following commands:

```bash
# Create Django project
django-admin startproject online_courses

# Navigate to the project directory
cd online_courses

# Create Django apps
python manage.py startapp courses
python manage.py startapp enrollments
python manage.py startapp quizzes
```

### Step 2: Define Models and Run Migrations

#### `courses/models.py`
```python
from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title
```

#### `enrollments/models.py`
```python
from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
```

#### `quizzes/models.py`
```python
from django.db import models
from courses.models import Lesson

class Quiz(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
```

#### Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Implement Views and Templates

#### `courses/views.py`
```python
from django.shortcuts import render
from .models import Course

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})
```

#### `courses/templates/courses/course_list.html`
{% raw %}
```html
<!-- courses/course_list.html -->
{% extends 'base.html' %}

{% block title %}Courses{% endblock %}

{% block content %}
  <h1>Available Courses</h1>
  {% for course in courses %}
    <div>
      <h2>{{ course.title }}</h2>
      <p>{{ course.description }}</p>
      <a href="{% url 'enroll' course.id %}">Enroll</a>
    </div>
  {% endfor %}
{% endblock %}
```
{% endraw %}

#### `courses/urls.py`
```python
from django.urls import path
from .views import course_list

urlpatterns = [
    path('', course_list, name='course_list'),
]
```

### Step 4: URL Routing

Configure the URLs in `urls.py` files of each app and the main project.

#### `online_courses/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),
    path('enrollments/', include('enrollments.urls')),
    path('quizzes/', include('quizzes.urls')),
]
```

#### `enrollments/urls.py`
```python
from django.urls import path
from .views import enroll, my_courses

urlpatterns = [
    path('enroll/<int:course_id>/', enroll, name='enroll'),
    path('my_courses/', my_courses, name='my_courses'),
]
```

#### `enrollments/views.py`
```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Enrollment
from courses.models import Course

@login_required
def enroll(request, course_id):
    course = Course.objects.get(pk=course_id)
    Enrollment.objects.create(user=request.user, course=course)
    return redirect('my_courses')

@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    return render(request, 'enrollments/my_courses.html', {'enrollments': enrollments})
```

#### `enrollments/templates/enrollments/my_courses.html`
{% raw %}
```html
<!-- enrollments/my_courses.html -->
{% extends 'base.html' %}

{% block title %}My Courses{% endblock %}

{% block content %}
  <h1>My Courses</h1>
  {% for enrollment in enrollments %}
    <div>
      <h2>{{ enrollment.course.title }}</h2>
      <p>{{ enrollment.course.description }}</p>
      <a href="{% url 'course_lessons' enrollment.course.id %}">Go to Course</a>
    </div>
  {% endfor %}
{% endblock %}
```
{% endraw %}

#### `quizzes/views.py`
```python
from django.shortcuts import render, get_object_or_404
from .models import Quiz
from courses.models import Lesson

def quiz_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    quiz = Quiz.objects.get(lesson=lesson)
    return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz})
```

#### `quizzes/templates/quizzes/quiz_detail.html`
{% raw %}
```html
<!-- quizzes/quiz_detail.html -->
{% extends 'base.html' %}

{% block title %}{{ quiz.title }}{% endblock %}

{% block content %}
  <h1>{{ quiz.title }}</h1>
  <p>{{ quiz.description }}</p>

  <form method="post" action="{% url 'submit_quiz' quiz.id %}">
    {% csrf_token %}
    {% for question in quiz.question_set.all %}
      <fieldset>
        <legend>{{ question.text }}</legend>
        {% for choice in question.choice_set.all %}
          <label>
            <input type="{{ 'radio' if question.is_multiple_choice else 'checkbox' }}" name="question_{{ question.id }}" value="{{ choice.id }}">
            {{ choice.text }}
          </label><br>
        {% endfor %}
      </fieldset>
    {% endfor %}
    <input type="submit" value="Submit">
  </form>
{% endblock %}
```
{% endraw %}

#### `quizzes/urls.py`
```python
from django.urls import path
from .views import quiz_detail, submit_quiz

urlpatterns = [
    path('<int:lesson_id>/', quiz_detail, name='quiz_detail'),
    path('submit/<int:quiz_id>/', submit_quiz, name='submit_quiz'),
]
```

#### `quizzes/views.py`
```python
from django.shortcuts import render

, get_object_or_404, redirect
from .models import Quiz
from courses.models import Lesson
from .forms import QuizSubmissionForm
from django.contrib import messages

def quiz_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    quiz = Quiz.objects.get(lesson=lesson)
    return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz})

def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    lesson = quiz.lesson
    form = QuizSubmissionForm(request.POST)

    if form.is_valid():
        # Process the quiz submission (evaluate answers, etc.)
        # For simplicity, let's assume correct answers are hardcoded
        correct_answers = {1: [1], 2: [2, 3], 3: [4]}

        user_answers = form.cleaned_data
        score = 0

        for question_id, selected_choices in user_answers.items():
            correct_choices = correct_answers.get(question_id, [])
            if set(selected_choices) == set(correct_choices):
                score += 1

        # Save the user's score or feedback in the database
        # For now, we'll just display a message
        messages.success(request, f"You scored {score} out of {quiz.question_set.count()}!")

        return redirect('course_lessons', lesson.course.id)

    return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz, 'form': form})
```

### Step 5: Update the URLs for Course Lessons

#### `courses/urls.py`
```python
from django.urls import path
from .views import course_list, course_lessons

urlpatterns = [
    path('', course_list, name='course_list'),
    path('<int:course_id>/lessons/', course_lessons, name='course_lessons'),
]
```

### Step 6: Update the Course Lessons View

#### `courses/views.py`
```python
from django.shortcuts import render, get_object_or_404
from .models import Course, Lesson

def course_lessons(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    lessons = Lesson.objects.filter(course=course)
    return render(request, 'courses/course_lessons.html', {'course': course, 'lessons': lessons})
```

#### `courses/templates/courses/course_lessons.html`
{% raw %}
```html
<!-- courses/course_lessons.html -->
{% extends 'base.html' %}

{% block title %}{{ course.title }} - Lessons{% endblock %}

{% block content %}
  <h1>{{ course.title }} - Lessons</h1>
  {% for lesson in lessons %}
    <div>
      <h2>{{ lesson.title }}</h2>
      <p>{{ lesson.content }}</p>
      <a href="{% url 'quiz_detail' lesson.id %}">Take Quiz</a>
    </div>
  {% endfor %}
{% endblock %}
```
{% endraw %}

### Step 7: Update the URLs for Quiz Detail and Quiz Submission

#### `quizzes/urls.py`
```python
from django.urls import path
from .views import quiz_detail, submit_quiz

urlpatterns = [
    path('<int:lesson_id>/', quiz_detail, name='quiz_detail'),
    path('submit/<int:quiz_id>/', submit_quiz, name='submit_quiz'),
]
```

### Step 8: Update the Navigation Bar in `base.html`

#### `templates/base.html`
{% raw %}
```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Default Title{% endblock %}</title>
</head>
<body>
    <nav>
        <ul>
            <li><a href="{% url 'course_list' %}">Courses</a></li>
            <li><a href="{% url 'my_courses' %}">My Courses</a></li>
            {% if user.is_authenticated %}
              <li><a href="{% url 'logout' %}">Logout</a></li>
            {% else %}
              <li><a href="{% url 'login' %}">Login</a></li>
              <li><a href="{% url 'register' %}">Register</a></li>
            {% endif %}
        </ul>
    </nav>
    {% block content %}
    {% endblock %}
</body>
</html>
```
{% endraw %}

### Step 9: Enhance Quiz Submission and Feedback

#### `quizzes/views.py`
```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz, Question, Choice
from courses.models import Lesson
from .forms import QuizSubmissionForm
from django.contrib import messages

def quiz_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    quiz = Quiz.objects.get(lesson=lesson)
    return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz})

def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    lesson = quiz.lesson
    form = QuizSubmissionForm(request.POST)

    if form.is_valid():
        user_answers = form.cleaned_data

        # Process the quiz submission (evaluate answers, etc.)
        # For simplicity, let's assume correct answers are hardcoded
        correct_answers = {question.id: [choice.id for choice in question.choice_set.filter(is_correct=True)] for question in quiz.question_set.all()}

        score = 0
        feedback = []

        for question_id, selected_choices in user_answers.items():
            correct_choices = correct_answers.get(question_id, [])
            if set(selected_choices) == set(correct_choices):
                score += 1
                feedback.append({'question_id': question_id, 'correct': True})
            else:
                feedback.append({'question_id': question_id, 'correct': False, 'correct_choices': correct_choices})

        # Save the user's score or feedback in the database
        # For now, we'll just display a message
        messages.success(request, f"You scored {score} out of {quiz.question_set.count()}!")

        return render(request, 'quizzes/quiz_feedback.html', {'quiz': quiz, 'feedback': feedback})

    return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz, 'form': form})
```

#### `quizzes/templates/quizzes/quiz_feedback.html`
{% raw %}
```html
<!-- quizzes/quiz_feedback.html -->
{% extends 'base.html' %}

{% block title %}Quiz Feedback{% endblock %}

{% block content %}
  <h1>Quiz Feedback</h1>
  <p>Your Quiz Results:</p>
  <p>You scored {{ feedback|length }} out of {{ quiz.question_set.count() }}!</p>

  <h2>Feedback:</h2>
  {% for item in feedback %}
    <div>
      <p>Question: {{ quiz.question_set.get(pk=item.question_id).text }}</p>
      {% if item.correct %}
        <p>Your Answer: Correct</p>
      {% else %}
        <p>Your Answer: Incorrect</p>
        <p>Correct Choices: {{ quiz.question_set.get(pk=item.question_id).choice_set.filter(is_correct=True)|join:", " }}</p>
      {% endif %}
    </div>
  {% endfor %}
{% endblock %}
```
{% endgraw %}

### Step 10: Update Navigation Bar for My Courses and Logout

#### `templates/base.html`
{% raw %}
```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Default Title{% endblock %}</title>
</head>
<body>
    <nav>
        <ul>
            <li><a href="{% url 'course_list' %}">Courses</a></li>
            <li><a href="{% url 'my_courses' %}">My Courses</a></li>
            {% if user.is_authenticated %}
              <li><a href="{% url 'logout' %}">Logout</a></li>
            {% else %}
              <li><a href="{% url 'login' %}">Login</a></li>
              <li><a href="{% url 'register' %}">Register</a></li>
            {% endif %}
        </ul>
    </nav>
    {% block content %}
    {% endblock %}
</body>
</html>
```
{% endraw %}