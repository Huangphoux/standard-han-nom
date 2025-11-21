import asyncio
import csv

from fasthtml.common import *
# from monsterui.all import *

from datastar_py import attribute_generator as data
from datastar_py.fasthtml import (
    DatastarResponse,
    ServerSentEventGenerator as SSE,
    datastar_response,
)


app, rt = fast_app(
    htmx=False,
    surreal=False,
    live=False,
    hdrs=(
        # Theme.green.headers(),
        Script(
            type="module",
            src="vendored/datastar_v1.0.0-RC.6.js",
        ),
    ),
)

with open("after-processing-list.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    global headers
    headers = reader.fieldnames or []

# result = [r for r in rows if r["column"] == "value"]


@rt
async def index():
    return (
        Titled(
            "Công cụ tra cứu chữ Hán Nôm chuẩn",
            Body(id="morph")(
                Input(
                    data.bind("search"),
                    data.on(
                        "input__debounce.200ms",
                        "@get('/examples/active_search/search')",
                    ),
                    type="search",
                    name="search",
                    placeholder="Gõ vô chỗ này để tìm chữ Hán Nôm",
                ),
                Table(
                    Thead(
                        Tr(
                            *[Th(hdr.capitalize()) for hdr in headers],
                        )
                    ),
                    Tbody(),
                ),
            ),
        ),
    )


serve() # switch to hypercorn
