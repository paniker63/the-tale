# coding: utf-8

from dext.forms import forms, fields

from utg import relations as utg_relations

from the_tale.common.utils import bbcode

from the_tale.linguistics.forms import WordField

from the_tale.game.mobs.storage import mobs_storage

from the_tale.game.artifacts import relations


EFFECT_CHOICES = sorted(relations.ARTIFACT_EFFECT.choices(), key=lambda v: v[1])


class ArtifactRecordBaseForm(forms.Form):

    level = fields.IntegerField(label=u'минимальный уровень')

    name = WordField(word_type=utg_relations.WORD_TYPE.NOUN, label=u'Название')

    description = bbcode.BBField(label=u'Описание', required=False)

    type = fields.TypedChoiceField(label=u'тип', choices=relations.ARTIFACT_TYPE.choices(), coerce=relations.ARTIFACT_TYPE.get_from_name)
    power_type = fields.TypedChoiceField(label=u'тип силы', choices=relations.ARTIFACT_POWER_TYPE.choices(), coerce=relations.ARTIFACT_POWER_TYPE.get_from_name)

    rare_effect = fields.TypedChoiceField(label=u'редкий эффект', choices=EFFECT_CHOICES, coerce=relations.ARTIFACT_EFFECT.get_from_name)
    epic_effect = fields.TypedChoiceField(label=u'эпический эффект', choices=EFFECT_CHOICES, coerce=relations.ARTIFACT_EFFECT.get_from_name)

    special_effect = fields.TypedChoiceField(label=u'особое свойство', choices=EFFECT_CHOICES, coerce=relations.ARTIFACT_EFFECT.get_from_name)

    mob = fields.ChoiceField(label=u'Монстр', required=False)

    def __init__(self, *args, **kwargs):
        super(ArtifactRecordBaseForm, self).__init__(*args, **kwargs)
        self.fields['mob'].choices = [('', u'-------')] + [(mob.id, mob.name) for mob in sorted(mobs_storage.all(), key=lambda mob: mob.name)]

    def clean_mob(self):
        mob = self.cleaned_data.get('mob')

        if mob:
            return mobs_storage[int(mob)]

        return None

    @classmethod
    def get_initials(cls, artifact):
        return {'level': artifact.level,
                'name': artifact.utg_name,
                'type': artifact.type,
                'power_type': artifact.power_type,
                'rare_effect': artifact.rare_effect,
                'epic_effect': artifact.epic_effect,
                'special_effect': artifact.special_effect,
                'description': artifact.description,
                'mob': artifact.mob.id if artifact.mob is not None else None}


class ArtifactRecordForm(ArtifactRecordBaseForm):
    pass


class ModerateArtifactRecordForm(ArtifactRecordBaseForm):
    approved = fields.BooleanField(label=u'одобрен', required=False)

    @classmethod
    def get_initials(cls, mob):
        initials = super(ModerateArtifactRecordForm, cls).get_initials(mob)
        initials.update({'approved': mob.state.is_ENABLED})

        return initials
