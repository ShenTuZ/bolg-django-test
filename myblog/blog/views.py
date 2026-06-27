from django.shortcuts import redirect


def index(request):
    return redirect("http://127.0.0.1:5173/")
