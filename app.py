import streamlit as st
from datetime import datetime
from io import BytesIO
st.image("logo.jpg")

# =========================================================
# CẤU HÌNH APP
# =========================================================

st.set_page_config(
    page_title="Tính Bill Trà Sữa",
    page_icon="🧋",
    layout="wide"
)

# =========================================================
# DỮ LIỆU MENU
# Bạn có thể thay đổi tên và giá tại đây
# =========================================================

MENU = {
    "Trà sữa truyền thống": {
        "M": 30000,
        "L": 35000
    },
    "Trà sữa matcha": {
        "M": 35000,
        "L": 40000
    },
    "Trà sữa socola": {
        "M": 35000,
        "L": 40000
    },
    "Trà sữa khoai môn": {
        "M": 35000,
        "L": 40000
    },
    "Trà sữa thái xanh": {
        "M": 30000,
        "L": 35000
    },
    "Trà sữa thái đỏ": {
        "M": 30000,
        "L": 35000
    },
    "Trà đào": {
        "M": 30000,
        "L": 35000
    },
    "Trà vải": {
        "M": 30000,
        "L": 35000
    },
}

TOPPINGS = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 5000,
    "Thạch dừa": 5000,
    "Pudding trứng": 7000,
    "Kem cheese": 10000,
}

SUGAR_LEVELS = ["100%", "70%", "50%", "30%", "0%"]
ICE_LEVELS = ["100%", "70%", "50%", "30%", "0%"]
TEA_LEVELS = ["100%", "70%", "50%", "30%"]

# =========================================================
# SESSION STATE
# =========================================================

if "items" not in st.session_state:
    st.session_state.items = []

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""


# =========================================================
# HÀM TIỆN ÍCH
# =========================================================

def format_money(number):
    """Định dạng tiền Việt Nam."""
    return f"{number:,.0f} VNĐ".replace(",", ".")


def calculate_item_price(drink, size, topping):
    """Tính giá 1 ly."""
    return MENU[drink][size] + TOPPINGS[topping]


def create_invoice(customer_name, items, total):
    """Tạo nội dung hóa đơn."""
    now = datetime.now()

    lines = []
    lines.append("=" * 60)
    lines.append("              HÓA ĐƠN TRÀ SỮA")
    lines.append("=" * 60)
    lines.append(f"Khách hàng : {customer_name}")
    lines.append(
        f"Thời gian  : {now.strftime('%d/%m/%Y %H:%M:%S')}"
    )
    lines.append("-" * 60)

    for index, item in enumerate(items, start=1):
        lines.append(
            f"{index}. {item['drink']} - Size {item['size']}"
        )
        lines.append(
            f"   Số lượng : {item['quantity']}"
        )
        lines.append(
            f"   Topping  : {item['topping']}"
        )
        lines.append(
            f"   Đường    : {item['sugar']}"
        )
        lines.append(
            f"   Đá       : {item['ice']}"
        )
        lines.append(
            f"   Trà      : {item['tea']}"
        )
        lines.append(
            f"   Đơn giá  : {format_money(item['unit_price'])}"
        )
        lines.append(
            f"   Thành tiền: {format_money(item['total_price'])}"
        )
        lines.append("-" * 60)

    lines.append(
        f"TỔNG THANH TOÁN: {format_money(total)}"
    )
    lines.append("=" * 60)
    lines.append("          Cảm ơn quý khách!")
    lines.append("=" * 60)

    return "\n".join(lines)


# =========================================================
# GIAO DIỆN
# =========================================================

st.title("🧋 ỨNG DỤNG TÍNH BILL TRÀ SỮA")

st.markdown(
    "Nhập thông tin khách hàng và các món khách gọi. "
    "Một hóa đơn có thể có nhiều loại trà sữa."
)

# =========================================================
# THÔNG TIN KHÁCH HÀNG
# =========================================================

st.subheader("👤 Thông tin khách hàng")

customer_name = st.text_input(
    "Tên khách hàng",
    value=st.session_state.customer_name,
    placeholder="Ví dụ: Nguyễn Văn An"
)

st.session_state.customer_name = customer_name

st.divider()

# =========================================================
# NHẬP MÓN
# =========================================================

st.subheader("🧋 Thêm món")

with st.form("add_item_form", clear_on_submit=False):

    col1, col2 = st.columns(2)

    with col1:
        drink = st.selectbox(
            "Loại trà sữa",
            list(MENU.keys())
        )

        size = st.radio(
            "Size",
            ["M", "L"],
            horizontal=True
        )

        quantity = st.number_input(
            "Số lượng",
            min_value=1,
            max_value=100,
            value=1,
            step=1
        )

        topping = st.selectbox(
            "Topping",
            list(TOPPINGS.keys())
        )

    with col2:
        sugar = st.selectbox(
            "Mức độ đường",
            SUGAR_LEVELS,
            index=0
        )

        ice = st.selectbox(
            "Mức độ đá",
            ICE_LEVELS,
            index=0
        )

        tea = st.selectbox(
            "Mức độ trà",
            TEA_LEVELS,
            index=0
        )

    # Hiển thị giá dự kiến
    unit_price = calculate_item_price(
        drink,
        size,
        topping
    )

    preview_total = unit_price * quantity

    st.info(
        f"Đơn giá: **{format_money(unit_price)}**  |  "
        f"Thành tiền: **{format_money(preview_total)}**"
    )

    add_item = st.form_submit_button(
        "➕ THÊM MÓN",
        use_container_width=True
    )

    if add_item:

        if not customer_name.strip():
            st.error("Vui lòng nhập tên khách hàng.")
        else:

            item = {
                "drink": drink,
                "size": size,
                "quantity": quantity,
                "topping": topping,
                "sugar": sugar,
                "ice": ice,
                "tea": tea,
                "unit_price": unit_price,
                "total_price": preview_total
            }

            st.session_state.items.append(item)

            st.success(
                f"Đã thêm {quantity} ly {drink} size {size}."
            )


# =========================================================
# HIỂN THỊ DANH SÁCH MÓN
# =========================================================

st.divider()

st.subheader("🧾 Danh sách món đã gọi")

if len(st.session_state.items) == 0:

    st.info(
        "Chưa có món nào. Hãy nhập thông tin món ở phía trên."
    )

else:

    total_bill = 0

    for index, item in enumerate(
        st.session_state.items
    ):

        with st.container(border=True):

            col1, col2, col3 = st.columns(
                [4, 3, 1]
            )

            with col1:

                st.markdown(
                    f"### {index + 1}. {item['drink']}"
                )

                st.write(
                    f"**Size:** {item['size']}"
                )

                st.write(
                    f"**Topping:** {item['topping']}"
                )

            with col2:

                st.write(
                    f"**Số lượng:** {item['quantity']}"
                )

                st.write(
                    f"**Đường:** {item['sugar']}"
                )

                st.write(
                    f"**Đá:** {item['ice']}"
                )

                st.write(
                    f"**Trà:** {item['tea']}"
                )

            with col3:

                st.write(
                    f"Đơn giá:"
                )

                st.write(
                    f"**{format_money(item['unit_price'])}**"
                )

                st.write(
                    f"Thành tiền:"
                )

                st.write(
                    f"**{format_money(item['total_price'])}**"
                )

                delete_item = st.button(
                    "🗑️ Xóa",
                    key=f"delete_{index}"
                )

                if delete_item:
                    st.session_state.items.pop(index)
                    st.rerun()

        total_bill += item["total_price"]


    # =====================================================
    # TỔNG BILL
    # =====================================================

    st.divider()

    st.subheader("💰 Tổng thanh toán")

    col1, col2 = st.columns([2, 1])

    with col1:

        total_quantity = sum(
            item["quantity"]
            for item in st.session_state.items
        )

        st.write(
            f"**Tổng số món:** {len(st.session_state.items)}"
        )

        st.write(
            f"**Tổng số ly:** {total_quantity}"
        )

    with col2:

        st.markdown(
            f"""
            <div style="
                background-color:#fff3cd;
                padding:20px;
                border-radius:12px;
                text-align:center;
                border:1px solid #ffc107;
            ">
                <div style="font-size:18px;">
                    TỔNG TIỀN
                </div>
                <div style="
                    font-size:32px;
                    font-weight:bold;
                    color:#d63384;
                ">
                    {format_money(total_bill)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # THANH TOÁN
    # =====================================================

    st.divider()

    st.subheader("💳 Thanh toán")

    if not customer_name.strip():

        st.warning(
            "Vui lòng nhập tên khách hàng trước khi thanh toán."
        )

    else:

        if st.button(
            "💳 THANH TOÁN & XUẤT HÓA ĐƠN",
            type="primary",
            use_container_width=True
        ):

            invoice = create_invoice(
                customer_name,
                st.session_state.items,
                total_bill
            )

            # Tạo tên file an toàn
            safe_name = "".join(
                c for c in customer_name
                if c.isalnum() or c in " _-"
            ).strip()

            if not safe_name:
                safe_name = "khach_hang"

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            filename = (
                f"hoa_don_{safe_name}_{timestamp}.txt"
            )

            st.success(
                "✅ Thanh toán thành công!"
            )

            st.download_button(
                label="📄 TẢI FILE HÓA ĐƠN",
                data=invoice.encode("utf-8"),
                file_name=filename,
                mime="text/plain",
                use_container_width=True
            )

            st.text_area(
                "Nội dung hóa đơn",
                invoice,
                height=400
            )


# =========================================================
# NÚT XÓA TOÀN BỘ ĐƠN
# =========================================================

if len(st.session_state.items) > 0:

    st.divider()

    if st.button(
        "🗑️ XÓA TOÀN BỘ ĐƠN",
        use_container_width=True
    ):

        st.session_state.items = []
        st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🧋 Ứng dụng tính bill trà sữa | "
    "Có thể tùy chỉnh menu và giá trong biến MENU ở đầu file."
)
