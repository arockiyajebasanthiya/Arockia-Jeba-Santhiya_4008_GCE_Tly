from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice
from .forms import UserRegisterForm
from django import forms  # Add this import
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    class QuestionForm(forms.ModelForm):
        choice1 = forms.CharField(label='Choice 1')
        choice2 = forms.CharField(label='Choice 2')
        choice3 = forms.CharField(label='Choice 3')

        class Meta:
            model = Question
            fields = ['question_text']

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user  # Assign the currently authenticated user
            question.save()

            choices = [form.cleaned_data[f'choice{i}'] for i in range(1, 4)]
            for choice_text in choices:
                Choice.objects.create(question=question, choice_text=choice_text)

            return redirect('polls:index')
    else:
        form = QuestionForm()

    context = {
        'latest_question_list': latest_question_list,
        'form': form
    }
    return render(request, 'polls/index.html', context)

@login_required
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all()
    return render(request, 'polls/detail.html', {'question': question, 'choices': choices})

@login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('polls:index')  # Redirect to the index page after successful login
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the form data to create a new user
            login(request, user)  # Log in the newly registered user
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('polls:index')  # Redirect to the index page after successful registration
        else:
            # If the form is invalid, display form errors
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def profile(request):
    return redirect('/')
