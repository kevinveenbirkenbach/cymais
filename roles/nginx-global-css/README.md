# 🌍 Nginx Global Theming Role

This **Ansible role** provides a **global theming solution** for Nginx-based web applications. It ensures a **consistent look and feel** across multiple applications by injecting a **unified global.css** with customizable theming options.  
---

## 🚀 Features
✅ **Automatic CSS Deployment** – Injects `global.css` into all Nginx-served applications.  
✅ **Dynamic Theming** – Uses `global_theming.css.colors` from Ansible variables for **full customization**.  
✅ **Bootstrap Override Support** – Ensures Bootstrap-based apps use the **unified global styles**.  
✅ **Versioning System** – Prevents caching issues with automatic **timestamp-based versioning**.  
✅ **Dark Mode Support** – Automatically adapts to user preferences.  
✅ **Runs Once Per Deployment** – Avoids redundant executions with `run_once_nginx_global_css`.  

---

## 📂 File Structure

```
.
├── tasks/
│   ├── main.yml        # Main Ansible tasks for deploying the global CSS
├── vars/
│   ├── main.yml        # Global variables (CSS paths, file names, etc.)
├── templates/
│   ├── global.css.j2   # Jinja2 template for generating the global CSS
│   ├── location.conf.j2     # Nginx configuration for serving global.css
│   ├── sub_filter.conf.j2   # Injects the global CSS link into served pages
└── README.md           # You are here 🚀
```

---

## 🎨 Theming Details

The **CSS template (`global.css.j2`)** dynamically applies the defined theme colors and ensures **Bootstrap, buttons, alerts, forms, and other UI elements** follow the **unified design**.

## 🛠️ Contribution
Feel free to **fork, modify, and improve** this role! Contributions are always welcome. 🛠️🔥

---

🚀 **Happy Theming!** 🎨✨  
*Created by [Kevin Veen-Birkenbach](https://www.veen.world) with the assistance of [ChatGPT](https://chatgpt.com/share/67a5fea3-4d5c-800f-8bc4-605712c02c9b).