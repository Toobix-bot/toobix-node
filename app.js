document.addEventListener('DOMContentLoaded', () => {
    // --- 1. Balance Slider (Mikro-Status) ---
    const slider = document.getElementById('stateSlider');
    const display = document.getElementById('statusDisplay');

    if (slider && display) {
        slider.addEventListener('input', (e) => {
            const val = parseInt(e.target.value);
            let message = '';
            let color = '';

            if (val < -30) {
                message = '🔴 ZUSTAND: MANGEL (Aktiv aufnahmesuchend). Meine Kapazitäten sind erschöpft. Ich benötige gezielte Unterstützung oder Ruhe, um wieder stabil zu werden.';
                color = 'var(--color-mangel)';
            } else if (val > 30) {
                message = '🔵 ZUSTAND: ÜBERFLUSS (Aktiv abgebend). Ich verfüge über überschüssige Energie, Zeit oder Fähigkeiten und möchte diese teilen. (Achtung: Eigene Grenzen wahren!)';
                color = 'var(--color-ueberfluss)';
            } else {
                message = '🟢 ZUSTAND: GLEICHGEWICHT (Sein & Vermitteln). Ich ruhe in mir, bin aufnahmefähig und kann als neutraler Vermittler zwischen Mangel und Überfluss agieren.';
                color = 'var(--color-balance)';
            }

            display.textContent = message;
            display.style.borderColor = color;
            display.style.boxShadow = `0 0 20px ${color}45`;
        });
        slider.dispatchEvent(new Event('input'));
    }

    // --- 2. Interactive Offer / Need Form (Local Storage) ---
    const entryForm = document.getElementById('entryForm');
    const offersList = document.getElementById('offersList');
    const needsList = document.getElementById('needsList');

    if (entryForm) {
        entryForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const type = document.getElementById('entryType').value;
            const title = document.getElementById('entryTitle').value;
            const desc = document.getElementById('entryDesc').value;
            const credits = document.getElementById('entryCredits').value;

            const card = document.createElement('div');
            card.className = `card ${type}`;
            card.innerHTML = `
                <h4>${escapeHtml(title)}</h4>
                <p>${escapeHtml(desc)}</p>
                <div class="price-tag">Wert: ${escapeHtml(credits)} Solidar-Credits (SC)</div>
                <div class="tausch-info">Neu eingetragen (Lokal auf deinem Gerät)</div>
            `;

            if (type === 'offer') {
                offersList.prepend(card);
            } else {
                needsList.prepend(card);
            }

            entryForm.reset();
        });
    }

    // --- 3. Makro-Explorer Data & Filtering ---
    const explorerData = [
        {
            name: "EUTB (Unabhängige Teilhabeberatung)",
            region: "local",
            tag: "Beratung & Teilhabe",
            desc: "Ergänzende unabhängige Teilhabeberatung bei Fragen zu Behinderung, Schwerbehindertenausweis, Reha und SGB IX.",
            status: "Überfluss: Unabhängige Fachberatung · Mangel: Bekanntheit bei Betroffenen"
        },
        {
            name: "Lokale Tafeln (Lebensmittelrettung)",
            region: "local",
            tag: "Lebensmittel & Ausgleich",
            desc: "Unterstützung von bedürftigen Menschen mit Lebensmitteln im lokalen Raum.",
            status: "Überfluss: Lebensmittelspenden · Mangel: Ehramtliche Helfer & Logistik"
        },
        {
            name: "Gemeindepsychiatrischer Verbund (GPV)",
            region: "local",
            tag: "Gemeindepsychiatrie & ABW",
            desc: "Ambulant Betreutes Wohnen, Soziotherapie und psychosoziale Hilfen für das selbstbestimmte Leben.",
            status: "Überfluss: Professionelle Begleitung · Mangel: Freie Kapazitäten in Hochphasen"
        },
        {
            name: "TelefonSeelsorge Deutschland",
            region: "national",
            tag: "Seelische Gesundheit & Notfall",
            desc: "Anonyme, kostenfreie Beratung rund um die Uhr per Telefon (0800 1110111) oder Chat.",
            status: "Überfluss: 24/7 Erreichbarkeit · Mangel: Auslastung in Krisenzeiten"
        },
        {
            name: "Regionale Verbraucherzentrale",
            region: "national",
            tag: "Recht & Finanzen",
            desc: "Unabhängige Beratung bei Verträgen, Schulden, Energiepreisen und Verbraucherrechten.",
            status: "Überfluss: Fachwissen · Mangel: Kapazität für Spontan-Termine"
        },
        {
            name: "Open Source Hardware & Software Movement",
            region: "global",
            tag: "Technologische Freiheit",
            desc: "Weltweite Gemeinschaft für freie Software, Open-Data und dezentrale Technologien ohne Profitzwang.",
            status: "Überfluss: Innovation & freier Code · Mangel: Lokale Anwendung im Alltag"
        }
    ];

    const explorerGrid = document.getElementById('explorerGrid');
    const regionFilter = document.getElementById('regionFilter');

    function renderExplorer(filter = 'all') {
        if (!explorerGrid) return;
        explorerGrid.innerHTML = '';

        const filtered = filter === 'all' 
            ? explorerData 
            : explorerData.filter(item => item.region === filter);

        filtered.forEach(item => {
            const card = document.createElement('div');
            card.className = 'exp-card';
            card.innerHTML = `
                <div>
                    <div class="exp-tag">${escapeHtml(item.tag)}</div>
                    <h4>${escapeHtml(item.name)}</h4>
                    <p class="exp-desc">${escapeHtml(item.desc)}</p>
                </div>
                <div class="exp-status">${escapeHtml(item.status)}</div>
            `;
            explorerGrid.appendChild(card);
        });
    }

    if (regionFilter) {
        regionFilter.addEventListener('change', (e) => renderExplorer(e.target.value));
        renderExplorer('all');
    }

    // --- 4. Transparency Chronicle Data (Proof of Work) ---
    const chronicleData = [
        { title: "Block 01: Planungsanpassung & Systemanalyse", desc: "Analyse der Toobix-Struktur, Wechsel von abstrakten Dashboards zu Solidarischer Ökonomie.", val: "12,50 €" },
        { title: "Block 02: Werkzeug-Erweiterung (`toobix.py`)", desc: "Entwicklung von CLI-Skripten für Credits, Angebote und automatisches Netzwerk-Matching.", val: "38,50 €" },
        { title: "Block 03: Philosophische Trennung von Wert & Mensch", desc: "Klarstellung: Menschlicher Wert ist unantastbar. Trennung von Beschäftigung und Arbeit.", val: "25,00 €" },
        { title: "Block 04: Pragmatische Existenzsicherung & Pitch", desc: "Erstellung des Pitch-Dokuments für lokale Träger (Fähigkeiten gegen Brot/Raum).", val: "15,00 €" },
        { title: "Block 05: Werte-Recherche (LETS & Timebanks)", desc: "Abgleich mit bestehenden Systemen. Erfindung der dezentralen 'Exchange Node'.", val: "20,00 €" },
        { title: "Block 06: Der visionäre Pivot zur Mangel/Überfluss-Börse", desc: "Geld als fiktiven Rechenschieber definiert. Fokus auf direkte Ausgleichs-Systeme.", val: "50,00 €" },
        { title: "Block 07: Web-Prototyp 1.0 (Balance-Tacho)", desc: "Programmierung der Benutzeroberfläche mit Mangel-, Gleichgewichts- und Überfluss-Zuständen.", val: "120,00 €" },
        { title: "Block 08: Datenschutz & Toobix Node 2.0", desc: "Restlose Anonymisierung (alle Klarnamen entfernt), universelle Mitgliedschaft & Makro-Explorer.", val: "37,50 €" }
    ];

    const chronicleTimeline = document.getElementById('chronicleTimeline');
    if (chronicleTimeline) {
        chronicleData.forEach(item => {
            const div = document.createElement('div');
            div.className = 'c-item';
            div.innerHTML = `
                <div>
                    <h4>${escapeHtml(item.title)}</h4>
                    <p>${escapeHtml(item.desc)}</p>
                </div>
                <div class="c-val">${escapeHtml(item.val)}</div>
            `;
            chronicleTimeline.appendChild(div);
        });
    }

    // Helper function
    function escapeHtml(str) {
        return str.replace(/[&<>"']/g, function(m) {
            return {
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                '"': '&quot;',
                "'": '&#039;'
            }[m];
        });
    }
});
