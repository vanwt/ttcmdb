from django.views.generic import ListView
from ..models import Tags


class TagsView(ListView):
    context_object_name = 'tag_list'
    template_name = 'assets/tags.html'
    model = Tags
    paginate_by = 20
    ordering = '-create_time'
