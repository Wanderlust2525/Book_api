from django_filters import rest_framework as filterset

from book.models import Book, Category


class BookFilter(filterset.FilterSet):

    categories = filterset.ModelMultipleChoiceFilter(queryset=Category.objects.all(), field_name='category')
    receive_types = filterset.MultipleChoiceFilter(choices=Book.RECEIVE_TYPE, field_name='receive_type')

    class Meta:
        model = Book
        fields = [
            'tags',
            'genres',
            'user',
            'is_published',
            'rating',
            'views'
        ]