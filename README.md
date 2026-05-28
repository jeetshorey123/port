# Jeet Shorey - Futuristic Gaming Portfolio

A production-ready, visually stunning futuristic gaming-inspired portfolio website built with pure HTML, CSS, and Vanilla JavaScript. Designed specifically for flawless deployment on Vercel without any build tools, backend requirements, or server-side rendering.

## 🚀 Features

### Design & Aesthetics
- **Futuristic Gaming UI** - Cyberpunk operating system aesthetic with glassmorphism effects
- **Glowing Neon Elements** - Cyan, neon green, and electric blue color scheme
- **Smooth Animations** - Premium animations, transitions, and reveal effects
- **Dark Theme** - Dark navy background with glowing accents
- **Fully Responsive** - Perfect on desktop, tablet, and mobile devices

### Interactive Elements
- **Loading Screen** - Animated loading bar with cyberpunk aesthetics
- **Sidebar Navigation** - Fixed, collapsible sidebar with active state tracking
- **Smooth Scrolling** - Navigation with smooth scroll behavior
- **Typing Animation** - Dynamic text typing effect on hero section
- **Particle Background** - Floating particles in hero section
- **Scroll Animations** - Elements animate in as they come into view
- **Hover Effects** - Interactive card and button hover animations
- **Mobile Menu Toggle** - Collapsible sidebar for mobile devices

### Sections
1. **Home** - Hero section with typing animation and CTA buttons
2. **Projects** - Featured project and grid of project cards
3. **Experience** - Interactive timeline of professional experience
4. **Skills** - Gaming-style skill cards with animated progress bars
5. **Education** - Educational background cards
6. **Contact** - Contact form and information

### Pages
- `index.html` - Main landing page
- `projects.html` - All projects grid
- `project-detail.html` - Project detail page template
- `experience.html` - Professional experience timeline
- `contact.html` - Contact form and information

## 📁 Project Structure

```
portfolio/
├── index.html                 # Main landing page
├── projects.html              # Projects listing
├── project-detail.html        # Project details template
├── experience.html            # Experience & timeline
├── contact.html               # Contact form
├── style.css                  # All styles (CSS only)
├── main.js                    # All JavaScript
├── vercel.json                # Vercel configuration
├── README.md                  # This file
└── assets/
    ├── images/                # Images directory
    ├── icons/                 # Icons directory
    ├── audio/                 # Audio files
    └── videos/                # Video files
```

## 🛠️ Technologies Used

- **HTML5** - Semantic markup
- **CSS3** - Animations, flexbox, grid, gradients
- **Vanilla JavaScript** - No frameworks, pure JS
- **Vercel** - Hosting platform

## 🎯 Key Features Implementation

### JavaScript
- ✅ Loading screen logic
- ✅ Navigation tracking and active states
- ✅ Typing animation
- ✅ Smooth scrolling
- ✅ IntersectionObserver for scroll animations
- ✅ Skill bar animations
- ✅ Form submission handling
- ✅ Mobile menu toggle
- ✅ Particle effects
- ✅ Button ripple effects

### CSS
- ✅ Glassmorphism cards
- ✅ Glowing borders and shadows
- ✅ Gradient backgrounds
- ✅ Smooth transitions
- ✅ Responsive grid layouts
- ✅ Mobile-first design
- ✅ CSS animations
- ✅ Custom scrollbar styling

## 🚀 Deployment on Vercel

### Prerequisites
- GitHub account with the repository

### Steps to Deploy

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit: Futuristic gaming portfolio"
   git push origin main
   ```

2. **Import to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Select your GitHub repository
   - Click "Import"
   - No configuration needed (vercel.json is included)
   - Click "Deploy"

3. **Done!**
   Your portfolio is live at `your-username.vercel.app`

## 📱 Responsive Breakpoints

- **Desktop**: 1200px and above
- **Tablet**: 768px - 1199px
- **Mobile**: Below 768px

All layouts adapt seamlessly across devices with no layout breaking.

## 🎨 Customization

### Colors
Edit the CSS variables in `style.css`:
```css
:root {
  --primary: #00d4ff;           /* Cyan */
  --secondary: #00ff88;         /* Neon green */
  --accent: #ff006e;            /* Hot pink */
  --accent-purple: #9d4edd;     /* Purple */
}
```

### Content
Update the following files to customize content:
- `index.html` - Hero, projects, skills sections
- `projects.html` - Project listings
- `experience.html` - Work experience
- `contact.html` - Contact information

### Images & Assets
Place your assets in the `assets/` directory:
- `assets/images/` - Profile pictures, project screenshots
- `assets/icons/` - Custom SVG icons
- `assets/audio/` - Background music or sound effects
- `assets/videos/` - Video content

Use relative paths in your HTML:
```html
<img src="./assets/images/photo.jpg" alt="Photo">
```

## ⚡ Performance Features

- **No Build Tools** - Instant deployment
- **No Backend** - 100% static files
- **No Dependencies** - Pure HTML/CSS/JS
- **Optimized CSS** - Minified animations
- **Fast Loading** - Loads in milliseconds
- **SEO Friendly** - Semantic HTML

## 🔧 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 📝 Customization Guide

### Add a New Project
1. Open `projects.html`
2. Copy a project card
3. Update the title, description, and tags
4. Update `project-detail.html` for detailed view

### Update Navigation Links
Edit the links in the `nav-links` section of sidebar (all HTML files)

### Change Color Scheme
Update CSS variables in `style.css`:
```css
--primary: #your-color;
```

### Add Social Links
Update social icons in sidebar:
```html
<a href="https://your-social.com" target="_blank" class="social-icon">
  <span>🔗</span>
</a>
```

## 🎯 Vercel Specific Notes

This portfolio uses Vercel's `cleanUrls` feature and rewrites to handle routing:

```json
{
  "cleanUrls": true,
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

This configuration:
- Removes `.html` extensions from URLs
- Handles client-side routing
- Works perfectly with static pages

## 📊 Animations Used

- `slideInUp` - Elements slide up on scroll
- `slideInLeft/Right` - Directional slide animations
- `fadeIn` - Simple fade effect
- `scaleIn` - Scale up effect
- `float` - Floating blob animations
- `glow` - Glowing border effect
- `pulse` - Pulsing opacity effect
- `typing` - Blinking cursor effect

## 🎬 Loading Screen

The loading screen automatically completes after 3 seconds and transitions to the main content. Customize the timing in `main.js`:

```javascript
setTimeout(() => {
  loadingScreen.classList.add('hidden');
}, 500);
```

## 📞 Contact Form

The contact form currently shows a success message. To integrate with a real email service:

1. Use a service like Formspree, Netlify Forms, or EmailJS
2. Update the form submission logic in `main.js`
3. Add your service's API key

## 🔒 Security

- No sensitive data stored in code
- No API keys in repository
- All client-side processing
- Safe form submission handling

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Jeet Shorey**
- Email: jeet@example.com
- GitHub: github.com/jeet
- LinkedIn: linkedin.com/in/jeet

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

## 🐛 Known Issues

- None at this time

## 📈 Future Enhancements

- [ ] Blog section
- [ ] Project filtering
- [ ] Dark/Light theme toggle
- [ ] Internationalization
- [ ] Advanced animations with Three.js
- [ ] Project showcase with image gallery

## ✅ Deployment Checklist

Before deploying:
- [ ] Update all personal information
- [ ] Check all links work correctly
- [ ] Test on mobile devices
- [ ] Verify images load properly
- [ ] Test contact form
- [ ] Update resume PDF link
- [ ] Add social media links

## 📚 Resources

- [Vercel Documentation](https://vercel.com/docs)
- [CSS Animations Guide](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Animations)
- [JavaScript Intersection Observer](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API)

## 🎉 Conclusion

This is a production-ready portfolio that deploys instantly to Vercel without any configuration. Simply push to GitHub and deploy. No build tools, no backend, no complications!

Enjoy your futuristic gaming portfolio! 🚀

---

**Last Updated**: 2024
**Version**: 1.0.0
