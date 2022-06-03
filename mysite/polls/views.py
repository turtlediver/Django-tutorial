from django.shortcuts import get_object_or_404, render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

#to raise a 404 error
from django.http import Http404

from django.urls import reverse
from .models import Question, Choice

"""
def index(request):
    return HttpResponse("Hello world. You're at the polls index.")
"""

"""
    index displays latest 5 poll questions in system,
    comma separated and according to publication date
"""
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    
    #use template in ./templates/polls
    #template = loader.get_template('polls/index.html')
    
    context = {
        'latest_question_list': latest_question_list
    }

    #return HttpResponse(template.render(context, request))
    #render() is a shortcut for above line ^ (and loader.get_template() above)
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    """
    try:
        question = Question.objects.get(pk=question_id)
    
    except Question.DoesNotExist:
        # - Here, Django catches the Http404 exception and returns the 
        # standard error page for the application, and HTTP error code 404.
        # - we can make an HTML template 404.html, will be used when DEBUG=False 
        raise Http404("Question does not exist")
    """
    #Can use get_object_or_404 as shortcut for above^.
    # - tries to an object, raises Http404 is it DNE
    question = get_object_or_404(Question, pk=question_id)

    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question':question})

#handle submitted data and do something with it
def vote(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    
    except (KeyError, Choice.DoesNotExist):
        #redisplay question voting form
        return render(request, 'polls/detail.html', { 
            'question': question, 
            'error_message': "You didn't select a choice.", 
        })
    
    else:
        selected_choice.votes += 1
        selected_choice.save()
        #Always return an HttpResponseRedirect after successfully
        #  dealing with POST data. This prevents data from being
        # posted twice if user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

    return HttpResponse("You're voting on question %s." %question_id)