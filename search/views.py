

from itertools import chain
from django.views.generic import ListView

from django.db.models import Q

from accounts.models import User, Student
from app.models import NewsAndEvents
from course.models import Program, Course


class SearchView(ListView):
    template_name = 'search/search_view.html'
    paginate_by = 20
    count = 0
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        
       
       
        return NewsAndEvents.objects.none() 