from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('details/<int:pk>', views.details.as_view(), name='details'),
    path('delete/<int:pk>', views.delete.as_view(), name='delete'),
    path('edit/<int:pk>', views.edit.as_view(), name='edit'),
    path('add_receta', views.add_receta.as_view(), name='add_receta'),
    path('buscar_receta', views.buscar_receta.as_view(), name='buscar_receta'),

    # path('post', views.post, name='post'),
    # path('author', views.author, name='author'),
    path('accounts/register/', views.register, name='register'),

    # path('list_categoria', views.list_categoria.as_view(), name='list_categoria'),
    path('add_categoria', views.add_categoria.as_view(), name='add_categoria'),
    path('details_categoria/<int:pk>', views.details_categoria.as_view(), name='details_categoria'),
    path('delete_categoria/<int:pk>', views.delete_categoria.as_view(), name='delete_categoria'),
    path('edit_categoria/<int:pk>', views.edit_categoria.as_view(), name='edit_categoria'),
    path('add_categoria', views.add_categoria.as_view(), name='add_categoria'),
    path('filtrar_categoria', views.filtrar_categoria.as_view(), name='filtrar_categoria'),

    path('details_perfil/<int:pk>', views.details_perfil.as_view(), name='details_perfil'),
    path('edit_perfil/<int:pk>', views.edit_perfil.as_view(), name='edit_perfil'),
    path('delete_perfil/<int:pk>', views.delete_perfil.as_view(), name='delete_perfil'),

    # path('is_favorite/<int:pk>', views.is_favorite.as_view(), name='is_favorite'),

]
# urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)