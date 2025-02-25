from typing import List

from pydantic import BaseModel
from pydantic_factories import ModelFactory

from starlite import Starlite, get
from starlite.pagination import AbstractSyncClassicPaginator, ClassicPagination


class Person(BaseModel):
    id: str
    name: str


class PersonFactory(ModelFactory[Person]):
    __model__ = Person


# we will implement a paginator - the paginator must implement two methods 'get_total' and 'get_items'
# we would usually use a database for this, but for our case we will "fake" the dataset using a factory.


class PersonClassicPaginator(AbstractSyncClassicPaginator[Person]):
    def __init__(self) -> None:
        self.data = PersonFactory.batch(50)

    def get_total(self, page_size: int) -> int:
        return round(len(self.data) / page_size)

    def get_items(self, page_size: int, current_page: int) -> List[Person]:
        return [self.data[i : i + page_size] for i in range(0, len(self.data), page_size)][current_page - 1]


paginator = PersonClassicPaginator()


# we now create a regular handler. The handler will receive two query parameters - 'page_size' and 'current_page', which
# we will pass to the paginator.
@get("/people")
def people_handler(page_size: int, current_page: int) -> ClassicPagination[Person]:
    return paginator(page_size=page_size, current_page=current_page)


app = Starlite(route_handlers=[people_handler])
