from typing import Any, Sequence

from factory import Faker, LazyFunction, SubFactory, post_generation
from factory.django import DjangoModelFactory

from atlas_web.simulation.models import AtlasSimulation
from atlas_web.users.tests.factories import UserFactory


class AtlasSimulationFactory(DjangoModelFactory):

    requested_by = SubFactory(UserFactory)

    @post_generation
    def name(self, create: bool, extracted: Sequence[Any], **kwargs):
        self.name = "Test: {}".format(self.name)

    class Meta:
        model = AtlasSimulation
