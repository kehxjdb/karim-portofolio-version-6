import streamlit as st
import hashlib
from datetime import datetime
import anthropic

# ══════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Karim Maher · Data Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DEFAULT_PW_HASH = hashlib.sha256("karim2024".encode()).hexdigest()

# ══════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════
def init_state():
    defaults = {
        "admin_logged_in": False,
        "chat_messages":   [],
        "chat_open":       False,
        "_page":           "portfolio",
        "profile": {
            "name_en":   "Karim Maher",
            "title":     "Data Analyst",
            "subtitle":  "محلل بيانات · Streamlit Developer",
            "location":  "Alexandria, Egypt",
            "phone":     "01063872784",
            "email":     "",
            "linkedin":  "",
            "github":    "",
            "edu":       "دبلومة تحليل البيانات — أكاديمية Tech Trek",
            "bio":       "محلل بيانات شغوف بتحويل الأرقام إلى قرارات. أبني نماذج تحليلية وتطبيقات Streamlit تفاعلية تجعل البيانات في متناول الجميع.",
            "skills":    "Python, SQL, Power BI, Streamlit, Pandas, Scikit-learn, Excel, Matplotlib, Seaborn",
            "photo_url": "",
            "pw_hash":   DEFAULT_PW_HASH,
        },
        "projects": [],
        "certs": [
            {"icon":"🏕️","name":"Data Analyst Track",    "issuer":"DataCamp",               "color":"#f97316"},
            {"icon":"🎓","name":"دبلومة تحليل البيانات", "issuer":"أكاديمية Tech Trek",     "color":"#00d4ff"},
            {"icon":"🏛️","name":"شهادة تحليل البيانات",  "issuer":"نقابة المهندسين المصريين","color":"#a855f7"},
        ],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def hp(pw): return hashlib.sha256(pw.encode()).hexdigest()
def P(k):   return st.session_state.profile.get(k, "")

TYPE_META = {
    "dashboard": ("📊","Dashboard",        "#00d4ff"),
    "streamlit": ("🚀","Streamlit App",    "#ec4899"),
    "notebook":  ("📓","Jupyter Notebook", "#f97316"),
    "pdf":       ("📄","PDF Report",       "#a855f7"),
    "video":     ("🎬","Video",            "#22c55e"),
    "link":      ("🔗","External Link",    "#64748b"),
}

SKILL_ICONS = {
    "python":"🐍","sql":"🗄️","power":"📊","streamlit":"🚀",
    "pandas":"📈","scikit":"🤖","excel":"📋","matplotlib":"📉",
    "seaborn":"🎨","numpy":"🔢","tableau":"📊",
}

# ══════════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════════
def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@300;400;500;600&family=Cairo:wght@400;600;700;900&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
  --ink:#07070f; --ink2:#0f0f1a; --ink3:#171724; --ink4:#21212f;
  --frost:#eeeeff; --frost2:#9898b8; --frost3:#484868;
  --cyan:#00e5ff; --pink:#f72585; --purple:#7b2fff;
  --green:#06d6a0; --orange:#f97316;
  --border:rgba(255,255,255,0.07); --r:14px;
}

html,body,[class*="css"],.stApp {
  font-family:'DM Sans','Cairo',sans-serif !important;
  background:var(--ink) !important; color:var(--frost) !important;
}
#MainMenu,footer,header{display:none !important;}
[data-testid="collapsedControl"]{display:none !important;}
section[data-testid="stSidebar"]{display:none !important;}
.block-container{padding:0 !important;max-width:100% !important;}

::-webkit-scrollbar{width:5px;}
::-webkit-scrollbar-track{background:var(--ink);}
::-webkit-scrollbar-thumb{background:rgba(0,229,255,0.2);border-radius:3px;}

/* BG GRID */
.stApp::after{
  content:'';position:fixed;inset:0;z-index:0;pointer-events:none;
  background-image:
    linear-gradient(rgba(255,255,255,0.018) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,0.018) 1px,transparent 1px);
  background-size:70px 70px;
  mask-image:radial-gradient(ellipse at 50% 0%,black 20%,transparent 80%);
}

/* NAV */
.km-nav{
  position:fixed;top:0;left:0;right:0;z-index:999;height:62px;
  display:flex;align-items:center;justify-content:space-between;
  padding:0 3rem;background:rgba(7,7,15,0.82);
  backdrop-filter:blur(20px) saturate(160%);
  border-bottom:1px solid var(--border);
}
.km-logo{
  font-family:'Syne',sans-serif;font-size:1.05rem;font-weight:800;
  color:var(--frost);display:flex;align-items:center;gap:0.3rem;
}
.km-logo .c{color:var(--cyan);}
.km-nav-links{display:flex;gap:2rem;align-items:center;}
.km-nav-a{font-size:0.82rem;font-weight:500;color:var(--frost3);transition:color 0.2s;}
.km-nav-a:hover{color:var(--frost);}

/* HERO */
.km-hero{
  min-height:100vh;position:relative;z-index:1;
  display:flex;align-items:center;padding:8rem 3rem 5rem;overflow:hidden;
}
.km-hero-glow{
  position:absolute;inset:0;pointer-events:none;
  background:
    radial-gradient(ellipse 55% 60% at 78% 50%,rgba(0,229,255,0.07) 0%,transparent 70%),
    radial-gradient(ellipse 40% 50% at 10% 70%,rgba(123,47,255,0.08) 0%,transparent 70%),
    radial-gradient(ellipse 30% 40% at 50% 5%,rgba(247,37,133,0.05) 0%,transparent 60%);
}
.km-hero-content{position:relative;z-index:1;max-width:580px;}
.km-badge{
  display:inline-flex;align-items:center;gap:0.6rem;
  font-family:'JetBrains Mono',monospace;font-size:0.67rem;font-weight:600;
  color:var(--cyan);letter-spacing:1.5px;text-transform:uppercase;
  background:rgba(0,229,255,0.06);border:1px solid rgba(0,229,255,0.18);
  border-radius:100px;padding:0.35rem 1rem;margin-bottom:2rem;
}
.ldot{
  width:7px;height:7px;background:var(--green);border-radius:50%;
  box-shadow:0 0 8px var(--green);animation:lpulse 2s ease-in-out infinite;
}
@keyframes lpulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:0.4;transform:scale(0.7)}}
.km-hname{
  font-family:'Syne',sans-serif;font-weight:800;
  font-size:clamp(3rem,6.5vw,5.5rem);letter-spacing:-3px;line-height:0.95;
  background:linear-gradient(140deg,#fff 30%,#8888cc 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  margin-bottom:0.8rem;
}
.km-hrole{
  font-family:'Syne',sans-serif;font-size:clamp(1.1rem,2vw,1.5rem);
  font-weight:700;color:var(--cyan);margin-bottom:1.5rem;letter-spacing:-0.3px;
}
.km-hbio{
  font-size:0.95rem;color:var(--frost2);line-height:1.85;
  font-weight:300;margin-bottom:2.5rem;
}
.km-pills{display:flex;gap:0.6rem;flex-wrap:wrap;margin-bottom:2.5rem;}
.km-pill{
  font-family:'JetBrains Mono',monospace;font-size:0.67rem;font-weight:500;
  padding:0.32rem 0.85rem;border:1px solid var(--border);
  border-radius:100px;color:var(--frost3);background:rgba(255,255,255,0.03);
}

/* AVATAR */
.km-av-area{position:absolute;right:4rem;top:50%;transform:translateY(-50%);z-index:1;}
.km-av-ring{
  width:220px;height:220px;border-radius:50%;padding:3px;
  background:conic-gradient(var(--cyan) 0%,var(--purple) 40%,var(--pink) 70%,var(--cyan) 100%);
  animation:spinring 8s linear infinite;
}
@keyframes spinring{to{transform:rotate(360deg);}}
.km-av-inner{
  width:100%;height:100%;border-radius:50%;
  background:var(--ink2);display:flex;align-items:center;
  justify-content:center;font-size:6rem;overflow:hidden;
}
.km-av-inner img{width:100%;height:100%;object-fit:cover;border-radius:50%;}

/* SECTIONS */
.km-sec{padding:5rem 3rem;max-width:1200px;margin:0 auto;position:relative;z-index:1;}
.km-eyebrow{
  font-family:'JetBrains Mono',monospace;font-size:0.65rem;font-weight:600;
  color:var(--frost3);letter-spacing:3px;text-transform:uppercase;
  display:flex;align-items:center;gap:1rem;margin-bottom:0.8rem;
}
.km-eyebrow::after{content:'';flex:1;height:1px;background:var(--border);}
.km-sec-title{
  font-family:'Syne',sans-serif;font-weight:800;
  font-size:clamp(2rem,4vw,3rem);letter-spacing:-1.5px;
  line-height:1.05;margin-bottom:2.5rem;
}
.km-sec-title .hl{color:var(--cyan);}

/* CARDS */
.km-card{
  background:var(--ink2);border:1px solid var(--border);
  border-radius:var(--r);padding:1.8rem;
  transition:border-color 0.3s,transform 0.3s,box-shadow 0.3s;
}
.km-card:hover{border-color:rgba(0,229,255,0.22);transform:translateY(-5px);box-shadow:0 20px 50px rgba(0,0,0,0.4),0 0 30px rgba(0,229,255,0.07);}
.km-card-icon{font-size:2rem;margin-bottom:1rem;}
.km-card-title{font-family:'Syne',sans-serif;font-size:0.85rem;font-weight:700;color:var(--cyan);margin-bottom:0.5rem;}
.km-card-body{font-size:0.82rem;color:var(--frost3);line-height:1.75;font-weight:300;}
.km-about-grid{display:grid;grid-template-columns:1fr 1fr;gap:1.2rem;}

/* SKILLS */
.km-skill{
  display:inline-block;font-family:'JetBrains Mono',monospace;
  font-size:0.67rem;font-weight:500;padding:0.28rem 0.7rem;
  background:rgba(255,255,255,0.04);border:1px solid var(--border);
  border-radius:6px;color:var(--frost2);margin:0.18rem;transition:all 0.2s;
}
.km-skill:hover{border-color:var(--cyan);color:var(--cyan);background:rgba(0,229,255,0.05);}

/* CERTS */
.km-cert{
  display:flex;align-items:center;gap:1.2rem;
  background:var(--ink2);border:1px solid var(--border);
  border-radius:12px;padding:1.1rem 1.4rem;margin-bottom:0.8rem;transition:all 0.25s;
}
.km-cert:hover{border-color:rgba(0,229,255,0.18);transform:translateX(5px);}
.km-cert-icon{font-size:1.4rem;width:42px;height:42px;border-radius:10px;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.km-cert-name{font-family:'Syne',sans-serif;font-size:0.9rem;font-weight:700;margin-bottom:0.15rem;}
.km-cert-issuer{font-size:0.72rem;color:var(--frost3);}
.km-cert-chip{font-family:'JetBrains Mono',monospace;font-size:0.6rem;font-weight:600;padding:0.2rem 0.6rem;border-radius:6px;white-space:nowrap;flex-shrink:0;}

/* METRICS */
.km-metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:1.2rem;}
.km-metric{
  background:var(--ink2);border:1px solid var(--border);
  border-radius:var(--r);padding:1.5rem;text-align:center;transition:all 0.3s;
  position:relative;overflow:hidden;
}
.km-metric::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--cyan),transparent);transform:scaleX(0);transition:transform 0.4s;}
.km-metric:hover::after{transform:scaleX(1);}
.km-metric:hover{transform:translateY(-3px);}
.km-metric-val{font-family:'Syne',sans-serif;font-size:2.4rem;font-weight:800;color:var(--cyan);line-height:1;}
.km-metric-label{font-size:0.72rem;color:var(--frost3);margin-top:0.4rem;font-weight:300;}

/* PROJ */
.km-proj-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1.4rem;}
.km-proj-card{
  background:var(--ink2);border:1px solid var(--border);
  border-radius:18px;overflow:hidden;
  transition:all 0.35s cubic-bezier(0.34,1.4,0.64,1);
}
.km-proj-card:hover{border-color:rgba(0,229,255,0.22);transform:translateY(-8px);box-shadow:0 30px 60px rgba(0,0,0,0.5),0 0 30px rgba(0,229,255,0.07);}
.km-proj-thumb{height:170px;background:var(--ink3);display:flex;align-items:center;justify-content:center;font-size:4rem;position:relative;overflow:hidden;}
.km-proj-thumb img{width:100%;height:100%;object-fit:cover;}
.km-thumb-ov{position:absolute;inset:0;background:linear-gradient(to top,rgba(7,7,15,0.7) 0%,transparent 50%);}
.km-proj-chip{position:absolute;bottom:10px;right:10px;font-family:'JetBrains Mono',monospace;font-size:0.58rem;font-weight:600;padding:0.22rem 0.6rem;border-radius:6px;backdrop-filter:blur(8px);}
.km-proj-body{padding:1.2rem 1.4rem 1.4rem;}
.km-proj-name{font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;margin-bottom:0.45rem;letter-spacing:-0.3px;}
.km-proj-desc{font-size:0.78rem;color:var(--frost3);line-height:1.65;margin-bottom:0.8rem;font-weight:300;}
.km-proj-footer{display:flex;align-items:center;justify-content:space-between;gap:0.5rem;flex-wrap:wrap;}
.km-proj-tools{display:flex;flex-wrap:wrap;gap:0.3rem;}
.km-proj-tool{font-family:'JetBrains Mono',monospace;font-size:0.58rem;padding:0.14rem 0.42rem;background:rgba(255,255,255,0.04);border:1px solid var(--border);border-radius:5px;color:var(--frost3);}

/* CONTACT */
.km-contact-item{
  background:var(--ink2);border:1px solid var(--border);
  border-radius:12px;padding:1.2rem;text-align:center;transition:all 0.25s;
}
.km-contact-item:hover{border-color:rgba(0,229,255,0.2);transform:translateY(-3px);box-shadow:0 10px 30px rgba(0,0,0,0.3);}
.km-contact-icon{font-size:1.8rem;margin-bottom:0.5rem;}
.km-contact-label{font-size:0.78rem;font-weight:600;color:var(--frost2);margin-bottom:0.6rem;}

/* CHAT FAB */
div[data-testid="stButton"] > button[title="chatfab"]{
  position:fixed !important;bottom:2rem !important;left:2rem !important;
  z-index:1000 !important;width:56px !important;height:56px !important;
  border-radius:50% !important;padding:0 !important;font-size:1.3rem !important;
  background:linear-gradient(135deg,var(--cyan),var(--purple)) !important;
  border:none !important;color:var(--ink) !important;
  box-shadow:0 8px 30px rgba(0,229,255,0.3) !important;
}

/* CHAT WINDOW */
.km-chatwin{
  position:fixed;bottom:5.5rem;left:2rem;z-index:900;width:360px;
  background:var(--ink2);border:1px solid rgba(0,229,255,0.15);
  border-radius:20px;overflow:hidden;
  box-shadow:0 30px 80px rgba(0,0,0,0.6),0 0 40px rgba(0,229,255,0.06);
}
.km-chat-hdr{padding:.9rem 1.1rem;border-bottom:1px solid var(--border);background:rgba(0,229,255,0.04);display:flex;align-items:center;gap:.7rem;}
.km-chat-av{width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,var(--cyan),var(--purple));display:flex;align-items:center;justify-content:center;font-size:.9rem;flex-shrink:0;}
.km-chat-nm{font-family:'Syne',sans-serif;font-size:.82rem;font-weight:700;}
.km-chat-st{font-size:.62rem;color:var(--green);}
.km-chat-body{display:flex;flex-direction:column;gap:.7rem;padding:.8rem;max-height:240px;overflow-y:auto;}
.km-chat-body::-webkit-scrollbar{width:3px;}
.km-chat-body::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.08);border-radius:2px;}
.km-msg-u{align-self:flex-end;max-width:80%;}
.km-msg-b{align-self:flex-start;max-width:85%;}
.km-bub-u{background:linear-gradient(135deg,var(--cyan),var(--purple));color:var(--ink);border-radius:14px 14px 4px 14px;padding:.6rem .9rem;font-size:.8rem;font-weight:500;}
.km-bub-b{background:var(--ink3);border:1px solid var(--border);color:var(--frost);border-radius:14px 14px 14px 4px;padding:.6rem .9rem;font-size:.8rem;line-height:1.6;font-weight:300;}
.km-suggs{padding:.4rem .8rem;display:flex;gap:.4rem;flex-wrap:wrap;}
.km-sugg{font-size:.67rem;font-weight:500;padding:.28rem .65rem;background:rgba(0,229,255,0.06);border:1px solid rgba(0,229,255,0.15);border-radius:100px;color:var(--cyan);cursor:pointer;white-space:nowrap;transition:all 0.2s;}
.km-sugg:hover{background:rgba(0,229,255,0.12);}

/* FOOTER */
.km-footer{border-top:1px solid var(--border);padding:2.5rem 3rem;text-align:center;}
.km-footer-logo{font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:800;color:var(--cyan);margin-bottom:0.3rem;}
.km-footer-copy{font-size:0.73rem;color:var(--frost3);font-weight:300;}
.km-div{height:1px;background:var(--border);margin:0 3rem;}

/* ADMIN */
.km-admin-top{margin-bottom:2rem;padding:1.2rem 1.5rem;background:rgba(247,37,133,0.05);border:1px solid rgba(247,37,133,0.15);border-radius:12px;}
.km-admin-title{font-family:'Syne',sans-serif;font-size:1rem;font-weight:800;color:var(--pink);}
.km-admin-sub{font-size:0.72rem;color:var(--frost3);margin-top:0.2rem;}

/* LOGIN */
.km-login{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:2rem;}
.km-login-box{background:var(--ink2);border:1px solid rgba(247,37,133,0.2);border-radius:24px;padding:3rem;width:100%;max-width:400px;text-align:center;box-shadow:0 40px 100px rgba(0,0,0,0.5),0 0 50px rgba(247,37,133,0.08);}

/* ST OVERRIDES */
.stButton>button{font-family:'DM Sans',sans-serif !important;font-weight:600 !important;border-radius:10px !important;transition:all 0.25s !important;}
.stButton>button[kind="primary"]{background:var(--cyan) !important;color:var(--ink) !important;border:none !important;}
.stButton>button[kind="primary"]:hover{transform:translateY(-2px) !important;box-shadow:0 8px 25px rgba(0,229,255,0.3) !important;}
.stTextInput>div>div>input,
.stTextArea>div>div>textarea,
.stSelectbox>div>div{background:var(--ink3) !important;border-color:var(--border) !important;color:var(--frost) !important;font-family:'DM Sans',sans-serif !important;border-radius:10px !important;}
.stTabs [data-baseweb="tab"]{font-family:'Syne',sans-serif !important;font-weight:700 !important;color:var(--frost3) !important;}
.stTabs [data-baseweb="tab"][aria-selected="true"]{color:var(--cyan) !important;}
.stTabs [data-baseweb="tab-list"]{background:var(--ink2) !important;border-radius:12px !important;}
.stTabs [data-baseweb="tab-highlight"]{background:var(--cyan) !important;}
/* link_button style */
a[data-testid="stLinkButton"]>button{background:var(--cyan) !important;color:var(--ink) !important;border:none !important;font-weight:700 !important;border-radius:9px !important;font-size:0.8rem !important;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  CHATBOT
# ══════════════════════════════════════════════════════════
def build_system_prompt() -> str:
    p     = st.session_state.profile
    projs = st.session_state.projects
    certs = st.session_state.certs
    proj_lines = "\n".join([
        f"- {TYPE_META.get(pr.get('type','link'),('📁','',''))[0]} {pr.get('name','')} "
        f"({TYPE_META.get(pr.get('type','link'),('','','Project'))[1]}): "
        f"{pr.get('desc','')} | Tools: {pr.get('tools','')} | Link: {pr.get('link','—')}"
        for pr in projs
    ]) or "لم تُضف مشاريع بعد"
    cert_lines = "\n".join([f"- {c['icon']} {c['name']} — {c['issuer']}" for c in certs])
    return f"""أنت مساعد ذكي خاص ببورتفوليو {p.get('name_en','Karim Maher')}.
أجب بشكل ودي ومختصر. تكلم بالعربي إذا السؤال بالعربي، بالإنجليزي إذا بالإنجليزي.

━━ صاحب البورتفوليو ━━
الاسم: {p.get('name_en','')} | المسمى: {p.get('title','')}
الموقع: {p.get('location','')} | الهاتف: {p.get('phone','')}
البريد: {p.get('email','غير متاح')} | LinkedIn: {p.get('linkedin','غير متاح')}
GitHub: {p.get('github','غير متاح')} | التعليم: {p.get('edu','')}
نبذة: {p.get('bio','')} | المهارات: {p.get('skills','')}

━━ الشهادات ━━
{cert_lines}

━━ المشاريع ({len(projs)}) ━━
{proj_lines}

قاعدة: لا تخترع معلومات. إذا غير موجودة قل ذلك بصدق. كن ودياً دائماً."""

def ask_claude(msg: str) -> str:
    try:
        key = st.secrets.get("ANTHROPIC_API_KEY", "")
        if not key:
            return "⚠️ لم يتم إعداد الـ API Key بعد. أضفه في secrets.toml"
        client  = anthropic.Anthropic(api_key=key)
        history = [{"role":m["role"],"content":m["content"]} for m in st.session_state.chat_messages[-10:]]
        history.append({"role":"user","content":msg})
        resp = client.messages.create(
            model="claude-sonnet-4-20250514", max_tokens=400,
            system=build_system_prompt(), messages=history
        )
        return resp.content[0].text
    except Exception as e:
        return f"خطأ: {str(e)}"

# ══════════════════════════════════════════════════════════
#  NAV
# ══════════════════════════════════════════════════════════
def render_nav():
    name = P("name_en").split()[0] if P("name_en") else "KM"
    st.markdown(f"""
    <div class="km-nav">
      <div class="km-logo">{name}<span class="c"> ◈</span></div>
      <div class="km-nav-links">
        <span class="km-nav-a">البروفايل</span>
        <span class="km-nav-a">الشهادات</span>
        <span class="km-nav-a">المشاريع</span>
        <span class="km-nav-a">تواصل</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Real nav button — fixed position via Streamlit column trick
    st.markdown('<div style="position:fixed;top:13px;left:24px;z-index:9999">', unsafe_allow_html=True)
    page = st.session_state._page
    if page == "portfolio":
        if st.button("⚙️ لوحة التحكم", key="nav_btn"):
            st.session_state._page = "admin"
            st.rerun()
    else:
        if st.button("← البورتفوليو", key="nav_btn"):
            st.session_state._page = "portfolio"
            st.session_state.admin_logged_in = False
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════
def render_hero():
    photo  = P("photo_url")
    avatar = f'<div class="km-av-inner"><img src="{photo}" alt="{P("name_en")}"></div>' if photo else '<div class="km-av-inner">👤</div>'
    st.markdown(f"""
    <div class="km-hero">
      <div class="km-hero-glow"></div>
      <div class="km-hero-content">
        <div class="km-badge"><span class="ldot"></span> متاح للعمل · Available for Work</div>
        <div class="km-hname">{P("name_en")}</div>
        <div class="km-hrole">{P("title")}</div>
        <div class="km-hbio">{P("bio")}</div>
        <div class="km-pills">
          <span class="km-pill">📍 {P("location")}</span>
          <span class="km-pill">📞 {P("phone")}</span>
          <span class="km-pill">🐍 Python · SQL · Power BI</span>
          <span class="km-pill">🚀 Streamlit</span>
        </div>
      </div>
      <div class="km-av-area"><div class="km-av-ring">{avatar}</div></div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  METRICS
# ══════════════════════════════════════════════════════════
def render_metrics():
    n  = len(st.session_state.projects)
    ns = len([p for p in st.session_state.projects if p.get("type")=="streamlit"])
    st.markdown(f"""
    <div class="km-sec" style="padding-top:3rem;padding-bottom:3rem">
      <div class="km-metrics">
        <div class="km-metric"><div class="km-metric-val">{n}+</div><div class="km-metric-label">مشروع مكتمل</div></div>
        <div class="km-metric"><div class="km-metric-val">3</div><div class="km-metric-label">شهادة احترافية</div></div>
        <div class="km-metric"><div class="km-metric-val">{ns}</div><div class="km-metric-label">Streamlit App</div></div>
        <div class="km-metric"><div class="km-metric-val">98%</div><div class="km-metric-label">رضا العملاء</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  ABOUT
# ══════════════════════════════════════════════════════════
def render_about():
    skills_html = "".join([f'<span class="km-skill">{s.strip()}</span>' for s in P("skills").split(",") if s.strip()])
    st.markdown(f"""
    <div class="km-sec">
      <div class="km-eyebrow">01 — About</div>
      <div class="km-sec-title">الخبرة و<span class="hl">المهارات</span></div>
      <div class="km-about-grid">
        <div class="km-card"><div class="km-card-icon">🎓</div><div class="km-card-title">التعليم والدبلومة</div><div class="km-card-body">{P("edu")}</div></div>
        <div class="km-card"><div class="km-card-icon">💼</div><div class="km-card-title">نبذة مهنية</div><div class="km-card-body">{P("bio")}</div></div>
        <div class="km-card" style="grid-column:1/-1"><div class="km-card-icon">⚙️</div><div class="km-card-title">المهارات التقنية</div><div style="margin-top:.6rem">{skills_html}</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  CERTS
# ══════════════════════════════════════════════════════════
def render_certs():
    html = ""
    for c in st.session_state.certs:
        col = c["color"]
        html += f"""<div class="km-cert">
          <div class="km-cert-icon" style="background:color-mix(in srgb,{col} 12%,transparent)">{c["icon"]}</div>
          <div style="flex:1"><div class="km-cert-name">{c["name"]}</div><div class="km-cert-issuer">{c["issuer"]}</div></div>
          <span class="km-cert-chip" style="background:color-mix(in srgb,{col} 12%,transparent);color:{col};border:1px solid color-mix(in srgb,{col} 30%,transparent)">{c["issuer"].split("—")[0].strip()}</span>
        </div>"""
    st.markdown(f"""
    <div class="km-sec">
      <div class="km-eyebrow">02 — Certificates</div>
      <div class="km-sec-title">الشهادات <span class="hl">المهنية</span></div>
      {html}
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  PROJECTS
# ══════════════════════════════════════════════════════════
def render_projects():
    projects = st.session_state.projects
    st.markdown("""
    <div class="km-sec" style="padding-bottom:1rem">
      <div class="km-eyebrow">03 — Projects</div>
      <div class="km-sec-title">معرض <span class="hl">المشاريع</span></div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div style="padding:0 3rem 4rem">', unsafe_allow_html=True)
        if not projects:
            st.info("📭 لم تُضف مشاريع بعد — ادخل لوحة التحكم وأضف أول مشروع!")
            st.markdown("</div>", unsafe_allow_html=True)
            return

        types_in = list(dict.fromkeys([p.get("type","link") for p in projects]))
        opts     = ["🗂️ الكل"] + [f"{TYPE_META[t][0]} {TYPE_META[t][1]}" for t in types_in if t in TYPE_META]
        sel      = st.selectbox("", opts, label_visibility="collapsed", key="proj_filter")
        filtered = projects if sel == "🗂️ الكل" else [
            p for p in projects
            if f"{TYPE_META.get(p.get('type','link'),('','',''))[0]} {TYPE_META.get(p.get('type','link'),('','',''))[1]}" == sel
        ]

        cols = st.columns(3)
        for i, proj in enumerate(filtered):
            t = proj.get("type","link")
            emoji, lbl, color = TYPE_META.get(t, ("📁","Project","#aaa"))
            img   = proj.get("image_url","")
            link  = proj.get("link","")
            tools = proj.get("tools","")
            thumb = f'<img src="{img}">' if img else f'<span style="font-size:3.8rem">{proj.get("emoji","📁")}</span>'
            tools_html = "".join([f'<span class="km-proj-tool">{t.strip()}</span>' for t in tools.split(",") if t.strip()])
            with cols[i % 3]:
                st.markdown(f"""
                <div class="km-proj-card">
                  <div class="km-proj-thumb">
                    {thumb}
                    <div class="km-thumb-ov"></div>
                    <span class="km-proj-chip" style="background:color-mix(in srgb,{color} 20%,rgba(0,0,0,.6));color:{color};border:1px solid color-mix(in srgb,{color} 35%,transparent)">{emoji} {lbl}</span>
                  </div>
                  <div class="km-proj-body">
                    <div class="km-proj-name">{proj.get("name","")}</div>
                    <div class="km-proj-desc">{proj.get("desc","مشروع تحليل بيانات")}</div>
                    <div class="km-proj-tools">{tools_html}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
                # ✅ Working link — Streamlit native
                if link:
                    st.link_button("فتح المشروع ↗", url=link, use_container_width=True)
                st.write("")
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  CONTACT  ✅ Real working links via st.link_button
# ══════════════════════════════════════════════════════════
def render_contact():
    phone    = P("phone")
    email    = P("email")
    linkedin = P("linkedin")
    github   = P("github")

    st.markdown("""
    <div class="km-sec" style="padding-bottom:1rem">
      <div class="km-eyebrow">04 — Contact</div>
      <div class="km-sec-title" style="text-align:center">تواصل <span class="hl">معي</span></div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div style="padding:0 3rem 5rem">', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(f'<div class="km-contact-item"><div class="km-contact-icon">📞</div><div class="km-contact-label">{phone}</div></div>', unsafe_allow_html=True)
            if phone:
                st.link_button("اتصل الآن", url=f"tel:{phone}", use_container_width=True)

        with c2:
            st.markdown('<div class="km-contact-item"><div class="km-contact-icon">✉️</div><div class="km-contact-label">البريد الإلكتروني</div></div>', unsafe_allow_html=True)
            if email:
                st.link_button("راسلني", url=f"mailto:{email}", use_container_width=True)
            else:
                st.caption("أضف بريدك من لوحة التحكم")

        with c3:
            st.markdown('<div class="km-contact-item"><div class="km-contact-icon">💼</div><div class="km-contact-label">LinkedIn</div></div>', unsafe_allow_html=True)
            if linkedin:
                st.link_button("الملف الشخصي", url=linkedin, use_container_width=True)
            else:
                st.caption("أضف LinkedIn من لوحة التحكم")

        with c4:
            st.markdown('<div class="km-contact-item"><div class="km-contact-icon">🐙</div><div class="km-contact-label">GitHub</div></div>', unsafe_allow_html=True)
            if github:
                st.link_button("الكود المصدري", url=github, use_container_width=True)
            else:
                st.caption("أضف GitHub من لوحة التحكم")

        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  CHATBOT WIDGET
# ══════════════════════════════════════════════════════════
def render_chatbot():
    # FAB button
    fab_icon = "✕" if st.session_state.chat_open else "💬"
    if st.button(fab_icon, key="chatfab", help="chatfab"):
        st.session_state.chat_open = not st.session_state.chat_open
        st.rerun()

    if not st.session_state.chat_open:
        return

    # Build messages HTML
    msgs_html = ""
    if not st.session_state.chat_messages:
        msgs_html = f'<div class="km-msg-b"><div class="km-bub-b">👋 أهلاً! أنا المساعد الذكي لـ {P("name_en")}. اسألني أي حاجة!</div></div>'
    else:
        for m in st.session_state.chat_messages[-8:]:
            if m["role"] == "user":
                msgs_html += f'<div class="km-msg-u"><div class="km-bub-u">{m["content"]}</div></div>'
            else:
                msgs_html += f'<div class="km-msg-b"><div class="km-bub-b">{m["content"]}</div></div>'

    suggs     = ["ما مهاراته؟","اعرض المشاريع","كيف أتواصل؟","ما شهاداته؟"]
    sugg_html = "".join([f'<span class="km-sugg">{s}</span>' for s in suggs])

    st.markdown(f"""
    <div class="km-chatwin">
      <div class="km-chat-hdr">
        <div class="km-chat-av">◈</div>
        <div><div class="km-chat-nm">KM Assistant</div><div class="km-chat-st">● متصل الآن</div></div>
      </div>
      <div class="km-chat-body">{msgs_html}</div>
      <div class="km-suggs">{sugg_html}</div>
    </div>
    """, unsafe_allow_html=True)

    # ✅ st.chat_input — works perfectly in Streamlit
    user_msg = st.chat_input("اسألني عن كريم ماهر...", key="chat_input")
    if user_msg:
        st.session_state.chat_messages.append({"role":"user","content":user_msg})
        with st.spinner(""):
            reply = ask_claude(user_msg)
        st.session_state.chat_messages.append({"role":"assistant","content":reply})
        st.rerun()

# ══════════════════════════════════════════════════════════
#  ADMIN — LOGIN
# ══════════════════════════════════════════════════════════
def render_login():
    st.markdown('<div class="km-login">', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown(f"""
        <div class="km-login-box">
          <div style="font-size:3.5rem;margin-bottom:.8rem">🔐</div>
          <div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;margin-bottom:.3rem">لوحة التحكم</div>
          <div style="font-size:.8rem;color:var(--frost3);margin-bottom:1.5rem;font-weight:300">خاص بـ {P("name_en")} فقط</div>
        </div>
        """, unsafe_allow_html=True)
        pw = st.text_input("", type="password", placeholder="• • • • • • • •", label_visibility="collapsed")
        if st.button("دخول ↗", use_container_width=True, type="primary"):
            if hp(pw) == P("pw_hash"):
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("❌ باسورد غلط!")
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  ADMIN — DASHBOARD
# ══════════════════════════════════════════════════════════
def render_admin():
    p = st.session_state.profile
    st.markdown('<div style="padding:6rem 3rem 2rem;max-width:1100px;margin:0 auto">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="km-admin-top">
      <div class="km-admin-title">◈ لوحة تحكم {p.get("name_en","")}</div>
      <div class="km-admin-sub">أي تغيير يظهر فوراً · الـ Chatbot يتعلم تلقائياً من بياناتك</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 تسجيل الخروج"):
        st.session_state.admin_logged_in = False
        st.session_state._page = "portfolio"
        st.rerun()

    tab1, tab2, tab3 = st.tabs(["👤  البروفايل والصورة", "🗂️  المشاريع", "🤖  الـ Chatbot"])

    with tab1:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown("#### 📷 صورتك الشخصية")
            photo = p.get("photo_url","")
            if photo:
                st.image(photo, width=170)
            else:
                st.markdown('<div style="width:170px;height:170px;background:#17172a;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:5rem;border:2px dashed rgba(0,229,255,0.15)">👤</div>', unsafe_allow_html=True)
            new_photo = st.text_input("🔗 رابط الصورة", value=photo, placeholder="https://i.imgur.com/...")
            st.caption("💡 ارفع على [imgur.com](https://imgur.com) وخذ الـ Direct Link")

        with c2:
            st.markdown("#### ✏️ بياناتك الشخصية")
            r1,r2 = st.columns(2)
            with r1:
                n_name  = st.text_input("الاسم (إنجليزي)",   value=p.get("name_en",""))
                n_loc   = st.text_input("الموقع",             value=p.get("location",""))
                n_li    = st.text_input("رابط LinkedIn",      value=p.get("linkedin",""))
                n_edu   = st.text_input("التعليم",            value=p.get("edu",""))
            with r2:
                n_title = st.text_input("المسمى الوظيفي",    value=p.get("title",""))
                n_phone = st.text_input("رقم الهاتف",        value=p.get("phone",""))
                n_gh    = st.text_input("رابط GitHub",        value=p.get("github",""))
                n_email = st.text_input("البريد الإلكتروني", value=p.get("email",""))
            n_sub = st.text_input("العنوان الثانوي", value=p.get("subtitle",""))
            n_bio = st.text_area("نبذة شخصية",       value=p.get("bio",""), height=90)
            n_sk  = st.text_input("المهارات (فاصلة)",value=p.get("skills",""))

            st.markdown("#### 🔑 تغيير الباسورد")
            pc1,pc2 = st.columns(2)
            with pc1: n_pw  = st.text_input("باسورد جديد",    type="password", placeholder="اتركه فاضي لو مش عايز تغيره")
            with pc2: n_pw2 = st.text_input("تأكيد الباسورد", type="password")

            if st.button("💾 حفظ كل التغييرات", type="primary", use_container_width=True):
                pw_hash = p.get("pw_hash", DEFAULT_PW_HASH)
                if n_pw:
                    if n_pw != n_pw2: st.error("❌ الباسوردان مختلفان!"); st.stop()
                    if len(n_pw) < 4:  st.error("❌ الباسورد قصير جداً!"); st.stop()
                    pw_hash = hp(n_pw)
                st.session_state.profile.update({
                    "name_en":n_name, "title":n_title, "subtitle":n_sub,
                    "location":n_loc, "phone":n_phone, "email":n_email,
                    "linkedin":n_li,  "github":n_gh,   "edu":n_edu,
                    "bio":n_bio, "skills":n_sk, "photo_url":new_photo, "pw_hash":pw_hash,
                })
                st.success("✅ تم الحفظ! يظهر للكل دلوقتي 🎉")
                st.rerun()

    with tab2:
        cf, cl = st.columns([1, 2])
        with cf:
            st.markdown("#### ➕ مشروع جديد")
            p_type  = st.selectbox("النوع", list(TYPE_META.keys()), format_func=lambda x: f"{TYPE_META[x][0]} {TYPE_META[x][1]}")
            p_name  = st.text_input("الاسم *", key="pn")
            p_desc  = st.text_area("الوصف",    key="pd", height=80)
            p_tools = st.text_input("التقنيات (فاصلة)", placeholder="Python, Pandas", key="pt")
            p_link  = st.text_input("الرابط الخارجي",   placeholder="https://...",    key="pl")
            p_img   = st.text_input("رابط صورة الغلاف", placeholder="https://i.imgur.com/...", key="pi")
            p_emoji = st.text_input("إيموجي", max_chars=2, key="pe", placeholder=TYPE_META.get(p_type,("📁","",""))[0])
            if st.button("✅ إضافة للبورتفوليو", type="primary", use_container_width=True):
                if not p_name: st.error("❌ أدخل الاسم!"); st.stop()
                st.session_state.projects.insert(0, {
                    "id":str(int(datetime.now().timestamp())),
                    "type":p_type, "name":p_name, "desc":p_desc,
                    "tools":p_tools, "link":p_link, "image_url":p_img,
                    "emoji":p_emoji or TYPE_META.get(p_type,("📁","",""))[0],
                    "date":datetime.now().strftime("%Y-%m-%d")
                })
                st.success(f"✅ تم إضافة '{p_name}'!")
                st.rerun()

        with cl:
            projs = st.session_state.projects
            st.markdown(f"#### المشاريع الحالية — {len(projs)} مشروع")
            if not projs:
                st.info("📭 لا توجد مشاريع بعد")
            for proj in projs:
                emoji,lbl,_ = TYPE_META.get(proj.get("type","link"),("📁","Project",""))
                ca, cb = st.columns([6, 1])
                with ca:
                    lnk = proj.get("link","")
                    st.markdown(f"""
                    <div style="background:var(--ink3);border:1px solid var(--border);border-radius:10px;padding:.8rem 1rem;margin-bottom:.5rem">
                      <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:.88rem">{emoji} {proj.get("name","")}</div>
                      <div style="font-size:.68rem;color:var(--frost3)">{lbl} · {proj.get("date","")} · {proj.get("tools","")}</div>
                      {"<div style='font-size:.67rem;color:var(--cyan);margin-top:.2rem'>🔗 "+lnk+"</div>" if lnk else ""}
                    </div>""", unsafe_allow_html=True)
                with cb:
                    if st.button("🗑️", key=f"del_{proj.get('id')}"):
                        st.session_state.projects = [x for x in st.session_state.projects if x.get("id") != proj.get("id")]
                        st.rerun()

    with tab3:
        st.markdown("### 🤖 إعداد الـ Chatbot")
        st.info("الـ Chatbot يتعلم تلقائياً! أي بيانات تضيفها تظهر فوراً في إجاباته.")
        st.code('ANTHROPIC_API_KEY = "sk-ant-api03-..."', language="toml")
        st.caption("حط ده في `.streamlit/secrets.toml` أو في إعدادات Streamlit Cloud")
        ok = bool(st.secrets.get("ANTHROPIC_API_KEY",""))
        if ok:
            st.success("✅ API Key موجود — الـ Chatbot شغال!")
        else:
            st.warning("⚠️ API Key مش موجود")
        if ok:
            tq = st.text_input("سؤال تجريبي")
            if st.button("إرسال") and tq:
                with st.spinner("جاري الرد..."):
                    st.info(ask_claude(tq))

    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════
def main():
    inject_css()
    page = st.session_state._page

    if page == "portfolio":
        render_nav()
        render_hero()
        st.markdown('<div class="km-div"></div>', unsafe_allow_html=True)
        render_metrics()
        st.markdown('<div class="km-div"></div>', unsafe_allow_html=True)
        render_about()
        st.markdown('<div class="km-div"></div>', unsafe_allow_html=True)
        render_certs()
        st.markdown('<div class="km-div"></div>', unsafe_allow_html=True)
        render_projects()
        st.markdown('<div class="km-div"></div>', unsafe_allow_html=True)
        render_contact()
        st.markdown(f"""
        <div class="km-footer">
          <div class="km-footer-logo">{P("name_en")} ◈</div>
          <div class="km-footer-copy">Alexandria, Egypt 🇪🇬 · Data Analyst · © 2026</div>
        </div>""", unsafe_allow_html=True)
        render_chatbot()

    elif page == "admin":
        render_nav()
        if not st.session_state.admin_logged_in:
            render_login()
        else:
            render_admin()

if __name__ == "__main__":
    main()
