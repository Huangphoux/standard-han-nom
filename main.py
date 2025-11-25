from fasthtml.common import *
from brotli_asgi import BrotliMiddleware

import csv


app, rt = fast_app(
    middleware=(
        Middleware(
            BrotliMiddleware,
            quality=6,  # compression speed vs compression density
            mode="font",  # "generic", "text" or "font"
            lgwin=22,  # Base 2 logarithm of the sliding window size. Range is 10 to 24.
            lgblock=0,  # Base 2 logarithm of the maximum input block size. Range is 16 to 24.
            minimum_size=400,  # Only compress responses that are bigger than this value in bytes.
            gzip_fallback=False,
        ),
    ),
    htmx=False,
    surreal=False,
    pico=False,
    hdrs=(
        Link(rel="icon", href="https://fav.farm/❤️"),  # favicon
        # Vendored
        Script(src="vendored/htmx.min_2.0.8.js"),
        Script(src="vendored/_hyperscript.min_0.9.14.js"),
        Script(src="vendored/idiomorph-ext.min_0.7.4.js"),
        Script(src="vendored/htmx-ext-preload.min_2.1.2.js"),
        Link(rel="stylesheet", href="vendored/simple.css"),
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
        Style(" td { font-size: 2rem; } tr td:first-child { font-size: 10rem; } "),
    ),
    htmlkw={"lang": "vi"},
)

serve()


with open("after-processing-list.csv", encoding="utf-8") as f:
    global reader, headers, rows
    reader = csv.DictReader(f, delimiter="\t")
    headers = reader.fieldnames or []
    rows = list(reader)


how_to_search = (
    "hướng dẫn sử dụng: tìm chữ cho từng từ.",
    "向: tìm chữ.",
    "hướng: tìm từ.",
)

symbols = (
    "Chữ hoa: âm Hán-Việt tiêu chuẩn.",
    "Chữ thường: cách đọc chữ Nôm, âm Hán-Việt không chuẩn.",
    "Xếp các chữ theo cách đọc, sau đó ưu tiên ít nét nhất.",
    "[摱] mượn để ghi âm.",
    "[嘆] thán từ.",
    "[俗] từ tục.",
    "[聲] từ tượng thanh.",
    "[𠸨] từ láy.",
    "⇔: chữ đọc khác nhưng nghĩa giống (một số là cách đọc phương ngữ).",
    "[異] dị thể trong lịch sử.",
    "[翻] chữ phiên âm, dùng để phiên âm, giống Ca-ta-ca-na của tiếng Nhật.",
    "Khi dùng để phiên âm, chúng giữ âm và mất nghĩa. Thanh ngang hoặc sắc.",
)


@rt
def index(search: Optional[str] = None):
    return home(search)


@timed_cache()
def home(search: Optional[str] = None):
    result = query(search)

    return (
        Title("Tìm chữ Hán Nôm"),
        # hx-boost targets <body>, and swap innerHTML
        Body(hx_boost="true", hx_ext="preload, morph", hx_swap="morph:innerHTML")(
            Header(
                H1("Tìm chữ Hán Nôm"),
                P("Công cụ tra cứu chữ Hán Nôm chuẩn"),
            ),
            Main(
                Details(
                    Summary("Hướng dẫn sử dụng"),
                    H2("Cách sử dụng thanh tìm kiếm"),
                    Ul(*[Li(text) for text in how_to_search]),
                    H2("Ý nghĩa các kí hiệu"),
                    Ul(*[Li(text) for text in symbols]),
                ),
                search_form(search),
                Button(
                    "Hiện Ghi chú, Mã Unicode, và Lớp (cần JavaScript)",
                    _="on click toggle .hide-cols on <table/>",
                    type="button",
                )
                if search
                else None,
                render_table(result),
            ),
            footer(),
        ),
    )


@timed_cache()
def query(search: Optional[str] = None):
    search_term = search.lower().strip() if search else ""

    result: list[dict] = []

    if " " in search_term:  # hướng dẫn sử dụng
        for term in search_term.split(" "):
            for row in rows:
                if term == str(row["Reading"]).lower():
                    result.append(row)
    elif not search_term:
        result = []
    else:  # 向, người
        for row in rows:
            if (
                search_term in str(row["Character"])
                or search_term == str(row["Reading"]).lower()
            ):
                result.append(row)

    return result


@timed_cache()
def search_form(search: Optional[str] = None):
    return (
        Form(role="search", action=index, method="get", preload=True)(
            Fieldset(role="group")(
                Label(_for="search")("Tìm chữ Hán Nôm"),
                Input(
                    id="search",
                    value=search.strip() if search else "",
                    type="search",
                    name="search",
                    maxlength="140",
                    placeholder="Gõ chữ Quốc Ngữ vào đây",
                    autofocus=True,
                    required=True,
                    onfocus="var temp_value=this.value; this.value=''; this.value=temp_value",
                    size="40",
                    autocomplete="on",
                ),
                Input(type="submit", value="Tìm", preload=True),
            ),
        ),
    )


@timed_cache()
def render_table(result: list[dict]):
    if not result:
        return None

    return (
        Table(_class="hide-cols")(
            Thead(
                Tr(
                    Th("Chữ"),
                    Th("Cách đọc"),
                    Th("Ví dụ"),
                    Th("Ghi chú"),
                    Th("Mã Unicode"),
                    Th("Lớp"),
                )
            ),
            Tbody()(
                *[
                    Tr(
                        *[Td(entry[header]) for header in headers],
                    )
                    for entry in result
                ]
            ),
        ),
    )


def footer():
    return (
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
                A("hyperscript", href="https://hyperscript.org"),
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
    )
