from fasthtml.common import *


navbar = Nav(
    A("Trang chủ", href="/"),
    A("Tìm kiếm", href="/hnc"),
)

footer = Footer(
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
)
