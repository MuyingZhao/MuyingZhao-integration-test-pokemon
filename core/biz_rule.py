import requests
from core.models import Service, Field, Object,Form, TextForm, IntegerForm, FloatForm, BooleanForm, DateForm, URLForm, CharacterForm
from datetime import datetime
#show detailed error messages
import traceback
# The secret should be added to gitignore, but keep it here for running the code
from core.secret import api_key
import hashlib


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

def _date_converter_marvel(date_str):

    parsed = datetime.strptime(date_str, "%Y-%m-%d")
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
    api_key = api_key.get("poken_key","")
    base_pokemon_url = "https://api.pokemontcg.io/v2/sets"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Api-Key": api_key
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

def _marvel_data():
    # variables for the API call
    # URL, API KEY
    comics_marvel_url = "https://gateway.marvel.com/v1/public/comics"
    public_key = api_key.get("marvel_public_key","")
    private_key = api_key.get("marvel_private_key","")
    ts = str(datetime.now().timestamp())
    # hash — a md5 digest of the ts parameter, your private key and your public key (e.g, md5(ts+privateKey+publicKey)
    hash_input = ts + private_key + public_key
    hash_result = hashlib.md5(hash_input.encode()).hexdigest()
    params = { "apikey": public_key, "ts": ts, "hash": hash_result}

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # make the request to get the data 
    response = requests.get(f"{comics_marvel_url}", headers=headers, params=params)
    print(f"Finished API Call, {str(response.status_code)}")
    

    # create a service, which is the virutal table 
    service = Service.objects.create(
        name="MarvelComicsCollection",
        description="Collection of Marvel Comics books",
    )

    created_objects = [] 
    for marvel_comic in response.json()["data"]["results"]:
        # create an object for each marvel comic book, like a row in the datatable
        obj = Object(service=service)
        obj.save() 
        created_objects.append(obj.human_id)
        # add fields to the object, like columns in the datatable
        _add_field(
            obj=obj,
            service=service,
            name="title",
            description="Name of the Marvel comic book",
            form_type=Field.TEXT,
            value=marvel_comic.get("title","")
        )
        _add_field(
            obj=obj,
            service=service,
            name="pageCount",
            description="The number of pages of the Marvel comic book",
            form_type=Field.TEXT,
            value=marvel_comic.get("pageCount","")
        )
        _add_field(
            obj=obj,
            service=service,
            name="resourceURI",
            description="The resource URI of the Marvel comic book",
            form_type=Field.URL,
            value=marvel_comic.get("resourceURI","")
        )
        # _add_field(
        #     obj=obj,
        #     service=service,
        #     name="focDate",
        #     description=" Final Order Cutoff date of the Marvel comic book",
        #     form_type=Field.DATE,
        #     value= _date_converter_marvel([date for date in marvel_comic["dates"] if date["type"] == "focDate"][0].get("date",""))
        # )
        _add_field(
            obj=obj,
            service=service,
            name="price",
            description="The print price of the Marvel comic book",
            form_type=Field.FLOAT,
            value= [price for price in marvel_comic["prices"] if price["type"] == "printPrice"][0].get("price",0.0)
        )
        

def main():
    # 
    try:
        #_pokenmon_data()
        _marvel_data()
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print("delete everything")
        # only delete the created objects in this round if an error occurs
        #_empty_all()
