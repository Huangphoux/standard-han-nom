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
        Link(rel="stylesheet", href="simple.css"),
        Script(src="htmx.min_2.0.8.js"),
        # CSS
        Style(
            "@font-face { font-family: gothic; src: url(_minh.woff2) format('woff2');}"
        ),
        Style("@view-transition { navigation: auto; }"),
        Style("* { font-family: gothic, system-ui, sans-serif; font-weight: normal; }"),
        Style(
            ".hide-cols { "
            + ", ".join([f"th:nth-child({i}), td:nth-child({i})" for i in (4, 5, 6)])
            + " {display: none;} }",
        ),
        Style("td { font-size: 2rem; } tr td:first-child { font-size: 10rem; }"),
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
