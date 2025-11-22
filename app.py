"""
AuraCycle - Main Streamlit Application
A multi-agent AI system for menstrual health management
"""

import streamlit as st
from datetime import datetime, date
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from agents import CoordinatorAgent
from database import Database

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="AuraCycle - AI Health Assistant",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== SESSION STATE INITIALIZATION ====================
if 'db' not in st.session_state:
    st.session_state.db = Database()

if 'agent' not in st.session_state:
    st.session_state.agent = CoordinatorAgent()

if 'user_id' not in st.session_state:
    st.session_state.user_id = "user_demo"  # In production, use authentication

# ==================== CUSTOM CSS ====================
st.markdown("""
    <style>
    /* Main Header */
    .main-header {
        font-size: 3rem;
        color: #FF69B4;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Agent Cards */
    .agent-card {
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #FFB6C1;
        margin: 1rem 0;
        background: linear-gradient(135deg, #FFF0F5 0%, #FFE4E1 100%);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .agent-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    .agent-card h3 {
        color: #FF1493;
        margin-bottom: 0.5rem;
    }
    
    /* Symptom Badges */
    .symptom-badge {
        background-color: #FFE4E1;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.2rem;
        display: inline-block;
        font-size: 0.9rem;
        border: 1px solid #FFB6C1;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    /* Chat Messages */
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .user-message {
        background-color: #E3F2FD;
        border-left: 4px solid #2196F3;
    }
    
    .assistant-message {
        background-color: #FFF0F5;
        border-left: 4px solid #FF69B4;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 20px;
        border: 2px solid #FF69B4;
        color: #FF69B4;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #FF69B4;
        color: white;
        transform: scale(1.05);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #FFF0F5;
    }
    
    /* Info boxes */
    .info-box {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .success-box {
        background-color: #D4EDDA;
        border-left: 4px solid #28A745;
    }
    
    .warning-box {
        background-color: #FFF3CD;
        border-left: 4px solid #FFC107;
    }
    
    .danger-box {
        background-color: #F8D7DA;
        border-left: 4px solid #DC3545;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown('<h1 class="main-header">🌸 AuraCycle</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your AI-Powered Menstrual Health Companion</p>', unsafe_allow_html=True)

# ==================== SIDEBAR NAVIGATION ====================
with st.sidebar:
    # Logo placeholder
    st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 4rem;">🌸</div>
            <h2 style="color: #FF69B4;">AuraCycle</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.title("📱 Navigation")
    
    page = st.radio("Go to", [
        "🏠 Home",
        "📅 Track Cycle", 
        "😊 Log Symptoms",
        "💬 Chat with AI",
        "📊 My Dashboard",
        "🔮 Predictions"
    ], label_visibility="collapsed")
    
    st.divider()
    
    # Quick Stats
    st.subheader("📈 Quick Stats")
    user_data = st.session_state.db.get_user_data(st.session_state.user_id)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Cycles", len(user_data.get('cycles', [])))
    with col2:
        st.metric("Symptoms", len(user_data.get('symptoms', [])))
    
    st.divider()
    
    # Medical Disclaimer
    st.caption("⚠️ **Medical Disclaimer**")
    st.caption("This is not medical advice. Always consult a healthcare provider for medical concerns.")
    
    st.divider()
    
    # About
    with st.expander("ℹ️ About"):
        st.caption("""
        **AuraCycle** is an AI-powered health assistant using multi-agent architecture to provide personalized menstrual health guidance.
        
        **Version**: 1.0.0  
        **Powered by**: Google Gemini
        """)

# ==================== PAGE: HOME ====================
if page == "🏠 Home":
    # Quick Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cycles_count = len(st.session_state.db.get_cycle_dates(st.session_state.user_id))
        st.metric(
            label="📅 Total Cycles Logged",
            value=cycles_count,
            delta="Track more for better predictions" if cycles_count < 3 else "Great job!"
        )
    
    with col2:
        user_data = st.session_state.db.get_user_data(st.session_state.user_id)
        symptoms_count = len(user_data.get('symptoms', []))
        st.metric(
            label="😊 Symptoms Logged",
            value=symptoms_count,
            delta="Daily tracking recommended"
        )
    
    with col3:
        next_cycle = st.session_state.agent.prediction_agent.predict_next_cycle(st.session_state.user_id)
        st.metric(
            label="🔮 Next Cycle",
            value=next_cycle if next_cycle != "Need more data" else "Log cycles",
            delta=None
        )
    
    st.divider()
    
    # Quick Actions
   #st.subheader("🚀 Quick Actions")
    
   # col1, col2 = st.columns(2)
    
    #with col1:
     #   with st.container():
      #      st.info("**📅 Track Your Cycle**\n\nLog your period start date to get accurate predictions and insights.")
       #     if st.button("🗓️ Track Now", key="track_home", use_container_width=True):
       #         st.switch_page
    
    #with col2:
      #  with st.container():
       #     st.success("**💬 Ask AI Anything**\n\nGet personalized health advice from our multi-agent AI system.")
        #    if st.button("💭 Chat Now", key="chat_home", use_container_width=True):
         #       st.switch_page
    
   # st.divider()
    
    # Meet the AI Agents
    st.subheader("🤖 Meet Your AI Agents")
    st.caption("Our multi-agent system works together to provide comprehensive health guidance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="agent-card">
            <h3>🧘 Wellness Agent</h3>
            <p><strong>Specialization:</strong> Physical Health</p>
            <p>Provides personalized yoga poses, exercises, and physical activities based on your symptoms and cycle phase. Helps you stay active safely throughout your cycle.</p>
            <p><em>Example: "Try Child's Pose for cramps"</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="agent-card">
            <h3>🥗 Nutrition Agent</h3>
            <p><strong>Specialization:</strong> Vegetarian Nutrition</p>
            <p>Recommends foods, recipes, and dietary adjustments to support your health. Tailored to your age, symptoms, and nutritional needs.</p>
            <p><em>Example: "Eat iron-rich spinach for fatigue"</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="agent-card">
            <h3>🔮 Prediction Agent</h3>
            <p><strong>Specialization:</strong> Data Analysis</p>
            <p>Analyzes your cycle history to predict your next period, calculate average cycle length, and detect irregularities that may need attention.</p>
            <p><em>Example: "Next period: Jan 28"</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="agent-card">
            <h3>🎯 Coordinator Agent</h3>
            <p><strong>Specialization:</strong> Orchestration</p>
            <p>The main agent that understands your questions, coordinates all specialist agents, and synthesizes their insights into comprehensive, personalized advice.</p>
            <p><em>Example: Combines wellness + nutrition advice</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # How It Works
    st.subheader("🔄 How the Multi-Agent System Works")
    
    st.markdown("""
    ```
    Your Question: "I have bad cramps"
            ↓
    Coordinator Agent (analyzes intent)
            ↓
    ┌───────┴───────┬──────────────┐
    ↓               ↓              ↓
    Wellness    Nutrition    Prediction
    Agent        Agent         Agent
    ↓               ↓              ↓
    Yoga poses   Foods to eat  Cycle info
    ↓               ↓              ↓
    └───────┬───────┴──────────────┘
            ↓
    Coordinator synthesizes all advice
            ↓
    Complete personalized response
    ```
    """)
    
    st.info("💡 **Smart Collaboration**: Agents work together automatically based on your needs!")

# ==================== PAGE: TRACK CYCLE ====================
elif page == "📅 Track Cycle":
    st.header("📅 Track Your Menstrual Cycle")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Log Period Start Date")
        
        with st.form("cycle_form"):
            cycle_date = st.date_input(
                "When did your period start?",
                value=date.today(),
                max_value=date.today(),
                help="Select the first day of your period"
            )
            
            flow_intensity = st.select_slider(
                "Flow Intensity",
                options=["Spotting", "Light", "Medium", "Heavy", "Very Heavy"],
                value="Medium",
                help="How would you describe your flow?"
            )
            
            notes = st.text_area("Notes (optional)", placeholder="Any additional observations...")
            
            submitted = st.form_submit_button("💾 Log Cycle", type="primary", use_container_width=True)
            
            if submitted:
                st.session_state.db.save_cycle_date(
                    st.session_state.user_id, 
                    cycle_date.strftime("%Y-%m-%d"),
                    flow_intensity
                )
                st.success(f"✅ Cycle logged successfully for {cycle_date.strftime('%B %d, %Y')}")
                st.balloons()
    
    with col2:
        st.info("""
        **💡 Tracking Tips**
        
        - Log the **first day** of your period
        - Track **consistently** each month
        - Need **2+ cycles** for predictions
        - More data = Better accuracy
        """)
        
        st.warning("""
        **🚨 See a Doctor If:**
        
        - Period lasts > 7 days
        - Severe pain (8+/10)
        - Very heavy bleeding
        - Irregular for > 3 months
        """)
    
    st.divider()
    
    # Cycle History
    st.subheader("📜 Your Cycle History")
    cycles = st.session_state.db.get_cycle_dates(st.session_state.user_id)
    
    if cycles:
        df = pd.DataFrame(cycles)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date', ascending=False)
        
        # Display table
        st.dataframe(
            df[['date', 'flow']].rename(columns={'date': 'Date', 'flow': 'Flow Intensity'}),
            use_container_width=True,
            hide_index=True
        )
        
        # Calculate statistics
        if len(df) > 1:
            df_sorted = df.sort_values('date')
            cycle_lengths = df_sorted['date'].diff().dt.days.dropna()
            
            if len(cycle_lengths) > 0:
                avg_length = cycle_lengths.mean()
                min_length = cycle_lengths.min()
                max_length = cycle_lengths.max()
                last_length = cycle_lengths.iloc[-1] if len(cycle_lengths) > 0 else 0
                
                st.subheader("📊 Cycle Statistics")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Average Cycle", f"{avg_length:.0f} days")
                with col2:
                    st.metric("Last Cycle", f"{last_length:.0f} days")
                with col3:
                    st.metric("Shortest", f"{min_length:.0f} days")
                with col4:
                    st.metric("Longest", f"{max_length:.0f} days")
                
                # Cycle length trend
                if len(cycle_lengths) >= 3:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=list(range(1, len(cycle_lengths) + 1)),
                        y=cycle_lengths.values,
                        mode='lines+markers',
                        name='Cycle Length',
                        line=dict(color='#FF69B4', width=3),
                        marker=dict(size=10)
                    ))
                    fig.add_hline(y=avg_length, line_dash="dash", line_color="green", 
                                 annotation_text=f"Average: {avg_length:.0f} days")
                    fig.update_layout(
                        title="Cycle Length Trend",
                        xaxis_title="Cycle Number",
                        yaxis_title="Days",
                        height=300
                    )
                    st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📝 No cycles logged yet. Start tracking today to get personalized insights!")

# ==================== PAGE: LOG SYMPTOMS ====================
elif page == "😊 Log Symptoms":
    st.header("😊 Log Your Symptoms")
    st.caption("Track daily symptoms to help our AI understand your patterns better")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("symptom_form"):
            symptom_date = st.date_input(
                "Date",
                value=date.today(),
                max_value=date.today()
            )
            
            st.subheader("🤕 Physical Symptoms")
            physical_symptoms = st.multiselect(
                "Select all that apply",
                ["Cramps", "Bloating", "Headache", "Breast Tenderness", 
                 "Back Pain", "Fatigue", "Nausea", "Acne", "Diarrhea"],
                help="Choose all physical symptoms you're experiencing"
            )
            
            st.subheader("💭 Emotional Symptoms")
            emotional_symptoms = st.multiselect(
                "Select all that apply",
                ["Mood Swings", "Irritability", "Anxiety", "Sadness", 
                 "Stress", "Brain Fog", "Difficulty Concentrating"],
                help="Choose all emotional symptoms you're experiencing"
            )
            
            st.subheader("⚡ Energy & Well-being")
            
            col_a, col_b = st.columns(2)
            with col_a:
                energy_level = st.slider("Energy Level", 1, 10, 5, 
                                        help="1 = Exhausted, 10 = Energetic")
            with col_b:
                pain_level = st.slider("Pain Level", 0, 10, 0,
                                      help="0 = No pain, 10 = Severe pain")
            
            sleep_quality = st.select_slider(
                "Sleep Quality Last Night",
                options=["Very Poor", "Poor", "Fair", "Good", "Excellent"],
                value="Fair"
            )
            
            st.subheader("📝 Additional Notes")
            notes = st.text_area(
                "Any other observations?",
                placeholder="E.g., unusual cravings, lifestyle changes, stress events...",
                height=100
            )
            
            submitted = st.form_submit_button("💾 Save Symptoms", type="primary", use_container_width=True)
            
            if submitted:
                symptom_data = {
                    "date": symptom_date.strftime("%Y-%m-%d"),
                    "physical": physical_symptoms,
                    "emotional": emotional_symptoms,
                    "energy_level": energy_level,
                    "sleep_quality": sleep_quality,
                    "pain_level": pain_level,
                    "notes": notes
                }
                
                st.session_state.db.save_symptom(st.session_state.user_id, symptom_data)
                st.success("✅ Symptoms logged successfully!")
                
                # Auto-generate AI suggestions if symptoms present
                if physical_symptoms or emotional_symptoms:
                    with st.spinner("🤖 AI Agents analyzing your symptoms..."):
                        all_symptoms = physical_symptoms + emotional_symptoms
                        response = st.session_state.agent.handle_symptoms(
                            st.session_state.user_id, 
                            all_symptoms
                        )
                    
                    st.markdown("### 🎯 Personalized Recommendations")
                    st.markdown(response)
                    st.balloons()
    
    with col2:
        st.info("""
        **📊 Why Track Symptoms?**
        
        - Identify patterns
        - Better AI recommendations
        - Predict PMS timing
        - Share data with doctor
        """)
        
        st.success("""
        **💡 Pro Tips**
        
        - Log at the **same time** daily
        - Be **honest** and detailed
        - Track even **good days**
        - Review patterns monthly
        """)
        
        st.warning("""
        **🚨 Urgent Symptoms**
        
        If you experience:
        - Severe pain (8+)
        - Heavy bleeding (soaking pad/hour)
        - Fever with symptoms
        - Sudden severe symptoms
        
        **→ Contact doctor immediately**
        """)

# ==================== PAGE: CHAT WITH AI ====================
elif page == "💬 Chat with AI":
    st.header("💬 Chat with Your AI Health Assistant")
    st.caption("Ask anything about menstrual health - our multi-agent system is here to help!")
    
    # Display chat history
    user_data = st.session_state.db.get_user_data(st.session_state.user_id)
    chat_history = user_data.get('chats', [])
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        if chat_history:
            for chat in chat_history[-10:]:  # Show last 10 conversations
                # User message
                with st.chat_message("user", avatar="🙋‍♀️"):
                    st.write(chat['question'])
                
                # Assistant message
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(chat['answer'])
        else:
            st.info("👋 Start a conversation! Ask me anything about menstrual health.")
    
    # Chat input
    user_question = st.chat_input("Type your question here...", key="chat_input")
    
    if user_question:
        # Display user message immediately
        with st.chat_message("user", avatar="🙋‍♀️"):
            st.write(user_question)
        
        # Show assistant thinking and response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🤖 Coordinating agents and analyzing..."):
                response = st.session_state.agent.chat(st.session_state.user_id, user_question)
            st.markdown(response)
        
        # Rerun to update chat history
        st.rerun()
    
    st.divider()
    
    # Quick question templates
    st.subheader("💡 Quick Questions")
    st.caption("Click any button to ask")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧘 Help with cramps", use_container_width=True):
            user_question = "I have bad cramps today, what can help?"
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("🤖 Getting recommendations..."):
                    response = st.session_state.agent.chat(st.session_state.user_id, user_question)
                st.markdown(response)
    
    with col2:
        if st.button("🥗 Foods for energy", use_container_width=True):
            user_question = "What vegetarian foods can boost my energy during my period?"
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("🤖 Getting recommendations..."):
                    response = st.session_state.agent.chat(st.session_state.user_id, user_question)
                st.markdown(response)
    
    with col3:
        if st.button("🔮 When is my next period?", use_container_width=True):
            user_question = "When will my next period start?"
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("🤖 Analyzing your data..."):
                    response = st.session_state.agent.chat(st.session_state.user_id, user_question)
                st.markdown(response)
    
    st.divider()
    
    # Clear chat history
    if st.button("🗑️ Clear Chat History", type="secondary"):
        if st.session_state.db.clear_chat_history(st.session_state.user_id):
            st.success("Chat history cleared!")
            st.rerun()

# ==================== PAGE: DASHBOARD ====================
elif page == "📊 My Dashboard":
    st.header("📊 Your Health Dashboard")
    st.caption("Visualize your health patterns and trends")
    
    user_data = st.session_state.db.get_user_data(st.session_state.user_id)
    symptoms = user_data.get('symptoms', [])
    cycles = user_data.get('cycles', [])
    
    if not symptoms and not cycles:
        st.info("📝 Start logging cycles and symptoms to see your personalized dashboard!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📅 Track Cycle Now", use_container_width=True):
                st.switch_page
        with col2:
            if st.button("😊 Log Symptoms Now", use_container_width=True):
                st.switch_page
    
    else:
        # Cycle Timeline
        if cycles:
            st.subheader("📅 Cycle Timeline")
            df_cycles = pd.DataFrame(cycles)
            df_cycles['date'] = pd.to_datetime(df_cycles['date'])
            df_cycles = df_cycles.sort_values('date')
            
            fig = go.Figure()
            
            # Add markers for each cycle
            fig.add_trace(go.Scatter(
                x=df_cycles['date'],
                y=[1]*len(df_cycles),
                mode='markers+text',
                marker=dict(size=20, color='#FF69B4', symbol='circle'),
                text=['🩸']*len(df_cycles),
                textposition="top center",
                textfont=dict(size=20),
                name='Period Start',
                hovertemplate='<b>Period Start</b><br>Date: %{x}<br><extra></extra>'
            ))
            
            fig.update_layout(
                title="Your Menstrual Cycle History",
                xaxis_title="Date",
                showlegend=False,
                height=250,
                yaxis=dict(showticklabels=False, showgrid=False),
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Symptom Analysis
        if symptoms:
            st.subheader("😊 Symptom Patterns")
            
            df_symptoms = pd.DataFrame(symptoms)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Most common physical symptoms
                st.markdown("**🤕 Most Common Physical Symptoms**")
                all_physical = []
                for s in symptoms:
                    all_physical.extend(s.get('physical', []))
                
                if all_physical:
                    symptom_counts = pd.Series(all_physical).value_counts().head(5)
                    
                    fig = go.Figure(data=[
                        go.Bar(
                            x=symptom_counts.values,
                            y=symptom_counts.index,
                            orientation='h',
                            marker=dict(color='#FF69B4')
                        )
                    ])
                    fig.update_layout(
                        xaxis_title="Frequency",
                        yaxis_title="Symptom",
                        height=300
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No physical symptoms logged yet")
            
            with col2:
                # Energy and pain trends
                st.markdown("**⚡ Energy & Pain Levels**")
                
                if 'energy_level' in df_symptoms.columns and 'pain_level' in df_symptoms.columns:
                    avg_energy = df_symptoms['energy_level'].mean()
                    avg_pain = df_symptoms['pain_level'].mean()
                    
                    fig = go.Figure()
                    
                    fig.add_trace(go.Indicator(
                        mode="gauge+number",
                        value=avg_energy,
                        title={'text': "Avg Energy"},
                        domain={'x': [0, 0.45], 'y': [0, 1]},
                        gauge={
                            'axis': {'range': [0, 10]},
                            'bar': {'color': "#4CAF50"},
                            'steps': [
                                {'range': [0, 3], 'color': "#FFE4E1"},
                                {'range': [3, 7], 'color': "#FFB6C1"},
                                {'range': [7, 10], 'color': "#FF69B4"}
                            ]
                        }
                    ))
                    
                    fig.add_trace(go.Indicator(
                        mode="gauge+number",
                        value=avg_pain,
                        title={'text': "Avg Pain"},
                        domain={'x': [0.55, 1], 'y': [0, 1]},
                        gauge={
                            'axis': {'range': [0, 10]},
                            'bar': {'color': "#F44336"},
                            'steps': [
                                {'range': [0, 3], 'color': "#D4EDDA"},
                                {'range': [3, 7], 'color': "#FFF3CD"},
                                {'range': [7, 10], 'color': "#F8D7DA"}
                            ]
                        }
                    ))
                    
                    fig.update_layout(height=250)
                    st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            
            # Recent symptoms timeline
            if len(df_symptoms) >= 3:
                st.subheader("📈 Recent Trends (Last 30 Days)")
                
                df_symptoms['date'] = pd.to_datetime(df_symptoms['date'])
                df_recent = df_symptoms[df_symptoms['date'] >= (datetime.now() - pd.Timedelta(days=30))]
                
                if len(df_recent) > 0:
                    fig = make_subplots(
                        rows=2, cols=1,
                        subplot_titles=('Energy Level Over Time', 'Pain Level Over Time'),
                        vertical_spacing=0.15
                    )
                    
                    # Energy line
                    fig.add_trace(
                        go.Scatter(
                            x=df_recent['date'],
                            y=df_recent['energy_level'],
                            mode='lines+markers',
                            name='Energy',
                            line=dict(color='#4CAF50', width=2),
                            marker=dict(size=8)
                        ),
                        row=1, col=1
                    )
                    
                    # Pain line
                    fig.add_trace(
                        go.Scatter(
                            x=df_recent['date'],
                            y=df_recent['pain_level'],
                            mode='lines+markers',
                            name='Pain',
                            line=dict(color='#F44336', width=2),
                            marker=dict(size=8)
                        ),
                        row=2, col=1
                    )
                    
                    fig.update_xaxes(title_text="Date", row=2, col=1)
                    fig.update_yaxes(title_text="Level (1-10)", range=[0, 10])
                    
                    fig.update_layout(height=500, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)

# ==================== PAGE: PREDICTIONS ====================
elif page == "🔮 Predictions":
    st.header("🔮 Cycle Predictions & Insights")
    st.caption("AI-powered predictions based on your cycle history")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Next cycle prediction
        prediction = st.session_state.agent.prediction_agent.predict_next_cycle(
            st.session_state.user_id
        )
        
        if prediction != "Need more data":
            st.success(f"### 📅 Next Period Expected: **{prediction}**")
            
            # Calculate days until
            try:
                next_date = datetime.strptime(prediction, "%Y-%m-%d")
                today = datetime.now()
                days_until = (next_date - today).days
                
                if days_until > 0:
                    st.info(f"🗓️ **{days_until} days** from today")
                    
                    # Progress bar
                    cycles = st.session_state.db.get_cycle_dates(st.session_state.user_id)
                    if cycles:
                        last_cycle = datetime.strptime(cycles[-1]['date'], "%Y-%m-%d")
                        total_days = (next_date - last_cycle).days
                        days_passed = (today - last_cycle).days
                        progress = min(days_passed / total_days, 1.0) if total_days > 0 else 0
                        
                        st.progress(progress, text=f"Day {days_passed} of {total_days}")
                
                elif days_until == 0:
                    st.warning("⚠️ Your period is expected **today**!")
                else:
                    st.error(f"⚠️ Your period is **{abs(days_until)} days late**")
                    st.caption("If this continues, consider consulting a healthcare provider.")
            
            except:
                pass
        
        else:
            st.info("""
            📊 **Need More Data**
            
            To generate predictions, please:
            - Log at least **2 cycle dates**
            - Track consistently each month
            - The more data, the better the accuracy!
            """)
            
            if st.button("📅 Track Cycle Now", type="primary"):
                st.switch_page
        
        st.divider()
        
        # Irregularity check
        st.subheader("🔍 Cycle Regularity Check")
        
        irregularity = st.session_state.agent.prediction_agent.detect_irregularity(
            st.session_state.user_id
        )
        
        if irregularity:
            st.warning(irregularity)
        else:
            st.success("✅ Your cycles appear to be within the normal range (21-35 days)")
        
        # Cycle statistics
        cycles = st.session_state.db.get_cycle_dates(st.session_state.user_id)
        if len(cycles) >= 2:
            df_cycles = pd.DataFrame(cycles)
            df_cycles['date'] = pd.to_datetime(df_cycles['date'])
            df_cycles = df_cycles.sort_values('date')
            
            cycle_lengths = df_cycles['date'].diff().dt.days.dropna()
            
            if len(cycle_lengths) > 0:
                st.subheader("📊 Cycle Statistics")
                
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    avg_cycle = cycle_lengths.mean()
                    st.metric("Average Cycle Length", f"{avg_cycle:.1f} days")
                
                with col_b:
                    std_cycle = cycle_lengths.std()
                    st.metric("Cycle Variation", f"±{std_cycle:.1f} days")
                
                with col_c:
                    total_tracked = len(cycles)
                    st.metric("Total Cycles Tracked", total_tracked)
    
    with col2:
        st.info("""
        **🎯 How Predictions Work**
        
        Our AI analyzes your cycle history using:
        - Average cycle length
        - Pattern recognition
        - Irregularity detection
        
        **Accuracy improves with:**
        - More logged cycles
        - Consistent tracking
        - Regular patterns
        """)
        
        st.success("""
        **💡 Prediction Tips**
        
        - Track for **3+ months** for best results
        - Log the **exact date** your period starts
        - Note any **lifestyle changes**
        - Check predictions weekly
        """)
        
        st.warning("""
        **⚠️ Important Notes**
        
        - Predictions are **estimates**
        - Many factors affect cycles
        - Stress, diet, exercise matter
        - Consult doctor for concerns
        """)
        
        # Data quality indicator
        cycles_count = len(cycles)
        if cycles_count < 3:
            quality = "Low"
            color = "🔴"
        elif cycles_count < 6:
            quality = "Medium"
            color = "🟡"
        else:
            quality = "High"
            color = "🟢"
        
        st.metric(
            "Prediction Quality",
            f"{color} {quality}",
            delta=f"{cycles_count} cycles logged"
        )

# ==================== FOOTER ====================
st.divider()

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.caption("🌸 **AuraCycle v1.0**")
    st.caption("Multi-Agent AI Health Assistant")

with footer_col2:
    #st.caption("⚡ **Powered by**")
    #st.caption("Google Gemini & Streamlit")

#with footer_col3:
    st.caption("⚠️ **Disclaimer**")
    st.caption("Not a substitute for medical advice")

st.caption("---")
st.caption("Made with ❤️ for women's health empowerment | © 2025")
