import streamlit as st
from datetime import datetime
from io import BytesIO
import unicodedata
import re
import os
import json
import urllib.request
import urllib.error
st.image("logo.jpg")


# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Lucky Tea",
    page_icon="🧋",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# OPENROUTER AI
# =========================================================

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "openrouter/auto"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

try:
    if not OPENROUTER_API_KEY:
        OPENROUTER_API_KEY = st.secrets.get(
            "OPENROUTER_API_KEY",
            ""
        )
except Exception:
    pass


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .lucky-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 0px;
    }

    .lucky-subtitle {
        text-align: center;
        font-size: 17px;
        margin-bottom: 20px;
    }

    .total-box {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 2px solid rgba(128,128,128,0.35);
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .total-title {
        font-size: 18px;
        font-weight: 600;
    }

    .total-money {
        font-size: 32px;
        font-weight: 800;
    }

    .bill-number {
        text-align: center;
        font-size: 23px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .ai-status {
        padding: 8px 12px;
        border-radius: 10px;
        border: 1px solid rgba(128,128,128,.3);
        margin-bottom: 10px;
        text-align: center;
    }

    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 45px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# MENU
# =========================================================

DRINK_INFO = {

    "Trà sữa truyền thống": {
        "price": 25000,
        "sold": 950,
        "new": False,
        "tags": ["tra sua", "beo", "ngot"],
        "desc": "Vị cổ điển, béo nhẹ, dễ uống."
    },

    "Trà sữa trân châu": {
        "price": 30000,
        "sold": 1200,
        "new": False,
        "tags": ["tra sua", "beo", "ngot", "tran chau"],
        "desc": "Món quốc dân: trà sữa kèm trân châu dai dai."
    },

    "Trà sữa matcha": {
        "price": 30000,
        "sold": 700,
        "new": False,
        st.session_state.bill_number = 1

if "chat" not in st.session_state:
    st.session_state.chat = [
        {
            "role": "assistant",
            "content": (
                "Xin chào! 👋 Mình là trợ lý AI của **Lucky Tea** 🧋\n\n"
                "Bạn có thể hỏi mình:\n\n"
                "• Món nào bán chạy?\n"
                "• Món nào dưới 30k?\n"
                "• Món nào thanh mát?\n"
                "• Mình thích béo nhưng ít ngọt thì uống gì?\n"
                "• Tư vấn cho mình một ly nhé!\n"
                "• Topping nào hợp với trà sữa?"
            ),
            "drinks": []
        }
    ]


# =========================================================
# HÀM TIỆN ÍCH
# =========================================================

def format_money(number):
    return f"{number:,.0f} VNĐ".replace(",", ".")


def pdf_money(number):
    return f"{number:,.0f} VND".replace(",", ".")


def remove_accents(text):
    text = str(text)
    text = text.replace("đ", "d").replace("Đ", "D")

    text = unicodedata.normalize(
        "NFD",
        text
    )

    return "".join(
        ch for ch in text
        if unicodedata.category(ch) != "Mn"
    )


def normalize(text):
    return remove_accents(text).lower()


def clean_words(text):
    return re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )


def has_keyword(text, keywords):
    padded = f" {text} "

    return any(
        f" {word} " in padded
        for word in keywords
    )


def get_bill_number():
    return f"HD{st.session_state.bill_number:04d}"


def calculate_cup_price(item):

    topping_total = sum(
        TOPPINGS[t]
        for t in item["toppings"]
    )

    return (
        item["price"]
        + SIZES[item["size"]]
        + topping_total
    )


def calculate_item_total(item):
    return (
        calculate_cup_price(item)
        * item["quantity"]
    )


def calculate_total():

    return sum(
        calculate_item_total(item)
        for item in st.session_state.cart
    )


def total_cups():

    return sum(
        item["quantity"]
        for item in st.session_state.cart
    )


def drink_badges(name):

    info = DRINK_INFO[name]

    badges = []

    if name in BESTSELLERS:
        badges.append("🔥 Bán chạy")

    if info["new"]:
        badges.append("🆕 Mới")

    if info["price"] <= CHEAP_LIMIT:
        badges.append("💸 Giá rẻ")

    return " ".join(badges)


def drink_label(name):

    badges = drink_badges(name)

    if badges:
        return f"{name}  {badges}"

    return name


# =========================================================
# CHATBOT CƠ BẢN
# =========================================================

BEST_WORDS = [
    "ban chay",
    "bestseller",
    "best seller",
    "hot",
    "pho bien",
    "nhieu nguoi",
    "noi bat",
    "top",
    "yeu thich",
    "duoc ua chuong"
]


CHEAP_WORDS = [
    "re",
    "gia re",
    "re nhat",
    "tiet kiem",
    "binh dan",
    "sinh vien",
    "it tien",
    "gia mem",
    "kinh te"
]


NEW_WORDS = [
    "moi",
    "mon moi",
    "new",
    "ra mat",
    "vua ra"
]


DIET_WORDS = [
    "it ngot",
    "it duong",
    "an kieng",
    "healthy",
    "giam can"
]


TOPPING_WORDS = [
    "topping",
    "top ping"
]


MENU_WORDS = [
    "menu",
    "thuc don",
    "danh sach",
    "tat ca"
]


GREETING_WORDS = [
    "xin chao",
    "chao",
    "hello",
    "hi",
    "alo",
    "hey"
]


KEYWORDS = {

    "tra sua": [
        "tra sua"
    ],

    "ngot": [
        "ngot",
        "dam vi"
    ],

    "beo": [
        "beo",
        "beo ngay",
        "beo beo"
    ],

    "chua": [
        "chua"
    ],

    "mat": [
        "mat",
        "thanh mat",
        "giai nhiet",
        "giai khat",
        "thanh nhe"
    ],

    "trai cay": [
        "trai cay",
        "hoa qua",
        "fruit"
    ],

    "matcha": [
        "matcha",
        "tra xanh"
    ],

    "socola": [
        "socola",
        "chocolate",
        "cacao"
    ],

    "dau": [
        "dau",
        "dau tay"
    ],

    "khoai mon": [
        "khoai mon",
        "khoai"
    ],

    "dao": [
        "dao"
    ],

    "vai": [
        "vai"
    ],

    "chanh": [
        "chanh"
    ],

    "tac": [
        "tac",
        "quat"
    ],

    "tran chau": [
        "tran chau"
    ],

    "oolong": [
        "oolong",
        "o long"
    ]
}


def parse_budget(text):

    text = re.sub(
        r"(?<=\d)[.,](?=\d{3}\b)",
        "",
        text
    )

    match = re.search(
        r"(\d+)\s*(k|nghin|ngan)\b",
        text
    )

    if match:
        return int(match.group(1)) * 1000

    match = re.search(
        r"\b(\d{4,6})\b",
        text
    )

    if match:
        return int(match.group(1))

    return None


def suggestion_text(title, drinks):

    lines = [
        title,
        ""
    ]

    for name in drinks:

        info = DRINK_INFO[name]

        badges = drink_badges(name)

        lines.append(
            f"• **{name}** — "
            f"{format_money(info['price'])} "
            f"{badges}\n"
            f"  _{info['desc']}_"
        )

    lines.extend([
        "",
        "Bấm **Chọn** để chỉnh size/topping "
        "hoặc **Thêm nhanh** để thêm size M."
    ])

    return "\n".join(lines)


def chatbot_reply(text):

    norm = normalize(text)

    clean = clean_words(norm)

    budget = parse_budget(norm)

    want_best = has_keyword(
        clean,
        BEST_WORDS
    )

    want_cheap = has_keyword(
        clean,
        CHEAP_WORDS
    )

    want_new = has_keyword(
        clean,
        NEW_WORDS
    )

    want_diet = has_keyword(
        clean,
        DIET_WORDS
    )

    want_topping = has_keyword(
        clean,
        TOPPING_WORDS
    )

    want_menu = has_keyword(
        clean,
        MENU_WORDS
    )

    tags = [
        tag
    for tag, keywords in KEYWORDS.items()
        if has_keyword(clean, keywords)
    ]

    if want_diet:
        tags = [
            tag
            for tag in tags
            if tag != "ngot"
        ]

        if not tags:
            tags = ["mat"]

    # MENU

    if (
        want_menu
        and not (
            want_best
            or want_cheap
            or want_new
            or tags
            or budget
        )
    ):

        lines = [
            "📋 **Menu Lucky Tea**",
            ""
        ]

        for name, info in DRINK_INFO.items():

            lines.append(
                f"• **{name}** — "
                f"{format_money(info['price'])} "
                f"{drink_badges(name)}"
            )

        lines.extend([
            "",
            "Size L +5.000 | "
            "XL +10.000 | "
            "XXL +15.000 VNĐ"
        ])

        return "\n".join(lines), []

    # TOPPING

    if (
        want_topping
        and not (
            want_best
            or want_cheap
            or want_new
            or tags
            or budget
        )
    ):

        return (
            "🍡 **Một số topping tại Lucky Tea:**\n\n"
            "• Trân châu đen — 5.000 VNĐ\n"
            "• Trân châu trắng — 5.000 VNĐ\n"
            "• Thạch dừa — 5.000 VNĐ\n"
            "• Thạch trái cây — 5.000 VNĐ\n"
            "• Pudding trứng — 7.000 VNĐ\n"
            "• Kem cheese — 8.000 VNĐ\n"
            "• Trân châu hoàng kim — 7.000 VNĐ\n"
            "• Hạt thủy tinh — 6.000 VNĐ\n\n"
            "💡 Nếu thích béo, bạn có thể thử "
            "Kem cheese hoặc Pudding trứng."
        ), []

    # GREETING

    if not (
        want_best
        or want_cheap
        or want_new
        or want_diet
        or tags
        or budget
    ):

        if has_keyword(
            clean,
            GREETING_WORDS
        ):
            return (
                "Chào bạn! 🥰\n\n"
                "Hôm nay bạn muốn uống gì? "
                "Mình có thể tư vấn theo vị, "
                "giá tiền hoặc sở thích của bạn nha!"
            ), []

        return (
            "Mình chưa hiểu ý bạn lắm 😅\n\n"
            "Bạn có thể hỏi:\n\n"
            "• Món bán chạy nhất?\n"
            "• Có món nào dưới 30k không?\n"
            "• Món mới là gì?\n"
            "• Món nào thanh mát?\n"
            "• Mình thích béo nhưng ít ngọt\n"
            "• Topping nào ngon?\n"
            "• Cho mình xem menu"
        ), []

    # FILTER

    candidates = list(
        DRINK_INFO.items()
    )

    if budget:

        candidates = [
            item
            for item in candidates
            if item[1]["price"] <= budget
        ]

    if want_new:

        candidates = [
            item
            for item in candidates
            if item[1]["new"]
        ]

    if tags:

        candidates = [
            item
            for item in candidates
            if any(
                tag in item[1]["tags"]
                for tag in tags
            )
        ]

    # SORT

    if want_cheap:

        candidates.sort(
            key=lambda x: (
                x[1]["price"],
                -x[1]["sold"]
            )
        )

    else:

        candidates.sort(
            key=lambda x: x[1]["sold"],
            reverse=True
        )

    # TITLE

    parts = []

    if want_best:
        parts.append("bán chạy")

    if want_cheap:
        parts.append("giá rẻ")

    if want_new:
        parts.append("món mới")

    if want_diet:
        parts.append("ít ngọt")

    if budget:
        parts.append(
            f"dưới {format_money(budget)}"
        )

    if tags and not want_diet:
        parts.append("hợp vị bạn chọn")

    title = ", ".join(parts)

    if not title:
        title = "phù hợp với bạn"

    # NOT FOUND

    if not candidates:

        cheapest = min(
            DRINK_INFO.items(),
            key=lambda x: x[1]["price"]
        )

        return (
            f"Hmm, mình chưa tìm được món "
            f"{title} 😢.\n\n"
            f"Món rẻ nhất hiện tại là "
            f"**{cheapest[0]}** "
            f"({format_money(cheapest[1]['price'])})."
        ), []

    drinks = [
        name
        for name, _ in candidates[:3]
    ]

    reply = suggestion_text(
        f"✨ Gợi ý {title} cho bạn:",
        drinks
    )

    if want_diet:

        reply += (
            "\n\n💡 Mẹo: bạn có thể chọn "
            "đường 30%–50% và hạn chế topping "
            "ngọt."
        )

    return reply, drinks


# =========================================================
# AI OPENROUTER
# =========================================================

def build_menu_for_ai():

    lines = []

    for name, info in DRINK_INFO.items():

        lines.append(
            f"- {name}: "
            f"{info['price']:,} VND; "
            f"{info['desc']}; "
            f"tags={', '.join(info['tags'])}"
        )

    lines.append("")
    lines.append("Size:")
    
    for size, fee in SIZES.items():

        lines.append(
            f"- {size}: +{fee:,} VND"
        )

    lines.append("")
    lines.append("Topping:")

    for topping, price in TOPPINGS.items():

        lines.append(
            f"- {topping}: +{price:,} VND"
        )

    return "\n".join(lines)


def call_openrouter(user_text):

    if not OPENROUTER_API_KEY:
        return None

    menu_text = build_menu_for_ai()

    system_prompt = f"""
Bạn là trợ lý bán hàng AI của quán trà sữa Lucky Tea.

Nhiệm vụ:
- Tư vấn đồ uống thân thiện, tự nhiên.
- Chỉ được giới thiệu món có trong menu.
- Không được tự tạo món hoặc tự tạo giá.
- Khi khách hỏi giá, phải dùng đúng giá trong menu.
- Có thể tư vấn theo vị: béo, ngọt, chua, thanh mát,
  trái cây, matcha, socola...
- Có thể tư vấn theo ngân sách.
- Có thể tư vấn topping.
- Nếu khách chưa biết uống gì, hãy hỏi hoặc đưa ra
    2-3 lựa chọn phù hợp.
- Không cần nói mình là mô hình AI.
- Trả lời bằng tiếng Việt.
- Nói chuyện thân thiện như nhân viên Lucky Tea.
- Không trả lời quá dài.

MENU LUCKY TEA:

{menu_text}
"""

    recent_messages = []

    for msg in st.session_state.chat[-8:]:

        recent_messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    recent_messages.append({
        "role": "user",
        "content": user_text
    })

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            *recent_messages
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    data = json.dumps(
        payload,
        ensure_ascii=False
    ).encode("utf-8")

    request = urllib.request.Request(
        OPENROUTER_URL,
        data=data,
        headers={
            "Authorization":
                f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type":
                "application/json",
            "HTTP-Referer":
                "https://luckytea.local",
            "X-Title":
                "Lucky Tea"
        },
        method="POST"
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=45
        ) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

        choices = result.get(
            "choices",
            []
        )

        if not choices:
            return None

        message = choices[0].get(
            "message",
            {}
        )

        answer = message.get(
            "content",
            ""
        )

        if not answer:
            return None

        return answer.strip()

    except Exception:
        return None


def extract_drinks_from_ai(text):

    found = []

    normalized_text = normalize(text)

    for name in DRINK_INFO:

        if normalize(name) in normalized_text:

            if name not in found:
                found.append(name)

    return found[:3]


# =========================================================
# CHAT
# =========================================================

def ask_bot(text):

    st.session_state.chat.append({
        "role": "user",
        "content": text,
        "drinks": []
    })

    ai_reply = call_openrouter(text)

    if ai_reply:

        drinks = extract_drinks_from_ai(
            ai_reply
        )

        st.session_state.chat.append({
            "role": "assistant",
            "content": ai_reply,
            "drinks": drinks
        })

    else:

        reply, drinks = chatbot_reply(text)

        st.session_state.chat.append({
            "role": "assistant",
            "content": reply,
            "drinks": drinks
        })


def submit_chat():

    text = st.session_state.get(
        "chat_text",
        ""
        ).strip()

    if text:
        ask_bot(text)


def quick_ask(text):
    ask_bot(text)


def reset_chat():

    st.session_state.chat = [
        st.session_state.chat[0]
    ]


def select_drink_from_chat(name):

    st.session_state.drink_select = name

    st.toast(
        f"Đã chọn {name}!",
        icon="👇"
    )


def add_from_chat(name):

    st.session_state.cart.append({
        "name": name,
        "price": MENU[name],
        "size": "M",
        "quantity": 1,
        "toppings": [],
        "sugar": "70%",
        "ice": "100%"
    })

    st.toast(
        f"Đã thêm 1 ly {name}!",
        icon="✅"
    )


# =========================================================
# ICON CHÓ / MÈO
# =========================================================

def create_pet_icon(bill_number):

    from PIL import Image, ImageDraw

    image = Image.new(
        "RGBA",
        (300, 300),
        (255, 255, 255, 0)
    )

    draw = ImageDraw.Draw(image)

    if bill_number % 2 == 1:

        # MÈO

        draw.polygon(
            [(65, 95), (50, 25), (120, 70)],
            fill=(255, 190, 200),
            outline=(90, 70, 70)
        )

        draw.polygon(
            [(180, 70), (250, 25), (235, 95)],
            fill=(255, 190, 200),
            outline=(90, 70, 70)
        )

        draw.ellipse(
            (55, 55, 245, 245),
            fill=(255, 220, 190),
            outline=(90, 70, 70),
            width=6
        )

        draw.ellipse(
            (70, 165, 115, 200),
            fill=(255, 160, 175)
        )

        draw.ellipse(
            (185, 165, 230, 200),
            fill=(255, 160, 175)
        )

        draw.ellipse(
            (90, 110, 120, 145),
            fill=(55, 45, 45)
        )

        draw.ellipse(
            (180, 110, 210, 145),
            fill=(55, 45, 45)
        )

        draw.ellipse(
            (98, 115, 106, 123),
            fill="white"
        )

        draw.ellipse(
            (188, 115, 196, 123),
            fill="white"
        )

        draw.polygon(
            [(140, 150), (160, 150), (150, 165)],
            fill=(240, 120, 145)
        )

        draw.arc(
            (130, 155, 150, 180),
            0,
            180,
            fill=(80, 60, 60),
            width=4
        )

        draw.arc(
            (150, 155, 170, 180),
            0,
            180,
            fill=(80, 60, 60),
            width=4
        )

        draw.line(
            (100, 155, 35, 145),
            fill=(90, 70, 70),
            width=4
        )

        draw.line(
            (100, 170, 30, 175),
            fill=(90, 70, 70),
            width=4
        )

        draw.line(
            (200, 155, 265, 145),
            fill=(90, 70, 70),
            width=4
        )

        draw.line(
            (200, 170, 270, 175),
            fill=(90, 70, 70),
            width=4
        )

    else:

        # CHÓ

        draw.ellipse(
            (30, 70, 105, 190),
            fill=(170, 125, 90),
            outline=(90, 70, 60),
            width=6
        )

        draw.ellipse(
            (195, 70, 270, 190),
            fill=(170, 125, 90),
            outline=(90, 70, 60),
            width=6
        )

        draw.ellipse(
            (55, 55, 245, 245),
            fill=(225, 185, 135),
            outline=(90, 70, 60),
            width=6
        )

        draw.ellipse(
            (105, 135, 195, 210),
            fill=(245, 220, 190)
        )

        draw.ellipse(
            (90, 110, 120, 145),
            fill=(50, 45, 40)
        )

        draw.ellipse(
            (180, 110, 210, 145),
            fill=(50, 45, 40)
        )

        draw.ellipse(
            (98, 115, 106, 123),
            fill="white"
        )

        draw.ellipse(
            (188, 115, 196, 123),
            fill="white"
        )

        draw.ellipse(
            (130, 145, 170, 175),
            fill=(50, 45, 45)
        )

        draw.arc(
            (130, 160, 150, 190),
            0,
            180,
            fill=(70, 55, 50),
            width=4
        )

        draw.arc(
            (150, 160, 170, 190),
            0,
            180,
            fill=(70, 55, 50),
            width=4
        )

        draw.ellipse(
            (70, 170, 110, 200),
            fill=(255, 170, 170)
        )

        draw.ellipse(
            (190, 170, 230, 200),
            fill=(255, 170, 170)
        )

    return image


# =========================================================
# TẠO PDF
# =========================================================

def create_pdf():

    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A5
    from reportlab.lib.utils import ImageReader

    buffer = BytesIO()

    regular_font = "Helvetica"
    bold_font = "Helvetica-Bold"

    canvas_pdf = canvas.Canvas(
        buffer,
        pagesize=A5
    )

    width, height = A5

    left = 30
    right = width - 30

    state = {
        "y": height - 30
    }

    def ensure_space(needed):

        if state["y"] - needed < 50:

            canvas_pdf.showPage()

            state["y"] = height - 40

            canvas_pdf.setFont(
                bold_font,
                10
            )

            canvas_pdf.drawCentredString(
                width / 2,
                state["y"],
                f"LUCKY TEA - "
                f"{get_bill_number()} "
                f"(tiep theo)"
            )

            state["y"] -= 22

    # ICON

    pet_icon = create_pet_icon(
        st.session_state.bill_number
    )

    pet_buffer = BytesIO()

    pet_icon.save(
        pet_buffer,
        format="PNG"
    )

    pet_buffer.seek(0)

    canvas_pdf.drawImage(
        ImageReader(pet_buffer),
        width / 2 - 30,
        state["y"] - 5,
        width=60,
        height=60,
        mask="auto"
    )

    state["y"] -= 72
    # HEADER

    canvas_pdf.setFont(
        bold_font,
        19
    )

    canvas_pdf.drawCentredString(
        width / 2,
        state["y"],
        "LUCKY TEA"
    )

    state["y"] -= 20

    canvas_pdf.setFont(
        regular_font,
        10
    )

    canvas_pdf.drawCentredString(
        width / 2,
        state["y"],
        "HOA DON BAN HANG"
    )

    state["y"] -= 22

    # BILL INFO

    current_time = datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )

    canvas_pdf.setFont(
        regular_font,
        9
    )

    canvas_pdf.drawString(
        left,
        state["y"],
        f"So bill: {get_bill_number()}"
    )

    state["y"] -= 14

    canvas_pdf.drawString(
        left,
        state["y"],
        f"Thoi gian: {current_time}"
    )

    state["y"] -= 14

    canvas_pdf.drawString(
        left,
        state["y"],
        f"Tong so ly: {total_cups()}"
    )

    state["y"] -= 14

    canvas_pdf.line(
        left,
        state["y"],
        right,
        state["y"]
    )

    state["y"] -= 18

    # PRODUCTS

    for index, item in enumerate(
        st.session_state.cart,
        start=1
    ):

        size_fee = SIZES[
            item["size"]
        ]

        n_toppings = len(
            item["toppings"]
        )

        needed = (
            14
            + 13
            + 13
            + (13 if size_fee else 0)
            + 13 * n_toppings
            + 13
            + 18
        )

        ensure_space(needed)

        canvas_pdf.setFont(
            bold_font,
            9
        )

        canvas_pdf.drawString(
            left,
            state["y"],
            remove_accents(
                f"{index}. "
                f"{item['name']} - "
                f"Size {item['size']}"
            )
        )

        state["y"] -= 14

        canvas_pdf.setFont(
            regular_font,
            8
        )

        canvas_pdf.drawString(
            left + 12,
            state["y"],
            f"Duong: {item['sugar']} | "
            f"Da: {item['ice']}"
        )

        state["y"] -= 13

        canvas_pdf.drawString(
            left + 12,
            state["y"],
            "Gia nuoc:"
        )

        canvas_pdf.drawRightString(
            right,
            state["y"],
            pdf_money(item["price"])
        )

        state["y"] -= 13

        if size_fee:

            canvas_pdf.drawString(
                left + 12,
                state["y"],
                f"Phu thu size "
                f"{item['size']}:"
            )

            canvas_pdf.drawRightString(
                right,
                state["y"],
                "+ " + pdf_money(size_fee)
            )

            state["y"] -= 13

        for topping in item["toppings"]:

            canvas_pdf.drawString(
                left + 12,
                state["y"],
                remove_accents(
                    f"+ {topping}"
                    )
            )

            canvas_pdf.drawRightString(
                right,
                state["y"],
                "+ " + pdf_money(
                    TOPPINGS[topping]
                )
            )

            state["y"] -= 13

        cup_price = calculate_cup_price(
            item
        )

        canvas_pdf.setFont(
            bold_font,
            8
        )

        canvas_pdf.drawString(
            left + 12,
            state["y"],
            f"SL: {item['quantity']} x "
            f"{pdf_money(cup_price)}"
        )

        canvas_pdf.drawRightString(
            right,
            state["y"],
            pdf_money(
                calculate_item_total(item)
            )
        )

        state["y"] -= 18

    # TOTAL

    ensure_space(80)

    canvas_pdf.line(
        left,
        state["y"],
        right,
        state["y"]
    )

    state["y"] -= 22

    canvas_pdf.setFont(
        bold_font,
        12
    )

    canvas_pdf.drawString(
        left,
        state["y"],
        "TONG THANH TOAN"
    )

    canvas_pdf.drawRightString(
        right,
        state["y"],
        pdf_money(
            calculate_total()
        )
    )

    state["y"] -= 30

    canvas_pdf.setFont(
        regular_font,
        9
    )

    canvas_pdf.drawCentredString(
        width / 2,
        state["y"],
        "Cam on quy khach!"
    )

    state["y"] -= 14

    canvas_pdf.drawCentredString(
        width / 2,
        state["y"],
        "Hen gap lai tai Lucky Tea"
    )

    canvas_pdf.save()

    buffer.seek(0)

    return buffer


# =========================================================
# ẢNH
# =========================================================

image_path = "photo1.jpg"

if os.path.exists(image_path):

    st.image(
        image_path,
        use_container_width=True
    )

else:

    st.warning(
        "Không tìm thấy ảnh photo1.jpg"
    )


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="lucky-title">'
    '🧋 LUCKY TEA'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="lucky-subtitle">'
    'Đặt món • Tùy chỉnh • Tính tiền • '
    'Xuất hóa đơn'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# CHATBOX AI
# =========================================================

with st.expander(
    "🤖 Trợ lý AI Lucky Tea",
    expanded=True
):

    if OPENROUTER_API_KEY:

        st.markdown(
            '<div class="ai-status">'
            '🟢 AI đang hoạt động — '
            'Bạn có thể trò chuyện tự nhiên với mình!'
            '</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<div class="ai-status">'
            '🟡 Chưa cấu hình OpenRouter — '
            'chatbot vẫn hoạt động ở chế độ gợi ý menu.'
            '</div>',
            unsafe_allow_html=True
        )

    # QUICK QUESTIONS

    q1, q2, q3, q4, q5 = st.columns(5)

    q1.button(
        "🔥 Bán chạy",
        use_container_width=True,
        on_click=quick_ask,
        args=("Món nào bán chạy nhất?",)
    )

    q2.button(
        "💸 Giá rẻ",
        use_container_width=True,
        on_click=quick_ask,
        args=("Có món nào giá rẻ dưới 30k không?",)
    )

    q3.button(
        "🆕 Món mới",
        use_container_width=True,
        on_click=quick_ask,
        args=("Cho mình xem món mới",)
    )

    q4.button(
        "🍑 Thanh mát",
        use_container_width=True,
        on_click=quick_ask,
        args=("Mình muốn uống món thanh mát",)
    )

    q5.button(
        "🥛 Béo ngậy",
        use_container_width=True,
        on_click=quick_ask,
        args=("Mình thích món béo ngậy",)
    )

    # CHAT AREA

    chat_box = st.container(
        height=430,
        border=True
    )

    with chat_box:

        for msg_index, msg in enumerate(
            st.session_state.chat
        ):

            avatar = (
                "🧋"
                if msg["role"] == "assistant"
                else "🙂"
            )

            with st.chat_message(
                msg["role"],
                avatar=avatar
            ):

                st.markdown(
                    msg["content"]
                )

                drinks = msg.get(
                    "drinks",
                    []
                )

                for d_index, name in enumerate(
                    drinks
                ):

                    b1, b2, b3 = st.columns(
                        [3, 1, 1.4]
                    )

                    with b1:

                        st.markdown(
                            f"**{name}**  \n"
                            f"{format_money(MENU[name])}"
                        )

                    with b2:

                        st.button(
                            "Chọn",
                            key=(
                                f"chat_select_"
                                f"{msg_index}_"
                                f"{d_index}"
                            ),
                            on_click=(
                                select_drink_from_chat
                            ),
                            args=(name,),
                            use_container_width=True
                        )

                    with b3:

                        st.button(
                            "➕ Thêm nhanh",
                            key=(
                                f"chat_add_"
                                f"{msg_index}_"
                                f"{d_index}"
                            ),
                            on_click=(
                                add_from_chat
                                ),
                            args=(name,),
                            use_container_width=True
                        )

    # INPUT

    with st.form(
        "chat_form",
        clear_on_submit=True
    ):

        f1, f2 = st.columns(
            [5, 1]
        )

        f1.text_input(
            "Nhập câu hỏi",
            key="chat_text",
            placeholder=(
                "VD: Tui thích béo nhưng ít ngọt, "
                "tư vấn cho tui..."
            ),
            label_visibility="collapsed"
        )

        f2.form_submit_button(
            "Gửi 📨",
            use_container_width=True,
            on_click=submit_chat
        )

    st.button(
        "🧹 Xóa lịch sử chat",
        on_click=reset_chat
    )


# =========================================================
# CHỌN MÓN
# =========================================================

left_col, right_col = st.columns(
    [1, 1],
    gap="large"
)


with left_col:

    st.subheader(
        "🧋 Chọn thức uống"
    )

    drink = st.selectbox(
        "Loại trà sữa",
        list(MENU.keys()),
        key="drink_select",
        format_func=drink_label
    )

    price = MENU[drink]

    size = st.radio(
        "📏 Size",
        options=list(SIZES.keys()),
        format_func=lambda s:
            (
                f"{s} (+{format_money(SIZES[s])})"
                if SIZES[s]
                else f"{s} (mặc định)"
            ),
        horizontal=True
    )

    st.info(
        f"Giá nước size {size}: "
        f"**{format_money(price + SIZES[size])}**"
    )

    quantity = st.number_input(
        "Số lượng ly",
        min_value=1,
        max_value=50,
        value=1,
        step=1
    )


with right_col:

    st.subheader(
        "⚙️ Tùy chỉnh"
    )

    sugar = st.select_slider(
        "🍬 Mức độ đường",
        options=SUGAR_LEVELS,
        value="70%"
    )

    ice = st.select_slider(
        "🧊 Mức độ đá",
        options=ICE_LEVELS,
        value="100%"
    )


# =========================================================
# TOPPING
# =========================================================

st.subheader(
    "🍡 Thêm topping"
)


def topping_format(t):

    return (
        f"{t} "
        f"(+{format_money(TOPPINGS[t])})"
    )


per_cup_mode = False

if quantity > 1:

    per_cup_mode = st.checkbox(
        f"Mỗi ly chọn topping khác nhau "
        f"({quantity} ly)",
        value=False
    )


cup_toppings = []


if per_cup_mode:

    for i in range(
        int(quantity)
    ):

        selected = st.multiselect(
            f"Topping cho ly {i + 1}",
            list(TOPPINGS.keys()),
            format_func=topping_format,
            key=f"cup_topping_{i}"
        )

        cup_toppings.append(
            selected
        )

else:

    selected = st.multiselect(
        (
            "Chọn topping "
            "(áp dụng cho tất cả ly)"
            if quantity > 1
            else "Chọn topping"
        ),
        list(TOPPINGS.keys()),
        format_func=topping_format,
        key="shared_topping"
    )

    cup_toppings = [
        selected
    ] * int(quantity)


# =========================================================
# TÍNH TIỀN MÓN ĐANG CHỌN
# =========================================================

current_item_total = sum(

    price
    + SIZES[size]
    + sum(
        TOPPINGS[t]
        for t in tops
    )

    for tops in cup_toppings
)


st.markdown(
    f"""
    <div class="total-box">

        <div class="total-title">
            Thành tiền món đang chọn
        </div>

        <div class="total-money">
            {format_money(current_item_total)}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# THÊM VÀO HÓA ĐƠN
# =========================================================

if st.button(
    "➕ THÊM MÓN VÀO HÓA ĐƠN",
    use_container_width=True
):

    if per_cup_mode:

        for tops in cup_toppings:

            st.session_state.cart.append({
                "name": drink,
                "price": price,
                "size": size,
                "quantity": 1,
                "toppings": list(tops),
                "sugar": sugar,
                "ice": ice
            })

    else:

        st.session_state.cart.append({
            "name": drink,
            "price": price,
            "size": size,
            "quantity": int(quantity),
            "toppings": list(
                cup_toppings[0]
            ),
            "sugar": sugar,
            "ice": ice
        })

    st.toast(
        f"Đã thêm {int(quantity)} ly "
        f"{drink} vào hóa đơn!",
        icon="✅"
    )

    st.rerun()


# =========================================================
# HÓA ĐƠN
# =========================================================

st.divider()

st.markdown(
    f"""
    <div class="bill-number">
        🧾 HÓA ĐƠN {get_bill_number()}
    </div>
    """,
    unsafe_allow_html=True
)


if not st.session_state.cart:

    st.info(
        "🧾 Chưa có món nào trong hóa đơn."
    )

else:

    for index, item in enumerate(
        st.session_state.cart
    ):

        cup_price = calculate_cup_price(
            item
        )

        item_total = calculate_item_total(
            item
        )

        with st.container(
            border=True
        ):

            col1, col2, col3 = st.columns(
                [4, 2, 2]
            )

            with col1:

                st.markdown(
                    f"### {index + 1}. "
                    f"{item['name']} — "
                    f"Size {item['size']}"
                )

                st.write(
                    f"🍬 Đường: "
                    f"**{item['sugar']}**  |  "
                    f"🧊 Đá: "
                    f"**{item['ice']}**"
                )

                if item["toppings"]:

                    for topping in item["toppings"]:

                        st.write(
                            f"🍡 {topping}: "
                            f"+{format_money(TOPPINGS[topping])}"
                        )

                else:

                    st.write(
                        "🍡 Topping: Không"
                    )

            with col2:

                st.write(
                    "Số lượng"
                )

                st.markdown(
                    f"### {item['quantity']}"
                )

                st.write(
                    "Giá 1 ly: "
                    + format_money(
                        cup_price
                    )
                )

            with col3:

                st.write(
                    "Thành tiền"
                )

                st.markdown(
                    f"### {format_money(item_total)}"
                )

            if st.button(
                "🗑️ Xóa món này",
                key=f"delete_{index}",
                use_container_width=True
            ):

                st.session_state.cart.pop(
                    index
                )

                st.rerun()


    # =====================================================
    # TOTAL
    # =====================================================

    st.markdown(
        f"""
        <div class="total-box">

            <div class="total-title">
                💰 TỔNG THANH TOÁN
                ({total_cups()} ly)
            </div>

            <div class="total-money">
                {format_money(calculate_total())}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # PDF
    # =====================================================

    st.subheader(
        "🧾 Xuất hóa đơn"
    )

    try:

        pdf_file = create_pdf()

        st.download_button(
            label="📄 XUẤT HÓA ĐƠN PDF",
            data=pdf_file,
            file_name=(
                f"{get_bill_number()}.pdf"
            ),
            mime="application/pdf",
            use_container_width=True
        )

    except Exception as error:

        st.error(
            "Không thể tạo hóa đơn PDF."
        )

        st.code(
            str(error)
        )


    # =====================================================
    # PAYMENT
    # =====================================================

    st.divider()

    col_pay, col_clear = st.columns(
        2
    )


    with col_pay:

        if st.button(
            "💰 THANH TOÁN & TẠO BILL MỚI",
            use_container_width=True
        ):

            old_bill = get_bill_number()

            st.session_state.cart = []

            st.session_state.bill_number += 1

            st.toast(
                f"Thanh toán thành công! "
            f"Bill {old_bill} đã hoàn tất.",
                icon="✅"
            )

            st.rerun()


    with col_clear:

        if st.button(
            "🧹 XÓA TOÀN BỘ HÓA ĐƠN",
            use_container_width=True
        ):

            st.session_state.cart = []

            st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;">

        🧋 <b>Lucky Tea</b><br>

        Cảm ơn quý khách đã ủng hộ 💕<br>

        <small>
        AI Assistant • Order • Customize • Bill
        </small>

    </div>
    """,
    unsafe_allow_html=True
)
