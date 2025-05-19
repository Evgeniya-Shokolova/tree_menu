from django.db import models


class MenuItem(models.Model):
    """
    Пункт меню, поддерживающий древовидную структуру.

    Атрибуты:
        name: Уникальное имя меню,
        url: URL (может быть пустым)
        parent: Ссылка на родительский пункт меню (для иерархии),
        named_url: URL из urls.py,
    """
    name = models.CharField('Название', max_length=100, unique=True)
    url = models.CharField('URL', max_length=255, blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True,
                               related_name='children',
                               on_delete=models.CASCADE,
                               verbose_name='Родительский пункт')
    named_url = models.CharField('Named URL', max_length=200, blank=True)

    class Meta:
        """Сортировка по id"""
        ordering = ['id']

    def __str__(self):
        return self.name
