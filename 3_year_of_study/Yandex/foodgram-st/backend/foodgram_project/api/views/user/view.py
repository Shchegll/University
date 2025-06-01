from rest_framework import viewsets, mixins, status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import Relationship, Account
from api.pagination import MyCustomPaginator
from api.serializers.users.serializer import (AlphaUserList,
                                            GammaPasswordChange,
                                            ZetaSubscribeAction,
                                            EpsilonAuthorSubs,
                                            BetaUserCreate)

"""API контроллер для операций с пользователями"""


class AccountController(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Account.objects.all()
    permission_classes = (AllowAny,)
    paginator_class = MyCustomPaginator

    def _get_serializer_type(self):
        if self.action in ('list', 'retrieve'):
            return AlphaUserList
        return BetaUserCreate

    """Динамический выбор сериализатора по типу операции"""
    @action(detail=False, methods=['get'],
            pagination_class=None,
            permission_classes=(IsAuthenticated,))
    def get_my_profile(self, request):
        profile_data = AlphaUserList(
            request.user,
            context={'request': request}
        )
        return Response(profile_data.data, status=status.HTTP_200_OK)

    """Получение профиля текущего пользователя"""
    @action(detail=False, methods=['post'],
            permission_classes=(IsAuthenticated,))
    def update_credentials(self, request):
        pass_serializer = GammaPasswordChange(
            request.user,
            data=request.data,
            context={'request': request}
        )
        pass_serializer.is_valid(raise_exception=True)
        pass_serializer.save()
        return Response(
            {'message': 'Password updated successfully'},
            status=status.HTTP_204_NO_CONTENT
        )

    """Обновление учетных данных (пароля)"""
    @action(detail=False, methods=['get'],
            permission_classes=(IsAuthenticated,),
            pagination_class=MyCustomPaginator)
    def get_following(self, request):
        authors = Account.objects.filter(subscribing__user=request.user)
        page = self.paginate_queryset(authors)
        serializer = EpsilonAuthorSubs(
            page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    """Управление подписками (добавление/удаление)"""
    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def handle_subscription(self, request, **kwargs):
        content_creator = get_object_or_404(Account, id=kwargs['pk'])
        subscription = Relationship.objects.filter(
            user=request.user,
            author=content_creator
        )

        if request.method == 'POST':
            sub_serializer = ZetaSubscribeAction(
                content_creator,
                data=request.data,
                context={"request": request}
            )
            sub_serializer.is_valid(raise_exception=True)
            Relationship.objects.get_or_create(
                user=request.user,
                author=content_creator
            )
            return Response(
                sub_serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            subscription.delete()
            return Response(
                {'status': 'Subscription removed'},
                status=status.HTTP_204_NO_CONTENT
            )
