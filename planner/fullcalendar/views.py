from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required  # Декоратор для защиты ваших вьюх авторизацией
from .models import Events


@login_required
def index(request):
    user = request.user
    all_events = Events.objects.filter(user=user)
    context = {
        "events": all_events,
    }
    return render(request, 'fullcalendar/index.html', context)


@login_required
def all_events(request):
    user = request.user
    all_events = Events.objects.filter(user=user)
    out = []
    for event in all_events:
        out.append({
            'title': event.name,
            'id': event.id,
            'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),
            'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"),
            'category': event.category,
        })

    return JsonResponse(out, safe=False)


@login_required
def add_event(request):
    user = request.user
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    category = request.GET.get("category", None)  # Добавьте получение категории
    event = Events(user=user, name=str(title), start=start, end=end, category=category)  # Учтите категорию
    event.save()
    data = {}
    return JsonResponse(data)


@login_required
def update(request):
    user = request.user
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id, user=user)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)


@login_required
def remove(request):
    user = request.user
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id, user=user)
    event.delete()
    data = {}
    return JsonResponse(data)
