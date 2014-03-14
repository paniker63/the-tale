# coding: utf-8


class ActionsContainer(object):

    __slots__ = ('updated', 'actions_list', 'is_single')

    def __init__(self):
        self.updated = False
        self.is_single = False
        self.actions_list = []

    def serialize(self):
        return {'actions': [action.serialize() for action in self.actions_list]}

    @classmethod
    def deserialize(cls, hero, data):
        from the_tale.game.actions.prototypes import ACTION_TYPES
        obj = cls()
        obj.actions_list = [ACTION_TYPES[action_data['type']].deserialize(hero=hero, data=action_data) for action_data in data.get('actions', [])]
        obj.is_single = obj._is_single
        return obj

    def ui_info(self):
        return {'actions': [action.ui_info() for action in self.actions_list]}

    @property
    def _is_single(self):
        return all(action.SINGLE for action in self.actions_list)

    def push_action(self, action):
        self.updated = True
        self.actions_list.append(action)
        self.is_single = self._is_single

    def pop_action(self):
        self.updated = True
        action = self.actions_list.pop()
        self.is_single = self._is_single
        return action

    @property
    def current_action(self): return self.actions_list[-1]

    def on_save(self):
        for action in self.actions_list:
            action.on_save()

    @property
    def has_actions(self): return len(self.actions_list)

    @property
    def number(self): return len(self.actions_list)

    def reset_to_idl(self):
        self.actions_list = self.actions_list[:1]
        self.updated = True

    def request_replane(self):
        for action in self.actions_list:
            action.replane_required = True
