from rest_framework import viewsets
from rest_framework.exceptions import ParseError
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from reviews.models import Review, Title

from .permissions import OwnerOrReadOnly
from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Создает
    - пагинированное множество отзывов для просмотра,
    или,
    - один отзыв для просмотра и/или изменений.
    Изменения должны быть доступны автору отзыва и администрации.
    """
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self, *args, **kwargs):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if Review.objects.filter(
                title=title, author=self.request.user).exists():
            raise ParseError
        serializer.save(author=self.request.user, title=title)

    def get_permissions(self):
        if self.action == 'create':
            return (IsAuthenticated(),)
        return (OwnerOrReadOnly(),)
        title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
        if Review.objects.filter(
                title=title,
                author=self.request.user
        ).exists():
            raise ParseError

    def perform_update(self, serializer):
        serializer.save()


class CommentViewSet(viewsets.ModelViewSet):
    """
    Создает
    - пагинированное множество комментов для просмотра,
    или,
    - один коммент для просмотра и/или изменений.
    Изменения должны быть доступны автору коммента и администрации.
    """
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self, *args, **kwargs):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title_id=title_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(
            author=self.request.user, review=review)
