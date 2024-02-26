# account/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Category, Note
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_GET

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

