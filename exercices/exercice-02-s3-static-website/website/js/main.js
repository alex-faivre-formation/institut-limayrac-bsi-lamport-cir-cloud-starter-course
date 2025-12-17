/**
 * AWS Basics Course - Main JavaScript
 * Handles theme toggle, smooth scrolling, and quiz functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    initTheme();
    initSmoothScroll();
    initMobileMenu();
});

/**
 * Theme Management
 */
function initTheme() {
    const themeToggle = document.getElementById('theme-toggle');
    const html = document.documentElement;
    
    // Check for saved theme preference or default to dark
    const savedTheme = localStorage.getItem('theme') || 'dark';
    html.classList.toggle('dark', savedTheme === 'dark');
    
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            html.classList.toggle('dark');
            const isDark = html.classList.contains('dark');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        });
    }
}

/**
 * Smooth Scrolling for anchor links
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * Mobile Menu Toggle (if needed)
 */
function initMobileMenu() {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
}

/**
 * Quiz Functionality
 */
function checkAnswers() {
    const answers = {
        q1: 'b', // S3
        q2: 'b', // Route vers IGW
        q3: 'a'  // Lambda
    };
    
    let score = 0;
    let total = Object.keys(answers).length;
    
    for (const [question, correctAnswer] of Object.entries(answers)) {
        const selected = document.querySelector(`input[name="${question}"]:checked`);
        if (selected && selected.value === correctAnswer) {
            score++;
        }
    }
    
    const resultDiv = document.getElementById('quiz-result');
    resultDiv.classList.remove('hidden');
    
    if (score === total) {
        resultDiv.className = 'mt-8 p-6 rounded-2xl text-center bg-green-100 dark:bg-green-900/30 border border-green-500';
        resultDiv.innerHTML = `
            <div class="text-4xl mb-4">🎉</div>
            <h3 class="text-2xl font-bold text-green-700 dark:text-green-400 mb-2">Excellent !</h3>
            <p class="text-green-600 dark:text-green-300">Vous avez obtenu ${score}/${total} ! Vous maîtrisez les bases d'AWS.</p>
        `;
    } else if (score >= total / 2) {
        resultDiv.className = 'mt-8 p-6 rounded-2xl text-center bg-yellow-100 dark:bg-yellow-900/30 border border-yellow-500';
        resultDiv.innerHTML = `
            <div class="text-4xl mb-4">👍</div>
            <h3 class="text-2xl font-bold text-yellow-700 dark:text-yellow-400 mb-2">Pas mal !</h3>
            <p class="text-yellow-600 dark:text-yellow-300">Vous avez obtenu ${score}/${total}. Relisez les sections pour améliorer votre score.</p>
        `;
    } else {
        resultDiv.className = 'mt-8 p-6 rounded-2xl text-center bg-red-100 dark:bg-red-900/30 border border-red-500';
        resultDiv.innerHTML = `
            <div class="text-4xl mb-4">📚</div>
            <h3 class="text-2xl font-bold text-red-700 dark:text-red-400 mb-2">Continuez d'apprendre !</h3>
            <p class="text-red-600 dark:text-red-300">Vous avez obtenu ${score}/${total}. Prenez le temps de revoir chaque section.</p>
        `;
    }
    
    // Scroll to result
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

/**
 * Intersection Observer for scroll animations
 */
function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fadeIn');
            }
        });
    }, {
        threshold: 0.1
    });
    
    document.querySelectorAll('section').forEach(section => {
        observer.observe(section);
    });
}

// Initialize scroll animations
if ('IntersectionObserver' in window) {
    initScrollAnimations();
}
