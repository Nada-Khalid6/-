import streamlit as st
import json
import os
import hashlib
import secrets
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
#  Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Injaz |إنجاز",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  تحسينات CSS – أيقونة القائمة الجانبية
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');

html, body, [class*="css"], * {
    font-family: 'Cairo', sans-serif !important;
}

.main .block-container {
    direction: rtl;
    padding-top: 2rem;
    max-width: 1100px;
}
.stApp { background: #F7F4F0; }

/* أيقونة فتح/إغلاق القائمة الجانبية */
[data-testid="collapsedControl"] {
    visibility: visible !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    z-index: 999 !important;
    position: fixed !important;
    top: 15px !important;
    left: 15px !important;
    background: #1A1A2E !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 5px 12px !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2) !important;
    font-size: 1.4rem !important;
    width: 44px !important;
    height: 44px !important;
}
[data-testid="collapsedControl"] * {
    display: none !important; /* إخفاء النص الافتراضي */
}
/* زر القائمة عند فتحها (يظهر ×) */
section[data-testid="stSidebar"] ~ [data-testid="collapsedControl"]::after {
    content: "✕";
}
/* زر القائمة عند إغلاقها (يظهر ☰) */
[data-testid="collapsedControl"][aria-expanded="false"]::after {
    content: "☰";
}
/* حل بديل: استخدام سهمين عربيين */
[data-testid="collapsedControl"]::before {
    content: "»";
    font-size: 1.6rem;
}

/* باقي التنسيقات */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1A1A2E 0%, #16213E 60%, #0F3460 100%) !important;
    width: 280px !important;
}
/* ... أكمل CSS كما في النسخة السابقة ... */
/* الملخص: أضفنا فقط الأيقونة أعلاه */
</style>
""", unsafe_allow_html=True)

# ( باقي كود الـ CSS الكامل موجود في النسخة الأصلية، تم حذفه للاختصار )

# ─────────────────────────────────────────────
#  الملفات والثوابت
# ─────────────────────────────────────────────
SERVICES = [ ... ]  # نفس القائمة السابقة
CITIES = [ ... ]
# ... كل الثوابت كما هي ...

# دمج ملف tokens لحفظ رموز تذكرني
USERS_FILE         = "anjaz_users.json"
BOOKINGS_FILE      = "anjaz_bookings.json"
REVIEWS_FILE       = "anjaz_reviews.json"
MESSAGES_FILE      = "anjaz_messages.json"
NOTIFICATIONS_FILE = "anjaz_notifications.json"
TOKENS_FILE        = "anjaz_tokens.json"

def _load(path):
    if os.path.exists(path):
        with open(path,"r",encoding="utf-8") as f:
            return json.load(f)
    return {}

def _save(path, data):
    with open(path,"w",encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# ─────────────────────────────────────────────
#  وظائف المستخدمين (كما هي)
# ─────────────────────────────────────────────
def register_user(...):
    # ... نفس الكود بدون تغيير ...
    pass

def login_user(email, password):
    # ... تحقق عادي ...
    pass

def get_providers(service=None, city=None, min_rating=0, keyword=""):
    # ... نفس البحث المتقدم ...
    pass

# ─────────────────────────────────────────────
#  وظائف "تذكرني"
# ─────────────────────────────────────────────
def generate_token():
    return secrets.token_hex(32)

def save_token(email):
    tokens = _load(TOKENS_FILE)
    token = generate_token()
    expiry = (datetime.now() + timedelta(days=30)).isoformat()
    tokens[token] = {"email": email, "expiry": expiry}
    _save(TOKENS_FILE, tokens)
    return token

def validate_token(token):
    tokens = _load(TOKENS_FILE)
    if token in tokens:
        data = tokens[token]
        if datetime.now() < datetime.fromisoformat(data["expiry"]):
            return data["email"]
    return None

# ─────────────────────────────────────────────
#  باقي الوظائف (حجوزات، تقييمات، رسائل، إشعارات)
#  - تم إضافة دالة save_review مباشرة بدون شرط الحجز
# ─────────────────────────────────────────────
def save_review(provider_email, client_name, rating, comment):
    # نفس الوظيفة السابقة (تحفظ التقييم)
    ...

def update_rating(provider_email, new_rating):
    # نفس الوظيفة لتحديث المتوسط
    ...

# ─────────────────────────────────────────────
#  الجلسة والتعامل مع "تذكرني"
# ─────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

# محاولة تسجيل الدخول التلقائي من الرمز الموجود في الرابط
if not st.session_state.logged_in and "token" in st.query_params:
    token = st.query_params["token"][0] if isinstance(st.query_params["token"], list) else st.query_params["token"]
    email = validate_token(token)
    if email:
        users = get_all_users()
        if email in users:
            st.session_state.logged_in = True
            st.session_state.user = users[email]
            # إزالة الرمز من الرابط لعدم مشاركته مرة أخرى (اختياري)
            st.query_params.clear()

# ... باقي التهيئة كاملة ...

# ─────────────────────────────────────────────
#  تعديل صفحة تسجيل الدخول: إضافة "تذكرني"
# ─────────────────────────────────────────────
def page_login():
    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="auth-title">⚡ تسجيل الدخول</div>', unsafe_allow_html=True)

    email = st.text_input("📧 الإيميل", key="li_e")
    pw    = st.text_input("🔒 كلمة المرور", type="password", key="li_p")
    remember = st.checkbox("تذكرني (للبقاء متصلاً)", key="remember_me")

    if st.button("دخول ⚡"):
        if email and pw:
            ok, user, msg = login_user(email.strip().lower(), pw)
            if ok:
                st.session_state.logged_in = True
                st.session_state.user = user
                if remember:
                    token = save_token(user["email"])
                    st.query_params["token"] = token
                st.session_state.page = "home"
                st.rerun()
            else:
                st.error(msg)
        else:
            st.warning("ادخل الإيميل وكلمة المرور ⚠️")
    # ... زر إنشاء حساب ...

# ─────────────────────────────────────────────
#  صفحة مقدم الخدمة التفصيلية (للعملاء)
# ─────────────────────────────────────────────
def page_provider_detail():
    # نستقبل بريد المزود من المتغير selected_provider (الذي يخزن كامل الكائن)
    p = st.session_state.get("selected_provider")
    if not p:
        go("services")
        return

    all_users = get_all_users()
    u = st.session_state.user  # العميل الحالي

    st.markdown(f"""
    <div class="hero" style="padding:24px;">
        <h1>🔧 {p['name']}</h1>
        <p>{p.get('service_type','')} | 📍 {p.get('city','')}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3,2])
    with col1:
        st.markdown(f"""
        <div class="card">
            <div style="font-size:1.1rem; font-weight:800;">نبذة عن مقدم الخدمة</div>
            <p style="color:#444; margin-top:8px;">{p.get('bio','لا توجد نبذة.')}</p>
            <p>⏱️ الخبرة: {p.get('experience','غير محدد')}</p>
            <p>📱 رقم الهاتف: {p.get('phone','غير متوفر')}</p>
            <p>🛡️ الحالة: {'موثق ✅' if p.get('verified') else 'غير موثق ❌'}</p>
        </div>
        """, unsafe_allow_html=True)

        # عرض التقييمات السابقة
        st.markdown('<div class="section-title">💬 تقييمات العملاء</div>', unsafe_allow_html=True)
        reviews = get_reviews(p["email"])
        if reviews:
            for r in reversed(reviews):
                st.markdown(f"""
                <div style="border-right:3px solid #FF6B35; padding:8px; margin-bottom:8px;
                            background:#FFF9F5; border-radius:8px;">
                    <strong>{r['client']}</strong> {'⭐'*r['rating']}<br>
                    <span style="color:#555;">{r['comment']}</span><br>
                    <span style="color:#aaa; font-size:0.75rem;">{r['date']}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("لا توجد تقييمات بعد.")

    with col2:
        # بطاقة التقييم السريع
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("**⭐ قيم هذا مقدم الخدمة**")
        with st.form("direct_rating"):
            rating_val = st.slider("تقييمك", 1, 5, 5)
            comment_val = st.text_area("تعليقك (اختياري)", height=80)
            if st.form_submit_button("إرسال التقييم"):
                if u and u["type"] == "client":
                    save_review(p["email"], u["name"], rating_val, comment_val)
                    update_rating(p["email"], rating_val)
                    st.success("تم إرسال تقييمك! شكراً ⭐")
                    st.rerun()
                else:
                    st.error("يجب تسجيل الدخول كعميل أولاً.")
        st.markdown("</div>", unsafe_allow_html=True)

        # أزرار المراسلة والحجز
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("💬 راسله الآن"):
                st.session_state.chat_partner = p["email"]
                go("messaging")
        with col_b:
            if st.button("📅 احجز الآن"):
                st.session_state.selected_provider = p
                go("booking")

        if st.button("🔙 العودة إلى الخدمات"):
            go("services")

# ─────────────────────────────────────────────
#  تعديل صفحة الخدمات: الضغط على اسم المزود يفتح صفحته
# ─────────────────────────────────────────────
def page_services():
    # ... الكود الحالي ...
    for p in providers_sorted:
        # جعل الاسم رابطًا ينقله إلى صفحة المزود
        if st.button(f"{SERVICE_ICON.get(p.get('service_type'),'')} {p['name']}", key=f"link_{p['email']}"):
            st.session_state.selected_provider = p
            go("provider_detail")
        # باقي العرض كما هو
        # ...

# ─────────────────────────────────────────────
#  صفحات أخرى كما هي (مع بقية الصفحات الجديدة)
# ─────────────────────────────────────────────

# ─────────────────────────────────────────────
#  المسار الرئيسي (يضاف صفحة "provider_detail" للعملاء)
# ─────────────────────────────────────────────
def main():
    render_sidebar()

    page = st.session_state.page
    logged = st.session_state.logged_in
    u = st.session_state.user

    # الصفحات العامة
    if not logged:
        if page=="login": page_login()
        elif page=="register": page_register()
        elif page=="about": page_about()
        else: page_landing()
        return

    if u["type"]=="client":
        if page=="home": page_client_home()
        elif page=="services": page_services()
        elif page=="provider_detail": page_provider_detail()  # ← صفحة جديدة
        elif page=="booking": page_booking()
        elif page=="my_bookings": page_my_bookings()
        elif page=="messaging": page_messaging()
        elif page=="notifications": page_notifications()
        elif page=="about": page_about()
        else: page_client_home()
    else:
        # ... صفحات مقدم الخدمة ...
        pass

if __name__=="__main__":
    main()