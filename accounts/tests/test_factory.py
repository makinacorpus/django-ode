#-*- coding: utf-8 -*-


import factory
from factory import fuzzy as factory_fuzzy

from accounts.models import Contact, User, Organization

USER_PASSWORD = "p4ssw0rd"


class ContactFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Contact

    name = factory.Sequence(lambda n: u'name_#%s' % n)
    email = factory.Sequence(lambda n: u'email_%s@ode.com' % n)
    phone_number = factory.Sequence(lambda n: u'number_#%s' % n)


class OrganizationFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Organization

    name = factory.Sequence(lambda n: u'name_#%s' % n)
    #picture = ImageField ?
    activity_field = factory.Sequence(lambda n: u'activity_#%s' % n)
    price_information = factory.Sequence(lambda n: u'price_info_#%s' % n)

    audience = factory.Sequence(lambda n: u'audience_#%s' % n)
    capacity = factory.Sequence(lambda n: u'capacity_#%s' % n)
    type = factory_fuzzy.FuzzyChoice(
        ['enterprise', 'public', 'individual', 'independent'])

    price_information = factory.Sequence(lambda n: u'address_#%s' % n)
    address = factory.Sequence(lambda n: u'address_#%s' % n)
    post_code = factory.Sequence(lambda n: u'postcode_#%s' % n)
    town = factory.Sequence(lambda n: u'town_#%s' % n)
    price_information = factory.Sequence(lambda n: u'price_info_#%s' % n)
    url = factory.Sequence(lambda n: u'http://url-%s-ode.com' % n)
    is_provider = False
    is_consumer = False
    is_host = False
    is_creator = False
    is_performer = False
    is_media = False
    is_website = False
    is_mobile_app = False
    is_other = False
    url = factory.Sequence(lambda n: u'http://media-url-%s-ode.com' % n)
    website_url = factory.Sequence(lambda n: u'http://wsit-url-%s-ode.com' % n)
    mobile_app_name = factory.Sequence(lambda n: u'mobile_app_#%s' % n)
    other_details = factory.Sequence(lambda n: u'other_details_#%s' % n)

    ticket_contact = factory.SubFactory(ContactFactory)
    press_contact = factory.SubFactory(ContactFactory)


class ProviderOrganizationFactory(OrganizationFactory):

    is_provider = True


class ConsumerOrganizationFactory(OrganizationFactory):

    is_consumer = True


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: u'user_#%s' % n)
    password = USER_PASSWORD
    email = factory.LazyAttribute(lambda obj: u'%s@example.com' % obj.username)
    is_active = False

    organization = factory.SubFactory(OrganizationFactory)

    phone_number = factory.Sequence(lambda n: u'phone_number_#%s' % n)
    confirmation_code = factory.Sequence(lambda n: u'code_#%s' % n)

    first_inscription = True

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user


class ProviderUserFactory(UserFactory):

    organization = factory.SubFactory(ProviderOrganizationFactory)


class ConsumerUserFactory(UserFactory):

    organization = factory.SubFactory(ConsumerOrganizationFactory)
