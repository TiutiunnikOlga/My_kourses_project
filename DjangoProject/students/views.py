from django.shortcuts import render


def about(request, item_id):
    return render(request, 'students/about.html')
