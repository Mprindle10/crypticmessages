# 🌍 Ngrok Setup Guide for The Riddle Room

## 🚨 **Authentication Required**

Ngrok now requires a free account to create tunnels. Here's how to set it up:

### 📝 **Step 1: Create Free Ngrok Account**
1. Go to: https://dashboard.ngrok.com/signup
2. Sign up with your email (it's completely free)
3. Verify your email address

### 🔑 **Step 2: Get Your Auth Token**
1. After signing in, go to: https://dashboard.ngrok.com/get-started/your-authtoken
2. Copy your personal authtoken (it looks like: `2AB123...xyz`)

### ⚙️ **Step 3: Configure Ngrok**
Run this command with YOUR authtoken:
```bash
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
```

### 🚀 **Step 4: Start the Tunnel**
```bash
cd /home/m/crypticmessages
./setup_ngrok.sh
```

---

## 🔄 **Alternative: Quick Setup Commands**

Once you have your authtoken, run these commands:

```bash
# Replace YOUR_AUTHTOKEN with your actual token from ngrok dashboard
ngrok config add-authtoken YOUR_AUTHTOKEN

# Start the tunnel for your beta page
ngrok http 8000
```

## 📱 **What You'll Get:**

After setup, ngrok will provide URLs like:
- **HTTP:** `http://abc123.ngrok.io`
- **HTTPS:** `https://abc123.ngrok.io` ← Use this one!

Your beta page will be accessible at:
- `https://abc123.ngrok.io/beta`

## 🎬 **For Your YouTube Video:**

Update your video description with:
```
🧩 Ready for more puzzles? 
Sign up for The Riddle Room: https://abc123.ngrok.io/beta

Get weekly cryptic challenges delivered to your inbox!
```

## 💡 **Pro Tips:**

1. **Keep it running:** The tunnel only works while ngrok is running
2. **Free tier limits:** 1 tunnel at a time, but that's perfect for this use case
3. **HTTPS preferred:** Always use the https:// URL for better security
4. **Custom domains:** Upgrade to paid plan for custom domains (optional)

---

## 🆘 **Need Help?**

If you encounter any issues:
1. Make sure your FastAPI server is running on port 8000
2. Verify your authtoken is set correctly: `ngrok config check`
3. Test locally first: `curl http://localhost:8000/beta`

**Ready to make your beta page globally accessible in 2 minutes!** 🚀
