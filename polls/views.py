from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import F
from django.views.decorators.http import require_http_methods

# Create your views here.
from polls.models import Question, Choice
from django.template import loader
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(generic.ListView):
    model = Question
    template_name = 'index.html'
    context_object_name = 'recent_questions'

    def get_queryset(self):
        return Question.objects.filter(text__icontains=self.request.GET.get('search', '')).order_by('-pub_date')[:5]


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'details.html'
    context_object_name = 'q'


class ResultView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'result.html'
    context_object_name = 'q'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_votes = context[self.context_object_name].choice_set.aggregate(Sum('votes'))['votes__sum']
        ordered = context[self.context_object_name].choice_set.order_by('-votes')
        winner = None
        if len(ordered) > 0 and (len(ordered) == 1 or ordered[0].votes > ordered[1].votes):
            winner = ordered[0]
        context['winner'] = winner
        context['total_votes'] = total_votes
        return context


#
# def index(request):
#     search_param = request.GET.get('search', '')
#     latest_questions = Question.objects.filter(text__contains=search_param).order_by('-pub_date')[:5]
#     temp = loader.get_template('index.html')
#     context = {'recent_questions': latest_questions}
#     return HttpResponse(temp.render(context, request))
#
#
# def detail(request, question_id):
#     temp = loader.get_template('details.html')
#     q = get_object_or_404(Question, pk=question_id)
#     choices = Choice.objects.filter(question_id=question_id)
#     context = {'q': q, 'choices': choices}
#     return HttpResponse(temp.render(context, request))
#
#
# def result(request, question_id):
#     q = get_object_or_404(Question, pk=question_id)
#     choices = Choice.objects.filter(question_id=question_id)
#     total_votes = choices.aggregate(Sum('votes'))['votes__sum']
#     ordered = choices.order_by('-votes')
#     winner = None
#     if len(ordered) > 0 and (len(ordered) == 1 or ordered[0].votes > ordered[1].votes):
#         winner = ordered[0]
#
#     template = loader.get_template('result.html')
#     context = {'total_votes': total_votes, 'winner': winner, 'q': q, 'choices': choices}
#     return HttpResponse(template.render(context, request))
#

@require_http_methods(["POST"])
@login_required(None, 'REDIRECT_FIELD_NAME')
def vote(request, question_id):
    if request.session.get(str(question_id)) is not None:
        return HttpResponse(f"You already voted for option {request.session.get(str(question_id))}!")
    # if request.method != "POST":
    #    raise Http404('This page must be accessed by voting!')
    choice_text = None

    q = get_object_or_404(Question, pk=question_id)
    if 'choice' in request.POST:
        choice_id = int(request.POST['choice'])
        choice_text = get_object_or_404(Choice, pk=choice_id).text
        q.choice_set.filter(id=choice_id).update(votes=F('votes') + 1)
        request.session[str(question_id)] = choice_id
    context = {'choice_text': choice_text, 'q': q}
    template = loader.get_template('vote.html')
    return HttpResponse(template.render(context, request))


def login_form(request):
    return render(request, 'login.html')


@require_http_methods(["POST"])
def do_login(request):
    if request.POST['username'] is None or request.POST['password'] is None or request.POST['username'] == '' or \
            request.POST['password'] == '':
        return HttpResponse('Please Enter username and password')
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        return render(request, 'login_response.html', {'username': user.get_username()})
    else:
        return render(request, 'login_response.html')


def log_out(request):
    logout(request)
    return redirect(reverse('login_form'))
