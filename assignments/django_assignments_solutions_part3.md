# Django Assignment Solutions: Part 3

## Solution for 11th qustion

### Step 1: Create the Django Project and Apps

```bash
# Create Django project
django-admin startproject quiz_maker

# Navigate to the project directory
cd quiz_maker

# Create Django apps
python manage.py startapp quizzes
python manage.py startapp questions
python manage.py startapp attempts
```

### Step 2: Define Models

#### `quizzes/models.py`
```python
from django.db import models

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty_levels = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    difficulty = models.CharField(max_length=10, choices=difficulty_levels)

    def __str__(self):
        return self.title
```

#### `questions/models.py`
```python
from django.db import models

class Question(models.Model):
    QUESTION_TYPES = [
        ('mc', 'Multiple Choice'),
        ('tf', 'True/False'),
        ('oe', 'Open-Ended'),
    ]

    quiz = models.ForeignKey('quizzes.Quiz', on_delete=models.CASCADE)
    content = models.TextField()
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPES)
    answer = models.TextField()

    def __str__(self):
        return self.content
```

#### `attempts/models.py`
```python
from django.db import models
from django.contrib.auth.models import User
from quizzes.models import Quiz

class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField(null=True, blank=True)
    submission_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"
```

### Step 3: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Implement Views and Templates

#### `quizzes/views.py`
```python
from django.shortcuts import render, get_object_or_404
from .models import Quiz

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quizzes/quiz_list.html', {'quizzes': quizzes})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz})
```

### `templates/base.html`
{% raw %}
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Quiz Maker{% endblock %}</title>
    <!-- Add your additional head content here -->
</head>
<body>
    <header>
        <h1>Quiz Maker</h1>
        <nav>
            <ul>
                <li><a href="{% url 'quiz_list' %}">Quizzes</a></li>
                <!-- Add other navigation links as needed -->
            </ul>
        </nav>
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <!-- Add footer content if needed -->
    </footer>
</body>
</html>
```

In this base template:
- The `{% block title %}` and `{% block content %}` are placeholders where specific content for the title and main content will be injected in templates that extend this base template.
- The navigation bar contains a link to the quizzes list page. You can add more links based on the structure of your project.

#### `quizzes/templates/quizzes/quiz_list.html`
```html
<!-- quizzes/quiz_list.html -->
{% extends 'base.html' %}

{% block title %}Quizzes{% endblock %}

{% block content %}
  <h1>Quizzes</h1>
  <ul>
    {% for quiz in quizzes %}
      <li>
        <h2><a href="{% url 'quiz_detail' quiz.id %}">{{ quiz.title }}</a></h2>
        <p>{{ quiz.description }}</p>
        <p>Difficulty: {{ quiz.get_difficulty_display }}</p>
      </li>
    {% endfor %}
  </ul>
{% endblock %}
```

#### `quizzes/templates/quizzes/quiz_detail.html`
```html
<!-- quizzes/quiz_detail.html -->
{% extends 'base.html' %}

{% block title %}{{ quiz.title }}{% endblock %}

{% block content %}
  <h1>{{ quiz.title }}</h1>
  <p>{{ quiz.description }}</p>
  <p>Difficulty: {{ quiz.get_difficulty_display }}</p>
  <!-- Add questions here -->
{% endblock %}
```
{% endraw %}


### Step 5: Update URLs

#### `quizzes/urls.py`
```python
from django.urls import path
from .views import quiz_list, quiz_detail

urlpatterns = [
    path('', quiz_list, name='quiz_list'),
    path('<int:quiz_id>/', quiz_detail, name='quiz_detail'),
]
```

#### `news_portal/urls.py`
Include the quiz app URLs.

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quizzes/', include('quizzes.urls')),
    # Add other app URLs here
]
```

### Step 6: Create Templates for Questions

Create templates for displaying and submitting questions.

#### `questions/views.py`
```python
from django.shortcuts import render, get_object_or_404
from .models import Question

def question_detail(request, quiz_id, question_id):
    question = get_object_or_404(Question, pk=question_id, quiz_id=quiz_id)
    return render(request, 'questions/question_detail.html', {'question': question})
```

#### `questions/templates/questions/question_detail.html`
{% raw %}
```html
<!-- questions/question_detail.html -->
{% extends 'base.html' %}

{% block title %}Question - {{ question.content }}{% endblock %}

{% block content %}
  <h1>{{ question.content }}</h1>
  {% if question.question_type == 'mc' %}
    <!-- Display multiple-choice options -->
    <ul>
      {% for option in question.options.all %}
        <li>{{ option.content }}</li>
      {% endfor %}
    </ul>
  {% endif %}

  <!-- Add other question types as needed -->

  <!-- Add a form for submitting answers -->
{% endblock %}
```
{% endraw %}

### Step 7: Update URLs

#### `questions/urls.py`
```python
from django.urls import path
from .views import question_detail

urlpatterns = [
    path('<int:quiz_id>/<int:question_id>/', question_detail, name='question_detail'),
]
```

#### `quizzes/urls.py`
Include the question app URLs.

```python
from django.urls import path, include
from .views import quiz_list, quiz_detail

urlpatterns = [
    path('', quiz_list, name='quiz_list'),
    path('<int:quiz_id>/', quiz_detail, name='quiz_detail'),
    path('<int:quiz_id>/questions/', include('questions.urls')),
]
```

### Step 8: Create Templates for Attempts

Create templates for taking quizzes and displaying feedback.

#### `attempts/views.py`
```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Attempt
from questions.models import Question
from django.contrib.auth.decorators import login_required

@login_required
def take_quiz(request, quiz_id):
    # Implement logic to handle quiz submission
    pass

@login_required
def feedback(request, attempt_id):
    attempt = get_object_or_404(Attempt, pk=attempt_id, user=request.user)
    questions = Question.objects.filter(quiz=attempt.quiz)
    return render(request, 'attempts/feedback.html', {'attempt': attempt, 'questions': questions})
```

#### `attempts/templates/attempts/feedback.html`
{% raw %}
```html
<!-- attempts/feedback.html -->
{% extends 'base.html' %}

{% block title %}Feedback - {{ attempt.quiz.title }}{% endblock %}

{% block content %}
  <h1>Feedback - {{ attempt.quiz.title }}</h1>
  <p>Your Score: {{ attempt.score }}</p>
  <ul>
    {% for question in questions %}
      <li>
        <h2>{{ question.content }}</h2>
        <p>Your Answer: {{ question.user_answers.get(attempt=attempt).content }}</p>
        <p>Correct Answer: {{ question.answer }}</p>
      </li>
    {% endfor %}
  </ul>
{% endblock %}
```
{% endraw %}

### Step 9: Update URLs

#### `attempts/urls.py`
```python
from django.urls import path
from .views import take_quiz, feedback

urlpatterns = [
    path('take/<int:quiz_id>/', take_quiz, name='take_quiz'),
    path('feedback/<int:attempt_id>/', feedback, name='feedback'),
]
```

#### `quizzes/urls.py`
Include the attempt app URLs.

```python
from django.urls import path, include
from .views import quiz_list, quiz_detail

urlpatterns = [
    path('', quiz_list, name='quiz_list'),
    path('<int:quiz_id>/', quiz_detail, name='quiz_detail'),
    path('<int:quiz_id>/questions/', include('questions.urls')),
    path('<int:quiz_id>/attempts/', include('attempts.urls')),
]
```

### Step 10: Run the Development Server

Run the development server to test your application:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/quizzes/` in your web browser to see the list of quizzes. You can explore and adapt the templates and views based on your specific requirements.

### Step 11: Implement Views for Quiz Taking

#### `attempts/views.py`
```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Attempt
from questions.models import Question
from django.contrib.auth.decorators import login_required

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.questions.all()

    if request.method == 'POST':
        # Process submitted answers
        answers = {}
        for question in questions:
            answer = request.POST.get(f'question_{question.id}', '')
            answers[question.id] = answer

        # Calculate score (you may need to customize this based on your scoring logic)
        score = calculate_score(quiz, answers)

        # Save the attempt
        attempt = Attempt.objects.create(user=request.user, quiz=quiz, score=score)

        # Save user answers
        for question_id, user_answer in answers.items():
            question = Question.objects.get(pk=question_id)
            question.user_answers.create(attempt=attempt, content=user_answer)

        # Redirect to the feedback page
        return redirect('feedback', attempt_id=attempt.id)

    return render(request, 'attempts/take_quiz.html', {'quiz': quiz, 'questions': questions})
```

### Step 12: Create Templates for Quiz Taking

#### `attempts/templates/attempts/take_quiz.html`
{% raw %}
```html
<!-- attempts/take_quiz.html -->
{% extends 'base.html' %}

{% block title %}Take Quiz - {{ quiz.title }}{% endblock %}

{% block content %}
  <h1>Take Quiz - {{ quiz.title }}</h1>
  <form method="post" action="{% url 'take_quiz' quiz.id %}">
    {% csrf_token %}
    {% for question in questions %}
      <fieldset>
        <legend>{{ question.content }}</legend>
        {% if question.question_type == 'mc' %}
          <!-- Display multiple-choice options -->
          {% for option in question.options.all %}
            <label>
              <input type="radio" name="question_{{ question.id }}" value="{{ option.content }}">
              {{ option.content }}
            </label><br>
          {% endfor %}
        {% elif question.question_type == 'tf' %}
          <!-- Display true/false options -->
          <label>
            <input type="radio" name="question_{{ question.id }}" value="True"> True
          </label>
          <label>
            <input type="radio" name="question_{{ question.id }}" value="False"> False
          </label>
        {% elif question.question_type == 'oe' %}
          <!-- Display open-ended input -->
          <label>
            Your Answer:
            <input type="text" name="question_{{ question.id }}">
          </label>
        {% endif %}
      </fieldset>
    {% endfor %}
    <button type="submit">Submit Quiz</button>
  </form>
{% endblock %}
```
{% endraw %}

### Step 13: Update URLs

#### `attempts/urls.py`
```python
from django.urls import path
from .views import take_quiz, feedback

urlpatterns = [
    path('take/<int:quiz_id>/', take_quiz, name='take_quiz'),
    path('feedback/<int:attempt_id>/', feedback, name='feedback'),
]
```

#### `quizzes/urls.py`
Include the attempt app URLs.

```python
from django.urls import path, include
from .views import quiz_list, quiz_detail

urlpatterns = [
    path('', quiz_list, name='quiz_list'),
    path('<int:quiz_id>/', quiz_detail, name='quiz_detail'),
    path('<int:quiz_id>/questions/', include('questions.urls')),
    path('<int:quiz_id>/attempts/', include('attempts.urls')),
]
```

### Step 14: Run the Development Server

Run the development server to test your application:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/quizzes/` in your web browser to see the list of quizzes. Click on a quiz to take it and submit your answers.

### Step 15: Implement Scoring Logic

In this step, we'll define a function to calculate the score based on the submitted answers.

#### `attempts/utils.py`
Create a new file for utility functions.

```python
# attempts/utils.py
def calculate_score(quiz, answers):
    # Implement your scoring logic here
    # For example, you may assign points for each correct answer

    total_questions = quiz.questions.count()
    correct_answers = 0

    for question in quiz.questions.all():
        if str(answers.get(question.id, '')) == str(question.answer):
            correct_answers += 1

    score_percentage = (correct_answers / total_questions) * 100
    return round(score_percentage, 2)
```

### Step 16: Update the Attempts Views

Update the attempts views to use the scoring logic.

#### `attempts/views.py`
```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Attempt
from questions.models import Question
from django.contrib.auth.decorators import login_required
from .utils import calculate_score

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.questions.all()

    if request.method == 'POST':
        # Process submitted answers
        answers = {}
        for question in questions:
            answer = request.POST.get(f'question_{question.id}', '')
            answers[question.id] = answer

        # Calculate score using the scoring logic
        score = calculate_score(quiz, answers)

        # Save the attempt
        attempt = Attempt.objects.create(user=request.user, quiz=quiz, score=score)

        # Save user answers
        for question_id, user_answer in answers.items():
            question = Question.objects.get(pk=question_id)
            question.user_answers.create(attempt=attempt, content=user_answer)

        # Redirect to the feedback page
        return redirect('feedback', attempt_id=attempt.id)

    return render(request, 'attempts/take_quiz.html', {'quiz': quiz, 'questions': questions})
```

### Step 17: Update the Feedback Template

Update the feedback template to display the user's score and correct answers.

#### `attempts/templates/attempts/feedback.html`
{% raw %}
```html
<!-- attempts/feedback.html -->
{% extends 'base.html' %}

{% block title %}Feedback - {{ attempt.quiz.title }}{% endblock %}

{% block content %}
  <h1>Feedback - {{ attempt.quiz.title }}</h1>
  <p>Your Score: {{ attempt.score }}%</p>
  <ul>
    {% for question in questions %}
      <li>
        <h2>{{ question.content }}</h2>
        <p>Your Answer: {{ question.user_answers.get(attempt=attempt).content }}</p>
        <p>Correct Answer: {{ question.answer }}</p>
      </li>
    {% endfor %}
  </ul>
{% endblock %}
```
{% endraw %}

### Step 18: Run the Development Server

Run the development server to test your application:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/quizzes/` in your web browser to see the list of quizzes. Click on a quiz to take it and submit your answers. After submission, you'll be redirected to a feedback page displaying your score and the correct answers.

## Solution for 12th qustion

### Step 1: Create the Django Project and Apps

```bash
# Create Django project
django-admin startproject e_learning

# Navigate to the project directory
cd e_learning

# Create Django apps
python manage.py startapp courses
python manage.py startapp lessons
python manage.py startapp forum_categories
python manage.py startapp forum_threads
```

### Step 2: Define Models

#### `courses/models.py`
```python
from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_lectures = models.FileField(upload_to='video_lectures/')
    quizzes = models.ManyToManyField('lessons.Quiz', related_name='courses', blank=True)
    assignments = models.ManyToManyField('lessons.Assignment', related_name='courses', blank=True)

    def __str__(self):
        return self.title
```

#### `lessons/models.py`
```python
from django.db import models

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    # Add relevant fields for quiz questions and options

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    description = models.TextField()
    file = models.FileField(upload_to='assignments/')

    def __str__(self):
        return self.title
```

#### `forum_categories/models.py`
```python
from django.db import models

class ForumCategory(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
```

#### `forum_threads/models.py`
```python
from django.db import models
from django.contrib.auth.models import User

class ForumThread(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey('forum_categories.ForumCategory', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.title
```

### Step 3: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Implement Views and Templates

#### `courses/views.py`
```python
from django.shortcuts import render
from .models import Course

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = Course.objects.get(pk=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})
```

#### `courses/templates/courses/course_list.html`
{% raw %}
```html
<!-- courses/course_list.html -->
{% extends 'base.html' %}

{% block title %}Courses{% endblock %}

{% block content %}
  <h1>Courses</h1>
  <ul>
    {% for course in courses %}
      <li>
        <h2><a href="{% url 'course_detail' course.id %}">{{ course.title }}</a></h2>
        <p>{{ course.description }}</p>
      </li>
    {% endfor %}
  </ul>
{% endblock %}
```

#### `courses/templates/courses/course_detail.html`
```html
<!-- courses/course_detail.html -->
{% extends 'base.html' %}

{% block title %}{{ course.title }}{% endblock %}

{% block content %}
  <h1>{{ course.title }}</h1>
  <p>{{ course.description }}</p>
  <!-- Add links to video lectures, quizzes, and assignments -->
{% endblock %}
```
{% endraw %}

#### `forum_threads/views.py`
```python
from django.shortcuts import render
from .models import ForumThread

def forum_thread_list(request):
    forum_threads = ForumThread.objects.all()
    return render(request, 'forum_threads/forum_thread_list.html', {'forum_threads': forum_threads})
```

#### `forum_threads/templates/forum_threads/forum_thread_list.html`
{% raw %}
```html
<!-- forum_threads/forum_thread_list.html -->
{% extends 'base.html' %}

{% block title %}Forum{% endblock %}

{% block content %}
  <h1>Forum</h1>
  <ul>
    {% for thread in forum_threads %}
      <li>
        <h2>{{ thread.title }}</h2>
        <p>Category: {{ thread.category.title }}</p>
        <p>Creator: {{ thread.creator.username }}</p>
        <p>Created on: {{ thread.creation_date }}</p>
        <p>{{ thread.content }}</p>
      </li>
    {% endfor %}
  </ul>
{% endblock %}
```
{% endraw %}

### Step 5: Update URLs

#### `courses/urls.py`
```python
from django.urls import path
from .views import course_list, course_detail

urlpatterns = [
    path('', course_list, name='course_list'),
    path('<int:course_id>/', course_detail, name='course_detail'),
]
```

#### `forum_threads/urls.py`
```python
from django.urls import path
from .views import forum_thread_list

urlpatterns = [
    path('', forum_thread_list

, name='forum_thread_list'),
]
```

#### `e_learning/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),
    path('forum/', include('forum_threads.urls')),
    # Add other app URLs here
]
```

### Step 6: Run the Development Server

Run the development server to test your application:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/courses/` and `http://127.0.0.1:8000/forum/` in your web browser to see the list of courses and forum threads.

### Step 7: Implement Forum Views and Templates

#### `forum_threads/views.py`
```python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ForumThread
from .forms import ForumThreadForm, ForumReplyForm

def forum_thread_detail(request, thread_id):
    thread = get_object_or_404(ForumThread, pk=thread_id)
    return render(request, 'forum_threads/forum_thread_detail.html', {'thread': thread})

@login_required
def create_forum_thread(request):
    if request.method == 'POST':
        form = ForumThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.creator = request.user
            thread.save()
            return redirect('forum_thread_detail', thread_id=thread.id)
    else:
        form = ForumThreadForm()
    return render(request, 'forum_threads/create_forum_thread.html', {'form': form})

@login_required
def create_forum_reply(request, thread_id):
    thread = get_object_or_404(ForumThread, pk=thread_id)

    if request.method == 'POST':
        form = ForumReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.thread = thread
            reply.creator = request.user
            reply.save()
            return redirect('forum_thread_detail', thread_id=thread.id)
    else:
        form = ForumReplyForm()

    return render(request, 'forum_threads/create_forum_reply.html', {'form': form, 'thread': thread})
```

#### `forum_threads/templates/forum_threads/forum_thread_detail.html`
{% raw %}
```html
<!-- forum_threads/forum_thread_detail.html -->
{% extends 'base.html' %}

{% block title %}{{ thread.title }}{% endblock %}

{% block content %}
  <h1>{{ thread.title }}</h1>
  <p>Category: {{ thread.category.title }}</p>
  <p>Creator: {{ thread.creator.username }}</p>
  <p>Created on: {{ thread.creation_date }}</p>
  <p>{{ thread.content }}</p>

  <h2>Replies</h2>
  <ul>
    {% for reply in thread.replies.all %}
      <li>
        <p>Creator: {{ reply.creator.username }}</p>
        <p>Created on: {{ reply.creation_date }}</p>
        <p>{{ reply.content }}</p>
      </li>
    {% endfor %}
  </ul>

  <a href="{% url 'create_forum_reply' thread.id %}">Reply to this thread</a>
{% endblock %}
```

#### `forum_threads/templates/forum_threads/create_forum_thread.html`
```html
<!-- forum_threads/create_forum_thread.html -->
{% extends 'base.html' %}

{% block title %}Create Forum Thread{% endblock %}

{% block content %}
  <h1>Create Forum Thread</h1>
  <form method="post" action="{% url 'create_forum_thread' %}">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Create Thread</button>
  </form>
{% endblock %}
```

#### `forum_threads/templates/forum_threads/create_forum_reply.html`
```html
<!-- forum_threads/create_forum_reply.html -->
{% extends 'base.html' %}

{% block title %}Reply to Forum Thread{% endblock %}

{% block content %}
  <h1>Reply to Forum Thread</h1>
  <form method="post" action="{% url 'create_forum_reply' thread.id %}">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Reply</button>
  </form>
{% endblock %}
```
{% endraw %}

### Step 8: Create Forum Forms

Create forms to handle the creation of forum threads and replies.

#### `forum_threads/forms.py`
```python
from django import forms
from .models import ForumThread, ForumReply

class ForumThreadForm(forms.ModelForm):
    class Meta:
        model = ForumThread
        fields = ['title', 'category', 'content']

class ForumReplyForm(forms.ModelForm):
    class Meta:
        model = ForumReply
        fields = ['content']
```

### Step 9: Update URLs

#### `forum_threads/urls.py`
```python
from django.urls import path
from .views import forum_thread_list, forum_thread_detail, create_forum_thread, create_forum_reply

urlpatterns = [
    path('', forum_thread_list, name='forum_thread_list'),
    path('<int:thread_id>/', forum_thread_detail, name='forum_thread_detail'),
    path('create/', create_forum_thread, name='create_forum_thread'),
    path('<int:thread_id>/reply/', create_forum_reply, name='create_forum_reply'),
]
```

### Step 10: Run the Development Server

Run the development server to test your application:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/forum/` to see the list of forum threads. You can create new threads and reply to existing ones.

### Step 11: Implement Forum Moderation Views and Templates

#### `forum_threads/views.py`
```python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .models import ForumThread, ForumReply
from .forms import ForumThreadForm, ForumReplyForm

@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_forum_thread(request, thread_id):
    thread = get_object_or_404(ForumThread, pk=thread_id)
    
    if request.method == 'POST':
        form = ForumThreadForm(request.POST, instance=thread)
        if form.is_valid():
            form.save()
            return redirect('forum_thread_detail', thread_id=thread.id)
    else:
        form = ForumThreadForm(instance=thread)

    return render(request, 'forum_threads/edit_forum_thread.html', {'form': form, 'thread': thread})

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_forum_thread(request, thread_id):
    thread = get_object_or_404(ForumThread, pk=thread_id)

    if request.method == 'POST':
        thread.delete()
        return redirect('forum_thread_list')

    return render(request, 'forum_threads/delete_forum_thread.html', {'thread': thread})

@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_forum_reply(request, thread_id, reply_id):
    reply = get_object_or_404(ForumReply, pk=reply_id)
    
    if request.method == 'POST':
        form = ForumReplyForm(request.POST, instance=reply)
        if form.is_valid():
            form.save()
            return redirect('forum_thread_detail', thread_id=thread_id)
    else:
        form = ForumReplyForm(instance=reply)

    return render(request, 'forum_threads/edit_forum_reply.html', {'form': form, 'reply': reply, 'thread_id': thread_id})

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_forum_reply(request, thread_id, reply_id):
    reply = get_object_or_404(ForumReply, pk=reply_id)

    if request.method == 'POST':
        reply.delete()
        return redirect('forum_thread_detail', thread_id=thread_id)

    return render(request, 'forum_threads/delete_forum_reply.html', {'reply': reply, 'thread_id': thread_id})
```

#### `forum_threads/templates/forum_threads/edit_forum_thread.html`
{% raw %}
```html
<!-- forum_threads/edit_forum_thread.html -->
{% extends 'base.html' %}

{% block title %}Edit Forum Thread{% endblock %}

{% block content %}
  <h1>Edit Forum Thread</h1>
  <form method="post" action="">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save Changes</button>
  </form>
  <a href="{% url 'forum_thread_detail' thread.id %}">Cancel</a>
{% endblock %}
```

#### `forum_threads/templates/forum_threads/delete_forum_thread.html`
```html
<!-- forum_threads/delete_forum_thread.html -->
{% extends 'base.html' %}

{% block title %}Delete Forum Thread{% endblock %}

{% block content %}
  <h1>Delete Forum Thread</h1>
  <p>Are you sure you want to delete the forum thread "{{ thread.title }}"?</p>
  <form method="post" action="">
    {% csrf_token %}
    <button type="submit">Yes, delete</button>
  </form>
  <a href="{% url 'forum_thread_detail' thread.id %}">Cancel</a>
{% endblock %}
```

#### `forum_threads/templates/forum_threads/edit_forum_reply.html`
```html
<!-- forum_threads/edit_forum_reply.html -->
{% extends 'base.html' %}

{% block title %}Edit Forum Reply{% endblock %}

{% block content %}
  <h1>Edit Forum Reply</h1>
  <form method="post" action="">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save Changes</button>
  </form>
  <a href="{% url 'forum_thread_detail' thread_id %}">Cancel</a>
{% endblock %}
```

#### `forum_threads/templates/forum_threads/delete_forum_reply.html`
```html
<!-- forum_threads/delete_forum_reply.html -->
{% extends 'base.html' %}

{% block title %}Delete Forum Reply{% endblock %}

{% block content %}
  <h1>Delete Forum Reply</h1>
  <p>Are you sure you want to delete the forum reply?</p>
  <form method="post" action="">
    {% csrf_token %}
    <button type="submit">Yes, delete</button>
  </form>
  <a href="{% url 'forum_thread_detail' thread_id %}">Cancel</a>
{% endblock %}
```
{% endraw %}

### Step 12: Update URLs

#### `forum_threads/urls.py`
```python
from django.urls import path
from .views import forum_thread_list, forum_thread_detail, create_forum_thread, create_forum_reply
from .views import edit_forum_thread, delete_forum_thread, edit_forum_reply, delete_forum_reply

urlpatterns = [
    path('', forum_thread_list, name='forum_thread_list'),
    path('<int:thread_id>/', forum_thread_detail, name='forum_thread_detail'),
    path('create/', create_forum_thread, name='create_forum_thread'),
    path('<int:thread_id>/reply/', create_forum_reply, name='create_forum_reply'),
    path('<int:thread_id>/edit/', edit_forum_thread, name='edit_forum_thread'),
    path('<int:thread_id>/delete/', delete_forum_thread, name='delete_forum_thread'),
    path('<int:thread_id>/edit/<int:reply_id>/', edit_forum_reply, name='

edit_forum_reply'),
    path('<int:thread_id>/delete/<int:reply_id>/', delete_forum_reply, name='delete_forum_reply'),
]
```

### Step 13: Run the Development Server

Run the development server to test your application:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/forum/` to see the list of forum threads. Moderators and staff members can edit and delete threads and replies.

## Solution for 13th qustion

### Step 1: Create Django Project and Apps

```bash
# Create Django project
django-admin startproject job_portal

# Change directory to the project folder
cd job_portal

# Create Django apps
python manage.py startapp companies
python manage.py startapp jobs
python manage.py startapp applicants
```

### Step 2: Define Models

#### `companies/models.py`
```python
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    industry = models.CharField(max_length=50)
    headquarters = models.CharField(max_length=100)

    def __str__(self):
        return self.name
```

#### `jobs/models.py`
```python
from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=100)
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    description = models.TextField()
    skills = models.CharField(max_length=200)
    requirements = models.TextField()

    def __str__(self):
        return self.title
```

#### `applicants/models.py`
```python
from django.db import models

class Applicant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    resume = models.FileField(upload_to='resumes/')

    def __str__(self):
        return self.name
```

### Step 3: Implement Views and Templates

#### `companies/views.py`
```python
from django.shortcuts import render
from .models import Company

def company_list(request):
    companies = Company.objects.all()
    return render(request, 'companies/company_list.html', {'companies': companies})
```

#### `companies/templates/companies/company_list.html`
{% raw %}
```html
<!-- companies/company_list.html -->
{% extends 'base.html' %}

{% block title %}Company List{% endblock %}

{% block content %}
  <h1>Company List</h1>
  <ul>
    {% for company in companies %}
      <li>{{ company.name }} - {{ company.industry }}</li>
    {% endfor %}
  </ul>
{% endblock %}
```
{% endraw %}

#### `jobs/views.py`
```python
from django.shortcuts import render
from .models import Job

def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})
```

#### `jobs/templates/jobs/job_list.html`
{% raw %}
```html
<!-- jobs/job_list.html -->
{% extends 'base.html' %}

{% block title %}Job List{% endblock %}

{% block content %}
  <h1>Job List</h1>
  <ul>
    {% for job in jobs %}
      <li>{{ job.title }} - {{ job.company.name }}</li>
    {% endfor %}
  </ul>
{% endblock %}
```
{% endraw %}

#### `applicants/views.py`
```python
from django.shortcuts import render
from .models import Applicant

def applicant_list(request):
    applicants = Applicant.objects.all()
    return render(request, 'applicants/applicant_list.html', {'applicants': applicants})
```

#### `applicants/templates/applicants/applicant_list.html`
{% raw %}
```html
<!-- applicants/applicant_list.html -->
{% extends 'base.html' %}

{% block title %}Applicant List{% endblock %}

{% block content %}
  <h1>Applicant List</h1>
  <ul>
    {% for applicant in applicants %}
      <li>{{ applicant.name }} - {{ applicant.email }}</li>
    {% endfor %}
  </ul>
{% endblock %}
```
{% endraw %}

### Step 4: Update URLs

#### `job_portal/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('companies/', include('companies.urls')),
    path('jobs/', include('jobs.urls')),
    path('applicants/', include('applicants.urls')),
]
```

#### `companies/urls.py`
```python
from django.urls import path
from .views import company_list

urlpatterns = [
    path('', company_list, name='company_list'),
]
```

#### `jobs/urls.py`
```python
from django.urls import path
from .views import job_list

urlpatterns = [
    path('', job_list, name='job_list'),
]
```

#### `applicants/urls.py`
```python
from django.urls import path
from .views import applicant_list

urlpatterns = [
    path('', applicant_list, name='applicant_list'),
]
```

### Step 5: Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/companies/`, `http://127.0.0.1:8000/jobs/`, and `http://127.0.0.1:8000/applicants/` in your web browser to see the company list, job list, and applicant list, respectively.

### Step 6: Implement Job Detail View

#### `jobs/views.py`
```python
from django.shortcuts import render, get_object_or_404
from .models import Job

def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'jobs/job_detail.html', {'job': job})
```

#### `jobs/templates/jobs/job_detail.html`
{% raw %}
```html
<!-- jobs/job_detail.html -->
{% extends 'base.html' %}

{% block title %}{{ job.title }} - {{ job.company.name }}{% endblock %}

{% block content %}
  <h1>{{ job.title }}</h1>
  <p>Company: {{ job.company.name }}</p>
  <p>Description: {{ job.description }}</p>
  <p>Skills: {{ job.skills }}</p>
  <p>Requirements: {{ job.requirements }}</p>
{% endblock %}
```
{% endraw %}

### Step 7: Update URLs

#### `jobs/urls.py`
```python
from django.urls import path
from .views import job_list, job_detail

urlpatterns = [
    path('', job_list, name='job_list'),
    path('<int:job_id>/', job_detail, name='job_detail'),
]
```

### Step 8: Update Navigation in `base.html`

#### `base.html`
{% raw %}
```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Your Project Title{% endblock %}</title>
    <!-- Add your CSS styles or include external stylesheets here -->
</head>

<body>
    <header>
        <h1>Your Project Name</h1>
        <nav>
            <ul>
                <li><a href="{% url 'company_list' %}">Companies</a></li>
                <li><a href="{% url 'job_list' %}">Jobs</a></li>
                <li><a href="{% url 'applicant_list' %}">Applicants</a></li>
            </ul>
        </nav>
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <!-- Add footer content or links here -->
    </footer>

    <!-- Add your JavaScript scripts or include external scripts here -->
</body>

</html>
```
{% endraw %}

### Step 9: Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/jobs/` to see the updated job list. Click on a job title to view the job details.

Certainly! Let's continue to implement the remaining features for the "job_portal" project.

### Step 10: Implement Search Functionality

#### `jobs/views.py`
```python
from django.shortcuts import render
from .models import Job

def job_search(request):
    query = request.GET.get('q', '')
    results = Job.objects.filter(skills__icontains=query)
    return render(request, 'jobs/job_search.html', {'query': query, 'results': results})
```

#### `jobs/templates/jobs/job_search.html`
{% raw %}
```html
<!-- jobs/job_search.html -->
{% extends 'base.html' %}

{% block title %}Search Results{% endblock %}

{% block content %}
  <h1>Search Results for "{{ query }}"</h1>
  <ul>
    {% for job in results %}
      <li><a href="{% url 'job_detail' job.id %}">{{ job.title }} - {{ job.company.name }}</a></li>
    {% endfor %}
  </ul>
{% endblock %}
```
{% endraw %}

#### `jobs/urls.py`
```python
from django.urls import path
from .views import job_list, job_detail, job_search

urlpatterns = [
    path('', job_list, name='job_list'),
    path('<int:job_id>/', job_detail, name='job_detail'),
    path('search/', job_search, name='job_search'),
]
```

### Step 11: Implement Online Job Application

#### `applicants/views.py`
```python
from django.shortcuts import render, redirect
from .models import Applicant
from .forms import ApplicantForm

def apply_for_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)

    if request.method == 'POST':
        form = ApplicantForm(request.POST, request.FILES)
        if form.is_valid():
            applicant = form.save()
            return redirect('applicant_detail', applicant.id)
    else:
        form = ApplicantForm()

    return render(request, 'applicants/apply_for_job.html', {'form': form, 'job': job})
```

#### `applicants/forms.py`
```python
from django import forms
from .models import Applicant

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['name', 'email', 'phone', 'resume']
```

#### `applicants/templates/applicants/apply_for_job.html`
{% raw %}
```html
<!-- applicants/apply_for_job.html -->
{% extends 'base.html' %}

{% block title %}Apply for Job{% endblock %}

{% block content %}
  <h1>Apply for Job - {{ job.title }}</h1>
  <form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Submit Application</button>
  </form>
{% endblock %}
```
{% endraw %}

#### `applicants/urls.py`
```python
from django.urls import path
from .views import applicant_list, apply_for_job

urlpatterns = [
    path('', applicant_list, name='applicant_list'),
    path('apply/<int:job_id>/', apply_for_job, name='apply_for_job'),
]
```

### Step 12: Update Navigation in `base.html`

#### `base.html`
{% raw %}
```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Your Project Title{% endblock %}</title>
    <!-- Add your CSS styles or include external stylesheets here -->
</head>

<body>
    <header>
        <h1>Your Project Name</h1>
        <nav>
            <ul>
                <li><a href="{% url 'company_list' %}">Companies</a></li>
                <li><a href="{% url 'job_list' %}">Jobs</a></li>
                <li><a href="{% url 'applicant_list' %}">Applicants</a></li>
                <li><a href="{% url 'job_search' %}">Job Search</a></li>
            </ul>
        </nav>
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <!-- Add footer content or links here -->
    </footer>

    <!-- Add your JavaScript scripts or include external scripts here -->
</body>

</html>
```
{% endraw %}

### Step 13: Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/jobs/search/` to see the job search functionality, and `http://127.0.0.1:8000/applicants/apply/1/` to apply for a job (assuming job with ID 1 exists).

## Solution for 14th qustion

### Step 1: Create Django Project and App

```bash
# Create Django project
django-admin startproject personal_organizer

# Change directory to the project folder
cd personal_organizer

# Create Django app
python manage.py startapp tasks
```

### Step 2: Define Model

#### `tasks/models.py`
```python
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    recurring_frequency = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.title
```

### Step 3: Implement Views and Templates

#### `tasks/views.py`
```python
from django.shortcuts import render
from .models import Task

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})
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
      <li>{{ task.title }} - Due: {{ task.due_date }} - Priority: {{ task.priority }}</li>
    {% endfor %}
  </ul>
{% endblock %}
```
{% endraw %}

### Step 4: Update URLs

#### `personal_organizer/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),
]
```

#### `tasks/urls.py`
```python
from django.urls import path
from .views import task_list

urlpatterns = [
    path('', task_list, name='task_list'),
]
```

### Step 5: Create Base Template

#### `tasks/templates/base.html`
{% raw %}
```html
<!-- tasks/templates/base.html -->
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Your Organizer{% endblock %}</title>
    <!-- Add your CSS styles or include external stylesheets here -->
</head>

<body>
    <header>
        <h1>Your Personal Organizer</h1>
        <nav>
            <ul>
                <li><a href="{% url 'task_list' %}">Task List</a></li>
                <!-- Add more navigation links as needed -->
            </ul>
        </nav>
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <!-- Add footer content or links here -->
    </footer>

    <!-- Add your JavaScript scripts or include external scripts here -->
</body>

</html>
```
{% endraw %}

### Step 6: Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/tasks/` to see the task list.

### Step 7: Add Create and Update Views

#### `tasks/views.py`
```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'tasks/create_task.html', {'form': form})

def update_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/update_task.html', {'form': form, 'task': task})
```

### Step 8: Create Task Forms

#### `tasks/forms.py`
```python
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'due_date', 'priority', 'recurring_frequency']
```

### Step 9: Create Templates for Task Creation and Update

#### `tasks/templates/tasks/create_task.html`
{% raw %}
```html
<!-- tasks/create_task.html -->
{% extends 'base.html' %}

{% block title %}Create Task{% endblock %}

{% block content %}
  <h1>Create Task</h1>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Create Task</button>
  </form>
  <a href="{% url 'task_list' %}">Back to Task List</a>
{% endblock %}
```

#### `tasks/templates/tasks/update_task.html`
```html
<!-- tasks/update_task.html -->
{% extends 'base.html' %}

{% block title %}Update Task{% endblock %}

{% block content %}
  <h1>Update Task - {{ task.title }}</h1>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Update Task</button>
  </form>
  <a href="{% url 'task_list' %}">Back to Task List</a>
{% endblock %}
```
{% endraw %}

### Step 10: Update URLs

#### `tasks/urls.py`
```python
from django.urls import path
from .views import task_list, create_task, update_task

urlpatterns = [
    path('', task_list, name='task_list'),
    path('create/', create_task, name='create_task'),
    path('update/<int:task_id>/', update_task, name='update_task'),
]
```

### Step 11: Update Navigation in `base.html`

#### `tasks/templates/base.html`
{% raw %}
```html
<!-- tasks/templates/base.html -->
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Your Organizer{% endblock %}</title>
    <!-- Add your CSS styles or include external stylesheets here -->
</head>

<body>
    <header>
        <h1>Your Personal Organizer</h1>
        <nav>
            <ul>
                <li><a href="{% url 'task_list' %}">Task List</a></li>
                <li><a href="{% url 'create_task' %}">Create Task</a></li>
                <!-- Add more navigation links as needed -->
            </ul>
        </nav>
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <!-- Add footer content or links here -->
    </footer>

    <!-- Add your JavaScript scripts or include external scripts here -->
</body>

</html>
```
{% endraw %}

### Step 12: Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/tasks/` to see the task list. You can create and update tasks using the provided links.

### Step 13: Add Category Model

#### `tasks/models.py`
```python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
```

### Step 14: Update Task Model to Include Category

#### `tasks/models.py`
```python
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    recurring_frequency = models.CharField(max_length=20, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
```

### Step 15: Add Category Form

#### `tasks/forms.py`
```python
from django import forms
from .models import Task, Category

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'due_date', 'priority', 'recurring_frequency', 'category']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
```

### Step 16: Update Views to Include Category

#### `tasks/views.py`
```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, Category
from .forms import TaskForm, CategoryForm

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'tasks/create_task.html', {'form': form})

def update_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/update_task.html', {'form': form, 'task': task})

def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = CategoryForm()

    return render(request, 'tasks/create_category.html', {'form': form})
```

### Step 17: Update Templates for Category

#### `tasks/templates/tasks/create_category.html`
{% raw %}
```html
<!-- tasks/create_category.html -->
{% extends 'base.html' %}

{% block title %}Create Category{% endblock %}

{% block content %}
  <h1>Create Category</h1>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Create Category</button>
  </form>
  <a href="{% url 'task_list' %}">Back to Task List</a>
{% endblock %}
```

#### `tasks/templates/base.html`
Add a link to create a category in the navigation:

```html
<!-- tasks/templates/base.html -->
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Your Organizer{% endblock %}</title>
    <!-- Add your CSS styles or include external stylesheets here -->
</head>

<body>
    <header>
        <h1>Your Personal Organizer</h1>
        <nav>
            <ul>
                <li><a href="{% url 'task_list' %}">Task List</a></li>
                <li><a href="{% url 'create_task' %}">Create Task</a></li>
                <li><a href="{% url 'create_category' %}">Create Category</a></li>
                <!-- Add more navigation links as needed -->
            </ul>
        </nav>
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <!-- Add footer content or links here -->
    </footer>

    <!-- Add your JavaScript scripts or include external scripts here -->
</body>

</html>
```
{% endraw %}

### Step 18: Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/tasks/` to see the task list. You can now create tasks with categories.

## Solution for 15th qustion

### Step 1: Create Django Project and App

```bash
# Create Django project
django-admin startproject url_shortener

# Change directory to the project folder
cd url_shortener

# Create Django app
python manage.py startapp links
```

### Step 2: Define Model

#### `links/models.py`
```python
from django.db import models

class Link(models.Model):
    original_url = models.URLField()
    shortcode = models.CharField(max_length=10, unique=True)
    clicks = models.PositiveIntegerField(default=0)
    unique_visitors = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.shortcode
```

### Step 3: Implement Views and Templates

#### `links/views.py`
```python
from django.shortcuts import render, redirect, get_object_or_404
from .models import Link
from .forms import ShortenLinkForm

def shorten_link(request):
    if request.method == 'POST':
        form = ShortenLinkForm(request.POST)
        if form.is_valid():
            link = form.save()
            return render(request, 'links/shorten_success.html', {'link': link})
    else:
        form = ShortenLinkForm()

    return render(request, 'links/shorten_link.html', {'form': form})

def redirect_to_original(request, shortcode):
    link = get_object_or_404(Link, shortcode=shortcode)
    link.clicks += 1
    if 'HTTP_REFERER' in request.META:
        link.unique_visitors += 1
    link.save()
    return redirect(link.original_url)

def link_analytics(request, shortcode):
    link = get_object_or_404(Link, shortcode=shortcode)
    return render(request, 'links/link_analytics.html', {'link': link})
```

#### `links/templates/links/shorten_link.html`
{% raw %}
```html
<!-- links/shorten_link.html -->
{% extends 'base.html' %}

{% block title %}Shorten Link{% endblock %}

{% block content %}
  <h1>Shorten Your Link</h1>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Shorten</button>
  </form>
  <a href="{% url 'shorten_link_success' %}">Go to Success Page</a>
{% endblock %}
```

#### `links/templates/links/shorten_success.html`
```html
<!-- links/shorten_success.html -->
{% extends 'base.html' %}

{% block title %}Link Shortened{% endblock %}

{% block content %}
  <h1>Your Link has been Shortened!</h1>
  <p>Shortcode: {{ link.shortcode }}</p>
  <p>Original URL: {{ link.original_url }}</p>
  <p>Clicks: {{ link.clicks }}</p>
  <p>Unique Visitors: {{ link.unique_visitors }}</p>
  <a href="{% url 'shorten_link' %}">Shorten Another Link</a>
{% endblock %}
```

#### `links/templates/links/link_analytics.html`
```html
<!-- links/link_analytics.html -->
{% extends 'base.html' %}

{% block title %}Link Analytics{% endblock %}

{% block content %}
  <h1>Link Analytics</h1>
  <p>Shortcode: {{ link.shortcode }}</p>
  <p>Original URL: {{ link.original_url }}</p>
  <p>Clicks: {{ link.clicks }}</p>
  <p>Unique Visitors: {{ link.unique_visitors }}</p>
  <a href="{% url 'shorten_link' %}">Shorten Another Link</a>
{% endblock %}
```
{% endraw %}

### Step 4: Create Link Form

#### `links/forms.py`
```python
from django import forms
from .models import Link
from django.utils.crypto import get_random_string

class ShortenLinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['original_url']

    def save(self, commit=True):
        shortcode = get_random_string(length=8)
        while Link.objects.filter(shortcode=shortcode).exists():
            shortcode = get_random_string(length=8)
        self.instance.shortcode = shortcode
        return super().save(commit)
```

### Step 5: Update URLs

#### `url_shortener/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('links/', include('links.urls')),
]
```

#### `links/urls.py`
```python
from django.urls import path
from .views import shorten_link, redirect_to_original, link_analytics

urlpatterns = [
    path('shorten/', shorten_link, name='shorten_link'),
    path('shorten/success/', shorten_success, name='shorten_link_success'),
    path('<str:shortcode>/', redirect_to_original, name='redirect_to_original'),
    path('<str:shortcode>/analytics/', link_analytics, name='link_analytics'),
]
```

### Step 6: Create Base Template

#### `links/templates/base.html`
{% raw %}
```html
<!-- links/templates/base.html -->
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}URL Shortener{% endblock %}</title>
    <!-- Add your CSS styles or include external stylesheets here -->
</head>

<body>
    <header

>
        <h1>URL Shortener</h1>
        <nav>
            <ul>
                <li><a href="{% url 'shorten_link' %}">Shorten Link</a></li>
                <!-- Add more navigation links as needed -->
            </ul>
        </nav>
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <!-- Add footer content or links here -->
    </footer>

    <!-- Add your JavaScript scripts or include external scripts here -->
</body>

</html>
```
{% endraw %}

### Step 7: Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/links/shorten/` to shorten a link and explore other functionalities.