from django.shortcuts import render, redirect
from .email_resender import test_send_message, send_all
from threading import Thread
import pyautogui
import requests


def index(request):
    if request.method == 'POST':
        email = request.POST.get('inputEmail','no email')
        if email != 'no email':
            eid = test_send_message(email)
            return render(request, 'confirm.html', context={'eid': eid})
        else:
            return render(request, 'error.html')
    return render(request, 'index.html', context={})


def confirm(request):
    if request.method == 'POST':
        eid = request.POST.get('eid', 'no eid')
        if eid != 'no eid':
            Thread(target=send_all, args=(eid,)).start()
        return redirect('index')
    return redirect('index')


def previous(request):
    print('previous')
    Thread(target=requests.get, args=('http://192.168.68.105/previous',)).start()
    return redirect('clicker')


def next(request):
    print('next')
    Thread(target=requests.get, args=('http://192.168.68.105/next',)).start()
    return redirect('clicker')


def clicker(request):
    return render(request, 'clicker.html')