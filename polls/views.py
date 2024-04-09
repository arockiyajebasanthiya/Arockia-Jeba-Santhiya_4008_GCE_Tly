from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice
from django import forms

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
            question = form.save()

            # Get choices from the form
            choices = [form.cleaned_data[f'choice{i}'] for i in range(1, 4)]

            # Create choices for the question
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

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all()
    return render(request, 'polls/detail.html', {'question': question, 'choices': choices})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

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
