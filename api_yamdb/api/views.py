"""Представления приложения api."""

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .mixins import CreateListDestroyMixinViewset
from .permissions import (AdminOnly, IsAdminOrIsSelf, IsAdminOrReadOnly,
                          IsAuthorPatch, IsModeratorAuthorDelete)
from .serializers import (CategorySerializer, CommentSerializer,
                          ConfirmUserSerializer, CreateUserSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleGetSerializer, TitlePostSerializer,
                          UserSerializer)
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from reviews.models import Category, Genre, Review, Title
from users.models import User


class CreateUser(APIView):
    """Представление для создания пользователя."""

    def post(self, request):
        """Метод, создающий пользователя с помощью сериализатора."""
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_mail(
            'confirmation_code',
            str(user.confirmation_code),
            DEFAULT_FROM_EMAIL,
            [serializer.validated_data['email']],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConfirmUser(APIView):
    """Представление для авторизации пользователя."""

    def post(self, request):
        """Метод, авторизирующий пользователя с помощью сериализатора."""
        serializer = ConfirmUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        username = serializer.validated_data.get('username')
        if User.objects.filter(
            username=username, confirmation_code=confirmation_code
        ).exists():
            user = get_object_or_404(
                User, username=username,
                confirmation_code=confirmation_code
            )
            refresh = RefreshToken.for_user(user)
            send_mail(
                'your_token',
                str(str(refresh.access_token)),
                DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return Response(
                {"token": str(refresh.access_token)},
                status=status.HTTP_200_OK
            )
        if User.objects.filter(username=username).exists():
            return Response(
                'Код подтверждения не верный!',
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            'Не найден такой username!',
            status=status.HTTP_404_NOT_FOUND
        )


class UserViewSet(viewsets.ModelViewSet):
    """Представление для обработки объектов User."""

    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, AdminOnly)
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(methods=['get', 'patch'], detail=False,
            permission_classes=(IsAuthenticated, IsAdminOrIsSelf),
            url_path='me', url_name='me')
    def me_detail_patch(self, request):
        """Метод, обрабатывающий уровни доступа."""
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            request.user, data=request.data, partial=True
        )
        role = request.user.role
        serializer.is_valid(raise_exception=True)
        serializer.save(role=role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    """Представление для обработки объектов Title."""

    queryset = Title.objects.annotate(
        rating=(Avg('reviews__score')),
    ).order_by('name')
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Метод, обрабатывающий объекты Title."""
        if self.action in ('list', 'retrieve',):
            return TitleGetSerializer
        return TitlePostSerializer


class GenreViewSet(CreateListDestroyMixinViewset):
    """Представление для обработки объектов Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class CategoryViewSet(CreateListDestroyMixinViewset):
    """Представление для обработки объектов Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление для обработки объектов Review."""

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorPatch,
        IsModeratorAuthorDelete,
    )
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """Метод, получающий объекты Review."""
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        """Метод, создающий объекты Review."""
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для обработки объектов Comment."""

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorPatch,
        IsModeratorAuthorDelete,
    )
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """Метод, получающий объекты Comment."""
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        """Метод, создающий объекты Comment."""
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
