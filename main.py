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
        Link(rel="stylesheet", href="vendored/simple.css"),
        # CSS
        Style(
            "@font-face { font-family: gothic; src: url(_minh.woff2) format('woff2');}"
        ),
        Style("@view-transition { navigation: auto; } * { font-family: gothic; }"),
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
    'hướng-dẫn sử-dụng: tìm cụm "hướng dẫn" và "sử dụng".',
    "向引使用: tìm từng chữ.",
    "hướng-dẫn: tìm cụm từ.",
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
    search_term = search.lower().strip() if search else ""

    result: list[dict] = []
    mode: str = ""

    space_dash = " " in search_term and "-" in search_term
    space_only = " " in search_term and "-" not in search_term
    nospace_dash = " " not in search_term and "-" in search_term
    nospace_only = " " not in search_term and "-" not in search_term

    if space_dash:  # hướng-dẫn sử-dụng; hướng-dẫn sử
        mode = "tìm từng cụm được nối bằng kí tự gạch ngang (-)"

        for term in search_term.split(" "):
            term = term.replace("-", " ")

            for row in rows:
                if term == str(row["Reading"]).lower():
                    result.append(row)
                elif term in str(row["Examples"]):
                    result.append(row)
                    break

    if space_only:  # hướng dẫn sử dụng
        mode = "tìm chữ cho từng từ"

        for term in search_term.split(" "):
            for row in rows:
                if term == str(row["Reading"]).lower():
                    result.append(row)

    if nospace_dash:  # hướng-dẫn
        mode = "tìm cụm từ"

        for row in rows:
            if search_term.replace("-", " ") in str(row["Examples"]).lower():
                result.append(row)
                break

    if nospace_only:  # 向引使用
        mode = "tìm từng chữ"

        for term in list(search_term):
            for row in rows:
                if (
                    term in str(row["Character"])
                    or search_term == str(row["Reading"]).lower()
                ):
                    result.append(row)
                    break

    return (
        Titled(
            "Tìm chữ Hán Nôm",
            Body(hx_boost="true")(
                Details(role="button")(
                    Summary("Hướng dẫn sử dụng"),
                    H2("Cách sử dụng thanh tìm kiếm"),
                    Ul(*[Li(text) for text in how_to_search]),
                    H2("Ý nghĩa các kí hiệu"),
                    Ul(*[Li(text) for text in symbols]),
                ),
                Form(role="search", action=index, method="get")(
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
                            size="50",
                        ),
                        Input(type="submit", value="Tìm"),
                    ),
                ),
                Button(
                    "Hiện Ghi chú, Mã Unicode, và Lớp (cần JavaScript)",
                    _="on click toggle .hide-cols on <table/>",
                    type="button",
                ),
                P(f"Cách tìm: {mode}."),
                Table(_class="hide-cols")(
                    Thead(
                        Tr(
                            *(
                                Th(hdr)
                                for hdr in [
                                    "Chữ",
                                    "Cách đọc",
                                    "Ví dụ",
                                    "Ghi chú",
                                    "Mã Unicode",
                                    "Lớp",
                                ]
                            ),
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
        ),
    )
