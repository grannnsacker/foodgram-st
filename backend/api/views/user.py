from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from api.decorators import is_authenticated_only
from api.text import ERROR_ALREADY_SUBS, ERROR_CANT_SUBS_ITSELF, ERROR_DONT_SUBS
from grannsacker_foodgram.models import Subscription
from api.serializers import (
    UserSerializer,
    UserCreateSerializer,
    SubscriptionsSerializer,
    UpdatePasswordSerializer,
    ChangeAvatarSerializer,
)

User = get_user_model()


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 100


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action in [
            'me',
            'avatar',
            'set_password',
            'delete_avatar',
            'subscriptions',
            'subscribe',
            'unsubscribe',
        ]:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self):
        serializers = {
            'create': UserCreateSerializer,
            'set_password': UpdatePasswordSerializer,
            'avatar': ChangeAvatarSerializer,
            'subscriptions': SubscriptionsSerializer,
        }
        return serializers.get(self.action, UserSerializer)

    @action(detail=True, methods=['post', 'delete'])
    @is_authenticated_only
    def subscribe(self, request, id=None):
        user = request.user
        author = self.get_object()

        if request.method == 'POST':
            if user == author:
                return Response(
                    {'error': ERROR_CANT_SUBS_ITSELF},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            subscription, created = Subscription.objects.get_or_create(
                user=user, author=author
            )

            if not created:
                return Response(
                    {'error': ERROR_ALREADY_SUBS},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = SubscriptionsSerializer(author, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        subscription = Subscription.objects.filter(user=user, author=author).first()

        if not subscription:
            return Response(
                {'error': ERROR_DONT_SUBS},
                status=status.HTTP_400_BAD_REQUEST,
            )

        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
    )
    @is_authenticated_only
    def subscriptions(self, request):
        user = request.user
        subscriptions = User.objects.filter(following__user=user).order_by('id')

        page = self.paginate_queryset(subscriptions)
        if page is not None:
            serializer = SubscriptionsSerializer(
                page, many=True, context={'request': request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = SubscriptionsSerializer(
            subscriptions, many=True, context={'request': request}
        )
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['put', 'delete'],
        url_path='me/avatar',
    )
    @is_authenticated_only
    def avatar(self, request, id=None):
        if request.method == 'PUT':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=False
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        if request.method == 'DELETE':
            request.user.avatar.delete(save=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubscriptionsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user).order_by('id')
