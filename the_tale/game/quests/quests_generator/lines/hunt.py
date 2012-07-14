# coding: utf-8
from ..quest_line import Quest, Line, ACTOR_TYPE
from .. import commands as cmd


class EVENTS:
    QUEST_DESCRIPTION = 'quest_description'
    MOVE_TO_QUEST = 'move_to_quest'
    TRACK = 'track'
    HUNT = 'hunt'
    MOVE_TO_CITY = 'move_to_city'
    GET_REWARD = 'get_reward'

class Hunt(Quest):

    SPECIAL = True

    ACTORS = [(u'место охоты', 'place_end', ACTOR_TYPE.PLACE)]

    @classmethod
    def can_be_used(cls, env):
        return env.knowlege_base.get_special('hero_pref_mob') is not None

    def initialize(self, identifier, env, place_start=None, place_end=None):
        super(Hunt, self).initialize(identifier, env)

        mob = env.knowlege_base.get_special('hero_pref_mob')

        self.env_local.register('place_start', place_start or env.new_place())
        self.env_local.register('place_end', place_end or env.new_place(terrain=mob['terrain']))


    def create_line(self, env):
        mob = env.knowlege_base.get_special('hero_pref_mob')

        main_line = Line(sequence=[cmd.Move(place=self.env_local.place_end, event=EVENTS.MOVE_TO_QUEST),

                                   cmd.MoveNear(place=self.env_local.place_end, back=False, event=EVENTS.TRACK),
                                   cmd.Battle(number=1, event=EVENTS.HUNT, mob_id=mob['id']),
                                   cmd.MoveNear(place=self.env_local.place_end, back=False, event=EVENTS.TRACK),
                                   cmd.Battle(number=1, event=EVENTS.HUNT, mob_id=mob['id']),
                                   cmd.MoveNear(place=self.env_local.place_end, back=False, event=EVENTS.TRACK),
                                   cmd.Battle(number=1, event=EVENTS.HUNT, mob_id=mob['id']),

                                   cmd.MoveNear(place=self.env_local.place_end, back=True, event=EVENTS.MOVE_TO_CITY),

                                   cmd.GetReward(person=None, event=EVENTS.GET_REWARD)   ])

        self.line = env.new_line(main_line)
