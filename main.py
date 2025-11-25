from fasthtml.common import *
from brotli_asgi import BrotliMiddleware

from hnc import hnc

serve()

app, rt = fast_app(
    middleware=(Middleware(BrotliMiddleware),),
    htmx=False,
    surreal=False,
    pico=False,
    hdrs=(
        Link(rel="icon", href="https://fav.farm/❤️"),  # favicon
        # Vendored
        Link(rel="stylesheet", href="vendored/simple.css"),
        Script(src="htmx.min_2.0.8.js"),
        Script(src="idiomorph-ext.min_0.7.4.js"),
        Script(src="htmx-ext-preload.min_2.1.2.js"),
        # CSS
        Style(
            "@font-face { font-family: gothic; src: url(static/_minh.woff2) format('woff2');}"
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

hnc.to_app(app)


@rt
def index():
    return (
        Title("Công cụ Hán Nôm chuẩn"),
        # hx-boost targets <body>, and swap innerHTML
        Body(hx_boost="true", hx_ext="preload, morph", hx_swap="morph:innerHTML")(
            Header(
                H1("Công cụ Hán Nôm chuẩn"),
                P("Các công cụ làm việc với các chữ Hán Nôm chuẩn"),
            ),
            Main(
                A(P("Tra cứu chữ Hán Nôm →"), href="/hnc", preload=True),
            ),
            Footer(
                P(
                    "Tất cả tài nguyên liên quan đến chữ Hán Nôm Chuẩn (",
                    A(
                        "bảng chữ Hán Nôm Chuẩn",
                        href="https://www.hannom-rcv.org/standard-nom/Lookup-CHNC.html?uiLang=vi",
                    ),
                    ", ",
                    A(
                        "phông chữ Minh Nguyên",
                        href="https://github.com/TKYKmori/Minh-Nguyen",
                    ),
                    ") đều được cung cấp bởi ",
                    A(
                        "Hội Nghiên cứu và Ứng dụng Hán Nôm",
                        href="https://www.hannom-rcv.org/",
                    ),
                    ".",
                ),
                P(
                    "Trang web được làm bằng ",
                    (A("Python", href="https://www.python.org/")),
                    ", ",
                    (A("FastHTML", href="https://fastht.ml/")),
                    ", ",
                    A("htmx", href="https://htmx.org"),
                    ", ",
                    A("Simple.css", href="https://simplecss.org"),
                    " và ❤️ của ",
                    A("Huangphoux", href="https://github.com/Huangphoux"),
                    ".",
                ),
                P(
                    "Mã nguồn (200 dòng) của trang này nằm ở ",
                    (
                        A(
                            "đây",
                            href="https://github.com/Huangphoux/standard-han-nom/blob/main/main.py",
                        )
                    ),
                    " nè nha. ❤️",
                ),
            ),
        ),
    )
