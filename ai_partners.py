import  json
import  streamlit as st
from openai import OpenAI
import os
from  datetime import datetime
from pathlib import Path
import base64
print('------>重新执行，渲染展示页面')
BASE_DIR = Path(__file__).resolve().parent
SESSIONS_DIR = BASE_DIR / "sessions"
BACKGROUND_DIR = BASE_DIR / "background"
LOGO_IMAGE = BASE_DIR / "logo" / "Bokutachi_no_Remake_Logo.png"
SKILLS_DIR = BASE_DIR / "skills"
BACKGROUND_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def get_first_background_image():
    if not BACKGROUND_DIR.exists():
        return None
    for image_path in sorted(BACKGROUND_DIR.iterdir()):
        if image_path.is_file() and image_path.suffix.lower() in BACKGROUND_IMAGE_EXTENSIONS:
            return image_path
    return None


CHAT_BACKGROUND_IMAGE = get_first_background_image()
st.set_page_config(
    page_title="我们的重制人生",           
    page_icon="🧊",                     
    layout="wide",
    initial_sidebar_state="expanded",                       
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
 }
)
SKILL_OPTIONS = {
    "sora_ginko": {
        "name": "空银子",
        "path": SKILLS_DIR / "空银子_skill",
    },
    "kawasegawa_eiko": {
        "name": "河濑川英子",
        "path": SKILLS_DIR / "河濑川英子_skill",
    },
    "chitose_saku": {
        "name": "上野原彩乃",
        "path": SKILLS_DIR / "上野原彩乃_skill",
    },
    "shino_aki": {
        "name": "志野亚贵",
        "path": SKILLS_DIR / "志野亚贵_skill",
    },
    "hashiba_kyoya": {
        "name": "桥场恭也",
        "path": SKILLS_DIR / "桥场恭也_skilll",
    },
    "kogure_nanako": {
        "name": "小暮奈奈子",
        "path": SKILLS_DIR / "小暮奈奈子_skill",
    },
    "rokuonji_tsurayuki": {
        "name": "鹿苑寺贯之",
        "path": SKILLS_DIR / "鹿苑寺贯之_skill",
    },
}


@st.cache_data(show_spinner=False)
def load_background_image_data():
    if CHAT_BACKGROUND_IMAGE is None:
        return ""
    if not CHAT_BACKGROUND_IMAGE.exists():
        return ""
    return base64.b64encode(CHAT_BACKGROUND_IMAGE.read_bytes()).decode("utf-8")

#聊天背景
def apply_chat_background():
    image_data = load_background_image_data()
    if not image_data:
        return

    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
                linear-gradient(rgba(255, 255, 255, 0.18), rgba(255, 255, 255, 0.26)),
                url("data:image/jpeg;base64,{image_data}");
            background-size: cover;
            background-position: center center;
            background-attachment: fixed;
        }}

        [data-testid="stHeader"] {{
            background: rgba(255, 255, 255, 0.12);
        }}

        [data-testid="stSidebar"] {{
            background: rgba(244, 247, 251, 0.78);
            backdrop-filter: blur(8px);
        }}

        [data-testid="stSidebarHeader"] {{
            height: 90px;
            align-items: flex-start;
        }}

        [data-testid="stLogo"] {{
            transform: translateY(28px);
            height: 56px;
            display: flex;
            align-items: flex-end;
        }}

        [data-testid="stLogo"] img {{
            max-height: 56px;
            width: auto;
            object-fit: contain;
        }}

        .block-container {{
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: none;
            border-radius: 12px;
            padding-top: 2rem;
            padding-bottom: 7rem;
        }}

        h1, [data-testid="stMarkdownContainer"] p {{
            text-shadow: 0 1px 10px rgba(255, 255, 255, 0.75);
        }}

        [data-testid="stChatMessage"] {{
            background: rgba(255, 255, 255, 0.38);
            backdrop-filter: blur(3px);
            border: 1px solid rgba(255, 255, 255, 0.42);
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.07);
            margin-bottom: 0.75rem;
        }}

        [data-testid="stChatMessage"] p {{
            color: #1f2937;
            font-weight: 500;
            text-shadow: 0 1px 8px rgba(255, 255, 255, 0.78);
        }}

        [data-testid="stChatInput"] {{
            background: rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(5px);
            border-radius: 14px;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.1);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def load_skill_prompt(skill_key):
    skill = SKILL_OPTIONS.get(skill_key)
    if not skill:
        return ""

    skill_path = skill["path"]
    if not skill_path.exists():
        return ""

    skill_files = sorted(skill_path.glob("*.md"))
    skill_parts = []
    for skill_file in skill_files:
        skill_parts.append(f"# 来源文件：{skill_file.name}\n\n{skill_file.read_text(encoding='utf-8')}")

    skill_content = "\n\n---\n\n".join(skill_parts)
    return f"""你正在加载角色 skill：{skill["name"]}。
        下面是此 skill 的全部角色资料。必须优先遵守这些资料来扮演角色，覆盖“伴侣信息”中的昵称、年龄、性格提示。
        通用回复规则：
                1. 每次只回1条消息
                2. 禁止任何场景或状态描述性文字
                3. 匹配用户的语言
                4. 回复简短，像微信聊天一样
                5. 不要主动解释你加载了 skill

{skill_content}"""


def get_current_system_prompt():
    active_skill_key = st.session_state.get("active_skill_key")
    if active_skill_key:
        skill_prompt = load_skill_prompt(active_skill_key)
        if skill_prompt:
            return skill_prompt
        st.warning("当前选择的 skill 没有读取成功，已临时使用伴侣信息提示词。")
        st.session_state.active_skill_key = None

    return system_prompt%(st.session_state.nickname,st.session_state.age,st.session_state.nature)

apply_chat_background()


def save_session():
    if st.session_state.current_session:

        session_data = {
            "nickname": st.session_state.nickname,
            "age": st.session_state.age,
            "nature": st.session_state.nature,
            "active_skill_key": st.session_state.get("active_skill_key"),
            "current_session": st.session_state.current_session,
            'messages': st.session_state.messages
        }
        SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
        with open(SESSIONS_DIR / f"{st.session_state.current_session}.json", "w",encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)

def generate_session_name():
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S") 

def load_session():
    session_list = []
    if SESSIONS_DIR.exists():
        file_list=SESSIONS_DIR.glob("*.json")
        for session_file in file_list:
            session_list.append(session_file.stem)
    session_list.sort(reverse=True) 
    return  session_list

def load_session_data(session_name):
    try:
        session_file = SESSIONS_DIR / f"{session_name}.json"
        if session_file.exists():
           with open(session_file, "r",encoding='utf-8') as f:
              session_data=json.load(f)
              st.session_state.messages=session_data["messages"]
              st.session_state.nature = session_data["nature"]
              st.session_state.nickname = session_data["nickname"]
              st.session_state.age = session_data.get("age", st.session_state.age)
              st.session_state.active_skill_key = session_data.get("active_skill_key")
              st.session_state.current_session = session_name
    except Exception as e:
           st.error(f"加载会话数据失败：{e}")

def delete_session(session_name):
    try:
        session_file = SESSIONS_DIR / f"{session_name}.json"
        if session_file.exists():
            session_file.unlink()
            if session_name == st.session_state.current_session:
                st.session_state.messages = []
                st.session_state.current_session = generate_session_name()
    except Exception as e:
        st.error(f"删除会话数据失败：{e}")

st.title('迟来的对话—relife')
if LOGO_IMAGE.exists():
    st.logo(str(LOGO_IMAGE), size="large")
system_prompt = ''' 你叫%s，现在是用户的真实伴侣，请完全代入伴侣角色。：
        规则：
            1. 每次只回1条消息
            2. 禁止任何场景或状态描述性文字
            3. 匹配用户的语言
            4. 回复简短，像微信聊天一样
            5. 有需要的话可以用❤️🌸等emoji表情
            6. 用符合伴侣性格的方式对话
            7. 回复的内容, 要充分体现伴侣的性格特征
        伴侣年龄：
            - %s
        伴侣性格：
            - %s       
        你必须严格遵守上述规则来回复用户''' 

if "messages" not in st.session_state:
    st.session_state.messages = []

if "nickname" not in st.session_state:
    st.session_state.nickname = "小甜甜"

if "nature" not in st.session_state:
    st.session_state.nature = "活泼开朗的东北姑娘"

if "age" not in st.session_state:
    st.session_state.age = "18"

if "active_skill_key" not in st.session_state:
    st.session_state.active_skill_key = None

if 'current_session' not in st.session_state:
    a=generate_session_name()
    st.session_state.current_session = a

st.text(f'会话名称: {st.session_state.current_session}')
for msg in st.session_state.messages:
     st.chat_message(msg["role"]).write(msg["content"])
#创建OpenAI客户端对象（deepseek_API_KEY ）是环境变量的名字，值就是Deepseek的API_KEY的值
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")
with st.sidebar:
    st.subheader("会话信息")
    if st.button('新建对话',width='stretch'):
       save_session() 
       if st.session_state.messages:
          st.session_state.messages = []  
          st.session_state.current_session = generate_session_name()  
          save_session()  
          st.rerun()  
   
    st.text("历史会话：")
    session_list=load_session() 
    for session in session_list:
        col1,col2=st.columns([4,1])
        with col1:
          if st.button(session,width='stretch',icon="✍️",key=f'switch_{session}',
             type="primary" if session == st.session_state.current_session else "secondary"):
              load_session_data(session) 
              st.rerun() 
        with col2:
           if  st.button("",width='stretch',icon="❌️",key=f'delete_{session}'):
              delete_session( session)
              st.rerun() 
    st.divider()
    st.subheader("伴侣信息") 
    partner_info_changed = False
    nickname=st.text_input("昵称：", placeholder='请输入昵称', value=st.session_state.nickname)
    if nickname and nickname!=st.session_state.nickname:
       st.session_state.nickname = nickname
       partner_info_changed = True
    age=st.text_input("年龄：", placeholder='请输入年龄', value=st.session_state.age)
    if age and age != st.session_state.age:
        st.session_state.age = age
        partner_info_changed = True
    nature=st.text_input("性格：", placeholder='请输入性格', value=st.session_state.nature)
    if nature and nature != st.session_state.nature:
        st.session_state.nature = nature
        partner_info_changed = True
    if partner_info_changed and st.session_state.active_skill_key:
        st.session_state.active_skill_key = None
        save_session()
        st.warning("已更改伴侣信息：当前会话退出 skill 模式，后续回复会改用昵称、年龄、性格生成的原提示词。")

    st.divider()
    st.subheader("角色 skill 加载")
    st.caption("点击不同按键，会让大模型加载不同的 skill。")
    st.warning("伴侣信息与这些 skill 相互独立：加载 skill 后会覆盖原来的提示词，原来由昵称、年龄、性格改变的人格不会使用；如果更改伴侣信息，就会退出 skill 模式，不能同时调用这些 skill。")
    for skill_key, skill in SKILL_OPTIONS.items():
        if st.button(
            f"加载 {skill['name']} skill",
            width='stretch',
            key=f"load_skill_{skill_key}",
            type="primary" if st.session_state.active_skill_key == skill_key else "secondary",
        ):
            st.session_state.active_skill_key = skill_key
            save_session()
            st.rerun()
    if st.session_state.active_skill_key:
        active_skill_name = SKILL_OPTIONS[st.session_state.active_skill_key]["name"]
        st.success(f"当前已加载：{active_skill_name} skill")
        if st.button("退出 skill 模式，使用伴侣信息", width='stretch'):
            st.session_state.active_skill_key = None
            save_session()
            st.rerun()

prompt = st.chat_input("请输入你的问题")
if prompt:      
   st.chat_message("user").write(prompt) 
   print('--------->调用ai大模型接口，提示词：', prompt)    
   st.session_state.messages.append({"role": "user", "content": prompt})
   response = client.chat.completions.create(
       model="deepseek-v4-pro",
       messages=[
           {"role": "system", "content": get_current_system_prompt()}, #如果已加载skill，则使用skill提示词；否则使用伴侣信息生成的提示词
           *st.session_state.messages    
       ],
       stream=True,      
       reasoning_effort="high",
       extra_body={"thinking": {"type": "enabled"}}
   )
   response_message=st.empty()
   full_response=''
   for chunk in response:  
         if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
            response_message.chat_message("assistant").write(full_response)
   st.session_state.messages.append({"role": "assistant", "content": full_response})
   save_session()
