from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, Message
from .forms import UserForm, MessageForm, MessageEditForm


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            request.session['user_id'] = user.id
            return redirect('chat')
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})


def chat(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('register')

    user = User.objects.get(id=user_id)

    #2
    date_filter = request.GET.get('date')
    messages_qs = Message.objects.filter(is_deleted=False).order_by('-timestamp')

    if date_filter:
        messages_qs = messages_qs.filter(timestamp__date=date_filter)

    if request.method == "POST":

        
        if 'edit_message_id' in request.POST:
            message = get_object_or_404(Message, id=request.POST['edit_message_id'])
            if message.user == user:
                form = MessageEditForm(request.POST, instance=message)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Сообщение успешно отредактировано")

        #3
        elif 'delete_message_id' in request.POST:
            message = get_object_or_404(Message, id=request.POST['delete_message_id'])
            if message.user == user:
                message.is_deleted = True
                message.save()
                messages.success(request, "Сообщение перемещено в архив")

        
        else:
            form = MessageForm(request.POST)
            if form.is_valid():
                msg = form.save(commit=False)
                msg.user = user
                msg.save()
                messages.success(request, "Сообщение отправлено")

        return redirect('chat')

    return render(request, 'chat.html', {
        'messages': messages_qs,
        'form': MessageForm(),
        'user': user
    })


def archive(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)

    archived_messages = Message.objects.filter(user=user, is_deleted=True)

    if request.method == "POST":
        msg = get_object_or_404(Message, id=request.POST['restore_id'])
        msg.is_deleted = False
        msg.save()
        messages.success(request, "Сообщение восстановлено")
        return redirect('archive')

    return render(request, 'archive.html', {'messages': archived_messages})
