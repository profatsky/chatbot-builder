import factory
from faker import Faker

from src.enums import KeyboardType
from src.projects.schemas import ProjectCreateSchema

fake = Faker()


class ProjectCreateSchemaFactory(factory.Factory):
    class Meta:
        model = ProjectCreateSchema

    name = factory.LazyFunction(lambda: fake.sentence(nb_words=3))
    start_message = factory.LazyFunction(lambda: fake.sentence(nb_words=6))
    start_keyboard_type = factory.Iterator([kb_type.value for kb_type in KeyboardType])
