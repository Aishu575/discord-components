from typing import List, Union, Optional

from discord import File

from aiohttp import FormData
from json import dumps

from .component import ActionRow, Component


__all__ = ("_get_components_json",)


def _get_components_json(
    components: List[Union[ActionRow, Component, List[Component]]] = None
) -> Optional[List[dict]]:
    if components is None:
        return None

    for i in range(len(components)):
        if isinstance(components[i], list):
            components[i] = ActionRow(*components[i])
        elif not isinstance(components[i], ActionRow):
            components[i] = ActionRow(components[i])

    lines = components
    return [row.to_dict() for row in lines] if lines else []


def form_files(data: dict, files: List[File] = None) -> FormData:
    form = FormData()
    form.add_field("payload_json", dumps(data))
    for i in range(len(files)):
        form.add_field(
            f"file{i if len(files) > 1 else ''}",
            files[i].fp,
            filename=files[i].filename,
            content_type="application/octet-stream",
        )
    return form
