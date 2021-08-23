from django.contrib.auth import get_user_model
from django.db import models

CHOICES = (
    (1, '*'),
    (2, '**'),
    (3, '***'),
    (4, '****'),
    (5, '*****'),
    (6, '******'),
    (7, '*******'),
    (8, '********'),
    (9, '*********'),
    (10, '**********'),
)

User = get_user_model()


class Category(models.Model):

    name = models.CharField(
        max_length=256,
        help_text='Введите наименование категории'
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        help_text=('Укажите адрес для страницы задачи. Используйте только '
                   'латиницу, цифры, дефисы и знаки подчёркивания')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('-id', )

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        help_text='Введите наименование жанра'
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        help_text=('Укажите адрес для страницы задачи. Используйте только '
                   'латиницу, цифры, дефисы и знаки подчёркивания')
    )

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'
        ordering = ('-id', )

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    name = models.CharField(
        default='новое произведение',
        max_length=256,
        help_text='Укажите название произведения'
    )
    year = models.PositiveSmallIntegerField(
        help_text='Укажите год создания'
    )
    description = models.TextField(
        blank=True,
        help_text='Добавьте описание для произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
        help_text=('Выберите один или несколько жанров, '
                   'для выбора используете slug жанра')
    )
    category = models.ForeignKey(
        Category,
        on_delete=None,
        related_name='titles',
        help_text=('Выберите одну категорию'
                   'для выбора используйте slug категории')
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'
        ordering = ('-id', )

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        'Текст отзыва',
        default='ваша статья',
        blank=False,
        help_text=('Отзыв не может быть пустым.'
                   'Не забывайте про абзацы.'
                   )
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    score = models.PositiveSmallIntegerField(
        'Рейтинг',
        default=1,
        choices=CHOICES,
        help_text='Укажите или выберите значение от 1 до 10.'
    )

    class Meta:
        """
        Юзер может оставить единственный отзыв на произведение.
        """
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ('-pub_date', )
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(
        'Текст коммента',
        default='ваш комментарий',
        blank=False,
        help_text=('Коммент не может быть пустым.'
                   'Не забывайте про абзацы.'
                   )
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ('-pub_date', )

    def __str__(self):
        return self.text[:50]
