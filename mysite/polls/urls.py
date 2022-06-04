from django.urls import path

from . import views

#set the application namespace
app_name = 'polls'

urlpatterns = [
    #ex: /polls/
    # - as_view() returns a callable function.
    #    - this function creates an instance of the view's class, 
    #          calls setup() to initialize attributes, then calls dispatch()
    path('', views.IndexView.as_view(), name='index'),
    #ex: /polls/5/
    # - DetailView generic view expects primary key value captured form URL
    #     to be called 'pk'
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    #ex: /polls/5/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    #ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),

]