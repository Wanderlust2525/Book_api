from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django_resized import ResizedImageField

from account.services import User




class TimeStampAbstractModel(models.Model):
    created_at = models.DateTimeField('дата добавление', auto_now_add=True)
    updated_at = models.DateTimeField('дата изменения', auto_now=True)

    class Meta:
        abstract = True

class Category(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(verbose_name='название', max_length=100, unique=True)

    def __str__(self):
        return f'{self.name}'


class Tag(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    name = models.CharField(verbose_name='название', max_length=100, unique=True)

    def __str__(self):
        return f'{self.id}. {self.name}'

class Genre(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    name = models.CharField(verbose_name='название', max_length=100, unique=True)

    def __str__(self):
        return f'{self.id}. {self.name}'
    

def example_validation(value):
    if float(value) == 3.3:
        raise ValidationError('Example error')

    return value


class Book(TimeStampAbstractModel):

    ORDER = 'order'
    IN_STOCK = 'in_stock'
    PICK_UP = 'pick_up'

    RECEIVE_TYPE = (
        (ORDER, 'На заказ'),
        (IN_STOCK, 'В наличии'),
        (PICK_UP, 'Самовывоз')
    )

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ('-created_at',)

    name = models.CharField(verbose_name='Название', max_length=100)
    # file  = models.FileField(verbose_name='PDF файлы', upload_to='books_files/',  blank =True ,null=True)
    description = models.CharField(verbose_name='Описание', max_length=300)
    content = models.TextField(verbose_name='Контент', )
    date = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)
    last_updated = models.DateTimeField(verbose_name='Дата изменении', auto_now=True)
    author_book = models.CharField(verbose_name='Автор книги',max_length=100)
    user = models.ForeignKey(User, models.CASCADE, verbose_name='пользователь')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='books', null=True,
                                 verbose_name='категория')
    tags = models.ManyToManyField(Tag, related_name='books', verbose_name='Теги')
    genres = models.ManyToManyField(Genre, related_name='books', verbose_name='Жанры')
    views = models.PositiveIntegerField(verbose_name='Просмотры', default=0,
                                        validators=[])
    rating = models.DecimalField('рейтинг', max_digits=2, decimal_places=1,
                                         validators=[MinValueValidator(1), MaxValueValidator(5), example_validation])
    is_published = models.BooleanField(verbose_name='публичный', default=True)

    @property
    def image(self):
        if self.images.first():
            return self.images.first().image
        return None

    def __str__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.id}) {self.name}'
    


class BookImage(TimeStampAbstractModel):
    class Meta:
            verbose_name = 'изображение товара'
            verbose_name_plural = 'изображении товаров'
            ordering = ('-created_at',)

    books = models.ForeignKey('book.Book', models.CASCADE, related_name='images', verbose_name='Книга')
    image = ResizedImageField('изображение', upload_to='book_images/', quality=90, force_format='WEBP')

    def __str__(self):
        return f'{self.books.name}'

# Create your models here.
