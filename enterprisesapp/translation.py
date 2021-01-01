from modeltranslation.translator import translator, TranslationOptions
from enterprisesapp.models.skill import Skill
from enterprisesapp.models.sector import Sector


class SkillTranslationOptions(TranslationOptions):

    # These are the field to be translated
    fields = [
        "name",
    ]


translator.register(Skill, SkillTranslationOptions)


class SectorTranslationOptions(TranslationOptions):

    # These are the field to be translated
    fields = [
        "name",
    ]


translator.register(Sector, SectorTranslationOptions)
