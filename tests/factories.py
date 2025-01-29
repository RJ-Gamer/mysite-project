import factory
from typing import Any, Optional, Sequence
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from faker import Faker

fake = Faker()
User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating User instances for testing.

    Attributes:
        email: Random email address
        first_name: Random first name
        last_name: Random last name
        password: Default password 'testpass123'
        is_active: Default True

    Example:
        >>> user = UserFactory()
        >>> user = UserFactory(email="custom@email.com")
        >>> user = UserFactory.create_batch(3)
    """

    class Meta:
        model = User
        skip_postgeneration_save = True

    email = factory.LazyAttribute(lambda _: fake.email())
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    password = factory.PostGenerationMethodCall("set_password", "testpass123")
    is_active = True

    @factory.post_generation
    def groups(self, create: bool, extracted: Optional[Sequence[Group]], **kwargs: Any) -> None:
        """
        Add groups to the user after creation.

        Args:
            create: Whether the model instance is being created
            extracted: Optional sequence of Group instances to add to the user
            **kwargs: Additional keyword arguments

        Example:
            >>> group1 = Group.objects.create(name="admin")
            >>> group2 = Group.objects.create(name="staff")
            >>> user = UserFactory(groups=(group1, group2))
        """
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)
        self.save()
