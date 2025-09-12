from threading import Lock
from polymorphic.models import PolymorphicModel
from typing import Optional
import contextlib
import re

from django.db import models, transaction


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Service: {str(self)}>"

class Object(models.Model):
    object_counter = models.IntegerField(default=0, editable=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    counter_lock = Lock()

    @property
    def human_id(self):
        return f"{self.service.name}-{self.object_counter}"

    @staticmethod
    def load(human_id: str) -> "Object":
        try:
            service, ticket = Object.extract_human_id_parts(human_id)
            service = Service.objects.get(name=service)

            return Object.objects.get(service=service, object_counter=ticket)

        except (Service.DoesNotExist, ValueError) as ex:
            raise Object.DoesNotExist from ex

    @staticmethod
    def extract_human_id_parts(human_id: str, service: Optional[str] = '') -> tuple[str, str]:
        BAD_HUMAN_ID_FORMAT_ERROR_STRING = "Bad value for human_id. Correct format is <SERVICE>-<ITEM>, got {}"

        if service:
            if human_id.startswith(service):
                human_id = human_id[len(service):]

            else:
                raise ValueError(f"Service name, <{service}>, does not match human ID, <{human_id}>")

        human_id_parts = re.search(r"-(\d+)-(\d+)$", human_id)

        if not human_id_parts:
            human_id_parts = re.search(r"-(\d+)$", human_id)

            if not human_id_parts:
                raise ValueError(BAD_HUMAN_ID_FORMAT_ERROR_STRING.format(human_id))

        start_of_number_match, _ = human_id_parts.span()
        service_name = service or human_id[0:start_of_number_match]

        if len(service_name) == 0:
            raise ValueError(BAD_HUMAN_ID_FORMAT_ERROR_STRING.format(human_id))

        ticket_ctr = human_id_parts.groups()[0]

        if not service and len(human_id_parts.groups()) == 2:
            try:
                Service.objects.get(name=service_name)

            except Service.DoesNotExist:
                possible_name = f'{service_name}-{human_id_parts.groups()[0]}'

                try:
                    Service.objects.get(name=possible_name)
                    service_name = possible_name
                    ticket_ctr = human_id_parts.groups()[1]

                except Service.DoesNotExist:
                    pass

        return service_name, ticket_ctr

    def get_absolute_url(self):
        return f"/core/{self.service}/objects/{self.id}/"

    def save(self, force_insert=False, force_update=False, **kwargs):
        if self.id:
            update = True

            try:
                Object.objects.get(pk=self.id)

            except Object.DoesNotExist:
                pass

        else:
            update = False

        # need counter for project
        if not update:
            self.allocate_next_object_counter(force_insert, force_update, **kwargs)

        else:
            super(Object, self).save(force_insert, force_update, **kwargs)

    def allocate_next_object_counter(self, force_insert, force_update, **kwargs) -> None:
        similar_objects = Object.objects.filter(service=self.service)
        similar_objects = similar_objects.select_for_update().order_by("-object_counter")

        with Object.counter_lock, transaction.atomic():
            max_counter = 0

            """
            @NOTE
            It's possible that no objects may be returned and an attribute error
            will be thrown when accessing the object_counter of a non-existing first() element
            of a query set, so just catch and pass the error, it's non fatal but does have
            to be handled.
            """
            with contextlib.suppress(AttributeError):
                max_counter = similar_objects.first().object_counter

            self.object_counter = max_counter + 1
            super(Object, self).save(force_insert, force_update, **kwargs)

    def __str__(self):
        return f"{self.service}-{self.object_counter}"

    def __repr__(self):
        return f"<Object: {str(self)}>"

class Field(models.Model):
    CHAR = "CHAR"
    TEXT = "TEXT"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    BOOLEAN = "BOOLEAN"
    DATE = "DATE"
    URL = "URL"

    FORM_TYPES = (
        (CHAR, "SHORT TEXT"),
        (TEXT, "LARGE TEXT"),
        (INTEGER, "INTEGER"),
        (FLOAT, "DECIMAL"),
        (BOOLEAN, "CHECKBOX"),
        (DATE, "DATE"),
        (URL, "URL"),
    )

    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    form_type = models.CharField(max_length=16, choices=FORM_TYPES)
    order = models.IntegerField(default=1)

    def save(self, **kwargs):
        if not self.id and (max_counter := Field.objects.filter(service=self.service).order_by("-order")):
            self.order = max_counter[0].order + 1 if max_counter else 1

        super(Field, self).save(**kwargs)

    def __str__(self):
        return f"{self.service}: {self.name} ({self.form_type})"

    def __repr__(self):
        return f"<Field: {str(self)}>"

class Form(PolymorphicModel):
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    value = None

    def __str__(self):
        return f"{self.object}: {self.field.name} - {self.value}"

class IntegerForm(Form):
    type = models.CharField(default="int", editable=False, max_length=3)
    value = models.IntegerField(default=0, null=True, blank=True)

class FloatForm(Form):
    type = models.CharField(default="float", editable=False, max_length=5)
    value = models.FloatField(default=0.0, null=True, blank=True)

class CharacterForm(Form):
    type = models.CharField(default="char", editable=False, max_length=4)
    value = models.CharField(max_length=255, default="", null=True, blank=True)

class TextForm(Form):
    type = models.CharField(default="text", editable=False, max_length=4)
    value = models.TextField(default="", null=True, blank=True)

class BooleanForm(Form):
    type = models.CharField(default="bool", editable=False, max_length=4)
    value = models.BooleanField(default=False, null=True, blank=True)

class DateForm(Form):
    type = models.CharField(default="date", editable=False, max_length=4)
    value = models.DateField()

class URLForm(Form):
    type = models.CharField(default="url", editable=False, max_length=4)
    value = models.URLField()
