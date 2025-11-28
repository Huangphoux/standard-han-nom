from fasthtml.common import *
import csv
from shared import navbar, footer
from loguru import logger


logger.remove()
logger.add("logs/search_chnc_debug.log")

chnc = APIRouter()

with open("csv/after-processing-list.csv", encoding="utf-8") as f:
    global reader, headers, rows
    reader = csv.DictReader(f)
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


@chnc.get("/hnc")
def index_hnc(search: Optional[str] = None):
    return render_hnc(search)


@timed_cache()
def get_result(search):
    if not search:  # để trống
        return []

    result: list[dict] = []

    for term in search.lower().strip().split(" "):
        result.extend(row for row in rows if term == row["Reading"].lower())

    logger.debug(result)

    return result


@timed_cache()
def render_hnc(search):
    result = get_result(search)

    return (
        Title("Tìm chữ Hán Nôm"),
        Body(hx_boost="true")(
            Header(
                navbar,
                H1("Tìm chữ Hán Nôm"),
                P("Tra cứu chữ Hán Nôm chuẩn"),
            ),
            Main(
                Form(
                    role="search",
                    action=index_hnc,
                    method="get",
                    hx_indicator="#loading",
                )(
                    Fieldset(
                        P(
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
                        ),
                        Input(type="submit", value="Tìm kiếm"),
                        Span(_class="htmx-indicator", id="loading")(
                            "(Đang tìm kiếm …)"
                        ),
                    ),
                ),
                Figure(
                    Table(
                        Thead(
                            Tr(
                                Th("Chữ"),
                                Th("Cách đọc"),
                                Th("Ví dụ"),
                                Th("Ghi chú"),
                                Th("Mã Unicode"),
                                Th("Chữ giản thể"),
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
                    else None
                ),  # hide table if no result
                Details(
                    Summary("Hướng dẫn sử dụng"),
                    H2("Cách sử dụng thanh tìm kiếm"),
                    Ul(*[Li(text) for text in how_to_search]),
                    H2("Ý nghĩa các kí hiệu"),
                    Ul(*[Li(text) for text in symbols]),
                ),
            ),
            footer,
        ),
    )
