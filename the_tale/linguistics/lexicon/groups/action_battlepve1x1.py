# coding: utf-8

from the_tale.linguistics.lexicon.relations import VARIABLE as V
from the_tale.linguistics.lexicon.groups.relations import LEXICON_GROUP

KEYS = [(u'ACTION_BATTLEPVE1X1_ARTIFACT_BROKEN', 0, u'Дневник: Артефакт сломался во время боя', LEXICON_GROUP.ACTION_BATTLEPVE1X1,
        u'Запись в дневник о том, что герой сломал артефакт во время боя.',
        [V.MOB, V.HERO, V.ARTIFACT]),

        (u'ACTION_BATTLEPVE1X1_BATTLE_STUN', 1, u'Стан', LEXICON_GROUP.ACTION_BATTLEPVE1X1,
        u'Герой или монстр дезориентирован и пропускает ход.',
        [V.ACTOR]),

        (u'ACTION_BATTLEPVE1X1_DESCRIPTION', 2, u'Описание', LEXICON_GROUP.ACTION_BATTLEPVE1X1,
        u'Краткая декларация того, что делает герой.',
        [V.MOB, V.HERO]),

        (u'ACTION_BATTLEPVE1X1_DIARY_HERO_KILLED', 3, u'Дневник: Герой убит', LEXICON_GROUP.ACTION_BATTLEPVE1X1,
        u'Герой умирает.',
        [V.MOB, V.HERO]),

        (u'ACTION_BATTLEPVE1X1_EXP_FOR_KILL', 4, u'Получить опыт за убийство монстра', LEXICON_GROUP.ACTION_BATTLEPVE1X1,
        u'Герой получил немного опыта за убийство монстра (испытал новый приём или монстр «особенный» попался)',
        [V.MOB, V.HERO, V.EXPERIENCE]),

        (u'ACTION_BATTLEPVE1X1_JOURNAL_HERO_KILLED', 5, u'Журнал: Герой убит', LEXICON_GROUP.ACTION_BATTLEPVE1X1,
        u'Герой умирает.',
        [V.MOB, V.HERO]),

        (u'ACTION_BATTLEPVE1X1_KILL_BEFORE_START', 6, u'Убить до боя', LEXICON_GROUP.ACTION_BATTLEPVE1X1,
        u'Герой заметил монстра до боя и убил его',
        [V.MOB, V.HERO]),

        (u'ACTION_BATTLEPVE1X1_LEAVE_BATTLE_IN_FEAR', 7, u'Противник бежит в страхе', LEXICON_GROUP.ACTION_BATTLEPVE1X1,
        u'Герой так напугал противника, что тот в ужасе убегает',
        [V.MOB, V.HERO]),

        (u'ACTION_BATTLEPVE1X1_MOB_KILLED', 8, u'Монстр убит', LEXICON_GROUP.ACTION_BATTLEPVE1X1,
        u'Монстр умирает.',
        [V.MOB, V.HERO]),

        (u'ACTION_BATTLEPVE1X1_NO_LOOT', 9, u'Нет добычи', LEXICON_GROUP.ACTION_BATTLEPVE1X1,
        u'Герой не получил добычу.',
        [V.MOB, V.HERO]),

        (u'ACTION_BATTLEPVE1X1_PEACEFULL_BATTLE', 10, u'Мирно разойтись с цивилизованных гуманоидом', LEXICON_GROUP.ACTION_BATTLEPVE1X1,
        u'Герой договорился с цивилизованным моснтром о том, чтобы драки не было',
        [V.MOB, V.HERO]),

        (u'ACTION_BATTLEPVE1X1_PERIODICAL_FIRE_DAMAGE', 11, u'Периодический урон огнём', LEXICON_GROUP.ACTION_BATTLEPVE1X1,
        u'Герой или монстр получает периодический урон огнём.',
        [V.DAMAGE, V.ACTOR]),

        (u'ACTION_BATTLEPVE1X1_PERIODICAL_POISON_DAMAGE', 12, u'Периодический урон ядом', LEXICON_GROUP.ACTION_BATTLEPVE1X1,
        u'Герой или монстр получает периодический урон ядом.',
        [V.DAMAGE, V.ACTOR]),

        (u'ACTION_BATTLEPVE1X1_PUT_LOOT', 13, u'Герой забрал добычу', LEXICON_GROUP.ACTION_BATTLEPVE1X1,
        u'Герой получил добычу с трупа противника и положил её в рюкзак.',
        [V.MOB, V.HERO, V.ARTIFACT]),

        (u'ACTION_BATTLEPVE1X1_PUT_LOOT_NO_SPACE', 14, u'Нет места в рюкзаке', LEXICON_GROUP.ACTION_BATTLEPVE1X1,
        u'Герой получил добычу, но в рюкзаке нет для неё места (добыча выкидывается).',
        [V.MOB, V.HERO, V.ARTIFACT]),

        (u'ACTION_BATTLEPVE1X1_START', 15, u'Начало боя', LEXICON_GROUP.ACTION_BATTLEPVE1X1,
        u'Встреча с противником.',
        [V.MOB, V.HERO]),

        ]
        