from fasthtml.common import *
from brotli_asgi import BrotliMiddleware
import csv
from loguru import logger


app, rt = fast_app(
    middleware=(Middleware(BrotliMiddleware, quality=7),),
    default_hdrs=False,
    hdrs=(
        # Link(rel="icon", href="https://fav.farm/❤️"),  # favicon
        Link(rel="stylesheet", href="style.css"),
        # Vendored
        Link(rel="stylesheet", href="simple@2.3.7.css"),
        Script(src="htmx@2.0.8.js"),
    ),
    htmlkw={"lang": "vi"},
    static_path="static",
)

serve()


logger.remove()
logger.add("logs/standard_han_nom_debug.log")

with open("csv/after-processing-list.csv", encoding="utf-8") as f:
    global reader, headers, rows
    reader = csv.DictReader(f)
    headers = reader.fieldnames or []
    rows = list(reader)


@rt("/")
def index(search: Optional[str] = None):
    if not search:  # để trống
        result = []
    else:
        result: list[dict] = []

        for term in search.lower().strip().split(" "):
            result.extend(row for row in rows if term == row["Reading"].lower())

        logger.debug(result)

    return (
        Title("Tìm kiếm chữ Hán Nôm"),
        Body(hx_boost="true", hx_swap="show:none")(
            Header(
                Nav(A("Trang chủ", href="/")),
                H1("Tìm chữ Hán Nôm"),
                P("Tìm bằng chữ Quốc Ngữ, tra ra chữ Hán Nôm"),
            ),
            Main(
                Form(role="search", action=index, method="get")(
                    Fieldset(
                        Label(
                            "Tìm chữ Hán Nôm",
                        ),
                        Input(
                            value=search.strip() if search else "",
                            type="search",
                            name="search",
                            maxlength="140",
                            size="40",
                            placeholder="Gõ chữ Quốc Ngữ vào đây",
                            required=True,
                            autofocus=True,
                            onfocus="let temp=this.value; this.value=''; this.value=temp",
                        ),
                        Input(
                            Img(
                                id="loading",
                                _class="htmx-indicator",
                                src="180-ring.svg",
                                alt="Loading...",
                            ),
                            type="submit",
                            value="Tìm kiếm",
                        ),
                    ),
                ),
                Table(
                    Thead(
                        Tr(
                            Th(
                                "Chữ",
                            ),
                            Th(
                                "Ví dụ",
                            ),
                        )
                    ),
                    Tbody()(
                        *[
                            Tr(
                                *[
                                    Td(entry[header])
                                    for header in ("Character", "Examples")
                                ],
                            )
                            for entry in result
                        ]
                    ),
                )
                if result
                else None,
            ),
            Footer(
                P(
                    A(
                        "Bảng chữ Hán Nôm Chuẩn",
                        href="https://www.hannom-rcv.org/standard-nom/Lookup-CHNC.html?uiLang=vi",
                    ),
                    " được cung cấp bởi ",
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
                    "Mã nguồn (135 dòng) của trang này nằm ở ",
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
