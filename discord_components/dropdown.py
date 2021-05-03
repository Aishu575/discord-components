from discord import InvalidArgument, PartialEmoji

from typing import List
from uuid import uuid1

from .component import Component


__all__ = ("Dropdown", "Option")


class Option:
    """The dropdown option

    Parameters
    ----------
    label: :class:`str`
        The option's label
    value: :class:`str`
        The option's value
    emoji: :class:`discord.PartialEmoji`
        The option's emoji
    description: :class:`str`
        The option's description
    default: :class:`bool`
        If the option is default
    """

    __slots__ = ("_label", "_value", "_emoji", "_description", "_default")

    def __init__(
        self,
        *,
        label: str,
        value: str,
        emoji: PartialEmoji = None,
        description: str = None,
        default: bool = False,
    ):
        self._label = label
        self._value = value
        self._description = description
        self._default = default

        if isinstance(emoji, PartialEmoji):
            self._emoji = emoji
        elif isinstance(emoji, str):
            self._emoji = PartialEmoji(name=emoji)
        else:
            self._emoji = None

    def to_dict(self) -> dict:
        """
        Converts the dropdown option information required for API request to dict and returns

        :returns: :class:`dict`
        """

        data = {
            "label": self.label,
            "value": self.value,
            "description": self.description,
            "default": self.default,
        }
        if self.emoji:
            data["emoji"] = self.emoji.to_dict()
        return data

    @property
    def label(self) -> str:
        """:class:`str`: The option's label"""
        return self._label

    @property
    def value(self) -> str:
        """:class:`str`: The option's value"""
        return self._value

    @property
    def emoji(self) -> PartialEmoji:
        """:class:`discord.PartialEmoji`: The option's emoji"""
        return self._emoji

    @property
    def description(self) -> str:
        """:class:`str`: The option's description"""
        return self._description

    @property
    def default(self) -> bool:
        """:class:`bool`: If the option is default"""
        return self._default

    @label.setter
    def label(self, value: str):
        if not len(value):
            raise InvalidArgument("Label musn't be empty")

        self._label = value

    @value.setter
    def value(self, value: str):
        self._value = value

    @emoji.setter
    def emoji(self, emoji: PartialEmoji):
        if isinstance(emoji, PartialEmoji):
            self._emoji = emoji
        elif isinstance(emoji, str):
            self._emoji = PartialEmoji(name=emoji)

    @description.setter
    def description(self, value: str):
        self._description = value

    @default.setter
    def default(self, value: bool):
        self._default = value

    def __repr__(self) -> str:
        emoji_st = f"emoji={str(self.emoji)}" if self.emoji else ""
        description_st = f"description='{self.description}'" if self.description else ""
        default_st = f"default={self.default}" if self.default else ""

        return f"<Button label='{self.label}' value='{self.value}' {emoji_st} {description_st} {default_st}>"

    def __str__(self) -> str:
        return self.__repr__()

    @staticmethod
    def from_json(data: dict):
        """Create option instance from json

        :returns: :class:`~discord_components.Option`

        Parameters
        ----------
        data: :class:`dict`
            The json
        """

        emoji = data.get("emoji")
        return Option(
            label=data["label"],
            value=data["value"],
            emoji=PartialEmoji(
                name=emoji["name"], animated=emoji.get("animated", False), id=emoji.get("id")
            )
            if emoji
            else None,
            description=data.get("description"),
            default=data.get("default", False),
        )


class Dropdown(Component):
    """The dropdown

    Parameters
    ----------
    options: List[:class:`~discord_components.Option`]
        The dropdown's options
    id: :class:`str`
        The dropdown's id
    """

    __slots__ = ("_id", "_options")

    def __init__(self, *, options: List[Option], id: str = None):
        if (not len(options)) or (len(options) > 25):
            raise InvalidArgument("options length should be between 1 and 25")

        self._id = id or str(uuid1())
        self._options = options

    def to_dict(self) -> dict:
        """
        Converts the dropdown information required for API request to dict and returns

        :returns: :class:`dict`
        """

        return {
            "type": 3,
            "options": list(map(lambda option: option.to_dict(), self.options)),
            "custom_id": self.id,
        }

    @property
    def id(self) -> str:
        """:class:`str`: The dropdown's id"""
        return self._id

    @property
    def options(self) -> List[Option]:
        """List[:class:`~discord_components.Option`]: The dropdown's options"""
        return self._options

    @id.setter
    def id(self, value: str):
        self._id = value

    @options.setter
    def options(self, value: List[Option]):
        if (not len(value)) or (len(value) > 25):
            raise InvalidArgument("options length should be between 1 and 25")

        self._options = value

    def __repr__(self) -> str:
        return f"<Button id='{self.id}' options=[{', '.join(map(lambda x: str(x), self.options))}]"

    def __str__(self) -> str:
        return self.__repr__()

    @staticmethod
    def from_json(data: dict):
        """Create dropdown instance from json

        :returns: :class:`~discord_components.Dropdown`

        Parameters
        ----------
        data: :class:`dict`
            The json
        """

        return Dropdown(
            id=data["custom_id"], options=list(map(lambda x: Option.from_json(x), data["options"]))
        )
