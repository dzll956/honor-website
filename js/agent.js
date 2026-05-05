class ParticleSystem {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;
        
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.animationId = null;
        this.mouse = { x: null, y: null };
        
        this.init();
    }

    init() {
        this.resizeCanvas();
        this.bindEvents();
        this.createParticles();
        this.animate();
    }

    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    bindEvents() {
        window.addEventListener('resize', () => {
            this.resizeCanvas();
            this.createParticles();
        });

        this.canvas.addEventListener('mousemove', (e) => {
            this.mouse.x = e.clientX;
            this.mouse.y = e.clientY;
        });

        this.canvas.addEventListener('mouseleave', () => {
            this.mouse.x = null;
            this.mouse.y = null;
        });
    }

    createParticles() {
        this.particles = [];
        const particleCount = Math.min(80, Math.floor(window.innerWidth * window.innerHeight / 15000));
        
        for (let i = 0; i < particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                size: Math.random() * 2 + 0.5,
                speedX: (Math.random() - 0.5) * 0.4,
                speedY: (Math.random() - 0.5) * 0.4,
                opacity: Math.random() * 0.5 + 0.2,
                color: Math.random() > 0.5 ? '0, 212, 255' : '168, 85, 247'
            });
        }
    }

    update() {
        this.particles.forEach(particle => {
            particle.x += particle.speedX;
            particle.y += particle.speedY;

            if (this.mouse.x !== null && this.mouse.y !== null) {
                const dx = particle.x - this.mouse.x;
                const dy = particle.y - this.mouse.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < 100) {
                    const force = (100 - distance) / 100;
                    particle.x += dx * force * 0.02;
                    particle.y += dy * force * 0.02;
                }
            }

            if (particle.x < 0 || particle.x > this.canvas.width) particle.speedX *= -1;
            if (particle.y < 0 || particle.y > this.canvas.height) particle.speedY *= -1;
            
            particle.x = Math.max(0, Math.min(this.canvas.width, particle.x));
            particle.y = Math.max(0, Math.min(this.canvas.height, particle.y));
        });
    }

    draw() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        this.particles.forEach(particle => {
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(${particle.color}, ${particle.opacity})`;
            this.ctx.fill();
        });

        this.drawConnections();
    }

    drawConnections() {
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const dx = this.particles[i].x - this.particles[j].x;
                const dy = this.particles[i].y - this.particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 120) {
                    const opacity = 0.15 * (1 - distance / 120);
                    this.ctx.beginPath();
                    this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
                    this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
                    this.ctx.strokeStyle = `rgba(0, 212, 255, ${opacity})`;
                    this.ctx.lineWidth = 0.5;
                    this.ctx.stroke();
                }
            }
        }
    }

    animate() {
        this.update();
        this.draw();
        this.animationId = requestAnimationFrame(() => this.animate());
    }

    destroy() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
    }
}

class ChatDemo {
    constructor() {
        this.chatArea = document.getElementById('chatArea');
        this.chatInput = document.getElementById('chatInput');
        this.sendBtn = document.getElementById('sendBtn');
        
        if (!this.chatArea) return;
        
        this.responses = {
            '你好': '你好！很高兴见到你。我是 AI Agent，有什么我可以帮助你的吗？',
            '你好呀': '你好呀！😊 有什么我可以帮助你的吗？',
            'hello': 'Hello! I am an AI Agent. How can I assist you today?',
            'hi': 'Hi there! How can I help you today?',
            '什么是agent': 'Agent（智能代理）是一种能够自主感知环境、做出决策并执行行动的智能系统。它具备自主性、反应性、主动性和社会性等特征。',
            '什么是智能代理': 'Agent（智能代理）是一种能够自主感知环境、做出决策并执行行动的智能系统。它具备自主性、反应性、主动性和社会性等特征。',
            'agent是什么': 'Agent（智能代理）是一种能够自主感知环境、做出决策并执行行动的智能系统。它具备自主性、反应性、主动性和社会性等特征。',
            '你能做什么': '我可以帮你：\n\n1. 解答各类问题\n2. 分析和处理数据\n3. 协助编写代码\n4. 制定计划和方案\n5. 提供学习建议\n6. 进行创意写作',
            '帮助': '我可以帮助你完成多种任务！比如：\n\n• 回答问题和解释概念\n• 协助编程和代码调试\n• 制定旅行计划\n• 写作和内容创作\n• 数据分析和整理\n\n有什么具体需求吗？',
            '帮我写代码': '当然可以！请告诉我：\n\n1. 你需要什么编程语言？（Python、JavaScript、Java等）\n2. 具体的功能需求是什么？\n\n我会为你编写完整的代码示例！',
            '谢谢': '不客气！很高兴能帮到你。如果还有其他问题，随时告诉我！',
            '谢谢你': '不客气！很高兴能帮到你。如果还有其他问题，随时告诉我！',
            '再见': '再见！👋 祝你有个愉快的一天，有需要随时来找我！',
            'bye': 'Bye! Have a great day! Feel free to come back anytime!',
            'bye bye': 'Bye! Have a great day! Feel free to come back anytime!',
            '你会取代人类吗': '这是一个很有深度的问题！AI Agent 是为了增强人类能力而设计的，而不是取代人类。我们擅长处理重复性任务和信息检索，但人类的创造力、情感智慧和道德判断是无可替代的。',
            '人工智能': '人工智能（AI）是当前最具变革性的技术之一。它正在改变我们的生活和工作方式。从智能助手到自动驾驶，从医疗诊断到艺术创作，AI 正在各个领域展现出巨大潜力。',
            '机器学习': '机器学习是人工智能的一个分支，它让计算机能够从数据中学习并改进。通过机器学习，计算机可以识别模式、做出预测，并随着时间推移不断提升性能。'
        };
        
        this.init();
    }

    init() {
        this.sendBtn.addEventListener('click', () => this.handleSend());
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleSend();
        });
    }

    addMessage(text, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-message';
        messageDiv.innerHTML = `
            <div class="chat-avatar ${isUser ? 'user' : 'agent'}">${isUser ? '👤' : '🤖'}</div>
            <div class="chat-bubble ${isUser ? '' : 'agent-bubble'}">${this.formatText(text)}</div>
        `;
        this.chatArea.appendChild(messageDiv);
        this.scrollToBottom();
    }

    formatText(text) {
        return text.replace(/\n/g, '<br>');
    }

    scrollToBottom() {
        this.chatArea.scrollTop = this.chatArea.scrollHeight;
    }

    showTyping() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'chat-message';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = `
            <div class="chat-avatar agent">🤖</div>
            <div class="chat-bubble agent-bubble">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `;
        this.chatArea.appendChild(typingDiv);
        this.scrollToBottom();
    }

    hideTyping() {
        const typing = document.getElementById('typingIndicator');
        if (typing) typing.remove();
    }

    getResponse(input) {
        const lowerInput = input.toLowerCase().trim();
        
        for (const [key, value] of Object.entries(this.responses)) {
            if (lowerInput.includes(key.toLowerCase())) {
                return value;
            }
        }
        
        return '这是一个很好的问题！作为 AI Agent，我正在不断学习和进化中。你可以尝试问我：\n\n• "什么是Agent"\n• "你能做什么"\n• "人工智能"\n\n来了解更多！';
    }

    handleSend() {
        const text = this.chatInput.value.trim();
        if (!text) return;

        this.addMessage(text, true);
        this.chatInput.value = '';
        this.showTyping();

        const delay = 1500 + Math.random() * 1000;
        setTimeout(() => {
            this.hideTyping();
            const response = this.getResponse(text);
            this.addMessage(response);
        }, delay);
    }
}

class ScrollAnimator {
    constructor() {
        this.fadeElements = document.querySelectorAll('.fade-in, .fade-in-left, .fade-in-right');
        if (this.fadeElements.length === 0) return;
        
        this.init();
    }

    init() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, { 
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        this.fadeElements.forEach(el => observer.observe(el));
    }
}

class Navigation {
    constructor() {
        this.nav = document.querySelector('nav');
        this.backToTop = document.getElementById('backToTop');
        this.mobileMenuBtn = document.querySelector('.mobile-menu-btn');
        this.mobileNav = document.querySelector('.mobile-nav');
        
        if (!this.nav) return;
        
        this.init();
    }

    init() {
        window.addEventListener('scroll', () => this.handleScroll());
        this.backToTop?.addEventListener('click', () => this.scrollToTop());
        this.mobileMenuBtn?.addEventListener('click', () => this.toggleMobileMenu());
        
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => this.handleSmoothScroll(e));
        });

        document.querySelectorAll('.mobile-nav a').forEach(anchor => {
            anchor.addEventListener('click', () => this.closeMobileMenu());
        });
    }

    handleScroll() {
        if (window.scrollY > 50) {
            this.nav.classList.add('scrolled');
        } else {
            this.nav.classList.remove('scrolled');
        }

        if (this.backToTop) {
            if (window.scrollY > 500) {
                this.backToTop.classList.add('visible');
            } else {
                this.backToTop.classList.remove('visible');
            }
        }
    }

    scrollToTop() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    handleSmoothScroll(e) {
        const href = e.currentTarget.getAttribute('href');
        if (href === '#') return;
        
        const target = document.querySelector(href);
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            this.closeMobileMenu();
        }
    }

    toggleMobileMenu() {
        this.mobileMenuBtn?.classList.toggle('active');
        this.mobileNav?.classList.toggle('active');
        document.body.style.overflow = this.mobileNav?.classList.contains('active') ? 'hidden' : '';
    }

    closeMobileMenu() {
        this.mobileMenuBtn?.classList.remove('active');
        this.mobileNav?.classList.remove('active');
        document.body.style.overflow = '';
    }
}

class App {
    constructor() {
        this.particleSystem = null;
        this.chatDemo = null;
        this.scrollAnimator = null;
        this.navigation = null;
        
        this.init();
    }

    init() {
        document.addEventListener('DOMContentLoaded', () => {
            this.particleSystem = new ParticleSystem('particle-canvas');
            this.chatDemo = new ChatDemo();
            this.scrollAnimator = new ScrollAnimator();
            this.navigation = new Navigation();
        });
    }

    destroy() {
        this.particleSystem?.destroy();
    }
}

const app = new App();

window.addEventListener('beforeunload', () => {
    app.destroy();
});
