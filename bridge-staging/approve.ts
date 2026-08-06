import * as fs from 'fs';
import * as path from 'path';
import { ApproveSnapshotRequest, PublicSnapshot } from './types';
import { generateHash } from './hash';

const PENDING_DIR = path.join(process.cwd(), '_TOOBIX_KNOWLEDGE_SPACE', 'bridge', 'pending');
const READY_DIR = path.join(process.cwd(), '_TOOBIX_KNOWLEDGE_SPACE', 'bridge', 'ready');

/**
 * Liest einen pending Snapshot, signiert ihn (v0.1 simpel) und verschiebt ihn nach "ready".
 */
export async function approveSnapshot(req: ApproveSnapshotRequest): Promise<string> {
    fs.mkdirSync(READY_DIR, { recursive: true });

    const pendingPath = path.join(PENDING_DIR, req.filename);
    if (!fs.existsSync(pendingPath)) {
        throw new Error(`Snapshot ${req.filename} existiert nicht in pending.`);
    }

    // Snapshot laden
    const rawData = fs.readFileSync(pendingPath, 'utf-8');
    const snapshot = JSON.parse(rawData) as PublicSnapshot;

    // Freigabe-Metadaten setzen
    snapshot.approved_by = req.approver_name;
    snapshot.approved_at = new Date().toISOString();

    // Hash generieren (verhindert nachträgliche Manipulation vor dem manuellen Push)
    snapshot.snapshot_hash = generateHash(snapshot);

    // Speichern im ready Ordner
    const readyPath = path.join(READY_DIR, req.filename);
    fs.writeFileSync(readyPath, JSON.stringify(snapshot, null, 2), 'utf-8');

    // Löschen aus pending
    fs.unlinkSync(pendingPath);

    // Der Snapshot ist nun im Ready-Ordner.
    // Der tatsächliche Push ins öffentliche Repo passiert absichtlich MANUELL 
    // durch einen Copy + Git Push Schritt im Terminal.
    return readyPath;
}
