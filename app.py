import streamlit as st
from main import run_agent_workflow
import pandas as pd
import os

st.set_page_config(page_title="Football Newsletter", page_icon="⚽")

st.title("📧 اشتراك في النشرة الإخبارية الرياضية")

# جمع بيانات المستخدم
user_email = st.text_input("أدخل إيميلك:")
topic = st.text_input("الموضوع المفضل (مثلاً: أخبار ليفربول):")

# خيارات الوقت والتردد
frequency = st.radio("كم مرة تريد استقبال النشرة؟", ("مرة واحدة", "مرتين"))

times = []
if frequency == "مرة واحدة":
    time_choice = st.selectbox("اختر الوقت المفضل:", ["الصباح (9 AM)", "بعد الظهر (3 PM)", "المساء (9 PM)"])
    times.append(time_choice)
else:
    time_1 = st.selectbox("الموعد الأول:", ["الصباح (9 AM)", "بعد الظهر (3 PM)"])
    time_2 = st.selectbox("الموعد الثاني:", ["المساء (9 PM)", "منتصف الليل (12 AM)"])
    times.extend([time_1, time_2])

if st.button("تأكيد الاشتراك 🚀"):
    if user_email and topic:
        # 1. حفظ البيانات في ملف Excel
        data_file = "data/subscribers.xlsx"
        new_data = {
            "Email": [user_email],
            "Topic": [topic],
            "Frequency": [frequency],
            "Preferred Times": [", ".join(times)],
            "Status": ["Active"]
        }
        df_new = pd.DataFrame(new_data)

        if not os.path.isfile(data_file):
            df_new.to_excel(data_file, index=False)
        else:
            df_old = pd.read_excel(data_file)
            df_final = pd.concat([df_old, df_new], ignore_index=True)
            df_final.to_excel(data_file, index=False)

        st.success(f"تم تسجيلك بنجاح! ستصلك النشرة في الأوقات التالية: {', '.join(times)}")
        
        # تشغيل تجريبي لإرسال أول رسالة فوراً (اختياري)
        # run_agent_workflow(topic, user_email)
    else:
        st.error("من فضلك أكمل البيانات!")