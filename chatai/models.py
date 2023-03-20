from django.db import models
from django.contrib.auth import get_user_model

import datetime



class ChatHistory(models.Model):
  user = models.ForeignKey(  get_user_model(), on_delete=models.CASCADE)
  time = models.DateTimeField(auto_now_add=True )
  question = models.TextField()
  answer = models.TextField()
  Date = models.DateTimeField(default= datetime.datetime.now,null=True)

  def __str__(self):
    return "("+self.user.get_username()+")" + self.question[:20]
