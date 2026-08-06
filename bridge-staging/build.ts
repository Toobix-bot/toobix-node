import * as fs from 'fs';
import * as path from 'path';
import { PublicSnapshot, BuildSnapshotRequest } from './types';
import { validateSnapshotData } from './validate';

const PENDING_DIR = path.join(process.cwd(), '_TOOBIX_KNOWLEDGE_SPACE', 'bridge', 'pending');

/**
 * Erstellt einen neuen Snapshot im "pending" Ordner zur manuellen Überprüfung.
 */
export async function buildSnapshot(req: BuildSnapshotRequest): Promise<string> {
    // 1. Validierung (Blockiert PII und Schema-Verstöße sofort)
    validateSnapshotData(req);

    // Ordner sicherstellen
    fs.mkdirSync(PENDING_DIR, { recursive: true });

    // Snapshot vorbereiten
    const snapshot: PublicSnapshot = {
        schema_version: "1.0",
        source_system: "TOOBIX_PRIVATE",
        visibility: "public",
        truth_status: req.truth_status,
        contains_personal_data: false, // Vertragliche Zusicherung + Validate-Schicht
        items: req.items
    };

    // Dateinamen generieren (z.B. 2026-08-07-principle-xyz.json)
    const dateStr = new Date().toISOString().split('T')[0];
    const firstType = req.items[0]?.type || 'mixed';
    const firstId = req.items[0]?.id || Date.now().toString();
    const filename = `${dateStr}-${firstType}-${firstId}.json`;
    
    const filePath = path.join(PENDING_DIR, filename);

    // Snapshot auf die Festplatte schreiben (air-gapped Review)
    fs.writeFileSync(filePath, JSON.stringify(snapshot, null, 2), 'utf-8');

    return filename;
}
