from fasthtml.common import *
import csv


app, rt = fast_app()


with open("after-processing-list.csv", encoding="utf-8") as f:
    global reader, headers, rows
    reader = csv.DictReader(f, delimiter="\t")
    headers = reader.fieldnames or []
    rows = list(reader)


@rt
def search(search: Optional[str] = None):
    search_term = search.lower() if search else ""

    result = []

    if " " not in search_term:
        result = [row for row in rows if search_term == str(row["Reading"]).lower()]

    if " " in search_term:
        result = [row for row in rows if search_term in str(row["Examples"]).lower()]

    return (
        Tr(
            *[Td(entry[header]) for header in headers],
        )
        for entry in result
    )


@rt
async def index():
    return (
        Titled(
            "Công cụ tra cứu chữ Hán Nôm chuẩn",
            Body(
                Details(role="button")(
                    Summary("Giải thích cách sử dụng"),
                    P(
                        "Chỉ tìm được bằng chữ Quốc Ngữ, chưa tìm được bằng chữ Hán Nôm."
                    ),
                    P(
                        "Không khoảng cách, tìm chính xác từ đó trong cột Reading. Có khoảng cách, tìm trong cột Examples."
                    ),
                    P(
                        "Chữ hoa ở cột Âm đọc là âm Hán-Việt tiêu chuẩn của chữ Hán; chữ thường ở cột Âm đọc là cách đọc của chữ Nôm hoặc âm Hán-Việt không chuẩn của chữ Hán."
                    ),
                    P(
                        "Chữ Hán Nôm Chuẩn được hiển thị trong cột Chữ Hán Nôm. Các chữ Hán Nôm được sắp xếp theo cách đọc. Trong trường hợp cách đọc giống nhau, cái nào có ít số nét hơn thì xếp trước."
                    ),
                    P(
                        "[摱] nghĩa là một hoặc nhiều chữ Hán Nôm trong từ này được sử dụng để dịch âm. [嘆] nghĩa là từ này là thán từ; [俗] nghĩa là từ này là tiếng tục; [聲] nghĩa là từ này là từ tượng thanh; [𠸨] nghĩa là là từ láy."
                    ),
                    P(
                        'Trong cột Ghi chú, chữ Hán Nôm có cách đọc khác nhau nhưng nghĩa hoàn toàn giống nhau (một số là cách đọc phương ngữ) được biểu thị với kí hiệu ⇔. Chữ dị thể thường gặp trong lịch sử của chữ Hán Nôm Chuẩn được biểu thị với kí hiệu [異]. Chữ Phiên âm được biểu thị với kí hiệu [翻]. Chữ Phiên âm là các chữ được chọn từ các chữ Hán Nôm Chuẩn dùng để phiên âm, chức năng của chữ Phiên âm tương tự như phiến giả danh (ca-ta-ca-na) tiếng Nhật, khi được sử dụng để phiên âm, chúng chỉ biểu âm và mất đi ý nghĩa. Thanh điệu của mỗi chữ Phiên âm là thanh ngang hoặc thanh sắc theo mặc định, và thanh điệu có thể thay đổi tự do theo tình hình thực tế. Để biết chi tiết về chữ Phiên âm, vui lòng tham khảo Phụ Lục. Số thập lục phân đằng sau "U+" cho biết Mã Thống nhất của chữ Hán Nôm Chuẩn này.'
                    ),
                ),
                Input(
                    type="search",
                    name="search",
                    placeholder="Tra cứu chữ Hán Nôm chuẩn",
                    hx_post=search,
                    hx_trigger="input changed delay:500ms, keyup[key=='Enter']",
                    hx_target="#search",
                ),
                Table(
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
                    Tbody(id="search")(),
                ),
            ),
        ),
    )


serve()
