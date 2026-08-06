import { BuildSnapshotRequest } from './types';

// Harte PII / DSGVO Filter
const PII_REGEXES = [
    /@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/, // E-Mail
    /(?:\+49|0049|0151|0157|0171|0172|0173|0174|0175|0176|0177|0178|0179)\s*\d+/, // Deutsche Telefonnummern (grob)
    /(?:token|password|secret|api_key|authorization)[\s:=]+[\w-]+/i, // Tokens / Passwörter
    /[A-ZÄÖÜ][a-zäöüß]+\s*(?:str|straße|weg|platz|allee)\.?\s+\d+[a-zA-Z]?/i // Deutsche Adressmuster
];

export function validateSnapshotData(req: BuildSnapshotRequest): void {
    if (!req.items || req.items.length === 0) {
        throw new Error("Validation Error: Snapshot muss mindestens ein Item enthalten.");
    }
    
    if (!['verified', 'prototype', 'idea'].includes(req.truth_status)) {
        throw new Error(`Validation Error: Ungültiger truth_status '${req.truth_status}'.`);
    }

    const payloadString = JSON.stringify(req);

    // 1. Harte PII Prüfung
    for (const regex of PII_REGEXES) {
        if (regex.test(payloadString)) {
            throw new Error(`Validation Error: Persönliche oder sensible Daten erkannt (PII Filter angeschlagen: ${regex}). Build abgebrochen.`);
        }
    }

    // 2. Erlaubte Type-Werte prüfen (wird durch TS-Type theoretisch gefangen, aber zur Laufzeit sicher)
    const allowedTypes = ['principle', 'architecture', 'module', 'manifest', 'project_status', 'scarcity', 'abundance', 'resource', 'release'];
    for (const item of req.items) {
        if (!allowedTypes.includes(item.type)) {
            throw new Error(`Validation Error: Ungültiger Typ '${item.type}' im Item ${item.id}.`);
        }
        if (!item.id || !item.title || !item.description) {
            throw new Error(`Validation Error: Fehlende Pflichtfelder im Item ${item.id || 'unknown'}. (Benötigt: id, title, description)`);
        }
        // Maximale Größe: z.B. 10.000 Zeichen pro Feld
        if (item.content && item.content.length > 10000) {
            throw new Error(`Validation Error: Content in Item ${item.id} überschreitet die maximale Größe von 10.000 Zeichen.`);
        }
    }
}
