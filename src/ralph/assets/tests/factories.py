# -*- coding: utf-8 -*-
import factory
from factory.django import DjangoModelFactory

from ralph.assets.models.assets import (
    AssetHolder,
    AssetModel,
    BudgetInfo,
    BusinessSegment,
    Category,
    Environment,
    Manufacturer,
    ProfitCenter,
    Service,
    ServiceEnvironment
)
from ralph.assets.models.base import BaseObject
from ralph.assets.models.choices import ComponentType, ObjectModelType
from ralph.assets.models.components import Ethernet
from ralph.assets.models.configuration import (
    ConfigurationClass,
    ConfigurationModule
)


def next_mac(n):
    mac = [
        0x00,
        0x16,
        0x3e,
        n >> 16 & 0xff,
        n >> 8 & 0xff,
        n & 0xff
    ]
    return ':'.join(map(lambda x: '%02x' % x, mac))


class BaseObjectFactory(DjangoModelFactory):

    class Meta:
        model = BaseObject


class CategoryFactory(DjangoModelFactory):

    imei_required = True
    show_buyout_date = True
    name = factory.Iterator([
        'Dictaphone', 'Disk', 'External disk', 'External drive', 'Headphones',
        'Keyboard', 'Mouse', 'Pendrive', 'Notebook'
    ])

    class Meta:
        model = Category
        django_get_or_create = ['name']


class DataCenterCategoryFactory(DjangoModelFactory):

    imei_required = False
    name = factory.Iterator([
        'ATS', 'Database Machine', 'Blade System', 'Chassis blade'
    ])

    class Meta:
        model = Category
        django_get_or_create = ['name']


class AssetHolderFactory(DjangoModelFactory):

    name = factory.Iterator(
        ['Grupa Allegro SP. z o.o.', 'Google Inc.', 'Dell Inc']
    )

    class Meta:
        model = AssetHolder
        django_get_or_create = ['name']


class BudgetInfoFactory(DjangoModelFactory):

    name = factory.Iterator(
        ['Python Team', 'Django team', 'Redis Team', 'PSQL Team']
    )

    class Meta:
        model = BudgetInfo
        django_get_or_create = ['name']


class ManufacturerFactory(DjangoModelFactory):

    name = factory.Iterator([
        'Dell', 'Apple', 'Samsung', 'Adobe', 'Asus', 'Atlassian', 'BenQ',
        'Belkin', 'Bosh', 'Brother', 'Foxconn', 'Fujitsu', 'HUAWEI', 'HTC'
    ])

    class Meta:
        model = Manufacturer
        django_get_or_create = ['name']


class BackOfficeAssetModelFactory(DjangoModelFactory):

    name = factory.Iterator([
        '3310', 'XD300S', 'Hero 3', 'Computer set', 'Advance', 'axs', 'compaq',
        'Dell XPS', 'Macbook', 'Iphone 6', 'Iphone 6S', 'Desire'
    ])
    type = ObjectModelType.back_office
    category = factory.SubFactory(CategoryFactory)
    manufacturer = factory.SubFactory(ManufacturerFactory)

    class Meta:
        model = AssetModel
        django_get_or_create = ['name']


class DataCenterAssetModelFactory(DjangoModelFactory):

    name = factory.Iterator(['DL360', 'DL380p', 'DL380', 'ML10', 'ML10 v21'])
    type = ObjectModelType.data_center
    manufacturer = factory.SubFactory(ManufacturerFactory)
    height_of_device = factory.Iterator([1, 2, 3, 4])
    category = factory.SubFactory(DataCenterCategoryFactory)

    class Meta:
        model = AssetModel
        django_get_or_create = ['name']


class EnvironmentFactory(DjangoModelFactory):

    name = factory.Iterator(['prod', 'dev', 'test'])

    class Meta:
        model = Environment
        django_get_or_create = ['name']


class ServiceFactory(DjangoModelFactory):

    name = factory.Iterator(['Backup systems', 'load_balancing', 'databases'])
    uid = factory.Sequence(lambda n: 'sc-{}'.format(n))

    class Meta:
        model = Service
        django_get_or_create = ['name']


class ServiceEnvironmentFactory(DjangoModelFactory):

    service = factory.SubFactory(ServiceFactory)
    environment = factory.SubFactory(EnvironmentFactory)

    class Meta:
        model = ServiceEnvironment
        django_get_or_create = ['service', 'environment']


class BusinessSegmentFactory(DjangoModelFactory):
    name = factory.Iterator(['IT', 'Ads', 'Research'])

    class Meta:
        model = BusinessSegment
        django_get_or_create = ['name']


class ProfitCenterFactory(DjangoModelFactory):
    name = factory.Iterator(['PC1', 'PC2', 'PC3'])
    business_segment = factory.SubFactory(BusinessSegmentFactory)

    class Meta:
        model = ProfitCenter
        django_get_or_create = ['name']


class EthernetFactory(DjangoModelFactory):
    base_object = factory.SubFactory(BaseObjectFactory)
    label = factory.Sequence(lambda n: 'ETH#{}'.format(n))
    mac = factory.Sequence(next_mac)

    class Meta:
        model = Ethernet
        django_get_or_create = ['label']


class ConfigurationModuleFactory(DjangoModelFactory):
    name = factory.Iterator(['ralph', 'allegro', 'auth', 'order'])

    class Meta:
        model = ConfigurationModule
        django_get_or_create = ['name']


class ConfigurationClassFactory(DjangoModelFactory):
    class_name = factory.Iterator(['www', 'db', 'worker', 'cache'])
    module = factory.SubFactory(ConfigurationModuleFactory)

    class Meta:
        model = ConfigurationClass
        django_get_or_create = ['class_name']
