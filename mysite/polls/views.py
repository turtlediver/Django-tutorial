from django.shortcuts import get_object_or_404, render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

#to raise a 404 error
from django.http import Http404

from django.urls import reverse
from django.views import generic

from .models import Question, Choice

"""
def index(request):
    return HttpResponse("Hello world. You're at the polls index.")
"""

"""
    IndexView is a ListView, a generic view in Django.
    ListView is a page representing a list of objects.
     /polls/ page displays latest 5 poll questions in system,
    comma separated and according to publication date.
"""

class IndexView(generic.ListView):

    #ListView uses the default template name: <app name>/<model name>_list.html
    #   - use template_name to override
    template_name = 'polls/index.html'

    #ListView uses default context variable name 'question_list'.
    #  - use context_object_name to override.
    #  - we use 'latest_question_list' since that is the context variable name 
    #       in polls/index.html template
    #  - our context contains the 5 latest questions, returned by get_queryset
    context_object_name = 'latest_question_list'

    """
    Get list of items for this view.
    """
    def get_queryset(self):
        """Return last 5 published questions."""
        return Question.objects.order_by('-pub_date')[:5]

"""
Uses Django's generic view DetailView to display a detail page
for a particular type of object (object = Question here).
"""
class DetailView(generic.DetailView):

    #each generic view needs to know which model it will be acting upon.
    # - use model attribute to set this
    model = Question
    #DetailView uses '<app name>/<model name>_detail.html' as default template.
    #  - use template_name attribute to override
    template_name = 'polls/detail.html'

"""
Uses Django's generic view DetailView to display a detail page
for a particular type of object (object = Question here).
"""
class ResultsView(generic.DetailView):

    #each generic view needs to know which model it will be acting upon.
    # - use model attribute to set this
    model = Question
    template_name = 'polls/results.html'

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

    