
    /* ─── Mobile Menu ─── */
    function toggleMenu() {
        const menu = document.getElementById('mobile-menu');
        const icon = document.getElementById('hamburger-icon');
        const isOpen = menu.classList.toggle('open');
        icon.textContent = isOpen ? 'close' : 'menu';
        document.getElementById('hamburger').setAttribute('aria-expanded', isOpen);
    }
    function closeMenu() {
        const menu = document.getElementById('mobile-menu');
        const icon = document.getElementById('hamburger-icon');
        menu.classList.remove('open');
        icon.textContent = 'menu';
        document.getElementById('hamburger').setAttribute('aria-expanded', 'false');
    }
    var hb=document.getElementById('hamburger'); if(hb) hb.addEventListener('click', toggleMenu);

    /* ─── Nav scroll compact ─── */
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        navbar.classList.toggle('scrolled', window.scrollY > 60);
    }, { passive: true });

    /* ─── Nav active state on scroll ─── */
    const navLinks = document.querySelectorAll('nav a.nav-link');
    const sections = ['solutions', 'about', 'contact', 'pourquoi'];

    function setActiveNav(id) {
        navLinks.forEach(link => {
            const href = link.getAttribute('href').replace('#', '');
            const span = link.querySelector('span');
            if (href === id || (id === '' && href === '')) {
                if (span) span.style.width = '100%';
                link.classList.add('text-secondary');
                link.classList.remove('text-white');
            } else {
                if (span) span.style.width = '';
                link.classList.remove('text-secondary');
                link.classList.add('text-white');
            }
        });
    }

    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                setActiveNav(entry.target.id);
            }
        });
    }, { threshold: 0.15, rootMargin: '-80px 0px -50% 0px' });

    sections.forEach(id => {
        const el = document.getElementById(id);
        if (el) sectionObserver.observe(el);
    });

    // Accueil actif quand en haut
    window.addEventListener('scroll', () => {
        if (window.scrollY < 200) setActiveNav('');
    }, { passive: true });

    // Active state on click immediately
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            const id = link.getAttribute('href').replace('#', '');
            setActiveNav(id);
        });
    });

    /* ─── Scroll Reveal ─── */
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12 });

    document.querySelectorAll('.reveal, .reveal-left, .reveal-right').forEach(el => {
        revealObserver.observe(el);
    });

    /* ─── Counter Animation ───
       Le texte des compteurs (15+, 500+…) n'est jamais modifié : robots et lecteurs
       d'écran lisent toujours la valeur réelle. L'animation est purement visuelle
       (pseudo-élément alimenté par data-count, voir .counter.is-counting). */
    function setCount(el, value) {
        el.dataset.count = value + (el.dataset.suffix || '');
    }

    function animateCounter(el) {
        const target = parseInt(el.dataset.target, 10);
        const duration = 1800;
        const startTime = performance.now();

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            // Ease out cubic
            const ease = 1 - Math.pow(1 - progress, 3);
            setCount(el, Math.round(ease * target));
            if (progress < 1) requestAnimationFrame(update);
            else el.classList.remove('is-counting');
        }
        requestAnimationFrame(update);
        // Filet de sécurité si requestAnimationFrame est suspendu (onglet en arrière-plan)
        setTimeout(() => el.classList.remove('is-counting'), duration + 200);
    }

    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                counterObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    // Prépare l'animation (affichage de 0) quand le compteur arrive à moins d'un demi-écran sous la ligne de flottaison
    const counterArmObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            counterArmObserver.unobserve(entry.target);
            const box = entry.boundingClientRect;
            if (box.top < window.innerHeight && box.bottom > 0) return; // déjà à l'écran : pas d'animation
            setCount(entry.target, 0);
            entry.target.classList.add('is-counting');
            counterObserver.observe(entry.target);
        });
    }, { rootMargin: '0px 0px 50% 0px' });

    if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        document.querySelectorAll('.counter').forEach(el => {
            counterArmObserver.observe(el);
        });
    }

    /* ─── Formulaire de contact (envoi vers contact.php, hébergement OVH) ─── */
    (function () {
        const form = document.getElementById('contact-form');
        if (!form) return;
        const btn = document.getElementById('cf-submit');
        const label = document.getElementById('cf-btn-label');
        const spinner = document.getElementById('cf-spinner');
        const feedback = document.getElementById('cf-feedback');
        const started = Date.now();

        function setLoading(on) {
            btn.disabled = on;
            spinner.classList.toggle('hidden', !on);
            label.textContent = on ? 'Envoi en cours…' : 'Envoyer la demande';
        }
        function showFeedback(ok, msg) {
            feedback.className = 'rounded-[20px] p-4 text-sm font-body font-semibold ' + (ok ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800');
            feedback.textContent = msg;
            feedback.classList.remove('hidden');
            feedback.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
        form.addEventListener('submit', async function (e) {
            e.preventDefault();
            feedback.classList.add('hidden');
            const first = document.getElementById('cf-name').value.trim();
            const last = document.getElementById('cf-lastname').value.trim();
            const name = (first + ' ' + last).trim();
            const email = document.getElementById('cf-email').value.trim();
            if (!first) { showFeedback(false, 'Merci d\'indiquer votre prénom.'); return; }
            if (!last) { showFeedback(false, 'Merci d\'indiquer votre nom.'); return; }
            if (!email) { showFeedback(false, 'Merci de renseigner votre adresse e-mail.'); return; }
            if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { showFeedback(false, 'Merci de vérifier votre adresse e-mail.'); return; }
            if (!document.getElementById('cf-consent').checked) { showFeedback(false, 'Merci de cocher la case de consentement pour que nous puissions vous recontacter.'); return; }
            setLoading(true);
            try {
                const res = await fetch('/contact.php', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        name, email,
                        phone: document.getElementById('cf-phone').value.trim(),
                        request_type: document.getElementById('cf-type').value,
                        message: document.getElementById('cf-message').value.trim(),
                        website: document.getElementById('cf-website').value,
                        consent: true,
                        elapsed: Date.now() - started
                    })
                });
                const data = await res.json();
                if (data.ok) { showFeedback(true, 'Votre demande a bien été envoyée. Nous vous recontacterons rapidement.'); form.reset(); }
                else { showFeedback(false, data.error || 'Une erreur est survenue, veuillez réessayer.'); }
            } catch (err) {
                showFeedback(false, 'Impossible de joindre le serveur. Écrivez-nous à contact@cabinet-valorys.com ou appelez le 06 69 94 56 08.');
            } finally { setLoading(false); }
        });
    })();

    /* ─── Onglets du formulaire : rappel / message ─── */
    (function () {
        const tabs = document.querySelectorAll('.v-tabs [data-tab]');
        if (!tabs.length) return;
        function show(name) {
            tabs.forEach(t => t.setAttribute('aria-selected', String(t.dataset.tab === name)));
            document.querySelectorAll('[data-panel]').forEach(p => { p.hidden = p.dataset.panel !== name; });
        }
        tabs.forEach(t => t.addEventListener('click', () => show(t.dataset.tab)));
        document.querySelectorAll('[data-open-tab]').forEach(a => a.addEventListener('click', () => show(a.dataset.openTab)));
    })();

    /* ─── Formulaire « Être rappelé » ─── */
    (function () {
        const form = document.getElementById('callback-form');
        if (!form) return;
        const btn = document.getElementById('cb-submit');
        const label = document.getElementById('cb-btn-label');
        const feedback = document.getElementById('cb-feedback');
        const started = Date.now();
        function show(ok, msg) {
            feedback.className = 'rounded-[20px] p-4 text-sm font-body font-semibold ' + (ok ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800');
            feedback.textContent = msg; feedback.classList.remove('hidden');
        }
        form.addEventListener('submit', async function (e) {
            e.preventDefault();
            feedback.classList.add('hidden');
            const first = document.getElementById('cb-name').value.trim();
            const last = document.getElementById('cb-lastname').value.trim();
            const name = (first + ' ' + last).trim();
            const phone = document.getElementById('cb-phone').value.trim();
            if (!first) { show(false, 'Merci d\'indiquer votre prénom.'); return; }
            if (!last) { show(false, 'Merci d\'indiquer votre nom.'); return; }
            if (phone.replace(/\D/g, '').length < 9) { show(false, 'Merci de vérifier votre numéro de téléphone.'); return; }
            if (!document.getElementById('cb-consent').checked) { show(false, 'Merci de cocher la case pour que nous puissions vous rappeler.'); return; }
            const slot = (form.querySelector('input[name=slot]:checked') || {}).value || '';
            btn.disabled = true; label.textContent = 'Envoi en cours…';
            try {
                const res = await fetch('/contact.php', {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ callback: true, name, phone, slot, request_type: document.getElementById('cb-type').value,
                        website: document.getElementById('cb-website').value, consent: true, elapsed: Date.now() - started })
                });
                const data = await res.json();
                if (data.ok) { show(true, 'C\'est noté : nous vous rappelons sur le créneau choisi.'); form.reset(); }
                else show(false, data.error || 'Une erreur est survenue, veuillez réessayer.');
            } catch (err) {
                show(false, 'Impossible de joindre le serveur. Appelez-nous directement au 06 69 94 56 08.');
            } finally { btn.disabled = false; label.textContent = 'Me faire rappeler'; }
        });
    })();
