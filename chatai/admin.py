from django.contrib import admin

from .models import ChatHistory

class ChatHistoryAdmin(admin.ModelAdmin):
  model = ChatHistory
  list_display = ("user" ,"question","time")
  fieldsets = (
        (None, {"fields": ("user" ,"Date","question","answer")}),
    )
  add_fieldsets = (
        (None, {"fields": ("user" , "Date","question","answer")}),
    )

admin.site.register(ChatHistory,ChatHistoryAdmin)

