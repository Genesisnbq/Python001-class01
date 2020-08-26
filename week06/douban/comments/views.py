from django.shortcuts import render
from .models import Comment


def comment(request):
    keyword = request.GET.get('q')
    conditions = {'rating__gt': 3}
    if keyword:
        conditions['content__contains'] = keyword
    comments_rating_gt_3 = Comment.objects.filter(**conditions).all().order_by('-rating')
    context = {'comments': comments_rating_gt_3}
    return render(request=request, template_name='comments.html', context=context)
