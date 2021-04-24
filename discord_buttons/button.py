from discord import InvalidArgument

from typing import Union, Optional
from uuid import uuid1
from random import randint


__all__ = ("ButtonStyle", "Button")


class ButtonStyle:
    blue = 1
    gray = 2
    grey = 2
    green = 3
    red = 4
    URL = 5

    @classmethod
    def randomColor(cls) -> int:
        return randint(1, cls.red)

    @classmethod
    def to_dict(cls) -> dict:
        return {
            "blue": cls.blue,
            "gray": cls.gray,
            "green": cls.green,
            "red": cls.red,
            "URL": cls.URL,
        }


class Button:
    __slots__ = ("_style", "_label", "_id", "_url")

    def __init__(
        self,
        *,
        label: str,
        style: int = ButtonStyle.gray,
        id: Optional[str] = None,
        url: Optional[str] = None,
    ):
        if style == ButtonStyle.URL and not url:
            raise InvalidArgument("You must provide a URL when the style is URL")
        if style == ButtonStyle.URL and id:
            raise InvalidArgument("You musn't use both id and url")
        if not (1 <= style <= ButtonStyle.URL):
            raise InvalidArgument(f"style must be in between 1, {ButtonStyle.URL}")

        if not len(label):
            raise InvalidArgument("Label musn't be empty")

        self._style = style
        self._label = label
        self._url = url

        if not self.style == ButtonStyle.URL:
            self._id = id or str(uuid1())
        else:
            self._id = None

    def to_dict(self) -> dict:
        return {
            "type": 2,
            "style": self.style,
            "label": self.label,
            "custom_id": self.id,
            "url": self.url if self.style == ButtonStyle.URL else None,
        }

    @property
    def style(self) -> int:
        return self._style

    @property
    def label(self) -> str:
        return self._label

    @property
    def id(self) -> str:
        return self._id

    @property
    def url(self) -> str:
        return self._url

    @label.setter
    def label(self, value: str):
        if not len(value):
            raise InvalidArgument("Label musn't be empty")

        self._label = value

    @url.setter
    def url(self, value: str):
        if self.style != ButtonStyle.URL:
            raise InvalidArgument("button style is not URL")

        self._url = value

    @id.setter
    def id(self, value: str):
        if self.style == ButtonStyle.URL:
            raise InvalidArgument("button style is URL")

        self._id = id

    def __repr__(self) -> str:
        id_st = f"id='{self.id}'" if self.id else ""
        url_st = f"url='{self.url}'" if self.url else ""
        return f"<Button style={self.style} label='{self.label}' {url_st} {id_st}>"

    def __str__(self) -> str:
        return self.__repr__()
