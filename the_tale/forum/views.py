# -*- coding: utf-8 -*-
import postmarkup

from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from dext.views.resources import handler
from dext.utils.decorators import nested_commit_on_success

from common.utils.resources import Resource

from forum.models import Category, SubCategory, Thread, Post
from forum.forms import NewPostForm, NewThreadForm
from forum.conf import forum_settings
from forum.logic import create_thread, create_post


class ForumResource(Resource):

    def __init__(self, request, category=None, subcategory=None, thread_id=None, *args, **kwargs):
        super(ForumResource, self).__init__(request, *args, **kwargs)

        self.thread_id = int(thread_id) if thread_id is not None else None
        self.category_slug = category
        self.subcategory_slug = subcategory

    @property
    def category(self):
        if not hasattr(self, '_category'):
            self._category = get_object_or_404(Category, slug=self.category_slug)
        return self._category

    @property
    def subcategory(self):
        if not hasattr(self, '_subcategory'):
            self._subcategory = get_object_or_404(SubCategory, slug=self.subcategory_slug)
        return self._subcategory

    @property
    def thread(self):
        if not hasattr(self, '_thread'):
            self._thread = get_object_or_404(Thread, id=self.thread_id)
        return self._thread


    @handler('', method='get')
    def index(self):
        categories = list(Category.objects.all().order_by('order', 'id'))

        subcategories = list(SubCategory.objects.all().order_by('order', 'id'))

        forum_structure = []

        for category in categories:
            children = []
            for subcategory in subcategories:
                if subcategory.category_id == category.id:
                    children.append(subcategory)

            forum_structure.append({'category': category,
                                    'subcategories': children})


        return self.template('forum/index.html',
                             {'forum_structure': forum_structure} )


    @handler('#category', '#subcategory', name='subcategory', method='get')
    def get_subcategory(self):

        threads = Thread.objects.filter(subcategory=self.subcategory).order_by('-updated_at')

        return self.template('forum/subcategory.html',
                             {'category': self.category,
                              'subcategory': self.subcategory,
                              'threads': threads} )


    @handler('#category', '#subcategory', 'new-thread', name='new_thread', method='get')
    def new_thread(self):

        if self.account is None:
            return self.template('error.html', {'msg': u'Вы должны войти на сайт, чтобы писать на форуме',
                                                'error_code': 'forum.new_thread.unlogined'})

        if self.account.is_fast:
            return self.template('error.html', {'msg': u'Вы не закончили регистрацию и не можете писать на форуме',
                                                'error_code': 'forum.new_thread.fast_account'})

        return self.template('forum/new_thread.html',
                             {'category': self.category,
                              'subcategory': self.subcategory,
                              'new_thread_form': NewThreadForm()} )

    @handler('#category', '#subcategory', 'create-thread', name='create_thread', method='post')
    def create_thread(self):

        if self.account is None:
            return self.json_error('forum.create_thread.unlogined', u'Вы должны войти на сайт, чтобы писать на форуме')

        if self.account.is_fast:
            return self.json_error('forum.create_thread.fast_account', u'Вы не закончили регистрацию и не можете писать на форуме')

        if self.subcategory.closed:
            return self.json_error('forum.create_thread.closed_subcategory', u'Вы не можете создавать темы в данном разделе')

        new_thread_form = NewThreadForm(self.request.POST)

        if not new_thread_form.is_valid():
            return self.json_error('forum.create_thread.form_errors', new_thread_form.errors)

        thread = create_thread(self.subcategory,
                               caption=new_thread_form.c.caption,
                               author=self.account.user,
                               text=new_thread_form.c.text)



        return self.json_ok(data={'thread_id': thread.id})


    @handler('#category', '#subcategory', '#thread_id', name='show_thread', method='get')
    def get_thread(self, page=1):

        page = int(page) - 1

        post_from = page * forum_settings.POSTS_ON_PAGE

        if post_from > self.thread.posts_count:
            last_page = self.thread.posts_count / forum_settings.POSTS_ON_PAGE + 1
            url = '%s?page=%d' % (reverse('forum:show_thread', args=[self.category.slug, self.subcategory.slug, self.thread.id]), last_page)
            return self.redirect(url, permanent=False)

        post_to = post_from + forum_settings.POSTS_ON_PAGE

        posts = Post.objects.filter(thread=self.thread).order_by('created_at')[post_from:post_to]

        pages_count = (self.thread.posts_count + 1) / forum_settings.POSTS_ON_PAGE
        if (self.thread.posts_count + 1) % forum_settings.POSTS_ON_PAGE:
            pages_count += 1

        return self.template('forum/thread.html',
                             {'category': self.category,
                              'subcategory': self.subcategory,
                              'thread': self.thread,
                              'new_post_form': NewPostForm(),
                              'posts': posts,
                              'pages_numbers': range(pages_count),
                              'start_posts_from': page * forum_settings.POSTS_ON_PAGE,
                              'current_page_number': page} )


    @handler('#category', '#subcategory', '#thread_id', 'create-post', name='create_post', method='post')
    @nested_commit_on_success
    def create_post(self):

        if self.account is None:
            return self.json_error('forum.create_post.unlogined', u'Вы должны войти на сайт, чтобы писать на форуме')

        if self.account.is_fast:
            return self.json_error('forum.create_post.fast_account', u'Вы не закончили регистрацию и не можете писать на форуме')

        new_post_form = NewPostForm(self.request.POST)

        if not new_post_form.is_valid():
            return self.json_error('forum.create_post.form_errors', new_post_form.errors)

        create_post(self.subcategory, self.thread, self.account.user, new_post_form.c.text)

        return self.json_ok()

    @handler('preview', name='preview', method='post')
    def preview(self):
        return self.string(postmarkup.render_bbcode(self.request.POST.get('text', '')))
