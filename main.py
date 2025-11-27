from fasthtml.common import *
from brotli_asgi import BrotliMiddleware
from search_chnc import chnc

from shared import navbar, footer

app, rt = fast_app(
    middleware=(Middleware(BrotliMiddleware),),
    htmx=False,
    surreal=False,
    pico=False,
    hdrs=(
        Link(rel="icon", href="https://fav.farm/❤️"),  # favicon
        # Vendored
        Link(rel="stylesheet", href="simple_2.3.7.css"),
        Link(rel="stylesheet", href="style.css"),
        Script(src="htmx.min_2.0.8.js"),
    ),
    htmlkw={"lang": "vi"},
    static_path="static",
)

chnc.to_app(app)


@rt
def index():
    return (
        Title("Công cụ Hán Nôm chuẩn"),
        Body(hx_boost="true")(
            Header(
                navbar,
                H1("Công cụ Hán Nôm chuẩn"),
                P("Công cụ làm việc với chữ Hán Nôm chuẩn"),
            ),
            Main(),
            footer,
        ),
    )


serve()
