from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import generic
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from polls.models import Question, Choice


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#
#     # template = loader.get_template('polls/index.html')
#     # return HttpResponse(template.render(context, request))
#
#     """这个写法是上述写法的简写"""
#     return render(request, 'polls/index.html', context)
#
#
# # 注意函数的参数
# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exits")
#
#     """这个写法是上述写法的简写"""
#     # question = get_object_or_404(Question, pk=question_id)
#     context = {
#         'question': question
#     }
#     return render(request, 'polls/detail.html', context=context)
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     context = {
#         'question': question,
#     }
#     return render(request, 'polls/results.html', context=context)


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


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'