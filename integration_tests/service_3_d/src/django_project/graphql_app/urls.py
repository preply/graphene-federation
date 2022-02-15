from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from .schema import schema

urlpatterns = [
    # when graphiql is set to True, we will also provide a graphql frontend to ease the queries
    path("/", csrf_exempt(GraphQLView.as_view(graphiql=True)))
]