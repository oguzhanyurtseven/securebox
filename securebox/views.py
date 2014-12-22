# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from securebox.forms import new_user_form, send_mail_form, decrypt_page_input_form

from securebox.hashids import *
from securebox.mailgun import mailgun
from securebox.models import message


__author__ = 'oguzhan'



def home_page(request):

    return render_to_response('main_page.html', locals(), context_instance=RequestContext(request))

def index(request):
    salt_key = ''
    try:
        user = request.user
    except:
        return HttpResponseRedirect('/404')
    form = send_mail_form(initial={'user': user})
    if request.method == 'POST':
        form = send_mail_form(request.POST, request.FILES)
        if form.is_valid():
            try:
                to_email = request.POST.get('to_email')
                title = request.POST.get('title')
                salt = request.POST.get('salt')
                message_text = request.POST.get('message')
                attachment = request.FILES.get('file')

                message_obj = message(user=request.user, title=title, message='', to_email=to_email, salt=salt, file=attachment)
                message_obj.save()

                hashids = Hashids(salt=salt)
                hashid = hashids.encrypt(message_obj.id)
                text = message_text + ' hashid:' + str(hashid)
                mailgun_operator = mailgun()
                mailgun_operator.send_mail(user.email, to_email, title, str(hashid))
                salt_key = salt
            except:
                return HttpResponseRedirect('/404')
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))


def new_user(request):
    form = new_user_form
    if request.method == 'POST':
        form = new_user_form(request.POST)
        if form.is_valid():
            try:
                username = request.POST.get('username')
                password = request.POST.get('password')
                email = request.POST.get('email')
                member_user_auth = User.objects.create_user(username, email, password)
                member_user_auth.save()
                return HttpResponseRedirect('/accounts/login/')
            except Exception as e:
                print e
    return render_to_response('new_user.html', {'form': form}, context_instance=RequestContext(request))

# @login_required
# def send_mail(request):
#     try:
#         user = request.user
#     except:
#         return HttpResponseRedirect('/404')
#     form = send_mail_form(initial={'user': user})
#     if request.method == 'POST':
#         form = send_mail_form(request.POST, request.FILES)
#         if form.is_valid():
#             try:
#                 to_email = request.POST.get('to_email')
#                 title = request.POST.get('title')
#                 salt = request.POST.get('salt')
#                 attachment = request.FILES.get('file')
#
#                 message_obj = message(user=request.user, title=title, message='', to_email=to_email, salt=salt, file=attachment)
#                 message_obj.save()
#
#                 hashids = Hashids(salt=salt)
#                 hashid = hashids.encrypt(message_obj.id)
#                 mailgun_operator = mailgun()
#                 mailgun_operator.send_mail(user.email, to_email, title, str(hashid))
#                 return HttpResponseRedirect('/public_key_page/' + salt)
#             except:
#                 return HttpResponseRedirect('/404')
#     return render_to_response('send_message.html', locals(), context_instance=RequestContext(request))

# @login_required
# def public_key_page(request, salt):
#     salt = salt
#     return render_to_response('public_key_page.html', locals(), context_instance=RequestContext(request))

@login_required
def decrypt_page_input(request):
    link = ''
    form = decrypt_page_input_form()
    if request.method == 'POST':
        form = decrypt_page_input_form(request.POST)
        if form.is_valid():
            mess = request.POST.get('message')
            salt = request.POST.get('salt')
            hashids = Hashids(salt=salt)
            hashid = hashids.decrypt(mess)
            id = ''
            for i in hashid:
                try:
                    id = id + str(int(i))
                except:
                    pass
            print id
            file_obj = message.objects.filter(id=id)[0]
            link = 'http://127.0.0.1:8000' + file_obj.file.url

    return render_to_response('decrypt_page_input.html', locals(), context_instance=RequestContext(request))

def my_uploads(request):
    messages = message.objects.all()
    return render_to_response('my_uploads.html', locals())

def delete_file(request, message_id):
    message_item = message.objects.filter(id=message_id)[0]
    message_item.delete()
    return HttpResponseRedirect('/my_uploads')

