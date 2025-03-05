from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from taggit.models import Tag
from .forms import CommentForm
from .models import Gamechat, Comment


def chat_list(request):
    """
    Here we get all chats using our custom manager (i.e the PublishedManager)
    It retrieves all chats with a status of PUBLISHED
    """
    chat_list = Gamechat.published.all()
    # Pagination with 3 chats per page
    paginator = Paginator(chat_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        chats = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer get the first page
        chats = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range get last page of results
        chats = paginator.page(paginator.num_pages)

    return render(
        request,
        'chat/chat/list.html',
        {'chats': chats}
    )


def chat_detail(request, year, month, day, chat):
    """
    This chat detail view takes the id arguement of a chat. It uses the
    get_object_or_404 shortcut.
    If the chat is not found a HTTP 404 exception is raised.
    """
    chat = get_object_or_404(
        Chat,
        status=chat.Status.PUBLISHED,
        slug=chat,
        created_on__year=year,
        created_on__month=month,
        created_on__day=day
    )

    comments = chat.comments.filter(is_active=True)
    form = CommentForm()
    most_commented_chats = Gamechat.published.most_commented()

    return render(
        request,
        'chat/chat/detail.html',
        {
            'chat': chat,
            'comments': comments,
            'form': form,
            'most_commented_chats': most_commented_chats
        }
    )


class chatListView(ListView):
    """
    Alternative chat list view
    """
    queryset = Gamechat.published.all()
    context_object_name = 'chats'
    paginate_by = 3
    template_name = 'chat/chat/list.html'

    def get_queryset(self):
        queryset = chat.published.all()
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            self.tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags__in=[self.tag])
        else:
            self.tag = None
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context[
            'most_commented_chats'] = Chat.published.most_commented()
        return context


@login_required
@require_POST
def chat_comment(request, chat_id):
    chat = get_object_or_404(
        chat, id=chat_id, status=Chat.Status.PUBLISHED)
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.chat = chat
        comment.user = request.user
        comment.save()
        return redirect(
            'chat:chat_detail',
            year=chat.created_on.year,
            month=chat.created_on.month,
            day=chat.created_on.day,
            chat=chat.slug
        )
    return render(
        request,
        'chat/chat/detail.html',
        {'chat': chat, 'form': form}
    )


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(
        Comment, id=comment_id, user=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(
                'chat:chat_detail',
                year=comment.chat.created_on.year,
                month=comment.chat.created_on.month,
                day=comment.chat.created_on.day,
                chat=comment.chat.slug
            )
    else:
        form = CommentForm(instance=comment)
    return render(
        request,
        'chat/chat/comment/edit_comment.html',
        {'form': form}
    )


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(
        Comment, id=comment_id, user=request.user)
    chat = comment.chat
    if request.method == 'POST':
        comment.delete()
        return redirect(
            'chat:chat_detail',
            year=chat.created_on.year,
            month=chat.created_on.month,
            day=chat.created_on.day,
            chat=chat.slug
        )
    return render(
        request,
        'chat/chat/comment/delete_comment.html',
        {'comment': comment}
    )
