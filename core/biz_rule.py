import requests
from core.models import Service, Field, Object,Form, TextForm, IntegerForm, FloatForm, BooleanForm, DateForm, URLForm, CharacterForm
from datetime import datetime
import traceback
# Error handling omitted for https requests for brevity
def _empty_all():
    form_list = [TextForm, IntegerForm, FloatForm, BooleanForm, DateForm, URLForm, CharacterForm]
    for form in form_list:
        form.objects.all().delete()
    Field.objects.all().delete()
    Object.objects.all().delete()
    Service.objects.all().delete()

def _date_converter(date_str):

    parsed = datetime.strptime(date_str, "%Y/%m/%d")
    formatted = parsed.strftime("%Y-%m-%d")
    return formatted


FORM_TYPE_MAP = {
    Field.CHAR: CharacterForm,
    Field.TEXT: TextForm,
    Field.INTEGER: IntegerForm,
    Field.FLOAT: FloatForm,
    Field.BOOLEAN: BooleanForm,
    Field.DATE: DateForm,
    Field.URL: URLForm,
}




def _add_field_value(obj: Object, field: Field, value):
    form_cls : Form = FORM_TYPE_MAP[field.form_type]
    # Simply using this line give creates a new field every time in the service 
    form_cls.objects.create(object=obj, field=field, value=value)


def _add_field(obj: Object, service: Service, name: str, description: str, form_type: str, value: str) -> Field:
    # Simply using this line give creates a new field every time in the service 
    # field = Field.objects.create(
    field = Field.objects.get_or_create(
        service=service,
        name=name,
        description=description,
        form_type=form_type
    )
    # if the field already exists, get_or_create returns a tuple (field, true/false)
    field = field[0]
    _add_field_value(obj=obj, field=field, value=value)


def _pokenmon_data():
    # This url gets a list of all pokemon card sets
    base_pokemon_url = "https://api.pokemontcg.io/v2/sets"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response = requests.get(f"{base_pokemon_url}", headers=headers)
    print(f"Finished API Call, {str(response.status_code)}")

    # the above is to get the data from the API

    # create a service, in the models.py given the hierarchy of the classes. The server is like a datatable 
    service = Service.objects.create(
        name="PokenmonSetCollection",
        description="Collection of Pokenmon Card Sets",
    )
    created_objects = [] 
    for pokemon_set in response.json()["data"]:
        # create an object for each pokemon set, like a row in the datatable
        obj = Object(service=service)
        obj.save() 
        created_objects.append(obj.human_id)
        # add fields to the object, like columns in the datatable
        _add_field(
            obj=obj,
            service=service,
            name="SetName",
            description="Name of the pokemon set",
            form_type=Field.TEXT,
            value=pokemon_set.get("name","")
        )
        _add_field(
            obj=obj,
            service=service,
            name="Series",
            description="Series of the pokemon set",
            form_type=Field.TEXT,
            value=pokemon_set.get("series","")
        )
        _add_field(
            obj=obj,
            service=service,
            name="TotalCards",
            description="Total number of cards in the set",
            form_type=Field.INTEGER,
            value=pokemon_set.get("printedTotal",0)
        )
        _add_field(
            obj=obj,
            service=service,
            name="ReleaseDate",
            description="Release date of the pokemon set",
            form_type=Field.DATE,
            value=_date_converter(pokemon_set.get("releaseDate",""))
        )
        _add_field(
            obj=obj,
            service=service,
            name="symbol",
            description="Pokemon set symbol URL",
            form_type=Field.URL,
            value=pokemon_set.get("images",{"symbol":""}).get("symbol","")
        )

        
def main():
    # 
    try:
        _pokenmon_data()
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print("delete everything")
        # only delete the created objects in this round if an error occurs
        _empty_all()
