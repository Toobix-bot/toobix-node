const API_BASE = localStorage.getItem('toobix-api-base') || 'http://localhost:8000';
const TOKEN_KEY = 'toobix-api-token';
let tokenPromptOpen = false;

function getApiToken() {
    return sessionStorage.getItem(TOKEN_KEY) || '';
}

function requestApiToken() {
    if (tokenPromptOpen) return '';
    tokenPromptOpen = true;
    const token = window.prompt(
        'Dieser Node verlangt einen API-Schlüssel. Er wird nur für diese Browser-Sitzung gespeichert.'
    );
    tokenPromptOpen = false;
    if (token) sessionStorage.setItem(TOKEN_KEY, token.trim());
    return token?.trim() || '';
}

window.clearToobixApiToken = () => sessionStorage.removeItem(TOKEN_KEY);

function apiHeaders(hasBody = false) {
    const headers = {};
    if (hasBody) headers['Content-Type'] = 'application/json';
    const token = getApiToken();
    if (token) headers.Authorization = `Bearer ${token}`;
    return headers;
}

async function apiFetch(endpoint, options = {}, retryOnUnauthorized = true) {
    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), 5000);
    const hasBody = options.body !== undefined;

    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            ...options,
            mode: 'cors',
            headers: { ...apiHeaders(hasBody), ...(options.headers || {}) },
            signal: controller.signal,
        });

        if (response.status === 401 && retryOnUnauthorized) {
            if (requestApiToken()) return apiFetch(endpoint, options, false);
        }
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        setConnectionStatus(true);
        return await response.json();
    } catch (error) {
        console.warn(`API ${endpoint}:`, error.message);
        setConnectionStatus(false);
        return null;
    } finally {
        window.clearTimeout(timeout);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    initScrollEffects();
    initNavHighlight();
    initForm();
    refreshAll();
    window.setInterval(refreshAll, 30000);
});

function initScrollEffects() {
    const header = document.getElementById('mainHeader');
    if (!header) return;
    window.addEventListener('scroll', () => {
        header.classList.toggle('scrolled', window.scrollY > 50);
    });
}

function initNavHighlight() {
    const links = document.querySelectorAll('.nav-link');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            links.forEach((link) => link.classList.remove('active'));
            document.querySelector(`.nav-link[href="#${entry.target.id}"]`)?.classList.add('active');
        });
    }, { threshold: 0.25 });
    document.querySelectorAll('section[id]').forEach((section) => observer.observe(section));
}

function setConnectionStatus(online) {
    const dot = document.querySelector('.status-dot');
    const text = document.querySelector('.status-text');
    if (dot && text) {
        dot.className = `status-dot ${online ? 'online' : 'offline'}`;
        text.textContent = online ? 'Node verbunden' : 'Keine Verbindung';
    }

    // Toggle local node view
    const localNodeView = document.getElementById('local-node-view');
    if (localNodeView) {
        if (online) {
            localNodeView.style.display = 'block';
        } else {
            localNodeView.style.display = 'none';
        }
    }
}

async function refreshAll() {
    const button = document.getElementById('btnRefresh');
    if (button) {
        button.disabled = true;
        button.textContent = '↻ Lädt...';
    }

    await Promise.all([
        loadHealth(),
        loadReflection(),
        loadPeerAwareness(),
        loadScarcity(),
        loadAbundance(),
    ]);

    if (button) {
        button.disabled = false;
        button.textContent = '↻ Aktualisieren';
    }
}

async function loadHealth() {
    const element = document.getElementById('healthBody');
    const data = await apiFetch('/api/health', {}, false);
    if (!element) return;
    element.innerHTML = data
        ? `<div class="status-badge online">● Online</div><p>${escapeHtml(data.node_id || 'Toobix Node')}</p>`
        : '<div class="no-data">Backend nicht erreichbar. Starte es mit <code>python3 -m app.main</code>.</div>';
}

async function loadReflection() {
    const body = document.getElementById('reflectionBody');
    const harmony = document.getElementById('harmonyBody');
    const data = await apiFetch('/api/reflection');
    if (!body || !harmony) return;

    if (!data) {
        body.innerHTML = '<div class="no-data">Keine Reflexionsdaten verfügbar</div>';
        harmony.innerHTML = '<div class="no-data">--</div>';
        return;
    }

    const needs = (data.mangel || []).map((item) => `<div class="reflection-item mangel">🔴 ${escapeHtml(item)}</div>`).join('');
    const offers = (data.ueberfluss || []).map((item) => `<div class="reflection-item ueberfluss">🟢 ${escapeHtml(item)}</div>`).join('');
    body.innerHTML = `
        <div class="reflection-grid">
            <div class="reflection-col mangel"><h4>Technische Bedarfe</h4>${needs || '<div class="no-data">Keine erkannt</div>'}</div>
            <div class="reflection-col ueberfluss"><h4>Technische Kapazitäten</h4>${offers || '<div class="no-data">Keine erkannt</div>'}</div>
        </div>
        <p>${escapeHtml(data.status_summary || '')}</p>`;

    const score = Math.max(0, Math.min(1, Number(data.harmony_score) || 0));
    const percent = Math.round(score * 100);
    harmony.innerHTML = `<div class="harmony-meter"><span class="harmony-score">${percent}%</span><div class="harmony-bar"><div class="harmony-fill" style="width:${percent}%"></div></div><span class="harmony-label">Technischer Balancewert</span></div>`;
    const stat = document.getElementById('statHarmony');
    if (stat) stat.textContent = `${percent}%`;
}

async function loadPeerAwareness() {
    const peerBody = document.getElementById('peerBody');
    const logBody = document.getElementById('praiseBody');
    const data = await apiFetch('/api/peers/awareness');
    if (!peerBody || !logBody) return;

    if (!data) {
        peerBody.innerHTML = '<div class="no-data">Keine Peer-Daten verfügbar</div>';
        logBody.innerHTML = '<div class="no-data">Keine technischen Prüfungen verfügbar</div>';
        return;
    }

    const peers = data.peers || {};
    const summary = data.network_awareness_summary || {};
    const peerEntries = Object.entries(peers);
    const nodeStat = document.getElementById('statNodes');
    if (nodeStat) nodeStat.textContent = String(peerEntries.length + 1);

    peerBody.innerHTML = peerEntries.length
        ? peerEntries.map(([url, info]) => `
            <div class="peer-item">
                <div class="peer-avatar">⬡</div>
                <div class="peer-info"><strong>${escapeHtml(url)}</strong><div>${escapeHtml(info.health || 'unknown')} · ${Number(info.last_response_time_ms || 0).toFixed(1)} ms</div></div>
            </div>`).join('')
        : '<div class="no-data">Noch keine Peers verbunden.</div>';

    const history = data.history || [];
    logBody.innerHTML = history.length
        ? history.slice(-20).reverse().map((item) => `<div class="praise-item ${escapeHtml(item.type || '')}"><span>⚙️</span><span class="praise-reason">${escapeHtml(item.reason || '')}</span></div>`).join('')
        : `<div class="no-data">Netzwerkstatus: ${escapeHtml(summary.overall_status || 'idle')}</div>`;
}

function renderEntries(entries, targetId, icon) {
    const element = document.getElementById(targetId);
    if (!element) return;
    element.innerHTML = entries.length
        ? entries.map((entry) => `
            <article class="entry-item">
                <h5>${icon} ${escapeHtml(entry.title || 'Ohne Titel')}</h5>
                <p>${escapeHtml(entry.description || '')}</p>
                <div class="entry-meta"><span>📁 ${escapeHtml(entry.category || 'Allgemein')}</span><span>📍 ${escapeHtml(entry.location || 'Nicht angegeben')}</span></div>
            </article>`).join('')
        : '<div class="no-data">Keine Einträge vorhanden</div>';
}

async function loadScarcity() {
    const data = await apiFetch('/api/scarcity');
    const entries = Array.isArray(data) ? data : [];
    renderEntries(entries, 'scarcityList', '🔴');
    const stat = document.getElementById('statNeeds');
    if (stat) stat.textContent = String(entries.length);
}

async function loadAbundance() {
    const data = await apiFetch('/api/abundance');
    const entries = Array.isArray(data) ? data : [];
    renderEntries(entries, 'abundanceList', '🟢');
    const stat = document.getElementById('statOffers');
    if (stat) stat.textContent = String(entries.length);

    const grid = document.getElementById('solidarityGrid');
    if (!grid) return;
    const seeded = entries.filter((entry) => Array.isArray(entry.tags) && entry.tags.includes('solidarity_offer'));
    grid.innerHTML = seeded.length
        ? seeded.map((entry) => `
            <article class="solidarity-card">
                <h4>${escapeHtml(entry.title || 'Hilfsangebot')}</h4>
                <p>${escapeHtml(entry.description || '')}</p>
                <p><strong>Vor Nutzung Aktualität und Zuständigkeit prüfen.</strong></p>
                <div>📍 ${escapeHtml(entry.location || '')}</div>
                ${entry.contact ? `<div>Kontakt: ${escapeHtml(entry.contact)}</div>` : ''}
            </article>`).join('')
        : '<div class="no-data">Keine geprüften Seed-Einträge geladen.</div>';
}

function initForm() {
    const form = document.getElementById('entryForm');
    if (!form) return;

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const feedback = document.getElementById('formFeedback');
        const type = document.getElementById('entryType').value;
        const endpoint = type === 'scarcity' ? '/api/scarcity' : '/api/abundance';
        const payload = {
            title: document.getElementById('entryTitle').value.trim(),
            category: document.getElementById('entryCategory').value,
            description: document.getElementById('entryDesc').value.trim(),
            location: document.getElementById('entryLocation').value.trim(),
            contact: document.getElementById('entryContact').value.trim(),
        };

        if (!payload.title || !payload.description) return;
        if (feedback) feedback.textContent = 'Speichere lokal und synchronisiere gegebenenfalls mit verbundenen Peers…';

        const result = await apiFetch(endpoint, {
            method: 'POST',
            body: JSON.stringify(payload),
        });

        if (result) {
            form.reset();
            if (feedback) feedback.textContent = 'Eintrag gespeichert. Keine vertraulichen Daten veröffentlichen.';
            await Promise.all([loadScarcity(), loadAbundance()]);
        } else if (feedback) {
            feedback.textContent = 'Speichern fehlgeschlagen. Verbindung und API-Schlüssel prüfen.';
        }
    });
}

function escapeHtml(value) {
    const element = document.createElement('div');
    element.textContent = String(value ?? '');
    return element.innerHTML;
}
