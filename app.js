document.addEventListener('DOMContentLoaded', () => {
    const STORAGE_KEY = 'toobix-node-entries-v1';

    const slider = document.getElementById('stateSlider');
    const display = document.getElementById('statusDisplay');
    const entryForm = document.getElementById('entryForm');
    const offersList = document.getElementById('offersList');
    const needsList = document.getElementById('needsList');
    const clearEntriesButton = document.getElementById('clearEntries');

    function escapeHtml(value) {
        return String(value).replace(/[&<>"']/g, (character) => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        }[character]));
    }

    function loadEntries() {
        try {
            const parsed = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
            return Array.isArray(parsed) ? parsed : [];
        } catch (error) {
            console.warn('Lokale Toobix-Einträge konnten nicht gelesen werden.', error);
            return [];
        }
    }

    function saveEntries(entries) {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(entries));
        } catch (error) {
            console.warn('Lokale Toobix-Einträge konnten nicht gespeichert werden.', error);
        }
    }

    function createEntryCard(entry) {
        const card = document.createElement('article');
        card.className = `card ${entry.type}`;
        card.dataset.entryId = entry.id;
        card.innerHTML = `
            <h4>${escapeHtml(entry.title)}</h4>
            <p>${escapeHtml(entry.description)}</p>
            <div class="price-tag">Wert: ${escapeHtml(entry.credits)} Solidar-Credits (SC)</div>
            <div class="tausch-info">Lokal auf diesem Gerät gespeichert</div>
            <button type="button" class="delete-entry" aria-label="Eintrag löschen">Eintrag löschen</button>
        `;

        card.querySelector('.delete-entry').addEventListener('click', () => {
            const updatedEntries = loadEntries().filter((item) => item.id !== entry.id);
            saveEntries(updatedEntries);
            card.remove();
        });

        return card;
    }

    function renderStoredEntries() {
        loadEntries().forEach((entry) => {
            const target = entry.type === 'offer' ? offersList : needsList;
            target?.prepend(createEntryCard(entry));
        });
    }

    if (slider && display) {
        slider.addEventListener('input', (event) => {
            const value = Number.parseInt(event.target.value, 10);
            let message;
            let color;

            if (value < -30) {
                message = '🔴 ZUSTAND: MANGEL. Meine Kapazitäten sind erschöpft. Ich benötige gezielte Unterstützung oder Ruhe.';
                color = 'var(--color-mangel)';
            } else if (value > 30) {
                message = '🔵 ZUSTAND: ÜBERFLUSS. Ich verfüge über freie Energie, Zeit oder Fähigkeiten und achte dabei auf meine Grenzen.';
                color = 'var(--color-ueberfluss)';
            } else {
                message = '🟢 ZUSTAND: GLEICHGEWICHT. Ich bin aufnahmefähig, kann Grenzen wahren und gegebenenfalls vermitteln.';
                color = 'var(--color-balance)';
            }

            display.textContent = message;
            display.style.borderColor = color;
            display.style.boxShadow = `0 0 20px ${color}45`;
        });
        slider.dispatchEvent(new Event('input'));
    }

    renderStoredEntries();

    entryForm?.addEventListener('submit', (event) => {
        event.preventDefault();

        const type = document.getElementById('entryType').value;
        const title = document.getElementById('entryTitle').value.trim();
        const description = document.getElementById('entryDesc').value.trim();
        const credits = document.getElementById('entryCredits').value;

        if (!title || !description || !credits || !['offer', 'need'].includes(type)) {
            return;
        }

        const entry = {
            id: globalThis.crypto?.randomUUID?.() || `${Date.now()}-${Math.random()}`,
            type,
            title,
            description,
            credits,
            createdAt: new Date().toISOString()
        };

        const entries = loadEntries();
        entries.push(entry);
        saveEntries(entries);

        const target = type === 'offer' ? offersList : needsList;
        target?.prepend(createEntryCard(entry));
        entryForm.reset();
    });

    clearEntriesButton?.addEventListener('click', () => {
        if (!window.confirm('Alle selbst erstellten lokalen Einträge auf diesem Gerät löschen?')) {
            return;
        }

        localStorage.removeItem(STORAGE_KEY);
        document.querySelectorAll('[data-entry-id]').forEach((element) => element.remove());
    });

    const explorerData = [
        {
            name: 'EUTB – Ergänzende unabhängige Teilhabeberatung',
            region: 'local',
            tag: 'Beratung & Teilhabe',
            desc: 'Unabhängige Beratung zu Rehabilitation, Teilhabe und Fragen rund um Behinderung.',
            status: 'Beispielkategorie – regionale Stelle vor Nutzung prüfen.'
        },
        {
            name: 'Lokale Tafeln und Lebensmittelrettung',
            region: 'local',
            tag: 'Lebensmittel & Ausgleich',
            desc: 'Lokale Unterstützung mit Lebensmitteln und Möglichkeiten zum ehrenamtlichen Mitwirken.',
            status: 'Beispielkategorie – Verfügbarkeit ist regional unterschiedlich.'
        },
        {
            name: 'Gemeindepsychiatrische und psychosoziale Hilfen',
            region: 'local',
            tag: 'Gesundheit & Teilhabe',
            desc: 'Mögliche Angebote sind Sozialpsychiatrischer Dienst, Soziotherapie oder ambulante Assistenz.',
            status: 'Kein Verzeichnis. Zuständigkeit vor Ort prüfen.'
        },
        {
            name: 'TelefonSeelsorge Deutschland',
            region: 'national',
            tag: 'Seelische Krise',
            desc: 'Anonyme und kostenfreie Gesprächsmöglichkeit rund um die Uhr.',
            status: 'Bundesweites Hilfsangebot; in akuter Gefahr 112 wählen.'
        },
        {
            name: 'Verbraucherzentralen',
            region: 'national',
            tag: 'Recht & Finanzen',
            desc: 'Beratung zu Verträgen, Energie, Schulden und Verbraucherrechten.',
            status: 'Kosten und Terminbedingungen regional prüfen.'
        },
        {
            name: 'Open-Source- und Commons-Bewegung',
            region: 'global',
            tag: 'Technologische Freiheit',
            desc: 'Gemeinschaften für freie Software, offene Standards und gemeinschaftlich nutzbares Wissen.',
            status: 'Globale Kategorie ohne zentrale Zuständigkeit.'
        }
    ];

    const explorerGrid = document.getElementById('explorerGrid');
    const regionFilter = document.getElementById('regionFilter');

    function renderExplorer(filter = 'all') {
        if (!explorerGrid) return;
        explorerGrid.replaceChildren();

        const filtered = filter === 'all'
            ? explorerData
            : explorerData.filter((item) => item.region === filter);

        filtered.forEach((item) => {
            const card = document.createElement('article');
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

    regionFilter?.addEventListener('change', (event) => renderExplorer(event.target.value));
    renderExplorer();

    const chronicleData = [
        { title: 'Konzept und Systemanalyse', desc: 'Vom persönlichen Dashboard zum solidarischen Austauschkonzept.', val: 'Konzeptarbeit' },
        { title: 'Lokaler Web-Prototyp', desc: 'Status-Tacho, Angebote, Bedarfe und Browser-Speicherung.', val: 'Prototyp' },
        { title: 'Datenschutz-Härtung', desc: 'Externe Abhängigkeiten entfernt und Aussagen präzisiert.', val: 'Sicherheit' },
        { title: 'Dokumentation und Lizenz', desc: 'Projektstatus, Grenzen, Datenschutz und MIT-Lizenz ergänzt.', val: 'Grundlage' }
    ];

    const chronicleTimeline = document.getElementById('chronicleTimeline');
    chronicleData.forEach((item) => {
        if (!chronicleTimeline) return;
        const element = document.createElement('article');
        element.className = 'c-item';
        element.innerHTML = `
            <div>
                <h4>${escapeHtml(item.title)}</h4>
                <p>${escapeHtml(item.desc)}</p>
            </div>
            <div class="c-val">${escapeHtml(item.val)}</div>
        `;
        chronicleTimeline.appendChild(element);
    });
});
