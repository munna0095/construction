# 📚 SETUP GUIDE - SIDDHI CONSTRUCTION WEBSITE

Complete setup, deployment, and customization guide.

---

## 📋 Table of Contents

1. [Local Development](#local-development)
2. [Customization](#customization)
3. [Deployment Options](#deployment-options)
4. [Git & Version Control](#git--version-control)
5. [Troubleshooting](#troubleshooting)
6. [Performance Optimization](#performance-optimization)

---

## 🚀 Local Development

### Prerequisites
- Python 3.6+ (for local server)
- Git (for version control)
- Text editor (VS Code recommended)
- Modern browser (Chrome, Firefox, Safari, Edge)

### Step 1: Start the Development Server

**Option A: Windows Batch File (Easiest)**
```bash
Double-click: START_SERVER.bat
```

**Option B: PowerShell**
```powershell
cd C:\Users\Admin\Desktop\PROJECTS\active\Construction_Website
python -m http.server 8000
```

**Option C: Command Prompt**
```cmd
cd C:\Users\Admin\Desktop\PROJECTS\active\Construction_Website
python -m http.server 8000
```

### Step 2: Open in Browser
```
http://localhost:8000
```

### Step 3: Test All Pages
- ✅ Home (with 3D animation)
- ✅ Projects (interactive cards with modals)
- ✅ Services (6 service types)
- ✅ About (company story)
- ✅ Team (6 team members)
- ✅ Gallery (12 photo slots)
- ✅ Contact (working form)

---

## 🎨 Customization

### 1. Update Company Name
**File:** `siddhi-construction-website.jsx`

Find and replace:
```javascript
"SIDDHI CONSTRUCTION" → "YOUR COMPANY NAME"
"SIDDHI" → "YOUR ABBREVIATION"
```

### 2. Update Contact Information

**Phone Number:**
```javascript
Find: "+91 9876543210"
Replace: "+91 YOUR_NUMBER"
```

**Email:**
```javascript
Find: "info@siddhiconstruction.com"
Replace: "your@email.com"
```

**Location:**
```javascript
Find: "Pune, Maharashtra, India"
Replace: "Your City, State, Country"
```

### 3. Change Theme Colors

Current colors:
```javascript
Primary Orange: #FF6B35
Secondary Yellow: #FFC72C
Dark Gray: #2D3436
```

To change, find and replace:
```javascript
from-orange-500 → from-blue-500  (or any color)
text-orange-500 → text-blue-500
bg-orange-500 → bg-blue-500
border-orange-500 → border-blue-500
```

### 4. Update Projects

**Edit ProjectsPage function:**

```javascript
const projects = [
  {
    id: 1,
    name: 'Your Project Name',
    location: 'City, State',
    category: 'Residential|Commercial|Infrastructure',
    area: 'Size in sq ft',
    timeline: '2024-2025',
    desc: 'Project description',
    image: '🏢', // Change to your image
    status: 'Ongoing|Completed'
  },
  // Add more projects...
];
```

### 5. Update Team Members

**Edit TeamPage function:**

```javascript
const team = [
  {
    id: 1,
    name: 'Person Name',
    role: 'Their Role',
    image: '👨‍💼' // Change emoji or URL
  },
  // Add more team members...
];
```

### 6. Add Project Photos

**Step 1:** Create images folder
```
Construction_Website/
└── images/
    ├── project-1.jpg
    ├── project-2.jpg
    └── ...
```

**Step 2:** Update image references in code
```javascript
// Change from:
image: '🏢'

// Change to:
image: '/images/project-1.jpg'

// Or use online URL:
image: 'https://example.com/photo.jpg'
```

### 7. Customize Services

**Edit ServicesPage function:**

```javascript
const services = [
  {
    icon: '🏡',
    title: 'Service Name',
    desc: 'Service description'
  },
  // Add more services...
];
```

### 8. Modify Features (Homepage)

**Edit HomePage function:**

```javascript
const features = [
  {
    icon: '🏢',
    title: 'Feature Title',
    desc: 'Feature description'
  },
  // Add more features...
];
```

---

## 🌐 Deployment Options

### Option 1: DigitalOcean (Your Current Server)

**Upload files:**
```bash
scp index.html root@168.144.30.73:/root/siddhi-website/
scp siddhi-construction-website.jsx root@168.144.30.73:/root/siddhi-website/
scp *.xml root@168.144.30.73:/root/siddhi-website/
scp *.txt root@168.144.30.73:/root/siddhi-website/
```

**Start on server:**
```bash
ssh root@168.144.30.73
cd /root/siddhi-website
python3 -m http.server 80 &
```

**Access:**
```
http://168.144.30.73
```

### Option 2: Vercel (Recommended)

1. Install Vercel:
```bash
npm i -g vercel
```

2. Deploy:
```bash
cd C:\Users\Admin\Desktop\PROJECTS\active\Construction_Website
vercel
```

3. Follow prompts to deploy

### Option 3: Netlify

1. Install Netlify CLI:
```bash
npm i -g netlify-cli
```

2. Deploy:
```bash
netlify deploy
```

3. Select your folder and deploy

### Option 4: GitHub Pages

1. Create GitHub repository
2. Push files to GitHub
3. Enable GitHub Pages in settings
4. Access at: `https://yourusername.github.io/repo-name`

---

## 🐙 Git & Version Control

### First-Time Setup

```bash
cd C:\Users\Admin\Desktop\PROJECTS\active\Construction_Website

# Initialize Git
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial SIDDHI website commit"

# Add remote (replace USERNAME)
git remote add origin https://github.com/USERNAME/siddhi-construction-website.git

# Create main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

### Regular Workflow

```bash
# Make changes to files

# Check status
git status

# Stage changes
git add .

# Commit changes
git commit -m "feat: Update projects with photos"

# Push to GitHub
git push origin main
```

### Pulling Changes

```bash
# If working on multiple devices
git pull origin main
```

### Branching Strategy

```bash
# Create feature branch
git checkout -b feature/new-projects

# Make changes and commit
git add .
git commit -m "feat: Add 3 new projects"

# Switch back to main
git checkout main

# Merge feature
git merge feature/new-projects

# Delete feature branch
git branch -d feature/new-projects

# Push changes
git push origin main
```

---

## 🔧 Troubleshooting

### Server Not Starting

**Issue:** "python: command not found" or similar

**Solution 1:** Check if Python is installed
```bash
python --version
```

**Solution 2:** Try python3
```bash
python3 -m http.server 8000
```

**Solution 3:** Use Node.js (if installed)
```bash
npx http-server
```

**Solution 4:** Install Python from https://www.python.org

### Port 8000 Already in Use

**Issue:** "Address already in use"

**Solution:**
```bash
# Use different port
python -m http.server 9000

# Access at: http://localhost:9000
```

### 3D Animation Not Loading

**Issue:** 3D shapes not showing on home page

**Solution:**
1. Open browser console: `F12`
2. Check for errors
3. Make sure JavaScript is enabled
4. Try different browser
5. Check internet connection (needs to load Three.js from CDN)

### Images Not Displaying

**Issue:** Image placeholder emojis show but not your photos

**Solutions:**
1. Check image path is correct
2. Use absolute paths: `/images/photo.jpg`
3. Clear browser cache: `Ctrl+Shift+Del`
4. Restart server
5. Check file name spelling

### Form Not Working

**Issue:** Contact form doesn't submit

**Solution:**
1. Open console (`F12`)
2. Check for errors
3. Make sure all fields are filled
4. Try different browser

---

## ⚡ Performance Optimization

### 1. Compress Images

Before uploading photos:
```bash
# Using ImageMagick
convert photo.jpg -quality 85 photo-optimized.jpg

# Or use online tools:
# - TinyPNG
# - Compressor.io
# - ImageOptimizer.com
```

### 2. Lazy Loading

Implement lazy loading for images (for future):
```javascript
<img src="..." loading="lazy" />
```

### 3. Enable Caching

In production, add caching headers:
```
Cache-Control: public, max-age=3600
```

### 4. Content Delivery Network (CDN)

For images, use CDN like:
- Cloudinary
- AWS CloudFront
- Bunny CDN

### 5. Minimize CSS/JS

Production versions:
```html
<!-- Use minified versions -->
<link href="...tailwindcss...min.css">
```

---

## 📊 Analytics Setup (Optional)

### Google Analytics

1. Create account at: https://analytics.google.com
2. Get your Tracking ID
3. Add to `index.html` before `</head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_ID');
</script>
```

### Facebook Pixel

1. Create account at: https://business.facebook.com
2. Get Pixel ID
3. Add before `</head>`:

```html
<!-- Facebook Pixel -->
<img height="1" width="1" style="display:none"
  src="https://www.facebook.com/tr?id=PIXEL_ID&ev=PageView&noscript=1"
/>
```

---

## 📝 File Reference

| File | Purpose | Size |
|------|---------|------|
| index.html | Main HTML entry | 3.5 KB |
| siddhi-construction-website.jsx | React component | 26 KB |
| package.json | Project metadata | 1 KB |
| .gitignore | Git ignore rules | 0.5 KB |
| sitemap.xml | SEO sitemap | 1.3 KB |
| robots.txt | Robot rules | 0.5 KB |
| START_SERVER.bat | Windows batch file | 1 KB |
| README.md | Documentation | 6 KB |
| QUICK_START.md | Quick reference | 4 KB |
| GIT_SETUP.md | Git guide | 7 KB |
| SETUP_GUIDE.md | This file | 10 KB |

---

## ✅ Pre-Launch Checklist

- [ ] Update company name
- [ ] Update contact information (phone, email, location)
- [ ] Update projects with real data
- [ ] Update team member names
- [ ] Add project photos
- [ ] Test on desktop browser
- [ ] Test on mobile browser
- [ ] Test contact form
- [ ] Create Git repository
- [ ] Deploy to production

---

## 🚀 Next Steps

1. **Customize:** Update company info (1 hour)
2. **Add Photos:** Replace emoji with real images (2 hours)
3. **Test:** Check all pages and functions (30 mins)
4. **Push to Git:** Create GitHub repository (15 mins)
5. **Deploy:** Choose hosting and deploy (1 hour)
6. **Monitor:** Check analytics and user feedback

---

## 📞 Support Resources

- **Tailwind CSS:** https://tailwindcss.com/docs
- **React:** https://react.dev
- **Three.js:** https://threejs.org/docs/
- **Git:** https://git-scm.com/doc

---

**Status:** ✅ Production Ready
**Last Updated:** April 28, 2026
**Version:** 1.0.0

Good luck with your SIDDHI Construction website! 🚀
