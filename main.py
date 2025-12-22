from fasthtml.common import *
from brotli_asgi import BrotliMiddleware
import csv
from loguru import logger


app, rt = fast_app(
    middleware=(Middleware(BrotliMiddleware),),
    htmx=False,
    surreal=False,
    pico=False,
    hdrs=(
        Link(rel="icon", href="https://fav.farm/❤️"),  # favicon
        Link(rel="stylesheet", href="style.css"),
        # Vendored
        Link(rel="stylesheet", href="simple@2.3.7.css"),
        Script(src="htmx@2.0.8.js"),
        Script(src="morph@0.7.4.js"),
        Script(src="preload@2.1.2.js"),
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
        Body(hx_boost="true", hx_ext="morph", hx_swap="morph:innerHTML")(
            Header(
                Nav(
                    A("Trang chủ", href="/"),
                ),
                H1("Tìm chữ Hán Nôm"),
                P("Tìm bằng chữ Quốc Ngữ, tra kết quả ra chữ Hán Nôm"),
            ),
            Main(hx_ext="preload")(
                Form(role="search", action=index, method="get", preload=True)(
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
                            hx_get="/",
                            hx_trigger="input changed delay:500ms, keyup[key=='Enter'], load",
                            hx_target="body",
                            hx_push_url="true",
                        ),
                        Input(
                            type="submit",
                            value="Tìm kiếm",
                            preload=True,
                        ),
                    )
                ),
                Table(
                    Thead(
                        Tr(
                            Th("Chữ"),
                            Th("Ví dụ"),
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
                    " và ",
                    A(
                        "phông chữ Minh Nguyên",
                        href="https://github.com/TKYKmori/Minh-Nguyen",
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
                    "Mã nguồn (146 dòng) của trang này nằm ở ",
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
