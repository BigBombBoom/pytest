from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from django.views import generic
from .models import Choice, Question,VoteRecord,VoteRecord_only
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin



class IndexView(LoginRequiredMixin,generic.ListView):
    login_url = '/login/'
    template_name = "vote/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:10]


class DetailView(LoginRequiredMixin,generic.DetailView):
    login_url = '/login/'
    model = Question
    template_name = "vote/detail.html"


class ResultsView(LoginRequiredMixin,generic.DetailView):
    login_url = '/login/'
    model = Question
    template_name = "vote/results.html"

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request,"vote/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        if question.is_only:
            vote_record_exists = VoteRecord_only.objects.filter(user=request.user, question=question).exists()
            if vote_record_exists:
                return render(request,"vote/detail.html",
            {
                "question": question,
                "error_message": "You have already voted.",
            },
        )
            else:
                VoteRecord_only.objects.create(user=request.user, question=question, choice=selected_choice)
        
        VoteRecord.objects.create(user=request.user, question=question, choice=selected_choice)
        
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("vote:results", args=(question.id,)))

@login_required
def create(request):
    if request.method == 'POST':
        data = request.POST
        question_new=data.get("question")
        if Question.objects.filter(question_text=question_new).exists():
            
            return render(
                request,
                "vote/create.html",
                {
                    "error_message": "The question is already exist.",
                },
            )
        else:
            choices = [value for key, value in data.items() if key.startswith("option-")]
            if len(choices) < 2:
                return render(
                    request,
                    "vote/create.html",
                    {
                        "error_message": "At least two choices are required.",
                    },
                )
            else:
                is_only = 'is-only' in request.POST
                question=Question(question_text=question_new,pub_date=datetime.now(),is_only=is_only)
                question.save()
                for choice_new in choices:
                    choice = Choice(question=question, choice_text=choice_new, votes=0)
                    choice.save()
                
                return redirect("/vote/")
    else:
        return render(request,"vote/create.html")

