import streamlit as st
import json
import os
import hashlib
import re
from datetime import datetime, timedelta
import time

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
#  CSS  — محدث مع ميزات جديدة
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
.badge-yellow { background:#FFF8E1; color:#F57F17; border-color:#FFE082; }
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

/* Chat styles */
.chat-container {
    background: white;
    border-radius: 14px;
    padding: 18px;
    height: 500px;
    overflow-y: auto;
    border: 1px solid #F0EBE3;
    margin-bottom: 14px;
}

.message-sent {
    background: linear-gradient(135deg, #FF6B35, #F7931E);
    color: white;
    border-radius: 14px 4px 14px 14px;
    padding: 10px 14px;
    margin-bottom: 8px;
    max-width: 70%;
    margin-left: auto;
    text-align: right;
    font-size: 0.9rem;
}

.message-received {
    background: #F0EBE3;
    color: #333;
    border-radius: 4px 14px 14px 14px;
    padding: 10px 14px;
    margin-bottom: 8px;
    max-width: 70%;
    margin-right: auto;
    text-align: right;
    font-size: 0.9rem;
}

.message-time {
    font-size: 0.7rem;
    opacity: 0.6;
    margin-top: 3px;
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

/* Notification badge */
.notification-badge {
    display: inline-block;
    background: #FF4757;
    color: white;
    border-radius: 50%;
    padding: 2px 6px;
    font-size: 0.7rem;
    font-weight: 900;
}

div[data-testid="stTabs"] button {
    font-family: 'Cairo', sans-serif !important;
    font-weight: 700 !important;
}
.stRadio > div { flex-direction: row !important; gap: 14px !important; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  ثوابت وملفات قاعدة البيانات
# ─────────────────────────────────────────────

SERVICES = [
    {"icon":"🚗","name":"سيارات"},
    {"icon":"🚚","name":"نقل و��وصيل"},
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

# DB helpers
USERS_FILE        = "anjaz_users.json"
BOOKINGS_FILE     = "anjaz_bookings.json"
REVIEWS_FILE      = "anjaz_reviews.json"
NOTIFICATIONS_FILE = "anjaz_notifications.json"
MESSAGES_FILE     = "anjaz_messages.json"
VERIFICATIONS_FILE = "anjaz_verifications.json"
TIME_SLOTS_FILE   = "anjaz_time_slots.json"

def _load(path):
    if os.path.exists(path):
        with open(path,"r",encoding="utf-8") as f:
            return json.load(f)
    return {} if path != MESSAGES_FILE else []

def _save(path, data):
    with open(path,"w",encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def validate_phone(phone):
    """التحقق من صيغة رقم الهاتف المصري"""
    phone = phone.replace(" ", "").replace("-", "")
    pattern = r'^(\+201|01|001201)[0-9]{9}$'
    return bool(re.match(pattern, phone))

def validate_id(id_num):
    """التحقق من صيغة رقم الهوية المصري"""
    return len(id_num) == 14 and id_num.isdigit()

# ─────────────────────────────────────────────
#  نظام المستخدمين والتسجيل
# ─────────────────────────────────────────────

def register_user(name,email,password,user_type,city,
                  service_type=None,bio=None,experience=None):
    users = _load(USERS_FILE)
    if email in users:
        return False,"هذا الإيميل مسجل بالفعل 📧"
    users[email] = {
        "name":name,"email":email,
        "password":hash_pw(password),
        "type":user_type,"city":city,
        "service_type":service_type,
        "bio":bio or "","experience":experience or "",
        "joined":datetime.now().strftime("%Y-%m-%d"),
        "rating":0.0,"rating_count":0,
        "phone":"", "id":"", "verified":False,
        "is_admin": False, "blocked": False,
    }
    _save(USERS_FILE,users)
    return True,"تم التسجيل بنجاح ✅"

def login_user(email,password):
    users = _load(USERS_FILE)
    if email not in users:
        return False,None,"الإيميل غير مسجل ❌"
    if users[email].get("blocked", False):
        return False,None,"حسابك معطل من قبل الإدارة ❌"
    if users[email]["password"] != hash_pw(password):
        return False,None,"كلمة المرور غير صحيحة ❌"
    return True,users[email],"مرحباً بك ✅"

def get_all_users():
    return _load(USERS_FILE)

def get_providers(service=None,city=None):
    users = _load(USERS_FILE)
    result = [u for u in users.values() if u["type"]=="provider" and not u.get("blocked", False)]
    if service: result = [u for u in result if u.get("service_type")==service]
    if city:    result = [u for u in result if u.get("city")==city]
    return result

def update_user(email, updates):
    """تحديث بيانات المستخدم"""
    users = _load(USERS_FILE)
    if email in users:
        users[email].update(updates)
        _save(USERS_FILE, users)
        return True
    return False

def update_rating(provider_email,new_rating):
    users = _load(USERS_FILE)
    if provider_email in users:
        u = users[provider_email]
        old_total = u["rating"]*u["rating_count"]
        u["rating_count"] += 1
        u["rating"] = round((old_total+new_rating)/u["rating_count"],1)
        _save(USERS_FILE,users)

# ─────────────────────────────────────────────
#  نظام الحجوزات
# ─────────────────────────────────────────────

def save_booking(client_email,provider_email,service,details,date,time_slot):
    bookings = _load(BOOKINGS_FILE)
    bid = f"B{len(bookings)+1:04d}_{datetime.now().strftime('%H%M%S')}"
    bookings[bid] = {
        "id":bid,"client":client_email,
        "provider":provider_email,"service":service,
        "details":details,"date":str(date),"time":time_slot,
        "status":STATUS_PENDING,"rated":False,
        "booked_at":datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    _save(BOOKINGS_FILE,bookings)
    
    # إرسال إشعار
    send_notification(provider_email, 
        f"طلب حجز جديد! عميل يريد حجزك لخدمة {service}", 
        "booking")
    
    return bid

def update_booking_status(bid,new_status):
    bookings = _load(BOOKINGS_FILE)
    if bid in bookings:
        old_status = bookings[bid]["status"]
        bookings[bid]["status"] = new_status
        _save(BOOKINGS_FILE,bookings)
        
        # إرسال إشعار للعميل
        send_notification(bookings[bid]["client"],
            f"تحديث الحجز: {new_status}",
            "status_update")

def mark_rated(bid):
    bookings = _load(BOOKINGS_FILE)
    if bid in bookings:
        bookings[bid]["rated"] = True
        _save(BOOKINGS_FILE,bookings)

def get_client_bookings(client_email):
    return [b for b in _load(BOOKINGS_FILE).values() if b["client"]==client_email]

def get_provider_bookings(provider_email):
    return [b for b in _load(BOOKINGS_FILE).values() if b["provider"]==provider_email]

# ─────────────────────────────────────────────
#  نظام التقييمات
# ─────────────────────────────────────────────

def save_review(provider_email,client_name,rating,comment):
    reviews = _load(REVIEWS_FILE)
    if provider_email not in reviews:
        reviews[provider_email]=[]
    reviews[provider_email].append({
        "client":client_name,"rating":rating,
        "comment":comment,"date":datetime.now().strftime("%Y-%m-%d"),
    })
    _save(REVIEWS_FILE,reviews)

def get_reviews(provider_email):
    return _load(REVIEWS_FILE).get(provider_email,[])

def get_provider_analytics(provider_email):
    """تحليلات مفصلة لمقدم الخدمة"""
    reviews = get_reviews(provider_email)
    if not reviews:
        return {"avg_rating": 0, "total_reviews": 0, "5_stars": 0, "4_stars": 0, "3_stars": 0}
    
    ratings = [r["rating"] for r in reviews]
    return {
        "avg_rating": round(sum(ratings) / len(ratings), 2),
        "total_reviews": len(reviews),
        "5_stars": len([r for r in reviews if r["rating"] == 5]),
        "4_stars": len([r for r in reviews if r["rating"] == 4]),
        "3_stars": len([r for r in reviews if r["rating"] == 3]),
    }

# ─────────────────────────────────────────────
#  نظام الإشعارات
# ─────────────────────────────────────────────

def send_notification(user_email, message, notification_type="info"):
    """حفظ الإشعارات للمستخدمين"""
    notifications = _load(NOTIFICATIONS_FILE)
    if user_email not in notifications:
        notifications[user_email] = []
    notifications[user_email].append({
        "message": message,
        "type": notification_type,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "read": False
    })
    _save(NOTIFICATIONS_FILE, notifications)

def get_notifications(user_email):
    """الحصول على إشعارات المستخدم"""
    notifications = _load(NOTIFICATIONS_FILE)
    return notifications.get(user_email, [])

def get_unread_count(user_email):
    """عدد الإشعارات غير المقروءة"""
    notifs = get_notifications(user_email)
    return len([n for n in notifs if not n.get("read", False)])

def mark_notification_read(user_email, index):
    """تعليم الإشعار كمقروء"""
    notifications = _load(NOTIFICATIONS_FILE)
    if user_email in notifications and index < len(notifications[user_email]):
        notifications[user_email][index]["read"] = True
        _save(NOTIFICATIONS_FILE, notifications)

# ─────────────────────────────────────────────
#  نظام الرسائل والدردشة
# ─────────────────────────────────────────────

def send_message(sender_email, receiver_email, message_text, booking_id=None):
    """إرسال رسالة مباشرة"""
    messages = _load(MESSAGES_FILE)
    msg_id = f"M{len(messages)+1:04d}"
    messages.append({
        "id": msg_id,
        "sender": sender_email,
        "receiver": receiver_email,
        "message": message_text,
        "booking_id": booking_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "read": False
    })
    _save(MESSAGES_FILE, messages)
    
    # إرسال إشعار
    send_notification(receiver_email, 
        f"رسالة جديدة من مستخدم", 
        "message")
    
    return msg_id

def get_conversation(email1, email2, booking_id=None):
    """الحصول على محادثة بين شخصين"""
    messages = _load(MESSAGES_FILE)
    conversation = [
        m for m in messages 
        if ((m["sender"] == email1 and m["receiver"] == email2) or
            (m["sender"] == email2 and m["receiver"] == email1))
    ]
    
    if booking_id:
        conversation = [m for m in conversation if m.get("booking_id") == booking_id]
    
    return sorted(conversation, key=lambda x: x["timestamp"])

def mark_messages_read(email1, email2):
    """تعليم الرسائل كمقروءة"""
    messages = _load(MESSAGES_FILE)
    for m in messages:
        if m["sender"] == email1 and m["receiver"] == email2 and not m.get("read"):
            m["read"] = True
    _save(MESSAGES_FILE, messages)

def get_unread_messages_count(user_email):
    """عدد الرسائل غير المقروءة"""
    messages = _load(MESSAGES_FILE)
    return len([m for m in messages 
                if m["receiver"] == user_email and not m.get("read", False)])

# ─────────────────────────────────────────────
#  نظام التحقق والتوثيق
# ─────────────────────────────────────────────

def save_verification(email, phone, id_number, id_type="national"):
    """حفظ بيانات التحقق"""
    verifications = _load(VERIFICATIONS_FILE)
    
    if not validate_phone(phone):
        return False, "رقم الهاتف غير صحيح ❌"
    
    if not validate_id(id_number):
        return False, "رقم الهوية يجب أن يكون 14 رقم ❌"
    
    verifications[email] = {
        "phone": phone,
        "id_number": id_number,
        "id_type": id_type,
        "verified_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": "verified"
    }
    _save(VERIFICATIONS_FILE, verifications)
    
    # تحديث بيانات المستخدم
    update_user(email, {
        "phone": phone,
        "id": id_number,
        "verified": True
    })
    
    return True, "تم التحقق بنجاح ✅"

def get_verification(email):
    """الحصول على بيانات التحقق"""
    verifications = _load(VERIFICATIONS_FILE)
    return verifications.get(email, None)

# ─────────────────────────────────────────────
#  نظام الأوقات المخصصة
# ─────────────────────────────────────────────

def set_custom_time_slots(provider_email, time_slots):
    """تعيين أوقات عمل مخصصة"""
    slots = _load(TIME_SLOTS_FILE)
    slots[provider_email] = {
        "time_slots": time_slots,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    _save(TIME_SLOTS_FILE, slots)

def get_custom_time_slots(provider_email):
    """الحصول على الأوقات المخصصة"""
    slots = _load(TIME_SLOTS_FILE)
    if provider_email in slots:
        return slots[provider_email].get("time_slots", [])
    return [
        "صباحاً 8:00 - 10:00","صباحاً 10:00 - 12:00",
        "ظهراً 12:00 - 2:00","عصراً 2:00 - 4:00",
        "مساءً 4:00 - 6:00","مساءً 6:00 - 8:00",
    ]

# ─────────────────────────────────────────────
#  نظام البحث المتقدم
# ─────────────────────────────────────────────

def search_providers(query, city=None, service=None, min_rating=0):
    """بحث متقدم عن مقدمي الخدمات"""
    providers = get_providers(service, city)
    query_lower = query.lower()
    
    results = [
        p for p in providers 
        if (query_lower in p.get("name", "").lower() or
            query_lower in p.get("bio", "").lower()) and
        p.get("rating", 0) >= min_rating
    ]
    return sorted(results, key=lambda x: -x.get("rating", 0))

# ─────────────────────────────────────────────
#  نظام الإحصائيات
# ─────────────────────────────────────────────

def get_provider_stats(provider_email):
    """الحصول على إحصائيات مقدم الخدمة"""
    orders = get_provider_bookings(provider_email)
    confirmed = len([o for o in orders if STATUS_CONFIRM in o["status"]])
    cancelled = len([o for o in orders if STATUS_CANCEL in o["status"]])
    pending = len([o for o in orders if STATUS_PENDING in o["status"]])
    
    return {
        "total": len(orders),
        "confirmed": confirmed,
        "cancelled": cancelled,
        "pending": pending,
        "acceptance_rate": round((confirmed / len(orders) * 100), 1) if orders else 0
    }

def get_admin_stats():
    """إحصائيات عامة للتطبيق"""
    users = get_all_users()
    bookings = _load(BOOKINGS_FILE)
    
    clients = len([u for u in users.values() if u["type"] == "client"])
    providers = len([u for u in users.values() if u["type"] == "provider"])
    verified = len([u for u in users.values() if u.get("verified", False)])
    
    confirmed_bookings = len([b for b in bookings.values() if STATUS_CONFIRM in b["status"]])
    pending_bookings = len([b for b in bookings.values() if STATUS_PENDING in b["status"]])
    
    return {
        "total_users": len(users),
        "clients": clients,
        "providers": providers,
        "verified_users": verified,
        "total_bookings": len(bookings),
        "confirmed_bookings": confirmed_bookings,
        "pending_bookings": pending_bookings,
    }

# Session state
for k,v in {
    "logged_in":False,"user":None,"page":"home",
    "selected_service":None,"selected_provider":None,
    "chat_partner": None, "chat_booking": None,
}.items():
    if k not in st.session_state:
        st.session_state[k]=v

def go(page):
    st.session_state.page=page
    st.rerun()

# ─────────────────────────────────────────────
#  شريط جانبي محدث
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
            verified_badge = "✅ موثق" if u.get("verified", False) else "⚠️ غير موثق"
            
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.09);border-radius:12px;
                        padding:12px;margin:0 10px 18px;text-align:center;'>
                <div style='font-size:0.98rem;font-weight:800;'>{u['name']}</div>
                <div style='font-size:0.78rem;opacity:0.7;margin-top:2px;'>{utype_label}</div>
                <div style='font-size:0.75rem;opacity:0.55;'>📍 {u.get("city","")}</div>
                <div style='font-size:0.75rem;color:#FFD700;margin-top:3px;'>{verified_badge}</div>
            </div>""", unsafe_allow_html=True)

            # شارة الإشعارات
            unread_notif = get_unread_count(u["email"])
            unread_msgs = get_unread_messages_count(u["email"])
            
            st.markdown("<div style='padding:0 10px;'>", unsafe_allow_html=True)

            if u["type"]=="client":
                menu=[
                    ("🏠","الرئيسية","home"),
                    ("🔧","الخدمات","services"),
                    ("📅","حجوزاتي","my_bookings"),
                    (f"💬 {unread_msgs}" if unread_msgs > 0 else "💬","الدردشات","messages"),
                    (f"🔔 {unread_notif}" if unread_notif > 0 else "🔔","الإشعارات","notifications"),
                    ("👤","حسابي","my_profile"),
                    ("ℹ️","عن التطبيق","about"),
                ]
            else:
                menu=[
                    ("🏠","لوحة التحكم","home"),
                    ("📋","طلباتي","provider_orders"),
                    (f"💬 {unread_msgs}" if unread_msgs > 0 else "💬","الدردشات","messages"),
                    (f"🔔 {unread_notif}" if unread_notif > 0 else "🔔","الإشعارات","notifications"),
                    ("👤","ملفي الشخصي","provider_profile"),
                    ("⚙️","الإعدادات","provider_settings"),
                    ("ℹ️","عن التطبيق","about"),
                ]
            
            # إضافة لوحة الإدارة للمسؤولين
            if u.get("is_admin", False):
                menu.insert(0, ("🛡️","لوحة الإدارة","admin_dashboard"))

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
#  صفحات المصادقة
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

    service_type=bio=experience=None
    if is_provider:
        st.markdown("---")
        st.markdown("**🔧 معلومات الخدمة**")
        service_type = st.selectbox("نوع الخدمة التي تقدمها", SERVICE_NAMES, key="rs")
        bio = st.text_area("📝 نبذة عنك",
            placeholder="اكتب نبذة عن خبرتك وما تقدمه للعملاء...",
            height=90, key="rb")
        experience = st.text_input("📅 سنوات الخبرة", placeholder="مثلاً: 5 سنوات", key="rx")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("إنشاء الحساب 🚀", key="btn_reg"):
        if name and email and pw and pw2 and city:
            if pw!=pw2:
                st.error("كلمتا المرور غير متطابقتين ❌")
            elif len(pw)<6:
                st.error("كلمة المرور أقل من 6 أحرف ❌")
            else:
                utype="provider" if is_provider else "client"
                ok,msg = register_user(name.strip(),email.strip().lower(),pw,
                                       utype,city,service_type,bio,experience)
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
#  صفحة التوثيق
# ─────────────────────────────────────────────

def page_verification():
    st.markdown('<div class="section-title">📋 التحقق والتوثيق</div>', unsafe_allow_html=True)
    
    u = st.session_state.user
    
    if u.get("verified", False):
        existing = get_verification(u["email"])
        st.success("✅ حسابك موثق بالفعل")
        st.markdown(f"""
        <div class="card">
            <strong>رقم الهاتف:</strong> {existing.get("phone", "—")}<br>
            <strong>رقم الهوية:</strong> {existing.get("id_number", "—")}<br>
            <strong>تاريخ التوثيق:</strong> {existing.get("verified_at", "—")}
        </div>""", unsafe_allow_html=True)
        return
    
    st.warning("⚠️ حسابك غير موثق. أكمل البيانات التالية للتوثق:")
    
    with st.form("verification_form"):
        phone = st.text_input(
            "📱 رقم الهاتف المصري",
            placeholder="مثال: 01012345678 أو +201012345678",
            key="verify_phone"
        )
        
        id_number = st.text_input(
            "🪪 رقم الهوية الشخصية",
            placeholder="14 رقم",
            key="verify_id",
            max_chars=14
        )
        
        id_type = st.selectbox(
            "نوع الهوية",
            ["بطاقة هوية وطنية", "جواز سفر"],
            key="verify_type"
        )
        
        submitted = st.form_submit_button("✅ التحقق الآن")
    
    if submitted:
        ok, msg = save_verification(u["email"], phone, id_number, 
                                   "national" if id_type == "بطاقة هوية وطنية" else "passport")
        if ok:
            st.success(msg)
            st.session_state.user["verified"] = True
            st.session_state.user["phone"] = phone
            st.session_state.user["id"] = id_number
            st.rerun()
        else:
            st.error(msg)

# ─────────────────────────────────────────────
#  صفحة الإشعارات
# ─────────────────────────────────────────────

def page_notifications():
    st.markdown('<div class="section-title">🔔 الإشعارات</div>', unsafe_allow_html=True)
    
    u = st.session_state.user
    notifications = get_notifications(u["email"])
    
    if not notifications:
        st.info("لا توجد إشعارات جديدة ✅")
        return
    
    # ترتيب الإشعارات من الأحدث
    sorted_notifs = sorted(notifications, key=lambda x: x["timestamp"], reverse=True)
    
    for i, notif in enumerate(sorted_notifs):
        read_status = "✅" if notif.get("read") else "🆕"
        bg_color = "#FFFAF7" if notif.get("read") else "#FFF3EC"
        
        col1, col2 = st.columns([0.9, 0.1])
        with col1:
            st.markdown(f"""
            <div style='background:{bg_color};border-radius:10px;padding:12px;
                        margin-bottom:8px;border-right:3px solid #FF6B35;'>
                <strong>{read_status} {notif["message"]}</strong><br>
                <span style='color:#999;font-size:0.8rem;'>⏰ {notif["timestamp"]}</span>
            </div>""", unsafe_allow_html=True)
        
        with col2:
            if not notif.get("read"):
                if st.button("✓", key=f"mark_read_{i}", help="تعليم كمقروء"):
                    mark_notification_read(u["email"], i)
                    st.rerun()

# ─────────────────────────────────────────────
#  صفحة الدردشة
# ─────────────────────────────────────────────

def page_messages():
    st.markdown('<div class="section-title">💬 الدردشات</div>', unsafe_allow_html=True)
    
    u = st.session_state.user
    messages = _load(MESSAGES_FILE)
    
    # الحصول على قائمة الأشخاص الذين تحدثت معهم
    contacts = set()
    for msg in messages:
        if msg["sender"] == u["email"]:
            contacts.add(msg["receiver"])
        elif msg["receiver"] == u["email"]:
            contacts.add(msg["sender"])
    
    if not contacts:
        st.info("لا توجد محادثات بعد.")
        return
    
    all_users = get_all_users()
    
    tab1, tab2 = st.tabs(["👥 المحادثات", "🔔 طلب محادثة جديدة"])
    
    with tab1:
        for contact_email in list(contacts):
            contact = all_users.get(contact_email, {})
            contact_name = contact.get("name", contact_email)
            
            unread = len([m for m in messages 
                         if m["sender"] == contact_email and m["receiver"] == u["email"] 
                         and not m.get("read")])
            
            unread_badge = f" <span class='notification-badge'>{unread}</span>" if unread > 0 else ""
            
            if st.button(f"👤 {contact_name}{unread_badge}" if unread == 0 
                        else f"👤 {contact_name} 🆕", 
                        key=f"contact_{contact_email}"):
                st.session_state.chat_partner = contact_email
                st.rerun()
    
    with tab2:
        st.markdown("**ابدأ محادثة جديدة مع مقدم خدمة:**")
        selected_provider = st.selectbox(
            "اختار المتخصص",
            [f"{p.get('name')} ({p.get('service_type')})" for p in get_providers()],
            key="new_chat"
        )
        if selected_provider:
            provider_email = [p["email"] for p in get_providers() 
                            if f"{p.get('name')} ({p.get('service_type')})" == selected_provider][0]
            if st.button("💬 فتح الدردشة"):
                st.session_state.chat_partner = provider_email
                st.rerun()
    
    # عرض الدردشة النشطة
    if st.session_state.chat_partner:
        render_chat(u, st.session_state.chat_partner)

def render_chat(user, partner_email):
    """عرض واجهة الدردشة"""
    all_users = get_all_users()
    partner = all_users.get(partner_email, {})
    partner_name = partner.get("name", partner_email)
    
    st.markdown(f"<hr style='margin:20px 0;'>", unsafe_allow_html=True)
    st.markdown(f"<h3>💬 محادثة مع {partner_name}</h3>", unsafe_allow_html=True)
    
    # الحصول على المحادثة
    conversation = get_conversation(user["email"], partner_email)
    mark_messages_read(partner_email, user["email"])
    
    # عرض الرسائل
    chat_html = "<div class='chat-container'>"
    for msg in conversation:
        if msg["sender"] == user["email"]:
            chat_html += f"""
            <div class='message-sent'>
                {msg['message']}
                <div class='message-time'>{msg['timestamp'].split()[1]}</div>
            </div>"""
        else:
            chat_html += f"""
            <div class='message-received'>
                {msg['message']}
                <div class='message-time'>{msg['timestamp'].split()[1]}</div>
            </div>"""
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)
    
    # إرسال رسالة جديدة
    st.markdown("<br>", unsafe_allow_html=True)
    message_text = st.text_input("اكتب رسالتك...", key=f"msg_{partner_email}")
    
    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        pass
    with col2:
        if st.button("📤 إرسال", key=f"send_{partner_email}"):
            if message_text.strip():
                send_message(user["email"], partner_email, message_text.strip())
                st.rerun()
            else:
                st.warning("اكتب رسالة ⚠️")

# ─────────────────────────────────────────────
#  صفحات العملاء
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
        if st.button("🔑 سجّل دخولك ��ابدأ الآن ⚡", key="landing_cta"):
            go("login")

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

    c1,c2,c3 = st.columns(3)
    with c1:
        default_idx=(SERVICE_NAMES.index(st.session_state.selected_service)+1
                     if st.session_state.selected_service else 0)
        filter_svc = st.selectbox("نوع الخدمة",["الكل"]+SERVICE_NAMES,
                                  index=default_idx, key="fs")
    with c2:
        filter_city = st.selectbox("المحافظة",["الكل"]+CITIES, key="fc")
    
    with c3:
        search_query = st.text_input("🔍 بحث عن متخصص", key="search_prov")

    svc_q  = None if filter_svc =="الكل" else filter_svc
    city_q = None if filter_city=="الكل" else filter_city
    
    if search_query:
        providers = search_providers(search_query, city_q, svc_q)
    else:
        providers = get_providers(svc_q, city_q)

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
        verified = "✅" if p.get("verified", False) else "⚠️"
        reviews  = get_reviews(p["email"])

        st.markdown(f"""
        <div class="pcard">
            <div class="bitem-header">
                <div>
                    <div class="pname">{icon} {p['name']} {verified}</div>
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

        col_r,col_b,col_c = st.columns([2,1,1])
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
            if st.button("📅 احجز", key=f"bk_{p['email']}"):
                st.session_state.selected_provider=p
                go("booking")
        
        with col_c:
            if st.button("💬 تحدث", key=f"chat_{p['email']}"):
                st.session_state.chat_partner = p['email']
                go("messages")

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

    # الحصول على الأوقات المخصصة لمقدم الخدمة
    available_times = get_custom_time_slots(p["email"])

    with st.form("bform"):
        c1,c2 = st.columns(2)
        with c1:
            date = st.date_input("📅 تاريخ الخدمة", min_value=datetime.today())
        with c2:
            time_slot = st.selectbox("🕐 الوقت المناسب", available_times)
        details = st.text_area("📝 وصف المشكلة",
            placeholder="اشرح المشكلة بالتفصيل...", height=100)
        address = st.text_input("📍 العنوان التفصيلي",
            placeholder="الشارع، رقم المبنى، الدور...")
        submitted = st.form_submit_button("✅ إرسال طلب الحجز")

    if submitted:
        if details and address:
            u = st.session_state.user
            booking_id = save_booking(u["email"], p["email"], p.get("service_type",""),
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

        col_chat, col_cancel, col_empty = st.columns([1, 1, 2])
        
        with col_chat:
            if st.button("💬 تحدث", key=f"booking_chat_{b['id']}"):
                st.session_state.chat_partner = b["provider"]
                go("messages")
        
        with col_cancel:
            if STATUS_PENDING in status:
                if st.button("❌ إلغاء", key=f"cli_cancel_{b['id']}"):
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

def page_my_profile():
    """صفحة حسابي للعملاء"""
    u = st.session_state.user
    
    st.markdown('<div class="section-title">👤 حسابي</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 البيانات الأساسية", "🔐 التحقق والأمان", "📊 إحصائياتي"])
    
    with tab1:
        st.markdown(f"""
        <div class="card">
            <strong>الاسم:</strong> {u['name']}<br>
            <strong>البريد الإلكتروني:</strong> {u['email']}<br>
            <strong>المدينة:</strong> {u.get('city', '—')}<br>
            <strong>تاريخ الانضمام:</strong> {u.get('joined', '—')}<br>
            <strong>حالة الحساب:</strong> {'✅ نشط' if not u.get('blocked') else '❌ معطل'}
        </div>""", unsafe_allow_html=True)
    
    with tab2:
        if u.get("verified", False):
            verification = get_verification(u["email"])
            st.success("✅ حسابك موثق")
            st.markdown(f"""
            <div class="card">
                <strong>📱 الهاتف:</strong> {verification.get("phone", "—")}<br>
                <strong>🪪 الهوية:</strong> {verification.get("id_number", "—")}<br>
                <strong>📅 تاريخ التوثيق:</strong> {verification.get("verified_at", "—")}
            </div>""", unsafe_allow_html=True)
        else:
            st.warning("⚠️ حسابك غير موثق")
            if st.button("التوثيق الآن"):
                go("verification")
    
    with tab3:
        bookings = get_client_bookings(u["email"])
        confirmed = len([b for b in bookings if STATUS_CONFIRM in b["status"]])
        pending = len([b for b in bookings if STATUS_PENDING in b["status"]])
        cancelled = len([b for b in bookings if STATUS_CANCEL in b["status"]])
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("📅 إجمالي الحجوزات", len(bookings))
      