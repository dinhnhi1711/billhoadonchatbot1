import streamlit as st
from datetime import datetime
from io import BytesIO
st.image("logo.jpg")

# =========================================================
# CẤU HÌNH
# =========================================================

st.set_page_config(
    page_title="Quản lý Bill Trà Sữa",
    page_icon="🧋",
    layout="wide"
)

# =========================================================
# MENU TRÀ SỮA
# =========================================================

MENU = {
    "Trà sữa truyền thống": {"M": 30000, "L": 35000},
    "Trà sữa matcha": {"M": 35000, "L": 40000},
    "Trà sữa socola": {"M": 35000, "L": 40000},
    "Trà sữa khoai môn": {"M": 35000, "L": 40000},
    "Trà sữa thái xanh": {"M": 30000, "L": 35000},
    "Trà sữa thái đỏ": {"M": 30000, "L": 35000},
    "Trà đào": {"M": 30000, "L": 35000},
    "Trà vải": {"M": 30000, "L": 35000},
}

# =========================================================
# TOPPING
# =========================================================

TOPPINGS = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 5000,
    "Thạch dừa": 5000,
    "Pudding trứng": 7000,
    "Kem cheese": 10000,
}

# =========================================================
# MỨC ĐỘ
# =========================================================

SUGAR_LEVELS = [
    "100%",
    "70%",
    "50%",
    "30%",
    "0%"
]

ICE_LEVELS = [
    "100%",
    "70%",
    "50%",
    "30%",
    "0%"
]

TEA_LEVELS = [
    "100%",
    "70%",
    "50%",
    "30%"
]

# =========================================================
# SESSION STATE
# =========================================================

if "orders" not in st.session_state:
    st.session_state.orders = []

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""


# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def money(value):
    return f"{value:,.0f}".replace(",", ".") + " đ"


# =========================================================
# HÀM TẠO HÓA ĐƠN
# =========================================================

def create_invoice(customer_name, orders):

    now = datetime.now()

    total = sum(
        item["total"]
        for item in orders
    )

    text = ""

    text += "=" * 55 + "\n"
    text += "             HÓA ĐƠN TRÀ SỮA\n"
    text += "=" * 55 + "\n"

    text += f"Khách hàng: {customer_name}\n"
    text += (
        f"Thời gian: "
        f"{now.strftime('%d/%m/%Y %H:%M:%S')}\n"
    )

    text += "-" * 55 + "\n"

    for i, item in enumerate(orders, 1):

        text += f"\n{i}. {item['drink']}\n"

        text += (
            f"   Size: {item['size']}\n"
        )

        text += (
            f"   Số lượng: {item['quantity']}\n"
        )

        text += (
            f"   Topping: {item['topping']}\n"
        )

        text += (
            f"   Đường: {item['sugar']}\n"
        )

        text += (
            f"   Đá: {item['ice']}\n"
        )

        text += (
            f"   Trà: {item['tea']}\n"
        )

        text += (
            f"   Đơn giá: {money(item['unit_price'])}\n"
        )

        text += (
            f"   Thành tiền: {money(item['total'])}\n"
        )

        text += "-" * 55 + "\n"

    text += "\n"
    text += (
        f"TỔNG THANH TOÁN: {money(total)}\n"
    )

    text += "=" * 55 + "\n"
    text += "              CẢM ƠN QUÝ KHÁCH!\n"
    text += "=" * 55 + "\n"

    return text


# =========================================================
# TIÊU ĐỀ
# =========================================================

st.title("🧋 QUẢN LÝ BILL TRÀ SỮA")

st.write(
    "Nhập thông tin khách hàng và thêm từng món vào hóa đơn."
)


# =========================================================
# THÔNG TIN KHÁCH HÀNG
# =========================================================

st.header("👤 Thông tin khách hàng")

customer_name = st.text_input(
    "Tên khách hàng",
    value=st.session_state.customer_name,
    placeholder="Nhập tên khách hàng..."
)

st.session_state.customer_name = customer_name


# =========================================================
# THÊM MÓN
# =========================================================

st.header("🧋 Thêm món")

with st.form("order_form"):

    col1, col2 = st.columns(2)

    # -----------------------------------------------------
    # CỘT 1
    # -----------------------------------------------------

    with col1:

        drink = st.selectbox(
            "Loại trà sữa",
            list(MENU.keys())
        )

        size = st.selectbox(
            "Size",
            ["M", "L"]
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

    # -----------------------------------------------------
    # CỘT 2
    # -----------------------------------------------------

    with col2:

        sugar = st.selectbox(
            "Mức độ đường",
            SUGAR_LEVELS
        )

        ice = st.selectbox(
            "Mức độ đá",
            ICE_LEVELS
        )

        tea = st.selectbox(
            "Mức độ trà",
            TEA_LEVELS
        )

    # -----------------------------------------------------
    # TÍNH GIÁ
    # -----------------------------------------------------

    unit_price = (
        MENU[drink][size]
        + TOPPINGS[topping]
    )

    total_price = unit_price * quantity

    st.info(
        "Đơn giá: "
        + money(unit_price)
        + " | Thành tiền: "
        + money(total_price)
    )

    submitted = st.form_submit_button(
        "➕ THÊM VÀO HÓA ĐƠN"
    )


# =========================================================
# XỬ LÝ THÊM MÓN
# =========================================================

if submitted:

    if customer_name.strip() == "":

        st.error(
            "⚠️ Vui lòng nhập tên khách hàng."
        )

    else:

        order = {
            "drink": drink,
            "size": size,
            "quantity": quantity,
            "topping": topping,
            "sugar": sugar,
            "ice": ice,
            "tea": tea,
            "unit_price": unit_price,
            "total": total_price
        }

        st.session_state.orders.append(order)

        st.success(
            "✅ Đã thêm món vào hóa đơn."
        )

        st.rerun()


# =========================================================
# HIỂN THỊ HÓA ĐƠN HIỆN TẠI
# =========================================================

st.divider()

st.header("🧾 HÓA ĐƠN HIỆN TẠI")


if len(st.session_state.orders) == 0:

    st.info(
        "Chưa có món nào trong hóa đơn."
    )

else:

    total_bill = 0

    # -----------------------------------------------------
    # HIỂN THỊ TỪNG MÓN
    # -----------------------------------------------------

    for index, item in enumerate(
        st.session_state.orders
    ):

        st.subheader(
            f"Món {index + 1}: {item['drink']}"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.write(
                f"**Size:** {item['size']}"
            )

            st.write(
                f"**Số lượng:** {item['quantity']}"
            )

            st.write(
                f"**Topping:** {item['topping']}"
            )

        with col2:

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
                f"**Đơn giá:** "
                f"{money(item['unit_price'])}"
            )

            st.write(
                f"**Thành tiền:** "
                f"{money(item['total'])}"
            )

            if st.button(
                "🗑️ Xóa món",
                key=f"delete_{index}"
            ):

                st.session_state.orders.pop(index)

                st.rerun()

        st.divider()

        total_bill += item["total"]


    # =====================================================
    # TỔNG TIỀN
    # =====================================================

    st.header("💰 TỔNG THANH TOÁN")

    total_quantity = sum(
        item["quantity"]
        for item in st.session_state.orders
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Số loại món",
            len(st.session_state.orders)
        )

    with col2:

        st.metric(
            "Tổng số ly",
            total_quantity
        )

    with col3:

        st.metric(
            "Tổng tiền",
            money(total_bill)
        )


    # =====================================================
    # THANH TOÁN
    # =====================================================

    st.divider()

    st.header("💳 Thanh toán")

    if st.button(
        "💳 THANH TOÁN & XUẤT HÓA ĐƠN",
        type="primary",
        use_container_width=True
    ):

        invoice_text = create_invoice(
            customer_name,
            st.session_state.orders
        )

        current_time = datetime.now()

        filename = (
            "hoa_don_"
            + current_time.strftime(
                "%Y%m%d_%H%M%S"
            )
            + ".txt"
        )

        st.success(
            "✅ Thanh toán thành công!"
        )

        st.download_button(
            label="📥 TẢI HÓA ĐƠN",
            data=invoice_text.encode("utf-8"),
            file_name=filename,
            mime="text/plain",
            use_container_width=True
        )

        st.text_area(
            "Xem trước hóa đơn",
            invoice_text,
            height=450
        )


# =========================================================
# XÓA HÓA ĐƠN
# =========================================================

if len(st.session_state.orders) > 0:

    st.divider()

    if st.button(
        "🗑️ XÓA TOÀN BỘ HÓA ĐƠN",
        use_container_width=True
    ):

        st.session_state.orders = []

        st.rerun()
