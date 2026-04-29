# 🚀 QUICK START - SIDDHI CONSTRUCTION WEBSITE

Get your website running in **2 minutes**!

---

## Step 1️⃣: Start the Server

### Option A: Click the Batch File (EASIEST)
```
Double-click: START_SERVER.bat
```

### Option B: Use PowerShell/CMD
```powershell
cd C:\Users\Admin\Desktop\PROJECTS\active\Construction_Website
python -m http.server 8000
```

### Option C: Use Node.js (if you have it)
```bash
npx http-server
```

---

## Step 2️⃣: Open in Browser

```
http://localhost:8000
```

The website will load with all 7 pages fully functional:
- ✅ Home (with 3D animation)
- ✅ Projects
- ✅ Services
- ✅ About
- ✅ Team
- ✅ Gallery
- ✅ Contact

---

## Step 3️⃣: Test on Mobile

Open on your phone (if on same network):
```
http://YOUR_COMPUTER_IP:8000
```

Get your IP from the server output or check it in Settings.

---

## ⚙️ Next Steps

### Update Your Info
Edit `siddhi-construction-website.jsx`:
```javascript
"SIDDHI CONSTRUCTION" → Your company name
"+91 XXX XXXX XXXX" → Your phone  
"info@siddhiconstruction.com" → Your email
"Pune, Maharashtra" → Your location
```

### Add Photos
1. Create `images/` folder
2. Add your project photos
3. Replace emoji in code with: `/images/photo.jpg`

### Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/repo.git
git push -u origin main
```

See `GIT_SETUP.md` for detailed Git instructions.

---

## 🛑 Troubleshooting

**Server won't start?**
```bash
python --version  # Check if Python is installed
```

**Port 8000 already in use?**
```bash
python -m http.server 9000  # Use different port
# Then visit: http://localhost:9000
```

**Images not loading?**
- Use full URLs: `https://example.com/image.jpg`
- Or place in `images/` folder: `/images/photo.jpg`
- Clear browser cache: `Ctrl+Shift+Del`

**3D shapes not rotating?**
- Check browser console: `F12`
- Make sure JavaScript is enabled
- Try different browser

---

## 📁 File Structure

```
Construction_Website/
├── index.html                          ← Open this in browser
├── siddhi-construction-website.jsx     ← React component (edit to customize)
├── START_SERVER.bat                    ← Double-click to start
├── README.md                           ← Full documentation
├── GIT_SETUP.md                        ← Git instructions
├── package.json                        ← Project info
├── .gitignore                          ← Git ignore rules
└── images/                             ← Add your photos here
```

---

## 🎯 Common Edits (Copy-Paste Ready)

### Change Company Name
Find: `"SIDDHI CONSTRUCTION"`
Replace: `"YOUR COMPANY NAME"`

### Change Theme Color
Find: `from-orange-500`
Replace: `from-blue-500`

### Change Phone
Find: `"+91 XXX XXXX XXXX"`
Replace: `"+91 9876543210"`

### Add Project
Find the `projects` array in `ProjectsPage()`, add:
```javascript
{
  id: 7,
  name: 'Your Project Name',
  location: 'City, State',
  category: 'Residential',
  area: '50,000 sq ft',
  timeline: '2024-2025',
  desc: 'Project description',
  image: '/images/photo.jpg',
  status: 'Ongoing',
}
```

---

## 📞 Stop the Server

Press `Ctrl+C` in the PowerShell/CMD window.

---

## ✅ You're Ready!

Your website is **LIVE locally** at `http://localhost:8000`

Next:
1. Customize your info
2. Add photos (in 3-4 days)
3. Push to GitHub
4. Deploy to production

---

**Need help?** See `README.md` or `SETUP_GUIDE.md` for detailed info.

Good luck! 🚀
