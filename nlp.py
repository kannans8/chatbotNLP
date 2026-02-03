import pandas as pd
import re
import nltk
nltk.download("punkt", quiet=True)
from nltk.tokenize import word_tokenize
import streamlit as st
import base64
from datetime import date,datetime
# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Roche Virtual Assistant",
    layout="wide"
)

# --------------------------------------------------
# STYLING (UI)
# --------------------------------------------------
st.markdown("""
<style>

/* -------------------------------
   GLOBAL
-------------------------------- */
.stApp {
    background-color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* -------------------------------
   HEADER (TRUE FIXED)
-------------------------------- */
.header-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background-color: white;
    padding: 15px 30px;
    border-bottom: 1px solid #e5e7eb;
    z-index: 1000;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo-wrapper {
    width: 200px;
    height: 80px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.logo-img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}

.title-wrapper {
    text-align: center;
    flex-grow: 1;
}

.title-wrapper h1 {
    margin: 0;
    color: #003366;
    font-size: 28px;
    font-weight: 600;
}

/* Reserve space below header */
div.block-container {
    padding-top: 160px !important;
}

/* -------------------------------
   CHAT SCROLL ONLY
-------------------------------- */

.chat-container {
    max-width: 800px;
    margin: 0 auto;
    max-height: calc(100vh - 220px);
    overflow-y: auto;
    padding-bottom: 140px;
}

/* -------------------------------
   CHAT BUBBLES - ZIGZAG ALIGNMENT
-------------------------------- */
.message-row {
    display: flex;
    margin: 15px 0;
}

.user-message {
    justify-content: flex-end;
}

.bot-message {
    justify-content: flex-start;
}

.user-bubble {
    background-color: #003366;
    color: white;
    padding: 16px 22px;
    border-radius: 22px;
    max-width: 75%;
    order: 2;
    box-shadow: 0 4px 12px rgba(0, 51, 102, 0.2);
}

.bot-bubble {
    background-color: #e5e7eb;
    color: #111827;
    padding: 16px 22px;
    border-radius: 22px;
    max-width: 75%;
    order: 2;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* -------------------------------
   INPUT FIXED
-------------------------------- */
div[data-testid="stChatInput"] {
    position: fixed;
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 800px;
    z-index: 99999;
}

/* -------------------------------
   AVATARS - ZIGZAG ALIGNMENT
-------------------------------- */
.avatar {
    width: 45px !important;
    height: 45px !important;
    border-radius: 50%;
    object-fit: cover;
    background-color: #fff;
    border: 2px solid #e5e7eb;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 16px;
}

.user-avatar {
    background: linear-gradient(135deg, #003366, #004080);
    color: white;
    margin-left: 12px;
}

.bot-avatar {
    background: linear-gradient(135deg, #e5e7eb, #d1d5db);
    color: #374151;
    margin-right: 12px;
}

.message-row.user-message {
    justify-content: flex-end;
}

.message-row.user-message .user-bubble {
    order: 1;
    margin-left: 8px;
}

.message-row.user-message .user-avatar {
    order: 2;
}

.message-row.bot-message {
    justify-content: flex-start;
}

.message-row.bot-message .bot-avatar {
    order: 1;
    margin-right: 8px;
}

.message-row.bot-message .bot-bubble {
    order: 2;
}
.custom-table th {
    font-weight: 700 !important;
    font-family: "Segoe UI Semibold", "Segoe UI", sans-serif !important;
    color: #000000 !important;
    background-color: #f8f9fa !important;
    padding: 12px 15px !important;
    border-bottom: 2px solid #dee2e6 !important;
    text-align: left !important;
}

.custom-table td {
    padding: 10px 15px !important;
    border-bottom: 1px solid #e9ecef !important;
}
.table-container {
    max-height: 300px;      /* Adjust as needed */
    overflow-y: auto;
    margin-top: 12px;
    margin-bottom: 12px;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 6px;
}



</style>

<script>
/* MOVE HEADER OUT OF STREAMLIT FLOW */
const moveHeader = () => {
    const header = document.querySelector('.header-container');
    if (header && header.parentElement.tagName !== 'BODY') {
        document.body.prepend(header);
    }
};
setInterval(moveHeader, 300);
</script>
""", unsafe_allow_html=True)


# --------------------------------------------------
# LOGO AND TITLE SECTION
# --------------------------------------------------
st.markdown("<div class='header-container'>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    try:
        with open("Roche_logo.png", "rb") as f:
            roche_logo_base64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <div class="logo-wrapper">
                <img src="data:image/jpeg;base64,{roche_logo_base64}" class="logo-img">
            </div>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.markdown('<div class="logo-wrapper"><div style="color: #666; font-size: 14px;">Roche Logo</div></div>', unsafe_allow_html=True)

with col2:
    st.markdown(
        """
        <div class="title-wrapper">
            <h1>Roche Chat bot NLP</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    try:
        with open("Genentech-logo.png", "rb") as f:
            genentech_logo_base64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <div class="logo-wrapper">
                <img src="data:image/jpeg;base64,{genentech_logo_base64}" class="logo-img">
            </div>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.markdown('<div class="logo-wrapper"><div style="color: #666; font-size: 14px;">Genentech Logo</div></div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# --------------------------------------------------
# DATA LOAD
# --------------------------------------------------
df = pd.read_csv("dcr_data.csv", na_values=["", " ", "NA", "N/A", "null", "NULL"])
df["ams_id"] = df["ams_id"].replace(r'^\s*$', pd.NA, regex=True)
df["priority_clean"] = df["priority"].astype(str).str.replace(r'\s+', '', regex=True).str.lower()
df["review_step_clean"] = df["review_step"].astype(str).str.replace(r'\s+', '', regex=True).str.lower()
df["entity_type_clean"] = df["entity_type"].astype(str).str.replace(r'\s+', '', regex=True).str.lower()
df["child_entity_type_clean"] = df["child_entity_type"].astype(str).str.replace(r'\s+', '', regex=True).str.lower()
df["source_system_clean"] = df["source_system"].astype(str).str.replace(r'\s+', '', regex=True).str.lower()
df["status_clean"] = df["source_dcr_status"].astype(str).str.replace(r'\s+', '', regex=True).str.lower()
df["dcr_assigned_to_clean"] = df["dcr_assigned_to"].astype(str).str.replace(r'\s+', '', regex=True).str.lower()
df["created_date"] = pd.to_datetime(df["created_date"], errors="coerce").dt.date


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []

if "processing" not in st.session_state:
    st.session_state.processing = False

# --------------------------------------------------
#  CHAT LOGIC 
# --------------------------------------------------
def csv_agent(user_input):
    text = user_input.lower()
    text=re.sub(r'[^a-z0-9\s/]', '', text)
    tokens = re.findall(r'\b\w+\b', text.lower())

    if "show" in tokens and "all" in tokens:
        return df

    if "how" in tokens and "many" in tokens:
        if "medium" in tokens:
            return len(df[df["priority_clean"] == "medium"])
        
        if "hcp" in tokens:
            return len(df[df["entity_type_clean"] == "hcp"])

        if "hco" in tokens:
            return len(df[df["child_entity_type_clean"] == "hco"])

        if "dcr" in tokens:
            return df["mdm_dcr_id"].nunique()

    if "assigned" in tokens and "to" in tokens:
        
        try:
            person = tokens[tokens.index("to") + 1]
        except IndexError:
            return "Please specify a person."

        
        df_filtered = df[df["dcr_assigned_to_clean"].str.contains(person, case=False, na=False)]

        # current
        if "today" in tokens:
            today = date.today()
            df_filtered = df_filtered[df_filtered["created_date"] == today]
        else:
            date_match = re.search(r"\b\d{2}/\d{2}/\d{4}\b", text)
            if date_match:
                specific_date = datetime.strptime(date_match.group(), "%d/%m/%Y").date()
                df_filtered = df_filtered[df_filtered["created_date"] == specific_date]
        #2nd condition null/not null
        if "not" in tokens and "null" in tokens:
            df_filtered = df_filtered[df_filtered["ams_id"].notna()]
        elif "null" in tokens:
            df_filtered = df_filtered[df_filtered["ams_id"].isna()]
        #3rd condition status
        
        status_map = {
            "pending review": {"awaiting_review"},
            "pending": {"awaiting_review"},
            "open": {"awaiting_review"},
            "approved": {"applied"},
            "rejected": {"rejected"},
            "deleted": {"deleted"}
        }

        matched = next((v for k, v in status_map.items() if k in text), None)

        if matched:
            grouped = (
                df_filtered
                .groupby("source_dcr_header_id")["review_step_clean"]
                .apply(lambda x: set(s.lower().strip() for s in x))
            )

            def match_fn(steps):
                if matched & {"applied", "rejected", "deleted"}:
                    return bool(steps & matched)
                return steps == matched

            matching_ids = [
                hid for hid, steps in grouped.items() if match_fn(steps)
            ]

            df_filtered = df_filtered[df_filtered["source_dcr_header_id"].isin(matching_ids)]  
       
        if "how" in tokens and "many" in tokens:
            return df_filtered["source_dcr_header_id"].nunique()
        elif "show" in tokens:
            return df_filtered.drop_duplicates(subset=["source_dcr_header_id"])
    if "assigned" in tokens and ("today" in tokens or "current" in tokens or "latest" in tokens):
        today = date.today()

        df_today = df[df["created_date"] == today]
        for token in tokens:
            try:
                specific_date = datetime.strptime(token, "%d/%m/%Y").date()
                df_filtered = df_filtered[df_filtered["created_date"] == specific_date]
                break
            except ValueError:
                continue

        if "how" in tokens and "many" in tokens:
            return len(df_today)
        else:
            return df_today

    grouped = df.groupby("source_dcr_header_id")["review_step_clean"].apply(set)

    status_map = {
        "pending review": {"awaiting_review"},
        "pending": {"awaiting_review"},
        "open": {"awaiting_review"},
        "approved": {"applied"},
        "rejected": {"rejected"},
        "deleted": {"deleted"}
    }

    matched = next((v for k, v in status_map.items() if k in text), None)

    if matched:
        def match_fn(steps):
            steps = set(s.lower() for s in steps)
            if matched & {"applied", "rejected", "deleted"}:
                return bool(steps & matched)
            else:
                return steps == matched
        if "how" in tokens and "many" in tokens:
            return sum(match_fn(steps) for steps in grouped)
        else:  
            ids = [hid for hid, steps in grouped.items() if match_fn(steps)]
            return df[df["source_dcr_header_id"].isin(ids)]

    if "medium" in tokens:
        return df[df["priority_clean"] == "medium"]

    if "hcp" in tokens:
        return df[df["entity_type_clean"] == "hcp"]

    if "hco" in tokens:
        return df[df["child_entity_type_clean"] == "hco"]

    if "veevacrm" in tokens or "veeva" in tokens:
        return df[df["source_system_clean"] == "veevacrm"]

    
    month_match = re.search(r"(0?[1-9]|1[0-2]|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[ /-]?(20\d{2})", text)
    if month_match:
        month_str = month_match.group(1)
        year_str = month_match.group(2)

        month_map = {
            "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
            "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12
        }

        try:
            month = int(month_str)
        except:
            month = month_map.get(month_str[:3].lower(), None)

        if month:
            df_month = df[pd.to_datetime(df["created_date"]).dt.month == month]
            df_month = df_month[pd.to_datetime(df_month["created_date"]).dt.year == int(year_str)]

            
            if "how" in tokens and "many" in tokens:
                return len(df_month)
            else:
                return df_month  

    year_match = re.search(r"20\d{2}", text)
    if year_match:
        year = year_match.group()
        df_year = df[pd.to_datetime(df["created_date"]).dt.year == int(year)]
        if "how" in tokens and "many" in tokens:
            return len(df_year)
        else:
            return df_year

    
    return "Unsupported query"


# --------------------------------------------------
#  IMAGE AS BASE64
# --------------------------------------------------
def get_image_base64(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bot_img_base64 = get_image_base64("bot_avatar.png")
user_img_base64 = get_image_base64("user_avatar.png")
# --------------------------------------------------
# CHAT DISPLAY (SCROLLABLE CONTAINER)
# --------------------------------------------------
with st.container(height=520): 
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

    for role, message in st.session_state.chat:
        if isinstance(message, pd.DataFrame):
            max_display = 100
            df_to_show = message.head(max_display) 
            html_table = df_to_show.to_html(classes="custom-table", index=False, escape=False)
            st.markdown(f'<div class="table-container">{html_table}</div>', unsafe_allow_html=True)
            if len(message) > max_display:
                st.info(f"Showing first {max_display} rows of {len(message)} total rows")
            continue

        # ---------------- User Message ----------------
        if role == "user":
            st.markdown(
                f"""
                <div class="message-row user-message">
                    <div class="user-bubble">{message}</div>
                    <img class="avatar user-avatar" width="45" height="45" src="data:image/png;base64,{user_img_base64}">
                </div>
                """,
                unsafe_allow_html=True
            )
        # ---------------- Bot Message ----------------
        else:
            st.markdown(
                f"""
                <div class="message-row bot-message">
                    <img class="avatar bot-avatar" width="45" height="45" src="data:image/png;base64,{bot_img_base64}">
                    <div class="bot-bubble">{message}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)



# --------------------------------------------------
# CHAT INPUT 
# --------------------------------------------------
user_input = st.chat_input("Type a message...")

if user_input:
    st.session_state.chat.append(("user", user_input))
    response = csv_agent(user_input)
    st.session_state.chat.append(("bot", response))
    st.rerun()
