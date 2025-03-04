from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from django.db.transaction import atomic
from utils.choices import AccountTypeChoice
from django.contrib.auth.models import User


class WithoutPutModelViewSet(GenericViewSet):
    http_method_names = [
        "get",
        "post",
        # "put",
        "patch",
        "delete",
        "head",
        "options",
        "trace",
    ]
    class Meta:
        abstract = True

class SoftDeleteModelViewset(GenericViewSet):

    @atomic()
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    class Meta:
        abstract = True

class ModelQuerySet(GenericViewSet):
    class Meta:
        abstract = True
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = '__all__'

    select_related_fields = []
    queryset_filter_kwargs = {}

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.select_related(
            *self.select_related_fields
            ).filter(
                **self.get_queryset_filter_kwargs()
            )

    def get_queryset_filter_kwargs(self):
        kwargs = self.queryset_filter_kwargs
        kwargs['is_active'] = True
        return kwargs


class BaseUserAccountModelViewSet(ModelQuerySet, GenericViewSet):
    # authentication_classes = [AuthorizationMiddleware]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = '__all__'
    permission_classes = [permissions.IsAuthenticated,]
    need_authentication = True
    base_key = None

    class Meta:
        abstract = True

    def get_base_key(self):
        user_id = self.request.user.id
        if self.base_key == 'user':
            base_key_kwargs = {'user_id': user_id}
        elif self.base_key == 'account':
            account_id = None
            if user_id:
                account_id = User.objects.get(pk=user_id).account_set.filter(type=AccountTypeChoice.MAIN).first().id
            base_key_kwargs = {'account_id': account_id}
        else:
            raise Exception('WrongSetUP')
        return base_key_kwargs
    
    @atomic()
    def perform_create(self, serializer):
        base_key_kwargs = self.get_base_key()
        serializer.save(**base_key_kwargs)

    def get_queryset_filter_kwargs(self):
        _kwargs = super().get_queryset_filter_kwargs()
        base_key_kwargs = self.get_base_key()
        kwargs = {**_kwargs, **base_key_kwargs}
        return kwargs

class UserModelViewSet(BaseUserAccountModelViewSet):
    base_key = 'user'
    @property
    def user_id(self):
        base_key_kwargs = self.get_base_key()
        return base_key_kwargs['user_id']

class AccountModelViewSet(BaseUserAccountModelViewSet):
    base_key = 'account'
    @property
    def account_id(self):
        base_key_kwargs = self.get_base_key()
        return base_key_kwargs['account_id']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['account_id'] = self.account_id
        return context


class CRUDModelViewset(ModelViewSet):
    class Meta:
        abstract = True

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = '__all__'

    @atomic()
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @atomic()
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @atomic()
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class UserCustomModelViewset(
    WithoutPutModelViewSet, 
    UserModelViewSet, 
    SoftDeleteModelViewset, 
    CRUDModelViewset
    ):

    class Meta:
        abstract = True

class AccountCustomModelViewset(
    WithoutPutModelViewSet, 
    AccountModelViewSet, 
    SoftDeleteModelViewset, 
    CRUDModelViewset
    ):

    class Meta:
        abstract = True

class NoAuthReadOnlyModelViewSet(ModelQuerySet, ReadOnlyModelViewSet):
    class Meta:
        abstract = True

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = '__all__'

    permission_classes = [permissions.AllowAny,]
    need_authentication = False
