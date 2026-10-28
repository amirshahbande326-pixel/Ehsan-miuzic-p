import streamlit as st
import whisper
import os

# تنظیمات ظاهر صفحه
st.set_page_config(page_title="تبدیل صوت آهنگ به متن", page_icon="🎵", layout="centered")

st.title("🎵 استخراج متن آهنگ با هوش مصنوعی")
st.write("فایل صوتی آهنگ مورد نظرت (فرمت‌های mp3، wav، m4a) رو آپلود کن تا هوش مصنوعی متن کاملش رو بهت بده.")

# بارگذاری مدل هوش مصنوعی (از کش استفاده می‌کنیم تا سرعت بالا بره)
@st.cache_resource
def load_model():
    return whisper.load_model("base")

with st.spinner("⏳ در حال آماده‌سازی هوش مصنوعی... لطفاً چند لحظه صبر کنید."):
    model = load_model()

# بخش آپلود فایل توسط کاربر
uploaded_file = st.file_uploader("انتخاب فایل صوتی:", type=["mp3", "wav", "m4a", "ogg"])

if uploaded_file is not None:
    # ذخیره موقت فایل در حافظه موقت
    with open("temp_audio.file", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.audio(uploaded_file, format='audio/mp3')
    
    if st.button("🚀 شروع پردازش و استخراج متن"):
        with st.spinner("🎧 هوش مصنوعی داره با دقت به آهنگ گوش میده..."):
            # پردازش فایل صوتی
            result = model.transcribe("temp_audio.file")
            
        st.success("✅ پردازش با موفقیت انجام شد!")
        
        # نمایش متن
        st.subheader("متن کامل استخراج شده:")
        st.text_area("متن آهنگ:", value=result['text'], height=300)
        
        # امکان دانلود متن به صورت فایل متنی
        st.download_button(
            label="📥 دانلود متن به صورت فایل متنی (TXT)",
            data=result['text'],
            file_name="lyrics.txt",
            mime="text/plain"
        )
        
        # پاک کردن فایل موقت
        if os.path.exists("temp_audio.file"):
            os.remove("temp_audio.file")
          
