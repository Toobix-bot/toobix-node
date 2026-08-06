/**
 * Toobix Node 2.0 – Live Dashboard Application
 * „Alle für alle! (Solidarität statt Isolation)"
 * 
 * Connects to the running Toobix Node backend and displays
 * real-time data: health, reflection, peer-awareness, scarcity, abundance.
 */

const API_BASE = 'http://localhost:8000';
let isConnected = false;

// ─── Boot ───────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    initScrollEffects();
    initNavHighlight();
    initForm();
    refreshAll();
    // Auto-refresh every 10 seconds
    setInterval(refreshAll, 10000);
});

// ─── Scroll Effects ─────────────────────────────────────────
function initScrollEffects() {
    const header = document.getElementById('mainHeader');
    window.addEventListener('scroll', () => {
        header.classList.toggle('scrolled', window.scrollY > 50);
    });
}

// ─── Navigation Highlight ───────────────────────────────────
function initNavHighlight() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                navLinks.forEach(link => link.classList.remove('active'));
                const activeLink = document.querySelector(`.nav-link[href="#${entry.target.id}"]`);
                if (activeLink) activeLink.classList.add('active');
            }
        });
    }, { threshold: 0.3 });
    
    sections.forEach(section => observer.observe(section));
}

// ─── API Fetch Helper ───────────────────────────────────────
async function apiFetch(endpoint) {
    try {
        const res = await fetch(`${API_BASE}${endpoint}`, { 
            mode: 'cors',
            signal: AbortSignal.timeout(5000)
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        setConnectionStatus(true);
        return data;
    } catch (err) {
        console.warn(`API ${endpoint}:`, err.message);
        setConnectionStatus(false);
        return null;
    }
}

// ─── Connection Status ──────────────────────────────────────
function setConnectionStatus(online) {
    isConnected = online;
    const dot = document.querySelector('.status-dot');
    const text = document.querySelector('.status-text');
    if (dot && text) {
        dot.className = `status-dot ${online ? 'online' : 'offline'}`;
        text.textContent = online ? 'Node verbunden' : 'Keine Verbindung';
    }
}

// ─── Refresh All ────────────────────────────────────────────
async function refreshAll() {
    const btn = document.getElementById('btnRefresh');
    if (btn) {
        btn.textContent = '↻ Lädt...';
        btn.disabled = true;
    }

    await Promise.all([
        loadHealth(),
        loadReflection(),
        loadPeerAwareness(),
        loadScarcity(),
        loadAbundance(),
    ]);

    if (btn) {
        btn.textContent = '↻ Aktualisieren';
        btn.disabled = false;
    }
}

// ─── Health ─────────────────────────────────────────────────
async function loadHealth() {
    const data = await apiFetch('/api/health');
    const el = document.getElementById('healthBody');
    if (!data) {
        el.innerHTML = `
            <div style="text-align:center; padding:1.5rem;">
                <div style="font-size:2.5rem; margin-bottom:0.5rem;">⚠️</div>
                <div style="color:var(--accent-red); font-weight:600;">Node nicht erreichbar</div>
                <div style="color:var(--text-muted); font-size:0.82rem; margin-top:0.5rem;">
                    Starte das Backend mit:<br>
                    <code style="background:rgba(255,255,255,0.05); padding:0.3rem 0.6rem; border-radius:4px; font-size:0.75rem;">
                        python3 -m app.main
                    </code>
                </div>
            </div>`;
        return;
    }
    el.innerHTML = `
        <div style="text-align:center; padding:1rem;">
            <div style="font-size:2.5rem; margin-bottom:0.5rem;">✅</div>
            <div class="status-badge online" style="margin:0 auto;">● Online</div>
            <div style="margin-top:0.75rem; font-size:0.85rem; color:var(--text-secondary);">
                ${data.node_id || 'Toobix-Node-2.0'}
            </div>
        </div>`;
}

// ─── Self Reflection ────────────────────────────────────────
async function loadReflection() {
    const data = await apiFetch('/api/reflection');
    const el = document.getElementById('reflectionBody');
    const harmonyEl = document.getElementById('harmonyBody');

    if (!data) {
        el.innerHTML = '<div class="no-data">Keine Reflexionsdaten verfügbar</div>';
        harmonyEl.innerHTML = '<div class="no-data">--</div>';
        return;
    }

    // Reflection grid
    const mangelItems = (data.mangel || []).map(m => 
        `<div class="reflection-item mangel">🔴 ${escHtml(m)}</div>`
    ).join('');
    const uebItems = (data.ueberfluss || []).map(u => 
        `<div class="reflection-item ueberfluss">🟢 ${escHtml(u)}</div>`
    ).join('');

    el.innerHTML = `
        <div class="reflection-grid">
            <div class="reflection-col mangel">
                <h4>Mangel (Eigene Schwächen)</h4>
                ${mangelItems || '<div class="no-data">Keine Mängel erkannt</div>'}
            </div>
            <div class="reflection-col ueberfluss">
                <h4>Überfluss (Eigene Stärken)</h4>
                ${uebItems || '<div class="no-data">Keine Stärken erkannt</div>'}
            </div>
        </div>
        <div style="text-align:center; margin-top:1rem; font-size:0.82rem; color:var(--text-muted);">
            ${escHtml(data.status_summary || '')}
        </div>`;

    // Harmony meter
    const score = data.harmony_score || 0;
    const pct = Math.round(score * 100);
    let color = 'var(--accent-green)';
    let label = 'Harmonisch';
    if (pct < 30) { color = 'var(--accent-red)'; label = 'Kritisch'; }
    else if (pct < 60) { color = 'var(--accent-orange)'; label = 'Ausbaufähig'; }

    harmonyEl.innerHTML = `
        <div class="harmony-meter">
            <span class="harmony-score" style="color:${color}">${pct}%</span>
            <div class="harmony-bar">
                <div class="harmony-fill" style="width:${pct}%; background:${color};"></div>
            </div>
            <span class="harmony-label">${label}</span>
        </div>`;

    // Hero stats
    document.getElementById('statHarmony').textContent = `${pct}%`;
}

// ─── Peer Awareness ─────────────────────────────────────────
async function loadPeerAwareness() {
    const data = await apiFetch('/api/peers/awareness');
    const peerEl = document.getElementById('peerBody');
    const praiseEl = document.getElementById('praiseBody');

    if (!data) {
        peerEl.innerHTML = '<div class="no-data">Keine Peer-Daten verfügbar</div>';
        praiseEl.innerHTML = '<div class="no-data">Keine Bewertungen verfügbar</div>';
        document.getElementById('statNodes').textContent = '1';
        return;
    }

    const peers = data.peers || {};
    const peerKeys = Object.keys(peers);
    const summary = data.network_awareness_summary || {};

    // Update hero stats
    document.getElementById('statNodes').textContent = (peerKeys.length + 1).toString();

    // Network summary
    let summaryHtml = `
        <div class="network-summary">
            <div class="net-stat">
                <span class="net-stat-val" style="color:var(--accent-blue)">${peerKeys.length + 1}</span>
                <span class="net-stat-label">Nodes gesamt</span>
            </div>
            <div class="net-stat">
                <span class="net-stat-val" style="color:var(--accent-green)">${summary.praised_peers || 0}</span>
                <span class="net-stat-label">Gelobte Peers</span>
            </div>
            <div class="net-stat">
                <span class="net-stat-val" style="color:var(--accent-red)">${summary.criticized_peers || 0}</span>
                <span class="net-stat-label">Kritisierte Peers</span>
            </div>
            <div class="net-stat">
                <span class="net-stat-val status-badge ${summary.overall_status || ''}" style="font-size:0.9rem;">
                    ${escHtml(summary.overall_status || 'unbekannt')}
                </span>
                <span class="net-stat-label">Netzwerk-Status</span>
            </div>
        </div>`;

    // Peer list
    let peerHtml = peerKeys.length > 0 ? '<div class="peer-list">' : '';
    for (const [url, info] of Object.entries(peers)) {
        const rep = info.reputation_score || 0;
        const shortUrl = url.replace(/https?:\/\//, '');
        peerHtml += `
            <div class="peer-item">
                <div class="peer-avatar">⬡</div>
                <div class="peer-info">
                    <div class="peer-rep">⭐ Reputation: ${rep}</div>
                    <div class="peer-url">${escHtml(shortUrl)}</div>
                    <div style="font-size:0.75rem; color:var(--text-muted);">
                        Praise: ${info.praise_count || 0} · Criticism: ${info.criticism_count || 0} · 
                        Antwortzeit: ${(info.last_response_time_ms || 0).toFixed(1)}ms
                    </div>
                </div>
                <span class="peer-health ${info.health || 'unknown'}">${escHtml(info.health || '?')}</span>
            </div>`;
    }
    if (peerKeys.length > 0) peerHtml += '</div>';
    else peerHtml = '<div class="no-data">Noch keine Peers verbunden. Starte einen zweiten Node!</div>';

    peerEl.innerHTML = summaryHtml + peerHtml;

    // Praise / Criticism log
    const history = data.history || data.praise_criticism_history || [];
    if (history.length === 0) {
        praiseEl.innerHTML = '<div class="no-data">Noch keine Bewertungen vorhanden</div>';
    } else {
        let logHtml = '<div class="praise-list">';
        for (const entry of history.slice(-20).reverse()) {
            const type = entry.type || 'praise';
            const icon = type === 'praise' ? '👍' : '⚠️';
            logHtml += `
                <div class="praise-item ${type}">
                    <span style="font-size:1.1rem;">${icon}</span>
                    <span class="praise-reason">${escHtml(entry.reason || '')}</span>
                    <span class="praise-token">${escHtml(entry.token || '')}</span>
                </div>`;
        }
        logHtml += '</div>';
        praiseEl.innerHTML = logHtml;
    }
}

// ─── Scarcity ───────────────────────────────────────────────
async function loadScarcity() {
    const data = await apiFetch('/api/scarcity');
    const el = document.getElementById('scarcityList');

    if (!data || data.length === 0) {
        el.innerHTML = '<div class="no-data">Keine Mangel-Einträge vorhanden</div>';
        document.getElementById('statNeeds').textContent = '0';
        return;
    }

    document.getElementById('statNeeds').textContent = data.length.toString();

    el.innerHTML = data.map(entry => `
        <div class="entry-item">
            <h5>🔴 ${escHtml(entry.title || 'Ohne Titel')}</h5>
            <p>${escHtml(entry.description || '')}</p>
            <div class="entry-meta">
                <span>📁 ${escHtml(entry.category || 'Allgemein')}</span>
                <span>📍 ${escHtml(entry.location || 'Unbekannt')}</span>
                <span>⚡ ${escHtml(entry.urgency || 'mittel')}</span>
            </div>
        </div>
    `).join('');
}

// ─── Abundance ──────────────────────────────────────────────
async function loadAbundance() {
    const data = await apiFetch('/api/abundance');
    const el = document.getElementById('abundanceList');
    const solidarityGrid = document.getElementById('solidarityGrid');

    if (!data || data.length === 0) {
        el.innerHTML = '<div class="no-data">Keine Überfluss-Einträge vorhanden</div>';
        solidarityGrid.innerHTML = '<div class="no-data">Keine Hilfsangebote in der Datenbank</div>';
        document.getElementById('statOffers').textContent = '0';
        return;
    }

    document.getElementById('statOffers').textContent = data.length.toString();

    // Exchange list (all entries)
    el.innerHTML = data.map(entry => `
        <div class="entry-item">
            <h5>🟢 ${escHtml(entry.title || 'Ohne Titel')}</h5>
            <p>${escHtml(entry.description || '')}</p>
            <div class="entry-meta">
                <span>📁 ${escHtml(entry.category || 'Allgemein')}</span>
                <span>📍 ${escHtml(entry.location || 'Unbekannt')}</span>
            </div>
        </div>
    `).join('');

    // Solidarity section (tagged entries only)
    const solidarityOffers = data.filter(e => 
        (e.tags && e.tags.includes('solidarity_offer')) || 
        e.contact && e.contact.match(/^\d/)
    );

    if (solidarityOffers.length > 0) {
        solidarityGrid.innerHTML = solidarityOffers.map(entry => `
            <div class="solidarity-card">
                <h4>${escHtml(entry.title || 'Hilfsangebot')}</h4>
                <p>${escHtml(entry.description || '')}</p>
                <div class="solidarity-meta">
                    ${(entry.tags || []).filter(t => t !== 'solidarity_offer').map(t => 
                        `<span class="solidarity-tag">${escHtml(t)}</span>`
                    ).join('')}
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:0.78rem; color:var(--text-muted);">📍 ${escHtml(entry.location || '')}</span>
                    ${entry.contact ? `<a href="tel:${entry.contact}" class="solidarity-contact">📞 ${escHtml(entry.contact)}</a>` : ''}
                </div>
            </div>
        `).join('');
    } else {
        solidarityGrid.innerHTML = '<div class="no-data">Keine verifizierten Hilfsangebote gefunden</div>';
    }
}

// ─── Form Handler ───────────────────────────────────────────
function initForm() {
    const form = document.getElementById('entryForm');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const feedback = document.getElementById('formFeedback');
        const type = document.getElementById('entryType').value;
        const endpoint = type === 'scarcity' ? '/api/scarcity' : '/api/abundance';

        const body = {
            title: document.getElementById('entryTitle').value.trim(),
            category: document.getElementById('entryCategory').value,
            description: document.getElementById('entryDesc').value.trim(),
            location: document.getElementById('entryLocation').value.trim() || 'Deutschland',
            contact: document.getElementById('entryContact').value.trim() || '',
        };

        if (!body.title || !body.description) {
            feedback.className = 'form-feedback error';
            feedback.textContent = 'Bitte Titel und Beschreibung ausfüllen.';
            return;
        }

        try {
            const res = await fetch(`${API_BASE}${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            
            feedback.className = 'form-feedback success';
            feedback.textContent = `✅ Eintrag "${body.title}" erfolgreich an das Netzwerk gesendet!`;
            form.reset();
            
            // Refresh data
            setTimeout(refreshAll, 1000);
        } catch (err) {
            feedback.className = 'form-feedback error';
            feedback.textContent = `❌ Fehler: ${err.message}. Ist das Backend gestartet?`;
        }
    });
}

// ─── Utility ────────────────────────────────────────────────
function escHtml(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = String(str);
    return div.innerHTML;
}
