from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from blog.models import Post, Category, Tag
from django.db.models import Q
# Create your views here.


class IndexView(ListView):
    model = Post
    template_name = 'home/index.html'
    context_object_name = 'post_list'
    paginate_by = 2

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)


        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')


        pagination_data = self.pagination_data(paginator, page, is_paginated)


        context.update(pagination_data)


        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:

            return {}


        left = []


        right = []


        left_has_more = False


        right_has_more = False


        first = False


        last = False


        page_number = page.number


        total_pages = paginator.num_pages


        page_range = paginator.page_range

        if page_number == 1:

            right = page_range[page_number:page_number + 2]


            if right[-1] < total_pages - 1:
                right_has_more = True


            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:

            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]


            if left[0] > 2:
                left_has_more = True


            if left[0] > 1:
                first = True
        else:

            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]


            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True


            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data


class CategoryView(IndexView):

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))

        return super(CategoryView, self).get_queryset().filter(category=cate)


class ArchivesView(IndexView):

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year, created_time__month=month)


class TagView(ListView):
    model = Post
    template_name = 'home/index.html'
    context_object_name = 'post_list'
    paginate_by = 2

    def get_queryset(self):
        tag  = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView,self).get_queryset().filter(tags=tag)


def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "请输入关键词"
        return render(request, 'home/index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'home/index.html', {'error_msg': error_msg,
                                               'post_list': post_list})
# def index(request):
#     post_list = Post.objects.all().order_by('-created_time')
#
#     context = {
#         'post_list': post_list
#     }
#     return render(request, 'home/index.html', context=context)
#
#
# def archives(request, year, month):
#
#     post_list = Post.objects.filter(created_time__year=year, created_time__month=month).order_by('-created_time')
#
#     context = {
#         'post_list': post_list
#     }
#
#     return render(request, 'home/index.html', context=context)
#
#
# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate).order_by('-created_time')
#     context = {
#         'post_list':post_list
#     }
#
#     return render(request, 'home/index.html', context=context)
