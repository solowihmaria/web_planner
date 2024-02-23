# account/models.py
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    # Связь с пользователем, который создал категорию
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Название категории
    name = models.CharField(max_length=255)

    def __str__(self):
        # Возвращает строковое представление объекта категории (используется в админке Django и др.)
        return self.name

class Note(models.Model):
    # Связь с пользователем, который создал заметку
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Связь с категорией, к которой привязана заметка
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # Текст заметки
    text = models.TextField()
    # Новое поле для отслеживания состояния заметки
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        # Возвращает строковое представление объекта заметки (используется в админке Django и др.)
        return f"{self.category.name} - {self.text[:50]}..."
