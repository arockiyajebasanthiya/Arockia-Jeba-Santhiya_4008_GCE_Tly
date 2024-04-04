from django.shortcuts import render
from polls.models import Question

def index(request):
    latest_question_list = Question.objects.all()
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'pages/index.html', context)
