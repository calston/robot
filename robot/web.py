import json
import inspect

from twisted.web.template import renderer, XMLFile
from twisted.python.filepath import FilePath
from twisted.web.static import File

from twisted.web.template import tags

from .web_base import BaseResource, ContentElement, JSONResource


class Index(BaseResource):
    isLeaf = True

    class Content(ContentElement):
        loader = XMLFile(FilePath('robot/resources/index.html'))

