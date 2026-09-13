# Premium DevOps & Cloud Engineering Jekyll Blog Template

A high-performance, print-optimized, and premium-themed personal blog and engineering portfolio website built using **Jekyll**. This template is tailor-made for DevOps, SRE, Systems, and Cloud engineers to showcase technical certifications, academic research, enterprise projects, and publish code-rich guides.


---

## Key Features
* 🌓 **Flash-Free Dark Mode:** Implemented with inline theme matching (stored in local storage) to avoid blinding page-load flashes.
* 📱 **Modern Translucent Design:** Sticky glassmorphism header, card lifts, micro-animations, and yellow/blue accent styling.
* 🔎 **Offline client-side Search:** Instant full-text search across titles, descriptions, categories, tags, and content using static JSON indexes.
* 📄 **Print-Friendly Resume (/cv):** Custom `@media print` rules that hide navbar, ads, and sidebars, outputting a professional black-and-white executive CV structure directly via browser prints.
* 📦 **Modular Configuration:** Skills, Projects, Experience, and Certifications managed entirely as structured YAML datasets under `_data/`.
* ⚡ **CNCF / OTel Observability Layout:** Custom 3-column article blueprint (Sticky left TOC, central post text flow, sticky right sharing and ad widgets).
* ⚙️ **CI/CD Built-in:** Automated GitHub Actions workflow compiling site files and deploying directly to GitHub Pages hosting.
* 🛡️ **SEO-Optimized:** Pre-configured schema structures (JSON-LD), sitemaps, RSS feeds, open-graph cards, and canonical URL mapping via `jekyll-seo-tag`.

---

## Directory Structure

```text
.
├── .github/workflows/
│   └── jekyll.yml       # Automatic cloud compiler & deployer to GitHub Pages
├── _data/               # Profile datasets
│   ├── certifications.yml
│   ├── experience.yml
│   ├── projects.yml
│   └── skills.yml
├── _includes/           # Component layouts
│   ├── ads/             # Google AdSense placeholders
│   │   ├── banner.html
│   │   ├── in-article.html
│   │   └── sidebar.html
│   ├── footer.html
│   ├── head.html
│   ├── header.html
│   ├── post-card.html
│   ├── project-card.html
│   └── toc.html         # Client-side dynamic TOC parser
├── _layouts/            # Template wrappers
│   ├── default.html
│   ├── page.html
│   └── post.html
├── _posts/              # Markdown technical posts
├── assets/              # Static files
│   ├── css/main.css     # Unified stylesheet (custom properties, print overrides)
│   ├── cv/cv.pdf        # Downloadable PDF resume path
│   └── js/
│       ├── main.js      # Copy button injector, theme-switcher click handler
│       └── search.js    # Search index processor
├── 404.html             # Missing page fallback routing
├── _config.yml          # Global settings, SEO, and social properties
├── CNAME                # Custom domain mapping
└── search.json.liquid   # Search index builder database
```

---

## 1. Local Development Setup

To run this blog locally on your laptop, you need **Ruby** and **Bundler** installed.

### Step 1: Install Ruby
* **Windows:** Download and install [RubyInstaller for Windows](https://rubyinstaller.org/) (choose Ruby + Devkit version).
* **macOS:** Install via Homebrew: `brew install ruby`.
* **Linux:** Install via package manager: `sudo apt install ruby-full build-essential zlib1g-dev`.

### Step 2: Install Bundler & Download Dependencies
Open your shell, navigate to the project directory, and install:
```bash
gem install bundler
bundle install
```

### Step 3: Serve Locally
Start the local Jekyll development server:
```bash
bundle exec jekyll serve
```
Open [http://localhost:4000](http://localhost:4000) in your web browser.

---

## 2. Publishing Articles

All articles are stored as Markdown files inside the `_posts/` directory.

### Step 1: Create a Post File
Filename must follow the pattern `YYYY-MM-DD-title.md` (e.g., `2026-08-10-aws-control-tower.md`).

### Step 2: Configure Front Matter
Insert the configuration header at the top of the file:
```yaml
---
layout: post
title: "AWS Control Tower: When Should You Use It?"
description: "An in-depth review of AWS Control Tower configurations and tradeoffs."
date: 2026-08-10 09:00:00 +0700
last_updated: 2026-08-11 07:00:00 +0700  # Optional (displays updated date)
categories: [AWS]                        # Main category (will map to badges)
tags: [Control Tower, Multi-Account]      # Sub-tags
---
```

### Step 3: Write Markdown Content
Add your article body using standard GitHub Flavored Markdown (GFM). Use backticks for code blocks; copy-to-clipboard utilities and language headers will be injected automatically!

---

## 3. Adding Media & Images

1. Place image files inside the `assets/images/` folder (create this directory if it does not exist).
2. Reference the image in your Markdown files using relative links:
```markdown
![AWS Architecture Blueprint]({{ '/assets/images/aws-architecture.png' | relative_url }})
```

---

## 4. Customizing Colors & Styling

Color variables are centralized using CSS variables inside [assets/css/main.css](file:///d:/ntk/assets/css/main.css).

```css
:root {
  /* Light Mode Palette */
  --background: #f8fafc;
  --surface: #ffffff;
  --text-primary: #0f172a;
  --primary: #0f4c81;         /* Classic Deep Blue */
  --accent: #d97706;          /* Contrasty Amber/Gold */
  /* ... */
}

html.dark-theme {
  /* Dark Mode Palette */
  --background: #020617;      /* Slate 950 */
  --surface: #0f172a;         /* Slate 900 */
  --text-primary: #f8fafc;
  --primary: #60a5fa;         /* Readable Soft Blue */
  --accent: #fbbf24;          /* Bright Gold */
}
```
Modify these hex values to instantly change the branding across the entire site (including navbar, cards, borders, buttons, and badges).

---

## 5. Enable / Disable Dark Mode Defaults

The dark mode setting is managed via the `dark-theme` class on the `<html>` node. 
* By default, the site automatically scans the visitor's computer preferences (`prefers-color-scheme: dark`) to match their OS settings.
* When they click the theme switcher, their preference is saved in their browser's `localStorage` (overriding the OS preference).
* To change the core logic, modify the script inside the `<head>` in [_includes/head.html](file:///d:/ntk/_includes/head.html).

---

## 6. Configuring Google AdSense (Monetization)

The template has three pre-allocated advertisement files under `_includes/ads/`:
1. `banner.html`: Leaderboard ads (728x90) loaded inside the article header and footer.
2. `in-article.html`: Native responsive ads loaded at the beginning and end of the article content.
3. `sidebar.html`: Sticky sidebar ads (300x250 or 300x600) on the left/right sections of the page.

To go live, replace the placeholder `div` inside these files with your Google AdSense code snippet:
```html
<!-- Example replacement in _includes/ads/sidebar.html -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
     data-ad-slot="XXXXXXXXXX"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
```

---

## 7. Configuring Custom Domain

To link your custom domain (e.g., `blog.example.com`):
1. Open the [CNAME](file:///d:/ntk/CNAME) file and replace `blog.example.com` with your actual domain.
2. Update the `url` property in [_config.yml](file:///d:/ntk/_config.yml):
```yaml
url: "https://blog.example.com"
```
3. Set up CNAME/A records in your DNS provider (Cloudflare, Route53, GoDaddy) pointing to your GitHub Pages domain (`username.github.io`).

---

## 8. Deployment to GitHub Pages

Our pre-configured CI/CD workflow compiles the site using GitHub Actions:
1. Push your code changes to the `main` branch on GitHub:
```bash
git add .
git commit -m "feat: complete jekyll setup"
git push -u origin main
```
2. Navigate to your repository page on GitHub and go to **Settings > Pages**.
3. Under **Build and deployment > Source**, select **GitHub Actions** (instead of Deploy from branch).
4. The deployment pipeline will trigger automatically. You can check its progress under the **Actions** tab.
