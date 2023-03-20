from django.shortcuts import render , redirect

from .models import ChatHistory
from .AI import gpt_chat


def chat_view(request):

    if request.method =="POST":
        prompt = request.POST["prompt"]
        try:
          res = gpt_chat(prompt)  if str(prompt) != '' else ''
        except:
          raise "Error in gpt_chat()"
        ChatHistory.objects.create(user=request.user ,answer=res,question=prompt)
        return render(request, "index.html",{"res":res})
    if request.user.is_authenticated:
        return render(request, "index.html")
    return redirect("login")
