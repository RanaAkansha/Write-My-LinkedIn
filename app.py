import streamlit as st
import requests
import time
from datetime import datetime

# CONFIGURATION
st.set_page_config(
    page_title="Write My LinkedIn - PlaceAI",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CUSTOM CSS
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        color: #0a66c2;
        text-align: center;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin-bottom: 1rem;
        color: #333;
    }
    .success-box {
        padding: 1.5rem;
        border-radius: 8px;
        background: #e7f3ff;
        border: 1px solid #0a66c2;
        margin: 1rem 0;
        color: #333;
    }
    .stats-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        border-top: 3px solid #0a66c2;
        color: #333;
    }
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        .feature-card {
            padding: 1rem;
        }
    }
    .stButton button {
        background-color: #0a66c2;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
    }
    .stButton button:hover {
        background-color: #004182;
    }
    .stProgress > div > div > div {
        background-color: #0a66c2;
    }
    .stTextArea textarea:focus {
        border-color: #0a66c2;
        box-shadow: 0 0 0 1px #0a66c2;
    }
    .stSelectbox div div {
        border: 1px solid #e9ecef;
    }
</style>
""",
    unsafe_allow_html=True,
)

# INITIALIZATION
if "generation_count" not in st.session_state:
    st.session_state.generation_count = 0
if "posts_generated" not in st.session_state:
    st.session_state.posts_generated = 0

# API CONFIGURATION
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")

# CACHE FUNCTIONS
@st.cache_data(show_spinner=False, ttl=3600)
def check_api_health():
    """Check if API is accessible"""
    try:
        test_response = requests.get(
            "https://api.groq.com/openai/v1/models",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            timeout=5,
        )
        return test_response.status_code == 200
    except:
        return False


# Header Section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(
        '<div class="main-header">Write My LinkedIn</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="sub-header">Make your LinkedIn posts stand out, with us.</div>',
        unsafe_allow_html=True,
    )

# Stats Bar
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(
        f'<div class="stats-card">Generations<br><strong>{st.session_state.generation_count}</strong></div>',
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f'<div class="stats-card">Posts Created<br><strong>{st.session_state.posts_generated}</strong></div>',
        unsafe_allow_html=True,
    )
with col3:
    status = "Active" if check_api_health() else "Limited"
    st.markdown(
        f'<div class="stats-card">API Status<br><strong>{status}</strong></div>',
        unsafe_allow_html=True,
    )
with col4:
    st.markdown(
        f'<div class="stats-card">Specialized<br><strong>CS professionals</strong></div>',
        unsafe_allow_html=True,
    )

# Main Content Area
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Create Your LinkedIn Post Now")

    # Achievement Input
    achievement = st.text_area(
        "**What have you accomplished?**",
        height=120,
        placeholder="Example: I built a machine learning model that predicts stock prices with 85% accuracy using Python and TensorFlow...",
        help="Be specific about technologies, outcomes, and learnings",
    )

    # Advanced Options
    with st.expander("Advanced Options", expanded=True):
        col1a, col2a = st.columns(2)
        with col1a:
            tone = st.selectbox(
                "**Tone**",
                [
                    "Viral / Hook-heavy",
                    "Humble & Relatable",
                    "Educational Thread",
                    "Professional & Concise",
                    "Funny / Engaging",
                    "Inspirational",
                ],
            )
            audience = st.selectbox(
                "**Target Audience**",
                [
                    "Tech Leads & Managers",
                    "Fellow Students",
                    "Recruiters & HR",
                    "General Tech Community",
                    "Indian Tech Ecosystem",
                ],
            )
        with col2a:
            num_variations = st.slider("**Number of variations**", 1, 10, 3)
            include_images = st.checkbox("Generate image prompts", value=True)

    # Industry-specific templates
    with st.expander("Quick Start Templates"):
        template = st.selectbox(
            "**Use Template**",
            [
                "Custom",
                "Project Completion",
                "Internship Experience",
                "Certification Achievement",
                "Open Source Contribution",
                "Hackathon Win",
                "New Skill Learned",
                "Interview Experience",
            ],
        )

        if template != "Custom":
            template_prompts = {
                "Project Completion": "I just completed a major project where I built [describe project] using [technologies]. The biggest challenge was [challenge] and I learned [key learnings].",
                "Internship Experience": "Just wrapped up my internship at [company] where I worked on [project]. Gained hands-on experience with [technologies] and learned [professional insights].",
                "Certification Achievement": "Thrilled to announce I've earned my [certification name] certification! This journey taught me [skills] and I'm excited to apply this knowledge to [future goals].",
                "Open Source Contribution": "Made my first significant contribution to [project name] open source project! Contributed [what you did] and learned the importance of [key learning] in collaborative coding.",
            }
            if template in template_prompts:
                achievement = template_prompts[template]

    # Generate Button
    generate_clicked = st.button(
        "Generate LinkedIn Posts",
        type="primary",
        use_container_width=True,
        disabled=not GROQ_API_KEY,
    )

with col2:
    st.markdown("### Tips for Better Posts")
    tips = [
        "Be Specific: Mention exact technologies, frameworks, and outcomes",
        "Show Journey: Share what you learned, not just what you built",
        "Add Value: Provide insights others can learn from",
        "Use Numbers: Quantify your achievements when possible",
        "Be Authentic: Share real challenges and how you overcame them",
    ]
    for tip in tips:
        st.markdown(f'<div class="feature-card">{tip}</div>', unsafe_allow_html=True)

    # Quick Examples
    with st.expander("Example Achievements"):
        examples = [
            "Built a React Native app that helps students track campus placement deadlines, used Firebase for backend",
            "Completed AWS Cloud Practitioner certification and implemented a cloud solution that reduced costs by 30%",
            "Led a team of 4 to win college hackathon with an AI-powered mental health chatbot using Python and NLP",
            "Contributed to open-source project by fixing critical bug, learned about collaborative development workflows",
        ]
        for example in examples:
            st.caption(f"• {example}")

# API Key Warning
if not GROQ_API_KEY:
    st.error(
        "API key not configured. Please add GROQ_API_KEY to your Streamlit secrets."
    )

# GENERATION LOGIC
if generate_clicked:
    if not achievement.strip():
        st.error("Please describe your achievement to generate posts!")
        st.stop()

    if len(achievement.strip()) < 20:
        st.warning("Provide more details (at least 20 characters) for better results")
        st.stop()

    # Update stats
    st.session_state.generation_count += 1

    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        status_text.text("Crafting your content strategy...")
        progress_bar.progress(20)

        prompt = f"""
        You are an expert LinkedIn content strategist specializing in the technology education and career space.

        CONTEXT: Computer science student/professional creating content for career growth
        ACHIEVEMENT: "{achievement}"
        TONE: {tone}
        AUDIENCE: {audience}
        VARIATIONS NEEDED: {num_variations}

        CREATE {num_variations} UNIQUE LINKEDIN POSTS WITH THESE REQUIREMENTS:

        POST STRUCTURE:
        1. STRONG HOOK: First line must grab attention (question, surprising fact, personal story)
        2. PERSONAL JOURNEY: Brief authentic story about the learning experience
        3. TECHNICAL INSIGHT: Clear, valuable takeaway for audience
        4. PRACTICAL VALUE: How others can replicate or learn from this
        5. ENGAGEMENT QUESTION: End with question to drive comments
        6. PROFESSIONAL FORMATTING: Use emojis sparingly (2-3 max), line breaks for readability

        TECH FOCUS:
        - Mention relevance to career growth and professional development
        - Use relevant hashtags
        - Keep language professional yet relatable for selected audience
        - Maximum 120 words per post (optimized for LinkedIn engagement)

        FORMATTING:
        - Number each post clearly (1, 2, 3...)
        - Use clear separation between posts
        - Add "---" between posts
        """

        if include_images:
            prompt += """
            After all posts, provide 3 AI IMAGE PROMPTS with this format:
            
            **AI Image Prompts:**
            1. [Detailed prompt for coding/tech related visual]
            2. [Detailed prompt for student/learning context]
            3. [Detailed prompt for professional achievement]

            Make image prompts specific, visual, and relevant to the content.
            """

        # API Call
        status_text.text("Generating AI-powered content...")
        progress_bar.progress(60)

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.8,
                "max_tokens": 4096,
                "top_p": 0.9,
            },
            timeout=60,
        )

        status_text.text("Finalizing your posts...")
        progress_bar.progress(90)

        # Process Response
        if response.status_code == 200:
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                result = data["choices"][0]["message"]["content"]

                # Validate content length
                if len(result.strip()) < 100:
                    st.error(
                        "The response seems too short. Please try again with more specific details."
                    )
                    st.stop()

                # Update posts generated count
                st.session_state.posts_generated += num_variations

                # Success UI
                progress_bar.progress(100)
                status_text.text("Generation complete!")

                st.success("Your LinkedIn posts are ready!")

                # Display Posts
                st.markdown("### Generated Posts")

                # Split posts and image prompts
                content_parts = result.split("**AI Image Prompts:**")
                posts_content = content_parts[0]

                # Extract individual posts
                posts = []
                current_post = []

                for line in posts_content.split("\n"):
                    line = line.strip()
                    if (
                        line.startswith(
                            ("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")
                        )
                        and current_post
                    ):
                        posts.append("\n".join(current_post))
                        current_post = [line]
                    elif line and not line.startswith("---"):
                        current_post.append(line)

                if current_post:
                    posts.append("\n".join(current_post))

                # Display each post in expandable sections
                for i, post in enumerate(posts):
                    if len(post.strip()) > 50:  # Only show substantial posts
                        with st.expander(f"Variation {i+1}", expanded=(i == 0)):
                            st.write(post)

                # Display Image Prompts if available
                if include_images and len(content_parts) > 1:
                    st.markdown("### AI Image Prompts")
                    st.info(
                        "Use these prompts with AI image tools like DALL-E, Midjourney, or Stable Diffusion:"
                    )
                    st.write(content_parts[1])

                # Download option
                st.download_button(
                    label="Download All Content",
                    data=result,
                    file_name=f"linkedin_posts_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

            else:
                st.error("Unexpected response format from AI service.")
        else:
            error_messages = {
                429: "Rate limit exceeded. Please wait a minute and try again.",
                401: "Invalid API key. Please check your configuration.",
                500: "AI service temporarily unavailable. Please try again shortly.",
                502: "Network issue. Please check your connection and try again.",
            }
            error_msg = error_messages.get(
                response.status_code, f"Error {response.status_code}: {response.text}"
            )
            st.error(error_msg)

    except requests.exceptions.Timeout:
        st.error(
            "Request timed out. The AI service is taking longer than expected. Please try again."
        )
    except requests.exceptions.ConnectionError:
        st.error(
            "Connection error. Please check your internet connection and try again."
        )
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")

# SIDEBAR
with st.sidebar:
    st.markdown("## About Write My LinkedIn")
    st.markdown(
        """
    **Professional AI Content Generator** 
    specifically designed for CS tech students and professionals.
    
    **Perfect For:**
    - Campus Placement Preparation
    - Internship Applications
    - Project Showcases
    - Skill Demonstrations
    - Career Growth Content
    
    **Pro Tips:**
    1. Be Authentic - Share real stories
    2. Add Value - Teach something new
    3. Engage - Ask questions to drive comments
    4. Be Consistent - Post regularly
    """
    )
    st.markdown("---")

    # Quick Actions
    st.markdown("### Quick Actions")
    if st.button("Reset Session", use_container_width=True):
        st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "© 2025 Write My LinkedIn | Built with Passion, only for you."
    "</div>",
    unsafe_allow_html=True,
)
