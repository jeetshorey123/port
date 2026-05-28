/* ========================================
   FUTURISTIC GAMING PORTFOLIO - MAIN JAVASCRIPT
   ======================================== */

// DOM Elements
const loadingScreen = document.querySelector('.loading-screen');
const loadingBar = document.querySelector('.loading-bar');
const loadingPercentage = document.querySelector('.loading-percentage');
const sidebar = document.querySelector('.sidebar');
const menuToggle = document.querySelector('.menu-toggle');
const navLinks = document.querySelectorAll('.nav-link a');
const mainContent = document.querySelector('main');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  initializeLoading();
  initializeNavigation();
  initializeScrollAnimations();
  initializeTypingAnimation();
  initializeParticles();
  initializeSkillBars();
  initializeFormSubmission();
});

/* ========================================
   LOADING SCREEN
   ======================================== */

function initializeLoading() {
  let progress = 0;
  const interval = setInterval(() => {
    progress += Math.random() * 30;
    if (progress > 100) progress = 100;

    loadingBar.style.width = progress + '%';
    loadingPercentage.textContent = Math.floor(progress) + '%';

    if (progress === 100) {
      clearInterval(interval);
      setTimeout(() => {
        loadingScreen.classList.add('hidden');
      }, 500);
    }
  }, 200);
}

/* ========================================
   NAVIGATION SYSTEM
   ======================================== */

function initializeNavigation() {
  // Mobile menu toggle
  if (menuToggle) {
    menuToggle.addEventListener('click', () => {
      sidebar.classList.toggle('active');
    });
  }

  // Close sidebar on link click
  navLinks.forEach((link) => {
    link.addEventListener('click', () => {
      sidebar.classList.remove('active');
      updateActiveNav(link);
    });
  });

  // Track active section on scroll
  window.addEventListener('scroll', () => {
    updateActiveNavOnScroll();
  });
}

function updateActiveNav(currentLink) {
  navLinks.forEach((link) => link.classList.remove('active'));
  currentLink.classList.add('active');
}

function updateActiveNavOnScroll() {
  const sections = document.querySelectorAll('section');
  const scrollY = window.scrollY + 100;

  sections.forEach((section) => {
    const sectionHeight = section.offsetHeight;
    const sectionTop = section.offsetTop;
    const sectionId = section.getAttribute('id');

    if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
      navLinks.forEach((link) => link.classList.remove('active'));
      const activeLink = document.querySelector(
        `.nav-link a[href="#${sectionId}"]`
      );
      if (activeLink) activeLink.classList.add('active');
    }
  });
}

/* ========================================
   SCROLL ANIMATIONS
   ======================================== */

function initializeScrollAnimations() {
  const observerOptions = {
    threshold: 0.15,
    rootMargin: '0px 0px -50px 0px',
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, observerOptions);

  // Observe all animated elements
  const animatedElements = document.querySelectorAll(
    '.project-card, .timeline-item, .skill-category, .education-card, .detail-section'
  );
  animatedElements.forEach((el) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
    observer.observe(el);
  });
}

/* ========================================
   TYPING ANIMATION
   ======================================== */

function initializeTypingAnimation() {
  const typingElement = document.querySelector('.typing-text');
  if (!typingElement) return;

  const textArray = [
    'Full Stack Developer',
    'AI/ML Engineer',
    'Cloud Architect',
    'Creative Technologist',
  ];

  let textIndex = 0;
  let charIndex = 0;
  let isDeleting = false;
  const typingSpeed = 100;
  const deletingSpeed = 50;
  const pauseTime = 2000;

  function type() {
    const currentText = textArray[textIndex];
    const displayText = isDeleting
      ? currentText.substring(0, charIndex - 1)
      : currentText.substring(0, charIndex + 1);

    typingElement.textContent = displayText;

    if (!isDeleting && charIndex === currentText.length) {
      setTimeout(() => {
        isDeleting = true;
        type();
      }, pauseTime);
      return;
    }

    if (isDeleting && charIndex === 0) {
      isDeleting = false;
      textIndex = (textIndex + 1) % textArray.length;
      type();
      return;
    }

    charIndex += isDeleting ? -1 : 1;
    const speed = isDeleting ? deletingSpeed : typingSpeed;
    setTimeout(type, speed);
  }

  type();
}

/* ========================================
   PARTICLE BACKGROUND
   ======================================== */

function initializeParticles() {
  const heroSection = document.querySelector('.hero');
  if (!heroSection) return;

  const particleCount = 20;
  const particles = [];

  class Particle {
    constructor() {
      this.x = Math.random() * window.innerWidth;
      this.y = Math.random() * window.innerHeight;
      this.size = Math.random() * 3 + 1;
      this.speedX = (Math.random() - 0.5) * 0.5;
      this.speedY = (Math.random() - 0.5) * 0.5;
      this.opacity = Math.random() * 0.5 + 0.2;
    }

    update() {
      this.x += this.speedX;
      this.y += this.speedY;

      if (this.x < 0 || this.x > window.innerWidth) this.speedX *= -1;
      if (this.y < 0 || this.y > window.innerHeight) this.speedY *= -1;
    }
  }

  for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle());
  }

  function animateParticles() {
    particles.forEach((particle) => {
      particle.update();
    });

    requestAnimationFrame(animateParticles);
  }

  animateParticles();
}

/* ========================================
   SKILL PROGRESS BARS
   ======================================== */

function initializeSkillBars() {
  const skillBars = document.querySelectorAll('.skill-progress');
  const skillSection = document.querySelector('.skills');

  if (!skillSection) return;

  const observerOptions = {
    threshold: 0.3,
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        skillBars.forEach((bar, index) => {
          const targetWidth = bar.parentElement.parentElement
            .querySelector('.skill-percent')
            .textContent.match(/\d+/)[0];
          animateSkillBar(bar, targetWidth);
        });
        observer.unobserve(skillSection);
      }
    });
  }, observerOptions);

  observer.observe(skillSection);
}

function animateSkillBar(bar, targetWidth) {
  let currentWidth = 0;
  const increment = parseInt(targetWidth) / 20;

  const interval = setInterval(() => {
    currentWidth += increment;
    if (currentWidth >= parseInt(targetWidth)) {
      currentWidth = parseInt(targetWidth);
      clearInterval(interval);
    }
    bar.style.width = currentWidth + '%';
  }, 50);
}

/* ========================================
   FORM SUBMISSION
   ======================================== */

function initializeFormSubmission() {
  const form = document.querySelector('.contact-form');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    // Get form data
    const name = form.querySelector('input[name="name"]');
    const email = form.querySelector('input[name="email"]');
    const message = form.querySelector('textarea[name="message"]');

    // Validate
    if (!name.value || !email.value || !message.value) {
      alert('Please fill all fields');
      return;
    }

    // Show success message
    const formSubmit = form.querySelector('.form-submit');
    const originalText = formSubmit.textContent;
    formSubmit.textContent = 'Message Sent! ✓';
    formSubmit.disabled = true;

    // Reset form
    setTimeout(() => {
      form.reset();
      formSubmit.textContent = originalText;
      formSubmit.disabled = false;
    }, 2000);
  });
}

/* ========================================
   SMOOTH SCROLLING
   ======================================== */

document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    if (href === '#') return;

    e.preventDefault();
    const target = document.querySelector(href);
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start',
      });
    }
  });
});

/* ========================================
   PROJECT DETAIL PAGE
   ======================================== */

// Handle project detail routing
function loadProjectDetail(projectId) {
  // Mock project data (in real app, fetch from API)
  const projects = {
    'project-1': {
      title: 'AWS Call Transcription & Sentiment Analysis',
      category: 'AWS + NLP',
      icon: '🎯',
      image: '📊',
      overview:
        'Dockerized AWS Lambda pipeline that transcribes calls with Whisper, separates agent/customer speech, scores sentiment with VADER.',
      problem:
        'The central challenge is to process noisy customer-care recordings at scale while preserving speaker separation, sentiment context.',
      methodology: [
        'Audio ingestion from S3',
        'Transcription with Whisper ASR',
        'Speaker diarization',
        'Sentiment analysis with VADER',
        'Results stored in DynamoDB',
      ],
      technologies: [
        'AWS Lambda',
        'Whisper ASR',
        'Python',
        'Docker',
        'DynamoDB',
      ],
      metrics: [
        { label: 'Transcription Accuracy', value: '94%' },
        { label: 'Processing Speed', value: '2.5x' },
        { label: 'Cost Reduction', value: '60%' },
        { label: 'User Satisfaction', value: '9.2/10' },
      ],
    },
    'project-2': {
      title: 'Computer Vision Sign Language Detection',
      category: 'Computer Vision',
      icon: '👁️',
      image: '🖼️',
      overview:
        'CNN-based real-time ASL gesture detection with OpenCV preprocessing and a user-friendly interface.',
      problem:
        'The challenge is to classify visual patterns that vary by angle, lighting, and framing while keeping inference fast.',
      methodology: [
        'Frame capture and normalization',
        'CNN feature extraction',
        'Real-time classification',
        'Interactive GUI interface',
      ],
      technologies: ['TensorFlow', 'OpenCV', 'Python', 'CNN'],
      metrics: [
        { label: 'Recognition Accuracy', value: '92%' },
        { label: 'Inference Speed', value: '30fps' },
        { label: 'Training Time', value: '4hrs' },
        { label: 'Model Size', value: '45MB' },
      ],
    },
  };

  const project = projects[projectId] || projects['project-1'];

  // Populate project detail
  const detailPage = document.querySelector('.project-detail');
  if (!detailPage) return;

  const detailHTML = `
    <div class="detail-hero">${project.image}</div>
    
    <div class="detail-section">
      <h3>Project Overview</h3>
      <p class="detail-content">${project.overview}</p>
    </div>

    <div class="detail-section">
      <h3>Problem Statement</h3>
      <p class="detail-content">${project.problem}</p>
    </div>

    <div class="detail-section">
      <h3>Methodology</h3>
      <div class="detail-grid">
        ${project.methodology.map((item) => `<div class="detail-item"><p class="detail-item-text">• ${item}</p></div>`).join('')}
      </div>
    </div>

    <div class="detail-section">
      <h3>Technologies Used</h3>
      <div class="detail-grid">
        ${project.technologies.map((tech) => `<div class="detail-item"><p class="detail-item-title">${tech}</p></div>`).join('')}
      </div>
    </div>

    <div class="detail-section">
      <h3>Results & Metrics</h3>
      <div class="metrics">
        ${project.metrics.map((metric) => `<div class="metric-card"><div class="metric-value">${metric.value}</div><div class="metric-label">${metric.label}</div></div>`).join('')}
      </div>
    </div>
  `;

  // Clear existing content and add new
  const mainContent = detailPage.querySelector('main') || detailPage;
  mainContent.innerHTML = detailHTML;

  // Re-initialize animations
  initializeScrollAnimations();
}

// Auto-load project detail if on project detail page
document.addEventListener('DOMContentLoaded', () => {
  if (document.querySelector('.project-detail')) {
    const projectId = new URLSearchParams(window.location.search).get('id');
    if (projectId) {
      loadProjectDetail(projectId);
    }
  }
});

/* ========================================
   UTILITY FUNCTIONS
   ======================================== */

// Smooth page transitions
function navigateTo(page) {
  const url = page + '.html';
  window.location.href = url;
}

// Animate counter numbers
function animateCounter(element, target, duration = 2000) {
  let current = 0;
  const increment = target / (duration / 16);

  const interval = setInterval(() => {
    current += increment;
    if (current >= target) {
      current = target;
      clearInterval(interval);
    }
    element.textContent = Math.floor(current);
  }, 16);
}

// Ripple effect on buttons
document.querySelectorAll('.btn').forEach((button) => {
  button.addEventListener('click', function (e) {
    const ripple = document.createElement('span');
    const rect = this.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;

    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    ripple.style.position = 'absolute';
    ripple.style.borderRadius = '50%';
    ripple.style.background = 'rgba(255, 255, 255, 0.5)';
    ripple.style.pointerEvents = 'none';
    ripple.style.animation = 'ripple 0.6s ease-out';

    this.style.position = 'relative';
    this.style.overflow = 'hidden';
    this.appendChild(ripple);

    setTimeout(() => ripple.remove(), 600);
  });
});

// Add ripple animation
const style = document.createElement('style');
style.textContent = `
  @keyframes ripple {
    to {
      transform: scale(4);
      opacity: 0;
    }
  }
`;
document.head.appendChild(style);

// Export functions for use in HTML
window.navigateTo = navigateTo;
window.loadProjectDetail = loadProjectDetail;
window.animateCounter = animateCounter;
