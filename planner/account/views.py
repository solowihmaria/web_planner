# account/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Category, Note, Events
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta



def profile(request):
    return render(request, 'account/profile.html')

def notes(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'account/notes.html', {'categories': categories})



@csrf_exempt
def add_category(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        category = Category(user=request.user, name=data['name'])
        category.save()
        response_data = {'name': category.name}
        return JsonResponse(response_data)

@csrf_exempt
def add_note(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        category_id = data.get('category_id')
        category = Category.objects.get(id=category_id)
        note = Note(user=request.user, category=category, text=data['text'])
        note.save()
        response_data = {'text': note.text}
        return JsonResponse(response_data)

@csrf_exempt
def update_note(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        note_id = data.get('note_id')
        note = Note.objects.get(id=note_id)
        note.is_completed = data.get('is_completed', False)
        note.save()
        response_data = {'note_id': note.id, 'is_completed': note.is_completed}
        return JsonResponse(response_data)


@require_POST
def edit_category(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        category_id = data.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        category.name = data['new_name']
        category.save()
        response_data = {'id': category.id, 'name': category.name}
        return JsonResponse(response_data)

@require_POST
def delete_category(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        category_id = data.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        response_data = {'success': True}
        return JsonResponse(response_data)

@csrf_exempt
@require_POST
def edit_note(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        note_id = data.get('note_id')
        note = get_object_or_404(Note, id=note_id)
        note.text = data['new_text']
        note.save()
        response_data = {'id': note.id, 'text': note.text}
        return JsonResponse(response_data)

@csrf_exempt
@require_POST
def delete_note(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        note_id = data.get('note_id')
        note = get_object_or_404(Note, id=note_id)
        note.delete()
        response_data = {'success': True}
        return JsonResponse(response_data)


@require_GET
def get_completion_data(request):
    # Получаем текущего пользователя
    user = request.user
    # Подсчитываем количество выполненных задач пользователя
    completed_tasks = Note.objects.filter(user=user, is_completed=True).count()
    # Подсчитываем общее количество задач пользователя
    total_tasks = Note.objects.filter(user=user).count()
    # Отправляем данные в формате JSON
    return JsonResponse({'completed': completed_tasks, 'total': total_tasks})


@login_required
def calendar(request):
    user = request.user
    all_events = Events.objects.filter(user=user)
    context = {
        "events": all_events,
    }
    return render(request, 'fullcalendar/calendar.html', context)


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


def get_notifications(request):
    # Получаем текущего пользователя
    user = request.user
    # Получаем ближайшие события за последние 3 дня
    today = datetime.now()
    end_date = today + timedelta(days=3)
    events = Events.objects.filter(user=user, start__range=(today, end_date)).order_by('start')
    # Создаем список уведомлений для передачи в шаблон
    notifications = [{'name': event.name, 'start': event.start.strftime('%Y-%m-%d')} for event in events]
    # Возвращаем JSON-ответ с уведомлениями
    return JsonResponse({'notifications': notifications})
