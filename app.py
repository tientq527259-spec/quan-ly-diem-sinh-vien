import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# 1. CẤU HÌNH TRANG WEB
# ==============================

st.set_page_config(
    page_title="Quản lý điểm sinh viên",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 QUẢN LÝ ĐIỂM SINH VIÊN")
st.write("Ứng dụng quản lý điểm bằng Python, Pandas và Streamlit.")

# ==============================
# 2. TẠO DỮ LIỆU
# ==============================

data = {
    "Ho_ten": [
        "An", "Binh", "Chi", "Dung", "Ha",
        "Lan", "Minh", "Nam", "Phuc", "Trang"
    ],

    "Chuyen_can": [
        8.0, 9.0, 7.5, 8.5, 7.0,
        9.0, 8.0, 7.5, 8.5, 9.5
    ],

    "Giua_ky": [
        7.5, 8.0, 6.5, 9.0, 7.5,
        6.5, 8.5, 7.0, 7.5, 9.0
    ],

    "Cuoi_ky": [
        8.0, 7.5, 7.0, 9.0, 8.0,
        7.0, 9.0, 8.0, 7.5, 9.5
    ]
}

df = pd.DataFrame(data)

# ==============================
# 3. TÍNH ĐIỂM TỔNG KẾT
# ==============================

df["Tong_ket"] = (
    0.2 * df["Chuyen_can"]
    + 0.3 * df["Giua_ky"]
    + 0.5 * df["Cuoi_ky"]
).round(2)

# ==============================
# 4. XẾP LOẠI SINH VIÊN
# ==============================

def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"

df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# ==============================
# 5. HIỂN THỊ BẢNG ĐIỂM
# ==============================

st.header("📋 Bảng điểm sinh viên")

bang_diem = df.rename(columns={
    "Ho_ten": "Họ tên",
    "Chuyen_can": "Chuyên cần",
    "Giua_ky": "Giữa kỳ",
    "Cuoi_ky": "Cuối kỳ",
    "Tong_ket": "Tổng kết",
    "Xep_loai": "Xếp loại"
})

st.dataframe(
    bang_diem,
    use_container_width=True,
    hide_index=True
)

# ==============================
# 6. THỐNG KÊ
# ==============================

diem_tb = df["Tong_ket"].mean()

diem_max = df["Tong_ket"].max()
diem_min = df["Tong_ket"].min()

sv_max = df.loc[df["Tong_ket"] == diem_max]
sv_min = df.loc[df["Tong_ket"] == diem_min]

so_sv_dat = int((df["Tong_ket"] >= 5).sum())

st.header("📊 Thống kê kết quả học tập")

cot1, cot2, cot3, cot4 = st.columns(4)

cot1.metric(
    "Điểm trung bình",
    f"{diem_tb:.2f}"
)

cot2.metric(
    "Điểm cao nhất",
    f"{diem_max:.2f}"
)

cot3.metric(
    "Điểm thấp nhất",
    f"{diem_min:.2f}"
)

cot4.metric(
    "Số sinh viên đạt",
    f"{so_sv_dat}/10"
)

st.write("**Sinh viên có điểm cao nhất:**")
st.dataframe(
    sv_max[["Ho_ten", "Tong_ket"]].rename(
        columns={
            "Ho_ten": "Họ tên",
            "Tong_ket": "Tổng kết"
        }
    ),
    hide_index=True
)

st.write("**Sinh viên có điểm thấp nhất:**")
st.dataframe(
    sv_min[["Ho_ten", "Tong_ket"]].rename(
        columns={
            "Ho_ten": "Họ tên",
          "Tong_ket": "Tổng kết"
        }
    ),
    hide_index=True
)

# ==============================
# 7. CHỌN SINH VIÊN
# ==============================

st.header("🔎 Tra cứu điểm sinh viên")

ten_sv = st.selectbox(
    "Chọn sinh viên:",
    df["Ho_ten"].tolist()
)

sv = df[df["Ho_ten"] == ten_sv].iloc[0]

st.subheader(f"Thông tin điểm của sinh viên {ten_sv}")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Chuyên cần",
    f"{sv['Chuyen_can']:.2f}"
)

c2.metric(
    "Giữa kỳ",
    f"{sv['Giua_ky']:.2f}"
)

c3.metric(
    "Cuối kỳ",
    f"{sv['Cuoi_ky']:.2f}"
)

c4, c5 = st.columns(2)

c4.metric(
    "Điểm tổng kết",
    f"{sv['Tong_ket']:.2f}"
)

c5.metric(
    "Xếp loại",
    sv["Xep_loai"]
)

# ==============================
# 8. VẼ BIỂU ĐỒ
# ==============================

st.header("📈 Biểu đồ điểm tổng kết")

fig, ax = plt.subplots(figsize=(10, 5))

bars = ax.bar(
    df["Ho_ten"],
    df["Tong_ket"]
)

ax.set_title("DIEM TONG KET CUA 10 SINH VIEN")
ax.set_xlabel("Ho ten sinh vien")
ax.set_ylabel("Diem tong ket")

ax.set_ylim(0, 10)
ax.grid(axis="y", linestyle="--", alpha=0.4)

ax.bar_label(
    bars,
    fmt="%.2f",
    padding=3
)

fig.tight_layout()

st.pyplot(fig)
plt.close(fig)

# ==============================
# 9. THÔNG TIN NGƯỜI TẠO
# ==============================

st.divider()

st.caption("Ứng dụng được xây dựng bằng Python, Pandas và Streamlit.")

st.caption("Người tạo: [Trần Quốc Tiễn]")

st.caption("MSSV: [052208007259]")
