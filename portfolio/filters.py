from django import forms
import django_filters
from django_filters import CharFilter

from .models import Post, Tag

class PostFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title', lookup_expr="icontains", label="Title")
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(), 
                                                    widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Post
        fields = ["title", "tags"]