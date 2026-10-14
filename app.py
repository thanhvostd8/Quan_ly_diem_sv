import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Quản Lý Điểm Sinh Viên", layout="wide")
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

@st.cache_data
def load_data():
    data = {
        'Ho_ten': ['Nguyễn Văn An', 'Trần Thị Bình', 'Lê Văn Cường', 'Trần Thị Dung',
                   'Võ Hoàng Em', 'Võ Thị Hoa', 'Đặng Văn Hùng', 'Bùi Thị Lan',
                   'Đỗ Văn Minh', 'Nguyễn Thị Nga'],
        'Diem_chuyen_can': [9, 8, 10, 7, 8, 9, 7, 10, 8, 9],
        'Diem_giua_ky': [8, 7, 9, 6, 8, 9, 7, 8, 6, 9],
        'Diem_cuoi_ky': [9, 8, 9, 7, 8, 10, 6, 9, 7, 8]
    }
    df = pd.DataFrame(data)
    df['Tong_ket'] = 0.2 * df['Diem_chuyen_can'] + 0.3 * df['Diem_giua_ky'] + 0.5 * df['Diem_cuoi_ky']
    def xep_loai(diem):
        if diem >= 8.5: return 'Giỏi'
        elif diem >= 7.0: return 'Khá'
        elif diem >= 5.0: return 'Trung bình'
        else: return 'Yếu'
    df['Xep_loai'] = df['Tong_ket'].apply(xep_loai)
    return df

df = load_data()
st.subheader("1. Bảng điểm sinh viên")
st.dataframe(df, use_container_width=True)

st.subheader("2. Thống kê chung")
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Điểm TB lớp", f"{df['Tong_ket'].mean():.2f}")
with col2: 
    sv_max = df.loc[df['Tong_ket'].idxmax()]
    st.metric("SV cao nhất", f"{sv_max['Ho_ten']} ({sv_max['Tong_ket']:.2f})")
with col3:
    sv_min = df.loc[df['Tong_ket'].idxmin()]
    st.metric("SV thấp nhất", f"{sv_min['Ho_ten']} ({sv_min['Tong_ket']:.2f})")
with col4: st.metric("SV đạt (>=5)", f"{len(df[df['Tong_ket'] >= 5])} / 10")

st.subheader("3. Tra cứu thông tin sinh viên")
sv_duoc_chon = st.selectbox("Chọn sinh viên:", df['Ho_ten'].tolist())
thong_tin_sv = df[df['Ho_ten'] == sv_duoc_chon].iloc[0]
st.write(f"**Họ tên:** {thong_tin_sv['Ho_ten']} | **Chuyên cần:** {thong_tin_sv['Diem_chuyen_can']} | **Giữa kỳ:** {thong_tin_sv['Diem_giua_ky']} | **Cuối kỳ:** {thong_tin_sv['Diem_cuoi_ky']} | **Tổng kết:** {thong_tin_sv['Tong_ket']:.2f} | **Xếp loại:** {thong_tin_sv['Xep_loai']}")

st.subheader("4. Biểu đồ điểm tổng kết")
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(df['Ho_ten'], df['Tong_ket'], color='skyblue', edgecolor='black')
ax.set_ylim(0, 11)
for i, v in enumerate(df['Tong_ket']): ax.text(i, v + 0.1, f"{v:.2f}", ha='center', fontweight='bold')
plt.xticks(rotation=45)
st.pyplot(fig)

st.caption("Ứng dụng được tạo bởi: Võ Khắc Thành- MSSV: 054208006689")
