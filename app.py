import streamlit as st
import pandas as pd
import plotly.express as px

# إعدادات الصفحة والخط العربي
st.set_page_config(page_title="مبادرة مؤشر", layout="wide")
st.markdown("<style>body{font-family:'Tajawal',sans-serif;direction:RTL;text-align:right;}</style>", unsafe_allow_html=True)

st.title("📊 مبادرة مؤشر الخوارزمية للتحليل التنبئي")
st.subheader("إدارة تعليم المنطقة - تحليل نتائج (نافس / قدرات / تحصيلي)")

# رفع ملف الإكسل
uploaded_file = st.file_uploader("اختر ملف البيانات (Excel)", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        
        # حساب الفجوة التعليمية والتصنيف
        df['الفجوة التعليمية'] = df['درجة المدرسة'] - df['درجة الاختبار المعياري']
        
        def classify(row):
            if row['الفجوة التعليمية'] <= 5 and row['درجة الاختبار المعياري'] >= 75:
                return '🟢 نطاق التميز'
            elif row['الفجوة التعليمية'] <= 15:
                return '🟡 النطاق الآمن'
            else:
                return '🔴 نطاق الدعم المستهدف'
        
        df['النطاق والتصنيف'] = df.apply(classify, axis=1)
        
        # عرض الإحصائيات
        st.markdown("---")
        st.header("📌 المؤشرات العامة للمنطقة")
        c1, c2 = st.columns(2)
        c1.metric("إجمالي المدارس", int(df['اسم المدرسة'].nunique()))
        c2.metric("متوسط الفجوة التعليمية", f"{round(df['الفجوة التعليمية'].mean(), 2)} %")
        
        # الرسم البياني
        st.markdown("---")
        st.subheader("📈 توزيع المدارس حسب نطاقات الدعم")
        fig = px.pie(df, names='النطاق والتصنيف', color='النطاق والتصنيف',
                     color_discrete_map={'🟢 نطاق التميز':'#2ecc71', '🟡 النطاق الآمن':'#f1c40f', '🔴 نطاق الدعم المستهدف':'#e74c3c'})
        st.plotly_chart(fig, use_container_width=True)
        
        # عرض الجدول
        st.markdown("---")
        st.header("📋 تقرير النتائج")
        st.dataframe(df[['اسم المدرسة', 'درجة المدرسة', 'درجة الاختبار المعياري', 'الفجوة التعليمية', 'النطاق والتصنيف']], use_container_width=True)
        
    except Exception as e:
        st.error(f"تأكد من مطابقة أسماء الأعمدة في ملف الإكسل: اسم المدرسة، درجة المدرسة، درجة الاختبار المعياري")
else:
    st.info("💡 بانتظار رفع ملف الـ Excel.")
