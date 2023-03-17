from django.views.generic import TemplateView,FormView
from django.shortcuts import render
from .AI import gpt_chat

class HomePage(TemplateView):
  template_name = "index.html"


def chat_view(request):

  if request.method =="POST":
    prompt = request.POST["prompt"] 
    res = gpt_chat(prompt)  if str(prompt) != '' else ''
    return render(request, "index.html",{"res":res})

  return render(request, "index.html")
  