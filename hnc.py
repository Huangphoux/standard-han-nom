from fasthtml.common import *
import csv

hnc = APIRouter()


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


@hnc.get("/hnc")
def index_hnc(search: Optional[str] = None):
    return render_hnc(search)


@timed_cache()
def render_hnc(search: Optional[str] = None):
    search_term = search.lower().strip() if search else ""

    result: list[dict] = []

    if " " in search_term:  # hướng dẫn sử dụng
        for term in search_term.split(" "):
            for row in rows:
                if term == str(row["Reading"]).lower() and row not in result:
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
    return (
        Title("Tìm chữ Hán Nôm"),
        # hx-boost targets <body>, and swap innerHTML
        Body(hx_boost="true", hx_ext="preload, morph", hx_swap="morph:innerHTML")(
            Header(
                H1("Tìm chữ Hán Nôm"),
                P("Công cụ tra cứu chữ Hán Nôm chuẩn"),
            ),
            Main(
                A(P("← Quay lại trang chủ"), href="/", preload=True),
                Details(
                    Summary("Hướng dẫn sử dụng"),
                    H2("Cách sử dụng thanh tìm kiếm"),
                    Ul(*[Li(text) for text in how_to_search]),
                    H2("Ý nghĩa các kí hiệu"),
                    Ul(*[Li(text) for text in symbols]),
                ),
                Form(
                    role="search",
                    action=index_hnc,
                    method="get",
                    preload=True,
                    hx_indicator="#loading",
                )(
                    Fieldset(role="group")(
                        Label(_for="search")("Tìm chữ Hán Nôm"),
                        Input(
                            id="search",
                            value=search.strip() if search else "",
                            type="search",
                            name="search",
                            maxlength="140",
                            size="40",
                            placeholder="Gõ chữ Quốc Ngữ vào đây",
                            autofocus=True,
                            required=True,
                            onfocus="let temp=this.value; this.value=''; this.value=temp",
                        ),
                        Input(
                            type="submit",
                            value="Tìm",
                            hx_disabled_elt="this",
                        ),
                    ),
                ),
                Button(
                    "Hiện Ghi chú, Mã Unicode, và Lớp (cần JavaScript)",
                    onclick="document.querySelector('table').classList.toggle('hide-cols')",
                    type="button",
                )
                if search
                else None,  # hide button if no result
                Div(_class="htmx-indicator", id="loading")("(Đang tìm kiếm …)"),
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
                )
                if result
                else None,  # hide table if no result
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
