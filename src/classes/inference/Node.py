from __future__ import print_function
from __future__ import absolute_import

from .SamplerUtils import *

TEXT_PLACE_HOLDER = "[]"

class Node:

    def __init__(self, key, parent_node, content_holder):
        self.key = key
        self.parent = parent_node
        self.children = []
        self.content_holder = content_holder

    def add_child(self, child):
        self.children.append(child)

    def show(self):
        for child in self.children:
            child.show()

    def rendering_function(self, key, value):
        if key.find("btn") != -1:
            value = value.replace(TEXT_PLACE_HOLDER, SamplerUtils.get_random_text())
        elif key.find("title") != -1:
            value = value.replace(TEXT_PLACE_HOLDER, SamplerUtils.get_random_text(length_text=5, space_number=0))
        elif key.find("text") != -1:
            value = value.replace(TEXT_PLACE_HOLDER,
                                  SamplerUtils.get_random_text(length_text=56, space_number=7, with_upper_case=False))
        return value

    def render(self, mapping, rendering_function=None):
        content = ""
        for child in self.children:
            placeholder = child.render(mapping, self.rendering_function)
            if placeholder is None:
                self = None
                return
            else:
                content += placeholder

        value = mapping.get(self.key, None)

        if value is None:
            self = None
            return None

        if rendering_function is not None:
            value = self.rendering_function(self.key, value)

        if len(self.children) != 0:
            value = value.replace(self.content_holder, content)

        return value