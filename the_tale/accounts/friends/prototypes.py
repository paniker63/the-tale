# coding: utf-8

from django.db import models

from dext.common.utils.urls import full_url

from the_tale.common.utils.prototypes import BasePrototype
from the_tale.common.utils.decorators import lazy_property
from the_tale.common.utils import bbcode

from the_tale.accounts.models import Account
from the_tale.accounts.prototypes import AccountPrototype
from the_tale.accounts.logic import get_system_user

from the_tale.accounts.personal_messages.prototypes import MessagePrototype

from the_tale.accounts.friends.models import Friendship




class FriendshipPrototype(BasePrototype):
    _model_class = Friendship
    _readonly = ('is_confirmed', 'id', 'friend_1_id', 'friend_2_id')
    _bidirectional = ()
    _get_by = ()

    def _confirm(self):
        MessagePrototype.create(get_system_user(),
                                self.friend_1,
                                u'игрок %(account_link)s подтвердил, что вы являетесь друзьями' %
                                {'account_link': u'[url=%s]%s[/url]' % (full_url('http', 'accounts:show', self.friend_2.id), self.friend_2.nick_verbose)})
        self._model.is_confirmed = True
        self.save()

    @lazy_property
    def friend_1(self): return AccountPrototype(model=self._model.friend_1)

    @lazy_property
    def friend_2(self): return AccountPrototype(model=self._model.friend_2)

    @property
    def text_html(self): return bbcode.render(self._model.text)

    @classmethod
    def _get_for(cls, friend_1, friend_2):
        try:
            return cls(model=cls._model_class.objects.get(friend_1_id=friend_1.id, friend_2_id=friend_2.id))
        except cls._model_class.DoesNotExist:
            return None

    @classmethod
    def get_for_bidirectional(cls, friend_1, friend_2):
        try:
            return cls(model=cls._model_class.objects.get(models.Q(friend_1_id=friend_1.id, friend_2_id=friend_2.id) |
                                                          models.Q(friend_1_id=friend_2.id, friend_2_id=friend_1.id)) )
        except cls._model_class.DoesNotExist:
            return None

    @classmethod
    def _get_accounts_for(cls, account, is_confirmed):
        friendship_query = cls._model_class.objects.filter(models.Q(friend_1_id=account.id)|models.Q(friend_2_id=account.id), is_confirmed=is_confirmed)
        values = list(friendship_query.values_list('friend_1_id', 'friend_2_id'))

        if not values: return []

        friends_1_ids, friends_2_ids = zip(*values)
        accounts_ids = (set(friends_1_ids) | set(friends_2_ids)) - set([account.id])
        return [AccountPrototype(model=model) for model in Account.objects.filter(id__in=accounts_ids)]

    @classmethod
    def get_friends_for(cls, account):
        friendship_query = cls._model_class.objects.filter(models.Q(friend_1_id=account.id)|models.Q(friend_2_id=account.id), is_confirmed=True)
        values = list(friendship_query.values_list('friend_1_id', 'friend_2_id'))

        if not values: return []

        friends_1_ids, friends_2_ids = zip(*values)
        accounts_ids = (set(friends_1_ids) | set(friends_2_ids)) - set([account.id])
        return [AccountPrototype(model=model) for model in Account.objects.filter(id__in=accounts_ids)]

    @classmethod
    def get_candidates_for(cls, account):
        friendship_query = cls._model_class.objects.filter(friend_2_id=account.id, is_confirmed=False)
        accounts_ids = friendship_query.values_list('friend_1_id', flat=True)
        return [AccountPrototype(model=model) for model in Account.objects.filter(id__in=accounts_ids)]

    @classmethod
    def request_friendship(cls, friend_1, friend_2, text=None):
        own_request = cls._get_for(friend_1, friend_2)
        if own_request:
            if text is not None: #
                own_request._model.text = text
                own_request.save()
            return own_request

        his_request = cls._get_for(friend_2, friend_1)
        if his_request:
            his_request._confirm()
            return his_request

        model = cls._model_class.objects.create(friend_1=friend_1._model,
                                                friend_2=friend_2._model,
                                                text=text)
        prototype = cls(model=model)

        message = u'''
игрок %(account_link)s предлагает вам дружить:

%(text)s

----------
принять или отклонить предложение вы можете на этой странице: %(friends_link)s
''' % {'account_link': u'[url="%s"]%s[/url]' % (full_url('http', 'accounts:show', friend_1.id), friend_1.nick_verbose),
       'text': text,
       'friends_link': u'[url="%s"]предложения дружбы[/url]' % full_url('http', 'accounts:friends:candidates')}

        # send message from name of user, who request friendship
        # since many users try to respod to system user
        MessagePrototype.create(friend_1, friend_2, message)

        return prototype

    @classmethod
    def remove_friendship(cls, initiator, friend):
        request = cls.get_for_bidirectional(initiator, friend)

        if request is None: return

        if request.is_confirmed:
            MessagePrototype.create(get_system_user(),
                                    friend,
                                    u'игрок %(account_link)s удалил вас из списка друзей' %
                                    {'account_link': u'[url="%s"]%s[/url]' % (full_url('http', 'accounts:show', initiator.id), initiator.nick_verbose)})
        else:
            MessagePrototype.create(get_system_user(),
                                    friend,
                                    u'игрок %(account_link)s отказался добавить вас в список друзей' %
                                    {'account_link': u'[url="%s"]%s[/url]' % (full_url('http', 'accounts:show', initiator.id), initiator.nick_verbose)})

        request.remove()

        return

    def save(self):
        self._model.save()

    def remove(self):
        self._model.delete()
