# Streamlit Deployment Guide

## 🚀 Deploy Your RAG Pipeline with Streamlit

### Option 1: Local Deployment (Quick Start)

#### Run Locally:
```bash
streamlit run app.py
```

This will open a web browser at `http://localhost:8501`

---

### Option 2: Deploy to Streamlit Cloud (FREE) ☁️

**Steps:**

1. **Push your code to GitHub** ✅ (Already done!)

2. **Go to Streamlit Cloud:**
   - Visit: https://share.streamlit.io

3. **Connect your repository:**
   - Click "New app"
   - Select your repository: `daim-ul-hassan/Smart-Q-A`
   - Branch: `main`
   - Main file path: `app.py`

4. **Add API Key as Secret:**
   - In Streamlit Cloud dashboard, go to your app
   - Click "Settings" → "Secrets"
   - Add this:
   ```toml
   [google]
   api_key = "your_actual_api_key_here"
   ```

5. **Deploy!**
   - Click "Deploy!"
   - Your app will be live in minutes

---

### Option 3: Deploy to Hugging Face Spaces (FREE) 🤗

**Steps:**

1. **Create Hugging Face account:**
   - Go to: https://huggingface.co

2. **Create new Space:**
   - Click your profile → "New Space"
   - Name: `smart-qa-rag`
   - License: MIT
   - SDK: Streamlit
   - Visibility: Public

3. **Configure requirements.txt:**
   - Already included in your repo! ✅

4. **Add files to Hugging Face:**
   - Clone your space
   - Copy all files from your project
   - Push to Hugging Face

5. **Set environment variable:**
   - Go to Space Settings
   - Add "Repository secret":
     - Key: `GOOGLE_API_KEY`
     - Value: `your_api_key`

6. **Deploy automatically!**

---

### Option 4: Deploy to Railway (FREE tier) 🚂

**Steps:**

1. **Create Railway account:**
   - Go to: https://railway.app

2. **Deploy from GitHub:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Add build settings:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

4. **Add environment variable:**
   - Go to Variables tab
   - Add: `GOOGLE_API_KEY=your_api_key`

5. **Deploy!**

---

### Option 5: Deploy to Render (FREE tier) 🎨

**Steps:**

1. **Create Render account:**
   - Go to: https://render.com

2. **Create new Web Service:**
   - Connect your GitHub repository
   - Choose free tier

3. **Configure:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

4. **Add environment variable:**
   - Add `GOOGLE_API_KEY` with your key

5. **Deploy!**

---

## 🔧 Custom app.py for Cloud Deployment

For cloud platforms, you may need to modify `app.py`:

```python
# Add at the top of app.py
import os

# Get API key from environment or secrets
api_key = os.getenv("GOOGLE_API_KEY") or \
          st.secrets.get("google", {}).get("api_key", "")

if not api_key:
    st.error("Please configure your Google API Key")
    st.stop()
```

---

## 📊 Platform Comparison

| Platform | Free Tier | Ease | Speed | Best For |
|----------|-----------|------|-------|----------|
| **Streamlit Cloud** | ✅ Yes | ⭐⭐⭐⭐⭐ | Fast | Quick demos |
| **Hugging Face** | ✅ Yes | ⭐⭐⭐⭐ | Medium | ML projects |
| **Railway** | ✅ $5 credit | ⭐⭐⭐⭐ | Fast | Production apps |
| **Render** | ✅ Yes (limited) | ⭐⭐⭐ | Medium | Long-term hosting |
| **Local** | ✅ Free | ⭐⭐⭐⭐⭐ | Instant | Development |

---

## 🎯 Recommended: Streamlit Cloud

**Why?**
- FREE forever
- Easy setup (3 clicks)
- Automatic HTTPS
- Built-in authentication
- Direct GitHub integration
- No server management

**Get started:** https://share.streamlit.io

---

## 🐛 Troubleshooting

### "Module not found" error:
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### "API Key missing" error:
- Check `.env` file exists
- Verify `GOOGLE_API_KEY` is set
- Restart Streamlit

### Port already in use:
```bash
# Use different port
streamlit run app.py --server.port=8502
```

### Vector store not found:
```bash
# Build vector store first
python rag_setup.py
```

---

## 🎉 Success Checklist

Before deploying, ensure:
- [ ] All dependencies installed
- [ ] `.env` file with valid API key
- [ ] Vector store built (`chroma_db/` folder exists)
- [ ] Sample documents in `docs/` folder
- [ ] Code pushed to GitHub
- [ ] `requirements.txt` includes streamlit

---

## 📞 Need Help?

- **Documentation:** See README.md
- **Quick Start:** See GET_STARTED.md
- **GitHub Issues:** https://github.com/daim-ul-hassan/Smart-Q-A/issues

---

**Happy Deploying! 🚀**

Your RAG pipeline is ready for the world!
