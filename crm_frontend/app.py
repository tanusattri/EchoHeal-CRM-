import streamlit as st
import httpx
import pandas as pd
import time

# Dynamic link that reads your cloud setting, falls back to local
BACKEND_URL = st.secrets.get("BACKEND_URL", "https://echoheal-backend-v2.onrender.com")

def get_analytics():
    try:
        response = httpx.get(f"{BACKEND_URL}/api/analytics/overview", timeout=15)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Analytics Error: {str(e)}")
    return {"customers": 0, "orders": 0, "revenue": 0, "high_value_customers": 0}

def get_customers():
    try:
        response = httpx.get(f"{BACKEND_URL}/api/customers", timeout=15)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Customer Error: {str(e)}")
    return []

def get_inactive_customers():
    try:
        response = httpx.get(f"{BACKEND_URL}/api/segments/inactive", timeout=15)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Inactive Segment Error: {str(e)}")
    return {"customers": [], "count": 0}

def get_high_value_customers():
    try:
        response = httpx.get(f"{BACKEND_URL}/api/segments/high-value", timeout=15)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"High Value Segment Error: {str(e)}")
    return {"customers": [], "count": 0}

def get_winter_buyers():
    try:
        response = httpx.get(f"{BACKEND_URL}/api/segments/winter-buyers", timeout=15)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Winter Segment Error: {str(e)}")
    return {"customers": [], "count": 0}

def get_dashboard_data():
    try:
        response = httpx.get(f"{BACKEND_URL}/api/dashboard/data", timeout=15)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Dashboard Error: {str(e)}")
    return {"logs": [], "ai_audit": []}

def check_backend_health():
    """Pings the backend home route to verify it is warm and awake."""
    try:
        # Fast timeout initially to see if it's already awake
        response = httpx.get(f"{BACKEND_URL}/", timeout=3.0)
        if response.status_code == 200:
            return True
    except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.RequestError):
        # Server is likely sleeping
        return False
    return False

# ====================================
# AI STUDIO & CAMPAIGN EXECUTION HOOKS
# ====================================

def generate_copilot(prompt):
    try:
        response = httpx.post(f"{BACKEND_URL}/api/copilot", json={"prompt": prompt}, timeout=60)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Copilot Error: {str(e)}")
    return {"response": "AI could not process this request."}

def generate_audience(prompt):
    try:
        response = httpx.post(f"{BACKEND_URL}/api/audience-builder", json={"prompt": prompt}, timeout=60)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Audience Builder Error: {str(e)}")
    return {"audience": "No audience generated."}

def launch_campaign(campaign_name, channel, message):
    try:
        response = httpx.post(
            f"{BACKEND_URL}/api/campaigns/launch",
            json={"campaign_name": campaign_name, "channel": channel, "base_message": message},
            timeout=120
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Campaign Error: {str(e)}")
    return None

st.set_page_config(
    page_title="EchoHeal",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ EchoHeal CRM")

st.success("Frontend Connected")
if "backend_awake" not in st.session_state:
    st.session_state["backend_awake"] = False
if not st.session_state["backend_awake"]:
    with st.spinner("⏳ Connecting to EchoHeal Cloud Infrastructure..."):
        if check_backend_health():
            st.session_state["backend_awake"] = True
            st.rerun()
        else:
            st.toast("☁️ Cloud container sleep detected. Booting instance...")
            st.warning("⚠️ **Cloud Server Warm-Up Note:** The backend is currently waking up from its free-tier inactive sleep state.")
            progress_bar = st.progress(0)
            status_text = st.empty()
            for percent_complete in range(100):
                time.sleep(0.35)
                progress_bar.progress(percent_complete + 1)
                status_text.caption(f"🔧 Synchronizing multi-service nodes... {percent_complete + 1}% complete")
                if percent_complete > 40 and percent_complete % 10 == 0:
                    if check_backend_health():
                        break
            if check_backend_health():
                st.session_state["backend_awake"] = True
                st.success("⚡ Infrastructure Online! Loading CRM modules...")
                time.sleep(1.5)
                st.rerun()
            else:
                st.error("🛑 Connection took longer than expected. Please manually refresh this page.")
                st.stop()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard",
    "👥 Customers",
    "🎯 Segments",
    "🤖 AI Studio",
    "🚀 Campaigns"
])

with tab1:

    st.header("📊 Executive Dashboard")

    analytics = get_analytics()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Customers",
        analytics.get("customers", 0)
    )

    col2.metric(
        "Orders",
        analytics.get("orders", 0)
    )

    col3.metric(
        "Revenue",
        f"₹{analytics.get('revenue', 0):,}"
    )

    col4.metric(
        "High Value",
        analytics.get(
            "high_value_customers",
            0
        )
    )

with tab2:

    st.header("👥 Customer Explorer")

    customers = get_customers()

    if customers:

        df = pd.DataFrame(customers)

        st.subheader("Customer Overview")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Total Customers",
            len(df)
        )

        c2.metric(
            "Average Spend",
            f"₹{int(df['total_spend'].mean())}"
        )

        c3.metric(
            "Highest Spend",
            f"₹{df['total_spend'].max()}"
        )

        st.divider()

        search = st.text_input(
            "Search Customer"
        )

        if search:

            df = df[
                df["name"]
                .str.contains(
                    search,
                    case=False
                )
            ]

        city_filter = st.selectbox(
            "Filter By City",
            ["All"] +
            sorted(
                df["city"]
                .unique()
                .tolist()
            )
        )

        if city_filter != "All":

            df = df[
                df["city"]
                == city_filter
            ]

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.warning(
            "No customer data available"
        )

with tab3:

    st.header("🎯 Segment Explorer")

    inactive = get_inactive_customers()
    high_value = get_high_value_customers()
    winter = get_winter_buyers()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Inactive Customers",
        inactive.get("count", 0)
    )

    c2.metric(
        "High Value Customers",
        high_value.get("count", 0)
    )

    c3.metric(
        "Winter Buyers",
        winter.get("count", 0)
    )

    st.divider()

    segment_tab1, segment_tab2, segment_tab3 = st.tabs([
        "Inactive",
        "High Value",
        "Winter Buyers"
    ])

    with segment_tab1:

        st.subheader(
            "Inactive Customers"
        )

        inactive_customers = (
            inactive.get(
                "customers",
                []
            )
        )

        if inactive_customers:

            st.dataframe(
                pd.DataFrame(
                    inactive_customers
                ),
                use_container_width=True
            )

    with segment_tab2:

        st.subheader(
            "High Value Customers"
        )

        high_value_customers = (
            high_value.get(
                "customers",
                []
            )
        )

        if high_value_customers:

            st.dataframe(
                pd.DataFrame(
                    high_value_customers
                ),
                use_container_width=True
            )

    with segment_tab3:

        st.subheader(
            "Winter Wear Buyers"
        )

        winter_customers = (
            winter.get(
                "customers",
                []
            )
        )

        if winter_customers:

            st.dataframe(
                pd.DataFrame(
                    winter_customers
                ),
                use_container_width=True
            )

with tab4:

    st.header("🤖 AI Studio")

    st.caption(
        "Generate CRM strategies and AI-powered customer audiences."
    )

    copilot_tab, audience_tab = st.tabs([
        "CRM Copilot",
        "Audience Builder"
    ])

    # =========================================
    # CRM COPILOT
    # =========================================

    with copilot_tab:

        st.subheader(
            "AI CRM Copilot"
        )

        copilot_prompt = st.text_area(

            "Describe your campaign goal",

            placeholder=
            "Example: Create a campaign for inactive winter wear customers"
        )

        if st.button(
            "Generate Strategy",
            use_container_width=True
        ):

            if not copilot_prompt:

                st.warning(
                    "Please enter a campaign goal."
                )

            else:

                with st.spinner(
                    "AI thinking..."
                ):

                    result = generate_copilot(
                        copilot_prompt
                    )

                    if result:

                        st.success(
                            "Strategy Generated"
                        )

                        st.markdown(
                            f"""
### 📋 CRM Strategy

{result.get('response', 'No response generated')}
"""
                        )

    # =========================================
    # AUDIENCE BUILDER
    # =========================================

    with audience_tab:

        st.subheader(
            "AI Audience Builder"
        )

        audience_prompt = st.text_area(

            "Describe the audience",

            placeholder=
            "Example: Customers who spent more than ₹5000 and haven't ordered in 60 days"
        )

        if st.button(
            "Build Audience",
            use_container_width=True
        ):

            if not audience_prompt:
 
                st.warning(
                    "Please enter audience criteria."
                )

            else:

                with st.spinner(
                    "Finding audience..."
                ):

                    result = generate_audience(
                        audience_prompt
                    )

                    if result:

                        st.success(
                            "Audience Generated"
                        )

                        st.markdown(
                            f"""
### 🎯 Recommended Audience

{result.get('audience', 'No audience found')}
"""
                        )

with tab5:

    st.header("🚀 Campaign Control Center")

    st.caption("End-to-End Campaign Execution + AI Recovery System")

    # =========================
    # CAMPAIGN LAUNCH
    # =========================

    st.subheader("🚀 Launch Campaign")

    campaign_name = st.text_input(
        "Campaign Name",
        value="Winter Clearance Sale"
    )

    channel = st.selectbox(
        "Channel",
        ["WhatsApp", "SMS", "Email", "RCS"]
    )

    message = st.text_area(
        "Campaign Message",
        value="Get 20% OFF on winter wear today only!"
    )

    if st.button("🚀 Launch Campaign", use_container_width=True):

        result = launch_campaign(campaign_name, channel, message)

        if result:

            st.success("Campaign Launched Successfully 🎉")

            st.json(result)
        st.rerun()

    st.divider()

    # =========================
    # DELIVERY TRACKING
    # =========================

    st.header("📡 Delivery Tracking (Live Logs)")

    dashboard = get_dashboard_data()
    logs = dashboard.get("logs", [])

    if logs:

        df = pd.DataFrame(logs)

        st.dataframe(df, use_container_width=True)

        st.subheader("Delivery Status Overview")

        st.bar_chart(df["delivery_status"].value_counts())

    else:

        st.info("No delivery logs yet.")

    st.divider()

    # =========================
    # AI SELF HEALING
    # =========================

    st.header("🧠 AI Self-Healing System")

    ai_audit = dashboard.get("ai_audit", [])

    if ai_audit:

        for item in ai_audit:

            st.subheader(f"👤 {item['customer_name']}")

            st.write("❌ Failed Channel:", item["failed_channel"])
            st.write("🔁 Fallback Channel:", item["fallback_channel"])
            st.write("⚠️ Reason:", item["failure_reason"])

            st.success("💬 AI Rewritten Message")
            st.write(item["new_message"])

            st.divider()

    else:

        st.info("No AI recovery events yet.")

    st.divider()

    # =========================
    # RECOVERY TIMELINE
    # =========================

    st.header("🕒 Recovery Timeline")

    if ai_audit:

        for i, item in enumerate(reversed(ai_audit)):

            st.markdown(f"""
### Step {i+1}: {item['customer_name']}

- ❌ Failed Channel: **{item['failed_channel']}**  
- 🔁 Fallback Channel: **{item['fallback_channel']}**  
- ⚠️ Reason: {item['failure_reason']}  

💬 AI Fix:
> {item['new_message']}
""")

            st.divider()

    else:

        st.info("No recovery timeline available.")