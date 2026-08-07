import { BuildSnapshotRequest } from './types';

// Harte PII / DSGVO Filter
// Harte PII / DSGVO Filter
// Extrahiert und normalisiert Text vor dem Regex-Match (entfernt Markdown-Links, Zero-Width-Spaces, etc.)
const PII_REGEXES = [
    // E-Mail (inkl. Variationen mit Leerzeichen oder Markdown)
    /(?:mailto:)?[\w.-]+(?:%20|\s|&nbsp;|\u202F)*@(?:%20|\s|&nbsp;|\u202F)*[\w.-]+\.(?:com|org|net|de|eu|info|me|io)/i,
    // Telefonnummern (sehr aggressiv gegen +49, 0049 und 015x)
    /(?:\+|00)?49(?:%20|\s|&nbsp;|\u202F|-)*0?1[567][1-9](?:%20|\s|&nbsp;|\u202F|-)*\d{3,}/,
    /(?:\+|00)?49(?:%20|\s|&nbsp;|\u202F|-)*[1-9]\d{2,}(?:%20|\s|&nbsp;|\u202F|-)*\d{4,}/,
    // API Keys und Tokens
    /(?:token|password|secret|api_key|authorization|bearer|sk-)[\s:=_'"*-]+[A-Za-z0-9_-]{10,}/i,
    // Deutsche Adressmuster
    /[A-ZÄÖÜ][a-zäöüß]+\s*(?:str|straße|weg|platz|allee)\.?(?:%20|\s|&nbsp;|\u202F)+\d+[a-zA-Z]?/i
];

function normalizeTextForRegex(text: string): string {
    // Entfernt typische Markdown- und Versteck-Muster für den Regex-Scan
    return text.replace(/[\u200B-\u200D\uFEFF]/g, ''); 
}

export function validateSnapshotData(req: any): void {
    if (!req.items || req.items.length === 0) {
        throw new Error("Validation Error: Snapshot muss mindestens ein Item enthalten.");
    }
    
    if (!['verified', 'prototype', 'idea'].includes(req.truth_status)) {
        throw new Error(`Validation Error: Ungültiger truth_status '${req.truth_status}'.`);
    }

    const payloadString = normalizeTextForRegex(JSON.stringify(req));

    // 1. Harte PII Prüfung
    for (const regex of PII_REGEXES) {
        if (regex.test(payloadString)) {
            throw new Error(`Validation Error: Persönliche oder sensible Daten erkannt (PII Filter angeschlagen: ${regex}). Build abgebrochen.`);
        }
    }

    // 2. Erlaubte Type-Werte und Feld-Längen prüfen
    const allowedTypes = ['principle', 'architecture', 'module', 'manifest', 'project_status', 'scarcity', 'abundance', 'resource', 'release'];
    
    // Check root metadata if present (added during prepare or build)
    if (req.summary && req.summary.length > 500) {
        throw new Error(`Validation Error: summary überschreitet das Limit von 500 Zeichen.`);
    }
    if (req.tags) {
        if (!Array.isArray(req.tags) || req.tags.length > 10) {
            throw new Error(`Validation Error: Maximal 10 Tags erlaubt.`);
        }
        for (const tag of req.tags) {
            if (tag.length > 32) throw new Error(`Validation Error: Tag '${tag}' ist länger als 32 Zeichen.`);
        }
    }

    for (const item of req.items) {
        if (!allowedTypes.includes(item.type)) {
            throw new Error(`Validation Error: Ungültiger Typ '${item.type}' im Item ${item.id}.`);
        }
        if (!item.id || !item.title || !item.description) {
            throw new Error(`Validation Error: Fehlende Pflichtfelder im Item ${item.id || 'unknown'}. (Benötigt: id, title, description)`);
        }
        if (item.title.length > 120) {
            throw new Error(`Validation Error: title in Item ${item.id} überschreitet 120 Zeichen.`);
        }
        if (item.content && item.content.length > 10000) {
            throw new Error(`Validation Error: content in Item ${item.id} überschreitet 10.000 Zeichen.`);
        }
    }
}
