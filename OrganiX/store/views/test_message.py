from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse


class Message(View):
    def get(self, request):
        return render(request, "test_message.html")

    def post(self, request):
        infobtn = request.POST.get("infobtn")
        if infobtn == "error":
            messages.error(request=request, message="Error!")
        elif infobtn == "warning":
            messages.warning(request=request, message="Warning!")
        elif infobtn == "info":
            messages.info(request=request, message="Info!")
        elif infobtn == "success":
            messages.success(request=request, message="Success!")
        elif infobtn == "debug":
            messages.debug(request=request, message="Debug!")
        return HttpResponse("hehe")
    
def get_message_list(request):
    message_list = []
    for message in messages.get_messages(request):
        message_list.append({
            'level': message.level_tag,  # success, error, warning, info
            'message': message.message
        })
    return message_list
