import streamlit as st
import json
import os
import hashlib
from datetime import datetime

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
#  CSS  — إضافة إظهار زر التحكم بالشريط الجانبي
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');

html, body, [class*="css"], * {
    font-family: 'Cairo', sans-serif !important;
}

/* Main content RTL */
.main .block-container {
    direction: rtl;
    padding-top: 2rem;
    max-width: 1100px;
}

.stApp { background: #F7F4F0; }

/* ── Sidebar المعدل ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1A1A2E 0%, #16213E 60%, #0F3460 100%) !important;
    width: 280px !important;
}

/* زر التحكم في إظهار/إخفاء الشريط الجانبي */
[data-testid="collapsedControl"] {
    visibility: visible !important;
    display: block !important;
    z-index: 999 !important;
    position: fixed !important;
    top: 15px !important;
    left: 15px !important;
    background: white !important;
    border-radius: 8px !important;
    padding: 5px !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.15) !important;
}

section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    color: white !important;
    border-radius: 10px !important;
    margin-bottom: 8px !important;
    font-size: 0.92rem !important;
    padding: 10px 16px !important;
    text-align: right !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,107,53,0.25) !important;
    border-color: #FF6B35 !important;
}

section[data-testid="stSidebar"] *:not(button) {
    color: white !important;
    direction: rtl;
}

/* Hero banner */
.hero {
    background: linear-gradient(135deg,#FF6B35 0%,#F7931E 60%,#FF4757 100%);
    border-radius: 20px;
    padding: 40px 32px;
    color: white;
    text-align: center;
    margin-bottom: 24px;
    box-shadow: 0 14px 40px rgba(255,107,53,0.28);
}
.hero h1 { font-size: 2.2rem; font-weight: 900; margin-bottom: 6px; }
.hero p  { font-size: 1rem; opacity: 0.92; margin: 0; }

/* Cards */
.card {
    background: white;
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 2px 14px rgba(0,0,0,0.06);
    margin-bottom: 14px;
    border: 1px solid #F0EBE3;
}
.section-title {
    font-size: 1.25rem;
    font-weight: 800;
    color: #1A1A2E;
    margin-bottom: 16px;
    padding-bottom: 7px;
    border-bottom: 3px solid #FF6B35;
    display: inline-block;
}

/* Provider card */
.pcard {
    background: white;
    border-radius: 16px;
    padding: 18px 20px;
    border: 2px solid #F0EBE3;
    margin-bottom: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    transition: border-color 0.18s, box-shadow 0.18s;
}
.pcard:hover {
    border-color: #FF6B35;
    box-shadow: 0 6px 22px rgba(255,107,53,0.13);
}
.pname { font-size: 1.05rem; font-weight: 800; color: #1A1A2E; }
.pmeta { color: #888; font-size: 0.85rem; margin-top: 3px; }
.pbio  { color: #444; font-size: 0.9rem; margin: 9px 0 0; }
.badge {
    display: inline-block;
    background: #FFF3EC; color: #FF6B35;
    border: 1px solid #FFD4B8;
    border-radius: 20px; padding: 2px 11px;
    font-size: 0.8rem; font-weight: 700; margin-left: 5px;
}
.badge-green { background:#E8F5E9; color:#2E7D32; border-color:#A5D6A7; }
.badge-red   { background:#FFEBEE; color:#C62828; border-color:#EF9A9A; }
.badge-blue  { background:#E3F2FD; color:#1565C0; border-color:#90CAF9; }
.stars { color: #FFB347; }

/* Service grid */
.svc-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px,1fr));
    gap: 10px;
}
.svc-item {
    background: white; border: 2px solid #F0EBE3;
    border-radius: 14px; padding: 16px 8px;
    text-align: center; transition: all 0.18s;
}
.svc-item:hover { border-color:#FF6B35; box-shadow:0 4px 16px rgba(255,107,53,0.13); }
.svc-icon { font-size: 1.9rem; margin-bottom: 5px; }
.svc-name { font-size: 0.82rem; font-weight: 700; color: #333; }

/* Booking item */
.bitem {
    background: white; border-radius: 14px;
    padding: 15px 18px; margin-bottom: 11px;
    border: 1px solid #F0EBE3;
    box-shadow: 0 1px 8px rgba(0,0,0,0.04);
}
.bitem-header {
    display: flex; justify-content: space-between;
    align-items: flex-start; flex-wrap: wrap; gap: 8px;
}

/* Auth */
.auth-wrap {
    max-width: 500px; margin: 0 auto;
    background: white; border-radius: 20px;
    padding: 34px; box-shadow: 0 8px 32px rgba(0,0,0,0.09);
}
.auth-title { font-size:1.6rem; font-weight:900; color:#FF6B35; text-align:center; margin-bottom:4px; }
.auth-sub   { text-align:center; color:#888; margin-bottom:22px; font-size:0.9rem; }

/* Main buttons */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg,#FF6B35,#F7931E) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important;
    font-family: 'Cairo', sans-serif !important;
    font-weight: 700 !important; font-size: 0.92rem !important;
    width: 100% !important; padding: 10px 18px !important;
    box-shadow: 0 3px 12px rgba(255,107,53,0.22) !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(255,107,53,0.32) !important;
}

/* Inputs */
.stTextInput>div>div>input,
.stSelectbox>div>div,
.stTextArea>div>div>textarea {
    border-radius: 11px !important;
    border: 2px solid #F0EBE3 !important;
    font-family: 'Cairo', sans-serif !important;
    direction: rtl !important;
}
.stTextInput>div>div>input:focus,
.stTextArea>div>div>textarea:focus {
    border-color: #FF6B35 !important;
    box-shadow: 0 0 0 3px rgba(255,107,53,0.1) !important;
}
div[data-testid="stTabs"] button {
    font-family: 'Cairo', sans-serif !important;
    font-weight: 700 !important;
}
.stRadio > div { flex-direction: row !important; gap: 14px !important; }
footer { visibility: hidden; }

/* Chat bubbles */
.chat-msg {
    padding: 12px 16px;
    border-radius: 20px;
    margin: 6px 0;
    max-width: 80%;
    word-wrap: break-word;
    font-size: 0.92rem;
}
.chat-sent { background: #FF6B35; color: white; }
.chat-recv { background: #F0EBE3; color: #333; }
.chat-time { font-size: 0.7rem; opacity: 0.7; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Constants
# ─────────────────────────────────────────────
SERVICES = [
    {"icon":"🚗","name":"سيارات"},
    {"icon":"🚚","name":"نقل وتوصيل"},
    {"icon":"💻","name":"خدمات أون لاين"},
    {"icon":"🔧","name":"سباكة"},
    {"icon":"⚡","name":"كهرباء"},
    {"icon":"🪚","name":"نجارة"},
    {"icon":"❄️","name":"تكييف"},
    {"icon":"🎨","name":"نقاشة"},
    {"icon":"📱","name":"صيانة أجهزة"},
    {"icon":"🧹","name":"نظافة"},
    {"icon":"🏗️","name":"خدمات صناعية"},
]
SERVICE_NAMES = [s["name"] for s in SERVICES]
SERVICE_ICON  = {s["name"]: s["icon"] for s in SERVICES}

CITIES = [
    "القاهرة","الجيزة","الإسكندرية","الدقهلية","البحيرة",
    "الفيوم","الغربية","الإسماعيلية","المنوفية","المنيا",
    "القليوبية","الوادي الجديد","السويس","أسوان","أسيوط",
    "بني سويف","بورسعيد","دمياط","الشرقية","جنوب سيناء",
    "كفر الشيخ","مطروح","الأقصر","قنا","شمال سيناء",
    "سوهاج","البحر الأحمر",
]

STATUS_PENDING  = "قيد الانتظار ⏳"
STATUS_CONFIRM  = "مؤكد ✅"
STATUS_CANCEL   = "ملغي ❌"

# ─────────────────────────────────────────────
#  File helpers
# ─────────────────────────────────────────────
USERS_FILE    = "anjaz_users.json"
BOOKINGS_FILE = "anjaz_bookings.json"
REVIEWS_FILE  = "anjaz_reviews.json"
MESSAGES_FILE = "anjaz_messages.json"
NOTIFICATIONS_FILE = "anjaz_notifications.json"

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
#  User functions (updated with verification fields)
# ─────────────────────────────────────────────
def register_user(name, email, password, user_type, city,
                  service_type=None, bio=None, experience=None,
                  phone=None, id_number=None):
    users = _load(USERS_FILE)
    if email in users:
        return False,"هذا الإيميل مسجل بالفعل 📧"
    
    # محاكاة للتحقق: نضع verified=True إذا تم توفير رقم هاتف وبطاقة
    verified = False
    if user_type == "provider" and phone and id_number:
        if len(phone) >= 11 and len(id_number) == 14:  # مثال: 14 رقم للبطاقة
            verified = True

    users[email] = {
        "name":name,
        "email":email,
        "password":hash_pw(password),
        "type":user_type,
        "city":city,
        "service_type":service_type,
        "bio":bio or "",
        "experience":experience or "",
        "phone":phone or "",
        "id_number":id_number or "",
        "verified":verified,
        "joined":datetime.now().strftime("%Y-%m-%d"),
        "rating":0.0,
        "rating_count":0,
    }
    _save(USERS_FILE, users)
    return True,"تم التسجيل بنجاح ✅"

def login_user(email, password):
    users = _load(USERS_FILE)
    if email not in users:
        return False, None, "الإيميل غير مسجل ❌"
    if users[email]["password"] != hash_pw(password):
        return False, None, "كلمة المرور غير صحيحة ❌"
    return True, users[email], "مرحباً بك ✅"

def get_all_users():
    return _load(USERS_FILE)

def get_providers(service=None, city=None, min_rating=0, keyword=""):
    users = _load(USERS_FILE)
    result = [u for u in users.values() if u["type"]=="provider"]
    if service: result = [u for u in result if u.get("service_type")==service]
    if city:    result = [u for u in result if u.get("city")==city]
    if min_rating > 0:
        result = [u for u in result if u.get("rating",0) >= min_rating]
    if keyword:
        kw = keyword.lower()
        result = [u for u in result if kw in u["name"].lower() or kw in u.get("bio","").lower()]
    return result

def update_rating(provider_email, new_rating):
    users = _load(USERS_FILE)
    if provider_email in users:
        u = users[provider_email]
        old_total = u["rating"]*u["rating_count"]
        u["rating_count"] += 1
        u["rating"] = round((old_total+new_rating)/u["rating_count"],1)
        _save(USERS_FILE, users)

# ─────────────────────────────────────────────
#  Booking functions
# ─────────────────────────────────────────────
def save_booking(client_email, provider_email, service, details, date, time_slot):
    bookings = _load(BOOKINGS_FILE)
    bid = f"B{len(bookings)+1:04d}_{datetime.now().strftime('%H%M%S')}"
    bookings[bid] = {
        "id":bid,"client":client_email,
        "provider":provider_email,"service":service,
        "details":details,"date":str(date),"time":time_slot,
        "status":STATUS_PENDING,"rated":False,
        "booked_at":datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    _save(BOOKINGS_FILE, bookings)
    # إشعار لمقدم الخدمة
    add_notification(provider_email, f"طلب حجز جديد من {client_email}")
    return bid

def update_booking_status(bid, new_status):
    bookings = _load(BOOKINGS_FILE)
    if bid in bookings:
        bookings[bid]["status"] = new_status
        _save(BOOKINGS_FILE, bookings)
        b = bookings[bid]
        client_email = b["client"]
        provider_email = b["provider"]
        # إشعار للعميل
        add_notification(client_email, f"طلب الحجز {bid} أصبح: {new_status}")
        # إشعار لمقدم الخدمة
        add_notification(provider_email, f"تم تحديث الطلب {bid} إلى {new_status}")

def mark_rated(bid):
    bookings = _load(BOOKINGS_FILE)
    if bid in bookings:
        bookings[bid]["rated"] = True
        _save(BOOKINGS_FILE, bookings)

def get_client_bookings(client_email):
    return [b for b in _load(BOOKINGS_FILE).values() if b["client"]==client_email]

def get_provider_bookings(provider_email):
    return [b for b in _load(BOOKINGS_FILE).values() if b["provider"]==provider_email]

# ─────────────────────────────────────────────
#  Reviews
# ─────────────────────────────────────────────
def save_review(provider_email, client_name, rating, comment):
    reviews = _load(REVIEWS_FILE)
    if provider_email not in reviews:
        reviews[provider_email]=[]
    reviews[provider_email].append({
        "client":client_name,"rating":rating,
        "comment":comment,"date":datetime.now().strftime("%Y-%m-%d"),
    })
    _save(REVIEWS_FILE, reviews)

def get_reviews(provider_email):
    return _load(REVIEWS_FILE).get(provider_email, [])

# ─────────────────────────────────────────────
#  Messaging
# ─────────────────────────────────────────────
def get_all_messages():
    return _load(MESSAGES_FILE)

def send_message(sender, receiver, text):
    msgs = get_all_messages()
    if "messages" not in msgs:
        msgs["messages"] = []
    msgs["messages"].append({
        "from": sender,
        "to": receiver,
        "text": text,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    _save(MESSAGES_FILE, msgs)
    # إشعار للمستقبل
    add_notification(receiver, f"رسالة جديدة من {sender}")

def get_conversation(user1, user2):
    msgs = get_all_messages().get("messages", [])
    return [m for m in msgs if (m["from"]==user1 and m["to"]==user2) or (m["from"]==user2 and m["to"]==user1)]

def get_chat_partners(email):
    """كل المستخدمين الذين تبادلت معهم رسائل"""
    msgs = get_all_messages().get("messages", [])
    partners = set()
    for m in msgs:
        if m["from"] == email:
            partners.add(m["to"])
        elif m["to"] == email:
            partners.add(m["from"])
    return list(partners)

# ─────────────────────────────────────────────
#  Notifications
# ─────────────────────────────────────────────
def add_notification(user_email, message):
    notif = _load(NOTIFICATIONS_FILE)
    if "notifications" not in notif:
        notif["notifications"] = []
    notif["notifications"].append({
        "user": user_email,
        "message": message,
        "read": False,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "id": len(notif["notifications"])
    })
    _save(NOTIFICATIONS_FILE, notif)

def get_notifications(user_email):
    notif = _load(NOTIFICATIONS_FILE).get("notifications", [])
    return [n for n in notif if n["user"] == user_email]

def unread_count(user_email):
    return len([n for n in get_notifications(user_email) if not n["read"]])

def mark_all_read(user_email):
    notif = _load(NOTIFICATIONS_FILE)
    for n in notif.get("notifications", []):
        if n["user"] == user_email:
            n["read"] = True
    _save(NOTIFICATIONS_FILE, notif)

# ─────────────────────────────────────────────
#  Session state
# ─────────────────────────────────────────────
for k,v in {
    "logged_in":False,"user":None,"page":"home",
    "selected_service":None,"selected_provider":None,
    "chat_partner":None,
}.items():
    if k not in st.session_state:
        st.session_state[k]=v

def go(page):
    st.session_state.page=page
    st.rerun()

# ─────────────────────────────────────────────
#  Sidebar
# ─────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center;padding:28px 12px 14px;'>
            <div style='font-size:2.2rem;'>⚡</div>
            <div style='font-size:1.4rem;font-weight:900;letter-spacing:1px;'>Anjaz</div>
            <div style='font-size:0.78rem;opacity:0.6;margin-top:2px;'>أنجز خدمتك بسرعة</div>
        </div>
        <hr style='border-color:rgba(255,255,255,0.12);margin:0 12px 14px;'>
        """, unsafe_allow_html=True)

        if st.session_state.logged_in:
            u = st.session_state.user
            utype_label = "مقدم خدمة 🔧" if u["type"]=="provider" else "عميل 👤"
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.09);border-radius:12px;
                        padding:12px;margin:0 10px 18px;text-align:center;'>
                <div style='font-size:0.98rem;font-weight:800;'>{u['name']}</div>
                <div style='font-size:0.78rem;opacity:0.7;margin-top:2px;'>{utype_label}</div>
                <div style='font-size:0.75rem;opacity:0.55;'>📍 {u.get("city","")}</div>
            </div>""", unsafe_allow_html=True)

            st.markdown("<div style='padding:0 10px;'>", unsafe_allow_html=True)
            notifications_badge = ""
            if u:
                unread = unread_count(u["email"])
                if unread > 0:
                    notifications_badge = f" 🔴({unread})"

            if u["type"]=="client":
                menu=[
                    ("🏠","الرئيسية","home"),
                    ("🔧","الخدمات","services"),
                    ("📅","حجوزاتي","my_bookings"),
                    ("💬","الرسائل","messaging"),
                    ("🔔",f"الإشعارات{notifications_badge}","notifications"),
                    ("ℹ️","عن التطبيق","about"),
                ]
            else:
                menu=[
                    ("🏠","لوحة التحكم","home"),
                    ("📋","طلباتي","provider_orders"),
                    ("👤","ملفي الشخصي","provider_profile"),
                    ("💬","الرسائل","messaging"),
                    ("🔔",f"الإشعارات{notifications_badge}","notifications"),
                    ("ℹ️","عن التطبيق","about"),
                ]

            for icon,label,pk in menu:
                dot = "🟠 " if st.session_state.page==pk else ""
                if st.button(f"{dot}{icon}  {label}", key=f"nav_{pk}"):
                    go(pk)

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<hr style='border-color:rgba(255,255,255,0.12);margin:16px 12px 10px;'>",
                        unsafe_allow_html=True)
            st.markdown("<div style='padding:0 10px;'>", unsafe_allow_html=True)
            if st.button("🚪  تسجيل الخروج"):
                st.session_state.logged_in=False
                st.session_state.user=None
                st.session_state.page="home"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.markdown("<div style='padding:0 10px;'>", unsafe_allow_html=True)
            if st.button("🔑  تسجيل الدخول"): go("login")
            if st.button("📝  إنشاء حساب"):    go("register")
            st.markdown("<hr style='border-color:rgba(255,255,255,0.12);margin:14px 0;'>",
                        unsafe_allow_html=True)
            if st.button("ℹ️  عن التطبيق"):     go("about")
            st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Auth pages (with verification fields)
# ─────────────────────────────────────────────
def page_login():
    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="auth-title">⚡ تسجيل الدخول</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-sub">أهلاً بك مجدداً في Anjaz</div>', unsafe_allow_html=True)

    email = st.text_input("📧 الإيميل", placeholder="example@email.com", key="li_e")
    pw    = st.text_input("🔒 كلمة المرور", type="password", placeholder="••••••••", key="li_p")
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("دخول ⚡", key="btn_login"):
        if email and pw:
            ok,user,msg = login_user(email.strip().lower(), pw)
            if ok:
                st.session_state.logged_in=True
                st.session_state.user=user
                st.session_state.page="home"
                st.rerun()
            else:
                st.error(msg)
        else:
            st.warning("ادخل الإيميل وكلمة المرور ⚠️")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;color:#888;font-size:0.88rem;'>مش عندك حساب؟</div>",
                unsafe_allow_html=True)
    if st.button("إنشاء حساب جديد 📝", key="go_reg"):
        go("register")
    st.markdown('</div>', unsafe_allow_html=True)

def page_register():
    st.markdown('<div class="auth-wrap" style="max-width:580px;">', unsafe_allow_html=True)
    st.markdown('<div class="auth-title">📝 حساب جديد</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-sub">اختار نوع حسابك أولاً</div>', unsafe_allow_html=True)

    user_type_raw = st.radio(
        "نوع الحساب",
        ["👤 عميل — أبحث عن خدمة","🔧 مقدم خدمة — أقدم خدمة"],
        key="reg_type"
    )
    is_provider = "مقدم" in user_type_raw

    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        name  = st.text_input("👤 الاسم كامل", placeholder="محمد أحمد", key="rn")
        pw    = st.text_input("🔒 كلمة المرور", type="password", placeholder="••••••••", key="rp")
    with c2:
        email = st.text_input("📧 الإيميل", placeholder="example@email.com", key="re")
        pw2   = st.text_input("🔒 تأكيد كلمة المرور", type="password", placeholder="••••••••", key="rp2")

    city = st.selectbox("📍 المحافظة", CITIES, key="rc")

    phone = id_number = service_type = bio = experience = None
    if is_provider:
        st.markdown("---")
        st.markdown("**🔧 معلومات الخدمة**")
        service_type = st.selectbox("نوع الخدمة التي تقدمها", SERVICE_NAMES, key="rs")
        bio = st.text_area("📝 نبذة عنك",
            placeholder="اكتب نبذة عن خبرتك وما تقدمه للعملاء...",
            height=90, key="rb")
        experience = st.text_input("📅 سنوات الخبرة", placeholder="مثلاً: 5 سنوات", key="rx")
        
        # حقول التوثيق
        st.markdown("**🛡️ توثيق الهوية (مطلوب للتحقق)**")
        phone = st.text_input("📱 رقم الهاتف", placeholder="01xxxxxxxxx", key="rphone")
        id_number = st.text_input("🆔 رقم البطاقة القومية", placeholder="14 رقم", key="rid")
    else:
        phone = st.text_input("📱 رقم الهاتف (اختياري)", placeholder="01xxxxxxxxx", key="rphone_cli")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("إنشاء الحساب 🚀", key="btn_reg"):
        if name and email and pw and pw2 and city:
            if pw!=pw2:
                st.error("كلمتا المرور غير متطابقتين ❌")
            elif len(pw)<6:
                st.error("كلمة المرور أقل من 6 أحرف ❌")
            else:
                utype="provider" if is_provider else "client"
                ok,msg = register_user(name.strip(),email.strip().lower(),pw, utype, city,
                                       service_type,bio,experience, phone, id_number)
                if ok:
                    ok2,user,_ = login_user(email.strip().lower(),pw)
                    if ok2:
                        st.session_state.logged_in=True
                        st.session_state.user=user
                        st.session_state.page="home"
                        st.rerun()
                else:
                    st.error(msg)
        else:
            st.warning("اكمل جميع الحقول ⚠️")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("عندي حساب بالفعل 🔑", key="go_login"):
        go("login")
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Landing page
# ─────────────────────────────────────────────
def page_landing():
    st.markdown("""
    <div class="hero">
        <h1>⚡ Anjaz | أنجز</h1>
        <p>المنصة الأولى لخدمات الصيانة والمنازل بالعربي</p>
    </div>""", unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        st.markdown("""<div class="card">
        <div style="font-size:1rem;font-weight:800;color:#CC3300;margin-bottom:10px;">😩 المشكلة</div>
        <ul style="list-style:none;padding:0;line-height:2.2;color:#444;">
            <li>❌ صعوبة إيجاد عمال موثوقين</li>
            <li>❌ ضياع الوقت في البحث</li>
            <li>❌ أسعار غير واضحة</li>
            <li>❌ لا توجد تقييمات</li>
        </ul></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="card">
        <div style="font-size:1rem;font-weight:800;color:#00796B;margin-bottom:10px;">✅ الحل</div>
        <ul style="list-style:none;padding:0;line-height:2.2;color:#444;">
            <li>✅ منصة تجمع كل الخدمات</li>
            <li>✅ بحث حسب المحافظة والخدمة</li>
            <li>✅ تقييمات حقيقية من عملاء</li>
            <li>✅ حجز سريع وسهل</li>
        </ul></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔧 الخدمات المتاحة</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="svc-grid">' +
        "".join(f'<div class="svc-item"><div class="svc-icon">{s["icon"]}</div>'
                f'<div class="svc-name">{s["name"]}</div></div>' for s in SERVICES) +
        '</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1,col2,col3 = st.columns([1,2,1])
    with col2:
        if st.button("🔑 سجّل دخولك وابدأ الآن ⚡", key="landing_cta"):
            go("login")

# ─────────────────────────────────────────────
#  Client pages
# ─────────────────────────────────────────────
def page_client_home():
    u = st.session_state.user
    bookings = get_client_bookings(u["email"])

    st.markdown(f"""
    <div class="hero">
        <h1>أهلاً {u['name'].split()[0]}! 👋</h1>
        <p>محتاج إيه النهارده؟ اختار الخدمة وإحنا نجيبلك أحسن متخصص</p>
    </div>""", unsafe_allow_html=True)

    s1,s2,s3 = st.columns(3)
    for col,label,val in [
        (s1,"📅 حجوزاتي",str(len(bookings))),
        (s2,"📍 مدينتي",u.get("city","—")),
        (s3,"🏆 عضويتي","مميز ⭐"),
    ]:
        with col:
            st.markdown(f"""<div class="card" style="text-align:center;">
                <div style="font-size:1.5rem;font-weight:900;color:#FF6B35;">{val}</div>
                <div style="font-size:0.85rem;color:#666;margin-top:4px;">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔧 ابدأ من هنا</div>', unsafe_allow_html=True)

    cols = st.columns(4)
    for i,svc in enumerate(SERVICES):
        with cols[i%4]:
            st.markdown(f"""<div class="svc-item">
                <div class="svc-icon">{svc['icon']}</div>
                <div class="svc-name">{svc['name']}</div>
            </div>""", unsafe_allow_html=True)
            if st.button("عرض", key=f"hs_{i}"):
                st.session_state.selected_service=svc["name"]
                go("services")

def page_services():
    st.markdown('<div class="section-title">🔧 تصفح مقدمي الخدمة</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2,2,1])
    with col1:
        default_idx=(SERVICE_NAMES.index(st.session_state.selected_service)+1
                     if st.session_state.selected_service else 0)
        filter_svc = st.selectbox("نوع الخدمة",["الكل"]+SERVICE_NAMES, index=default_idx, key="fs")
    with col2:
        filter_city = st.selectbox("المحافظة",["الكل"]+CITIES, key="fc")
    with col3:
        min_rating = st.slider("أدنى تقييم ⭐", 0.0, 5.0, 0.0, 0.5, key="min_rating")

    st.text_input("🔍 بحث بالاسم أو النبذة", key="search_keyword")

    svc_q   = None if filter_svc =="الكل" else filter_svc
    city_q  = None if filter_city=="الكل" else filter_city
    keyword = st.session_state.get("search_keyword","").strip()
    providers = get_providers(svc_q, city_q, min_rating, keyword)

    if not providers:
        st.info("🔍 لا يوجد مقدمو خدمة بهذا الاختيار حتى الآن.")
        return

    providers_sorted = sorted(providers, key=lambda x: -x.get("rating",0))
    st.markdown(f"<p style='color:#888;margin-bottom:14px;'>تم إيجاد "
                f"<strong>{len(providers_sorted)}</strong> مقدم خدمة</p>",
                unsafe_allow_html=True)

    for p in providers_sorted:
        rating   = p.get("rating",0)
        r_count  = p.get("rating_count",0)
        stars    = "⭐"*round(rating) if rating else "لا يوجد تقييم بعد"
        icon     = SERVICE_ICON.get(p.get("service_type",""),"🔧")
        reviews  = get_reviews(p["email"])
        verified_badge = " 🛡️ موثق" if p.get("verified") else ""

        st.markdown(f"""
        <div class="pcard">
            <div class="bitem-header">
                <div>
                    <div class="pname">{icon} {p['name']}{verified_badge}</div>
                    <div class="pmeta">📍 {p.get('city','—')} &nbsp;|&nbsp; 🔧 {p.get('service_type','—')}</div>
                    <div class="pmeta">⏱️ خبرة: {p.get('experience','غير محدد')}</div>
                </div>
                <div>
                    <span class="badge">{p.get('service_type','')}</span>
                    <span class="badge badge-green">✅ متاح</span>
                    <div style="margin-top:5px;">
                        <span class="stars">{stars}</span>
                        <span style="color:#aaa;font-size:0.8rem;"> ({r_count} تقييم)</span>
                    </div>
                </div>
            </div>
            <div class="pbio">{p.get('bio','') or 'لم تتم إضافة نبذة.'}</div>
        </div>""", unsafe_allow_html=True)

        col_r,col_b = st.columns([2,1])
        with col_r:
            if reviews:
                with st.expander(f"💬 التقييمات ({len(reviews)})"):
                    for r in reviews[-5:]:
                        st.markdown(f"""
                        <div style="border-right:3px solid #FF6B35;padding:7px 13px;
                                    margin-bottom:7px;background:#FFFAF7;border-radius:8px;">
                            <strong>{r['client']}</strong> &nbsp; {'⭐'*r['rating']}
                            <br><span style="color:#555;font-size:0.86rem;">{r['comment']}</span>
                            <br><span style="color:#bbb;font-size:0.76rem;">{r['date']}</span>
                        </div>""", unsafe_allow_html=True)
        with col_b:
            if st.button("📅 احجز الآن", key=f"bk_{p['email']}"):
                st.session_state.selected_provider=p
                go("booking")
            if st.button("💬 راسله", key=f"chat_{p['email']}"):
                st.session_state.chat_partner = p["email"]
                go("messaging")

def page_booking():
    p = st.session_state.selected_provider
    if not p:
        go("services"); return

    icon = SERVICE_ICON.get(p.get("service_type",""),"🔧")
    st.markdown(f"""
    <div class="hero" style="padding:28px;">
        <h1 style="font-size:1.7rem;">{icon} حجز مع {p['name']}</h1>
        <p>📍 {p.get('city','—')} &nbsp;|&nbsp; 🔧 {p.get('service_type','—')}</p>
    </div>""", unsafe_allow_html=True)

    with st.form("bform"):
        c1,c2 = st.columns(2)
        with c1:
            date = st.date_input("📅 تاريخ الخدمة", min_value=datetime.today())
        with c2:
            time_slot = st.selectbox("🕐 الوقت المناسب",[
                "صباحاً 8:00 - 10:00","صباحاً 10:00 - 12:00",
                "ظهراً 12:00 - 2:00","عصراً 2:00 - 4:00",
                "مساءً 4:00 - 6:00","مساءً 6:00 - 8:00",
            ])
        details = st.text_area("📝 وصف المشكلة",
            placeholder="اشرح المشكلة بالتفصيل...", height=100)
        address = st.text_input("📍 العنوان التفصيلي",
            placeholder="الشارع، رقم المبنى، الدور...")
        submitted = st.form_submit_button("✅ إرسال طلب الحجز")

    if submitted:
        if details and address:
            u = st.session_state.user
            save_booking(u["email"], p["email"], p.get("service_type",""),
                         f"{details} | العنوان: {address}", date, time_slot)
            st.success(f"🎉 تم إرسال طلب الحجز مع {p['name']} ليوم {date}!\nسيتم تأكيده من مقدم الخدمة قريباً.")
            st.session_state.selected_provider=None
            go("my_bookings")
        else:
            st.warning("ادخل تفاصيل المشكلة والعنوان ⚠️")

    if st.button("← رجوع للخدمات"):
        st.session_state.selected_provider=None
        go("services")

def page_my_bookings():
    u = st.session_state.user
    bookings  = get_client_bookings(u["email"])
    all_users = get_all_users()

    st.markdown('<div class="section-title">📅 حجوزاتي</div>', unsafe_allow_html=True)

    if not bookings:
        st.info("مفيش حجوزات لحد دلوقتي. روح تصفح الخدمات! ⚡")
        if st.button("🔧 تصفح الخدمات"): go("services")
        return

    for b in sorted(bookings, key=lambda x: x["booked_at"], reverse=True):
        provider      = all_users.get(b["provider"],{})
        provider_name = provider.get("name", b["provider"])
        icon          = SERVICE_ICON.get(b["service"],"🔧")
        status        = b["status"]

        if STATUS_CONFIRM in status:
            badge_class="badge-green"
        elif STATUS_CANCEL in status:
            badge_class="badge-red"
        else:
            badge_class="badge-blue"

        st.markdown(f"""
        <div class="bitem">
            <div class="bitem-header">
                <div>
                    <div style="font-weight:800;color:#1A1A2E;font-size:1rem;">
                        {icon} {b['service']}
                    </div>
                    <div style="color:#666;font-size:0.85rem;margin-top:3px;">
                        مع <strong>{provider_name}</strong>
                    </div>
                    <div style="color:#aaa;font-size:0.8rem;margin-top:2px;">
                        📅 {b['date']} &nbsp;|&nbsp; 🕐 {b['time']}
                    </div>
                </div>
                <span class="badge {badge_class}">{status}</span>
            </div>
        </div>""", unsafe_allow_html=True)

        if STATUS_PENDING in status:
            col_c, col_sp = st.columns([1,3])
            with col_c:
                if st.button("❌ إلغاء الطلب", key=f"cli_cancel_{b['id']}"):
                    update_booking_status(b["id"], STATUS_CANCEL)
                    st.success("تم إلغاء الطلب.")
                    st.rerun()

        if STATUS_CONFIRM in status and not b.get("rated"):
            with st.expander(f"⭐ قيّم {provider_name}"):
                rating  = st.slider("تقييمك من 5", 1, 5, 5, key=f"rt_{b['id']}")
                comment = st.text_area("تعليقك", placeholder="شاركنا تجربتك...",
                                       key=f"cm_{b['id']}", height=75)
                if st.button("إرسال التقييم ⭐", key=f"sb_{b['id']}"):
                    update_rating(b["provider"], rating)
                    save_review(b["provider"], u["name"], rating, comment)
                    mark_rated(b["id"])
                    st.success("شكراً على تقييمك! ⭐")
                    st.rerun()

# ─────────────────────────────────────────────
#  Provider pages
# ─────────────────────────────────────────────
def page_provider_home():
    u         = st.session_state.user
    orders    = get_provider_bookings(u["email"])
    all_users = get_all_users()
    rating    = u.get("rating",0)
    r_count   = u.get("rating_count",0)
    icon      = SERVICE_ICON.get(u.get("service_type",""),"🔧")
    verified  = "✅ موثق" if u.get("verified") else "❌ غير موثق"

    st.markdown(f"""
    <div class="hero">
        <h1>{icon} أهلاً {u['name'].split()[0]}!</h1>
        <p>لوحة التحكم — {u.get('service_type','')} | {verified}</p>
    </div>""", unsafe_allow_html=True)

    pending = [o for o in orders if STATUS_PENDING in o["status"]]
    s1,s2,s3 = st.columns(3)
    for col,label,val in [
        (s1,"📋 إجمالي الطلبات",str(len(orders))),
        (s2,"⏳ طلبات معلقة",str(len(pending))),
        (s3,"⭐ تقييمي",f"{rating:.1f} ({r_count})"),
    ]:
        with col:
            st.markdown(f"""<div class="card" style="text-align:center;">
                <div style="font-size:1.5rem;font-weight:900;color:#FF6B35;">{val}</div>
                <div style="font-size:0.85rem;color:#666;margin-top:4px;">{label}</div>
            </div>""", unsafe_allow_html=True)

    if pending:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">⏳ طلبات تحتاج ردك</div>', unsafe_allow_html=True)
        for b in pending[:3]:
            client      = all_users.get(b["client"],{})
            client_name = client.get("name", b["client"])
            st.markdown(f"""
            <div class="bitem">
                <div class="bitem-header">
                    <div>
                        <div style="font-weight:800;color:#1A1A2E;">👤 {client_name}</div>
                        <div style="color:#aaa;font-size:0.8rem;">
                            📅 {b['date']} &nbsp;|&nbsp; 🕐 {b['time']}
                        </div>
                    </div>
                    <span class="badge badge-blue">{b['status']}</span>
                </div>
            </div>""", unsafe_allow_html=True)
            ca,cb = st.columns(2)
            with ca:
                if st.button("✅ قبول", key=f"ph_acc_{b['id']}"):
                    update_booking_status(b["id"], STATUS_CONFIRM)
                    st.success("تم قبول الطلب ✅")
                    st.rerun()
            with cb:
                if st.button("❌ رفض", key=f"ph_rej_{b['id']}"):
                    update_booking_status(b["id"], STATUS_CANCEL)
                    st.info("تم رفض الطلب.")
                    st.rerun()

def page_provider_orders():
    u         = st.session_state.user
    orders    = get_provider_bookings(u["email"])
    all_users = get_all_users()

    st.markdown('<div class="section-title">📋 جميع الطلبات</div>', unsafe_allow_html=True)

    if not orders:
        st.info("لم تصلك طلبات بعد.")
        return

    for b in sorted(orders, key=lambda x: x["booked_at"], reverse=True):
        client      = all_users.get(b["client"],{})
        client_name = client.get("name", b["client"])
        client_city = client.get("city","—")
        status      = b["status"]

        if STATUS_CONFIRM in status:   badge_class="badge-green"
        elif STATUS_CANCEL in status:  badge_class="badge-red"
        else:                          badge_class="badge-blue"

        st.markdown(f"""
        <div class="bitem">
            <div class="bitem-header">
                <div>
                    <div style="font-weight:800;color:#1A1A2E;">👤 {client_name}</div>
                    <div style="color:#888;font-size:0.83rem;">
                        📍 {client_city} &nbsp;|&nbsp; 📅 {b['date']} &nbsp;|&nbsp; 🕐 {b['time']}
                    </div>
                    <div style="color:#555;font-size:0.85rem;margin-top:5px;">{b['details']}</div>
                    <div style="color:#bbb;font-size:0.77rem;margin-top:4px;">
                        تم الحجز: {b['booked_at']}
                    </div>
                </div>
                <span class="badge {badge_class}">{status}</span>
            </div>
        </div>""", unsafe_allow_html=True)

        if STATUS_PENDING in status:
            ca,cb = st.columns(2)
            with ca:
                if st.button("✅ قبول الطلب", key=f"acc_{b['id']}"):
                    update_booking_status(b["id"], STATUS_CONFIRM)
                    st.success("تم قبول الطلب ✅")
                    st.rerun()
            with cb:
                if st.button("❌ رفض الطلب", key=f"rej_{b['id']}"):
                    update_booking_status(b["id"], STATUS_CANCEL)
                    st.info("تم رفض الطلب.")
                    st.rerun()

def page_provider_profile():
    u       = st.session_state.user
    icon    = SERVICE_ICON.get(u.get("service_type",""),"🔧")
    rating  = u.get("rating",0)
    r_count = u.get("rating_count",0)
    stars   = "⭐"*round(rating) if rating else "لا يوجد تقييم بعد"
    reviews = get_reviews(u["email"])
    verified_badge = "✅ موثق" if u.get("verified") else "❌ غير موثق"

    st.markdown('<div class="section-title">👤 ملفي الشخصي</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <div style="display:flex;gap:18px;align-items:center;flex-wrap:wrap;">
            <div style="font-size:3rem;">{icon}</div>
            <div>
                <div style="font-size:1.2rem;font-weight:900;color:#1A1A2E;">{u['name']} {verified_badge}</div>
                <div style="color:#888;font-size:0.87rem;">
                    📍 {u.get('city','—')} &nbsp;|&nbsp; 🔧 {u.get('service_type','—')}
                </div>
                <div style="color:#888;font-size:0.87rem;">
                    ⏱️ خبرة: {u.get('experience','غير محدد')}
                </div>
                <div style="margin-top:5px;">
                    <span class="stars">{stars}</span>
                    <span style="color:#aaa;font-size:0.83rem;"> ({r_count} تقييم)</span>
                </div>
            </div>
        </div>
        <div style="margin-top:14px;padding-top:14px;border-top:1px solid #F0EBE3;
                    color:#444;font-size:0.92rem;">
            {u.get('bio','لم تتم إضافة نبذة.')}
        </div>
    </div>""", unsafe_allow_html=True)

    if reviews:
        st.markdown('<div class="section-title">💬 تقييمات العملاء</div>', unsafe_allow_html=True)
        for r in reversed(reviews):
            st.markdown(f"""
            <div style="border-right:3px solid #FF6B35;padding:9px 14px;margin-bottom:9px;
                        background:white;border-radius:10px;box-shadow:0 1px 6px rgba(0,0,0,0.05);">
                <strong>{r['client']}</strong> &nbsp; {'⭐'*r['rating']}
                <br><span style="color:#555;font-size:0.88rem;">{r['comment']}</span>
                <br><span style="color:#bbb;font-size:0.76rem;">{r['date']}</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("لم تصلك تقييمات بعد ⭐")

# ─────────────────────────────────────────────
#  Messaging page
# ─────────────────────────────────────────────
def page_messaging():
    u = st.session_state.user
    all_users = get_all_users()

    st.markdown('<div class="section-title">💬 المحادثات</div>', unsafe_allow_html=True)

    # قائمة جهات الاتصال المحتملة
    if u["type"] == "client":
        # كل مقدمي الخدمة، أو من تعامل معهم
        providers = get_providers()
        contacts = {p["email"]: p["name"] for p in providers}
    else:
        # العملاء الذين حجزوا معي أو راسلتهم
        bookings = get_provider_bookings(u["email"])
        clients_emails = set()
        for b in bookings:
            clients_emails.add(b["client"])
        # أيضًا من المحادثات
        chat_partners = get_chat_partners(u["email"])
        clients_emails.update(chat_partners)
        contacts = {}
        for email in clients_emails:
            user = all_users.get(email)
            if user:
                contacts[email] = user["name"]

    # إذا كنت فاتح محادثة مع شخص محدد
    if st.session_state.chat_partner and st.session_state.chat_partner in contacts:
        partner_email = st.session_state.chat_partner
        partner_name = contacts[partner_email]
    else:
        partner_email = None
        partner_name = None

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("جهات الاتصال")
        if contacts:
            for email, name in contacts.items():
                if st.button(f"{'🟢' if email==partner_email else '⚪'} {name}", key=f"contact_{email}"):
                    st.session_state.chat_partner = email
                    st.rerun()
        else:
            st.info("لا يوجد جهات اتصال بعد.")

    with col2:
        if partner_email:
            st.subheader(f"محادثة مع {partner_name}")
            msgs = get_conversation(u["email"], partner_email)
            # عرض الرسائل
            chat_container = st.container()
            with chat_container:
                for msg in msgs:
                    is_me = msg["from"] == u["email"]
                    align = "left" if is_me else "right"
                    color_class = "chat-sent" if is_me else "chat-recv"
                    st.markdown(f"""
                    <div style="display:flex; justify-content:{'flex-end' if is_me else 'flex-start'};">
                        <div class="chat-msg {color_class}">
                            {msg["text"]}
                            <div class="chat-time">{msg["timestamp"]}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # إرسال رسالة جديدة
            with st.form(key="chat_form", clear_on_submit=True):
                new_msg = st.text_input("اكتب رسالتك...", key="msg_input")
                if st.form_submit_button("إرسال") and new_msg:
                    send_message(u["email"], partner_email, new_msg)
                    st.rerun()
        else:
            st.info("اختر جهة اتصال للبدء")

# ─────────────────────────────────────────────
#  Notifications page
# ─────────────────────────────────────────────
def page_notifications():
    u = st.session_state.user
    notifications = get_notifications(u["email"])

    st.markdown('<div class="section-title">🔔 الإشعارات</div>', unsafe_allow_html=True)

    if not notifications:
        st.info("لا توجد إشعارات حالياً.")
        return

    if st.button("✅ تعليم الكل كمقروء"):
        mark_all_read(u["email"])
        st.rerun()

    for n in reversed(notifications):
        bg = "#FFF3EC" if not n["read"] else "#F9F9F9"
        st.markdown(f"""
        <div style="background:{bg}; padding:12px; border-radius:10px; margin-bottom:8px;
                    border-right: 4px solid {'#FF6B35' if not n['read'] else '#ccc'};">
            <div style="font-size:0.9rem;">{n['message']}</div>
            <div style="color:#999; font-size:0.7rem; margin-top:5px;">{n['time']}</div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  About page
# ─────────────────────────────────────────────
def page_about():
    st.markdown("""
    <div class="hero">
        <h1>⚡ Anjaz | أنجز</h1>
        <p>وسيط بين العميل ومقدم الخدمة</p>
    </div>""", unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        st.markdown("""<div class="card">
        <div style="font-size:1rem;font-weight:800;color:#FF6B35;margin-bottom:10px;">
            🎯 الفئة المستهدفة
        </div>
        <ul style="list-style:none;padding:0;line-height:2.2;color:#444;">
            <li>👨‍👩‍👧 الأسر</li><li>🧑 الشباب</li>
            <li>🏢 أصحاب الشقق</li><li>👤 أي شخص يحتاج خدمة</li>
        </ul></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="card">
        <div style="font-size:1rem;font-weight:800;color:#FF6B35;margin-bottom:10px;">
            💰 نموذج الربح
        </div>
        <ul style="list-style:none;padding:0;line-height:2.2;color:#444;">
            <li>💸 عمولة على كل طلب</li>
            <li>📢 إعلانات ممولة</li>
            <li>🏆 اشتراكات لمقدمي الخدمة</li>
        </ul></div>""", unsafe_allow_html=True)

    st.markdown("""<div class="card" style="text-align:center;">
        <div style="font-size:0.95rem;color:#555;line-height:2;">
            Anjaz — فكرة بسيطة، قابلة للتنفيذ، وتخدم المجتمع ❤️<br>
            <strong style="color:#FF6B35;">Anjaz © 2025</strong>
        </div>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Router
# ─────────────────────────────────────────────
def main():
    render_sidebar()

    page   = st.session_state.page
    logged = st.session_state.logged_in
    u      = st.session_state.user

    if not logged:
        if   page=="login":    page_login()
        elif page=="register": page_register()
        elif page=="about":    page_about()
        else:                  page_landing()
        return

    if u["type"]=="client":
        if   page=="home":         page_client_home()
        elif page=="services":     page_services()
        elif page=="booking":      page_booking()
        elif page=="my_bookings":  page_my_bookings()
        elif page=="messaging":    page_messaging()
        elif page=="notifications":page_notifications()
        elif page=="about":        page_about()
        else:                      page_client_home()
    else:
        if   page=="home":               page_provider_home()
        elif page=="provider_orders":    page_provider_orders()
        elif page=="provider_profile":   page_provider_profile()
        elif page=="messaging":          page_messaging()
        elif page=="notifications":      page_notifications()
        elif page=="about":              page_about()
        else:                            page_provider_home()

if __name__=="__main__":
    main()