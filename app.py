import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# تحميل البيانات
df = pd.read_excel("data/data.xlsx")

# التحقق من البيانات
st.write("📊 البيانات الأولية:")
st.dataframe(df.head())

# اختيار السنة
years = df["year"].dropna().unique()
selected_year = st.selectbox("اختر السنة", sorted(years))

# اختيار الدولة
# فقط الدول اللي ظهرت في السنة المختارة (عشان القائمة تكون أنظف)
countries = df[df["year"] == selected_year]["country"].dropna().unique()
selected_country = st.selectbox("اختر الدولة", sorted(countries))

# فلترة البيانات
filtered_df = df[(df["year"] == selected_year) & (df["country"] == selected_country)]

# تحقق لو في بيانات
if not filtered_df.empty:
    st.subheader(f"👥 عدد المستخدمين النشطين حسب أداة الذكاء الاصطناعي في {selected_country} سنة {selected_year}")

    # تجميع المستخدمين حسب الأداة
    ai_users = filtered_df.groupby("ai_tool")["daily_active_users"].sum()

    # رسم الشارت
    fig, ax = plt.subplots(figsize=(10, 5))
    ai_users.sort_values(ascending=False).plot(kind="bar", ax=ax, color="dodgerblue")
    ax.set_ylabel("عدد المستخدمين النشطين")
    ax.set_xlabel("أداة الذكاء الاصطناعي")
    ax.set_title("المستخدمين النشطين لكل أداة")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # عرض جدول البيانات المفصّلة
    st.subheader("📋 تفاصيل البيانات:")
    st.dataframe(filtered_df)

else:
    st.warning("⚠️ لا توجد بيانات لهذه الدولة في هذه السنة.")
