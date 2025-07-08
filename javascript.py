import streamlit as st
import datetime
import time
from io import BytesIO
import base64

# Page configuration
st.title("Javascript")

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    .status-success {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
    }
    
    .status-error {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #f5c6cb;
    }
    
    .button-container {
        text-align: center;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>📱 Multi-Feature Dashboard</h1>
    <p>Your all-in-one solution for camera, email, location, and social media</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'photo_taken' not in st.session_state:
    st.session_state.photo_taken = False
if 'email_sent' not in st.session_state:
    st.session_state.email_sent = False
if 'location_shared' not in st.session_state:
    st.session_state.location_shared = False

# Create tabs for different features
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📸 Camera & Email", "📧 Gmail", "📍 Location", "🗺️ Maps", "📱 Social Media"])

with tab1:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("📸 Camera & Photo Email")
    
    col1, col2 = st.columns(2)
    
    with col1:
        import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time

# Initialize session state
if 'photo_taken' not in st.session_state:
    st.session_state.photo_taken = False
if 'captured_image' not in st.session_state:
    st.session_state.captured_image = None

st.markdown("### Take Photo")

def capture_photo():
    """Capture photo using OpenCV"""
    try:
        # Initialize camera
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            st.error("❌ Could not access camera. Please check if camera is connected and not being used by another application.")
            return None
        
        # Set camera properties for better quality
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Capture frame
        ret, frame = cap.read()
        
        if ret:
            # Convert BGR to RGB (OpenCV uses BGR, but we need RGB for display)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Release camera
            cap.release()
            
            return frame_rgb
        else:
            st.error("❌ Failed to capture image from camera")
            cap.release()
            return None
            
    except Exception as e:
        st.error(f"❌ Error accessing camera: {str(e)}")
        return None

# Camera interface
camera_placeholder = st.empty()
with camera_placeholder:
    st.info("📷 Make sure your camera is connected and not being used by another application")

# Capture button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("📸 Capture Photo", key="capture", use_container_width=True):
        with st.spinner("Taking photo..."):
            captured_frame = capture_photo()
            
            if captured_frame is not None:
                st.session_state.captured_image = captured_frame
                st.session_state.photo_taken = True
                st.success("✅ Photo captured successfully!")
                time.sleep(1)
                st.rerun()

# Photo preview
if st.session_state.photo_taken and st.session_state.captured_image is not None:
    st.markdown("### Captured Photo")
    
    # Display the captured image
    st.image(st.session_state.captured_image, 
             caption="Your Captured Photo", 
             width=400)
    
    # Additional options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Take Another Photo"):
            st.session_state.photo_taken = False
            st.session_state.captured_image = None
            st.rerun()
    
    with col2:
        # Convert to PIL Image for saving
        pil_image = Image.fromarray(st.session_state.captured_image)
        
        # Convert PIL image to bytes for download
        import io
        img_bytes = io.BytesIO()
        pil_image.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()
        
        st.download_button(
            label="💾 Download Photo",
            data=img_bytes,
            file_name=f"captured_photo_{int(time.time())}.png",
            mime="image/png"
        )
    
    with col3:
        if st.button("🗑️ Delete Photo"):
            st.session_state.photo_taken = False
            st.session_state.captured_image = None
            st.rerun()

# Live camera preview (optional)
st.markdown("---")
if st.checkbox("📹 Show Live Camera Preview"):
    st.markdown("### Live Camera Preview")
    
    # Placeholder for live preview
    live_placeholder = st.empty()
    
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                live_placeholder.image(frame_rgb, caption="Live Camera Feed", width=400)
            cap.release()
        else:
            live_placeholder.error("❌ Could not access camera for live preview")
    except:
        live_placeholder.error("❌ Error accessing camera for live preview")

# Instructions
st.markdown("---")
st.markdown("### Instructions:")
st.markdown("""
1. **Make sure your camera is connected** and not being used by another application
2. **Click 'Capture Photo'** to take a picture
3. **View your captured photo** below the button
4. **Download, retake, or delete** the photo using the action buttons
5. **Optional:** Enable live preview to see your camera feed

**Note:** You may need to grant camera permissions to your browser/application.
""")

# Troubleshooting section
with st.expander("🔧 Troubleshooting"):
    st.markdown("""
    **If camera doesn't work:**
    - Make sure no other application is using the camera
    - Check if camera drivers are installed
    - Try restarting the application
    - On some systems, you might need to run: `pip install opencv-python`
    
    **Camera index issues:**
    - If camera 0 doesn't work, try camera index 1 or 2
    - Some systems have multiple camera devices
    """)
    with col2:
        st.markdown("### Email Photo")
        
        email_to = st.text_input("📧 Send to Email:", placeholder="recipient@gmail.com")
        email_subject = st.text_input("📝 Subject:", value="Photo from Dashboard")
        email_message = st.text_area("💬 Message:", value="Here's the photo I just captured!")
        
        if st.button("📤 Send Email", key="send_email"):
            if email_to and st.session_state.photo_taken:
                with st.spinner("Sending email..."):
                    time.sleep(2)
                    st.session_state.email_sent = True
                    st.success(f"✅ Email sent to {email_to}")
            else:
                st.error("❌ Please capture a photo and enter email address")
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("📧 Gmail Integration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Account Settings")
        gmail_account = st.text_input("Gmail Account:", placeholder="your-email@gmail.com")
        
        if st.button("🔗 Connect Gmail", key="connect_gmail"):
            if gmail_account:
                st.info("🔐 Gmail OAuth integration required for production")
                st.success("✅ Connected to Gmail (Demo Mode)")
            else:
                st.error("❌ Please enter Gmail address")
    
    with col2:
        st.markdown("### Latest Emails")
        
        if st.button("📬 Fetch Latest Emails", key="fetch_emails"):
            with st.spinner("Fetching emails..."):
                time.sleep(2)
                
                # Simulated email data
                emails = [
                    {"from": "colleague@company.com", "subject": "Meeting Update", "time": "2 hours ago"},
                    {"from": "newsletter@tech.com", "subject": "Weekly Tech News", "time": "5 hours ago"},
                    {"from": "friend@gmail.com", "subject": "Weekend Plans", "time": "1 day ago"}
                ]
                
                for email in emails:
                    st.markdown(f"""
                    **From:** {email['from']}  
                    **Subject:** {email['subject']}  
                    **Time:** {email['time']}
                    ---
                    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("📍 Location & SMS")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Current Location")
        
        if st.button("📍 Get GPS Location", key="get_location"):
            with st.spinner("Getting location..."):
                time.sleep(2)
                # Simulated location data
                st.success("✅ Location acquired!")
                st.info("📍 Latitude: 26.9124, Longitude: 75.7873")
                st.info("📍 Address: Jaipur, Rajasthan, India")
                st.session_state.location_shared = True
    
    with col2:
        st.markdown("### Send SMS")
        
        phone_number = st.text_input("📱 Phone Number:", placeholder="+91-XXXXXXXXXX")
        sms_message = st.text_area("💬 SMS Message:", value="Check out my current location!")
        
        if st.button("📱 Send SMS", key="send_sms"):
            if phone_number and st.session_state.location_shared:
                with st.spinner("Sending SMS..."):
                    time.sleep(2)
                    st.success(f"✅ SMS sent to {phone_number}")
            else:
                st.error("❌ Please get location first and enter phone number")
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("🗺️ Maps & Navigation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Current Location Map")
        
        if st.button("🗺️ Show on Google Maps", key="show_maps"):
            st.success("✅ Location displayed on map")
            # Simulated map (in production, use actual Google Maps embed)
            st.markdown("""
            <iframe 
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d227749.69278379493!2d75.65046970649679!3d26.8856568!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x396c4adf4c57e281%3A0xce1c63a0cf22e09!2sJaipur%2C%20Rajasthan!5e0!3m2!1sen!2sin!4v1625000000000!5m2!1sen!2sin" 
                width="100%" 
                height="300" 
                style="border:0; border-radius:10px;" 
                allowfullscreen="" 
                loading="lazy">
            </iframe>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Nearby Places")
        
        search_type = st.selectbox("🔍 Search for:", 
                                 ["Grocery Stores", "Restaurants", "Gas Stations", "Hospitals", "ATMs"])
        
        if st.button("🔍 Find Nearby", key="find_nearby"):
            with st.spinner(f"Finding nearby {search_type.lower()}..."):
                time.sleep(2)
                
                # Simulated nearby places
                places = [
                    {"name": "Big Bazaar", "distance": "0.5 km", "rating": "4.2"},
                    {"name": "Reliance Fresh", "distance": "0.8 km", "rating": "4.0"},
                    {"name": "Spencer's", "distance": "1.2 km", "rating": "4.1"}
                ]
                
                st.success(f"✅ Found {len(places)} {search_type.lower()} nearby")
                
                for place in places:
                    st.markdown(f"""
                    **{place['name']}** ⭐ {place['rating']}  
                    📍 {place['distance']} away
                    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab5:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("📱 Social Media Posting")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Create Post")
        
        post_message = st.text_area("✍️ Write your post:", 
                                   value="Just captured an amazing moment! 📸 #photography #life")
        
        platforms = st.multiselect("📱 Select Platforms:", 
                                 ["Instagram", "Facebook", "WhatsApp Status", "Twitter"])
        
        include_photo = st.checkbox("📸 Include captured photo")
        include_location = st.checkbox("📍 Include location")
    
    with col2:
        st.markdown("### Post Status")
        
        if st.button("📤 Post to Social Media", key="post_social"):
            if post_message and platforms:
                with st.spinner("Posting to social media..."):
                    time.sleep(3)
                    
                    for platform in platforms:
                        st.success(f"✅ Posted to {platform}")
                        time.sleep(0.5)
                    
                    st.balloons()
            else:
                st.error("❌ Please write a message and select platforms")
        
        st.markdown("### Account Status")
        for platform in ["Instagram", "Facebook", "WhatsApp", "Twitter"]:
            status = "🔗 Connected" if platform in ["Instagram", "Facebook"] else "❌ Not Connected"
            st.markdown(f"**{platform}:** {status}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer with JavaScript integration note
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 10px; margin-top: 2rem;">
    <h4>🚀 Ready to Deploy?</h4>
    <p>This demo shows the UI structure. For production deployment, you'll need:</p>
    <ul style="text-align: left; max-width: 600px; margin: 0 auto;">
        <li>📧 <strong>Email Integration:</strong> SMTP server or Gmail API</li>
        <li>📱 <strong>SMS Service:</strong> Twilio, AWS SNS, or similar</li>
        <li>🗺️ <strong>Maps API:</strong> Google Maps JavaScript API</li>
        <li>📱 <strong>Social Media:</strong> Platform-specific APIs (Instagram Basic Display, Facebook Graph API)</li>
        <li>📸 <strong>Camera Access:</strong> HTML5 Media Capture API with HTTPS</li>
        <li>📍 <strong>Location Services:</strong> Browser Geolocation API</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# JavaScript integration example
st.markdown("""
### 🔧 JavaScript Integration Example

To integrate with your main page, use this JavaScript code:

```javascript
// Add this to your main page
function openDashboard() {
    // Replace with your Streamlit app URL
    window.open('http://localhost:8501', '_blank');
}

// HTML button on your main page
<button onclick="openDashboard()" class="dashboard-btn">
    Open Multi-Feature Dashboard
</button>
```
""")

# Real-time status display
with st.sidebar:
    st.markdown("### 📊 Dashboard Status")
    st.metric("Photos Taken", "1" if st.session_state.photo_taken else "0")
    st.metric("Emails Sent", "1" if st.session_state.email_sent else "0")
    st.metric("Location Shared", "Yes" if st.session_state.location_shared else "No")
    
    st.markdown("### ⏰ Current Time")
    st.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))