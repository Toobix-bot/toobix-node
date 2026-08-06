import { createHash } from 'crypto';

/**
 * Erzeugt einen SHA256 Hash über das serialisierte Snapshot-Objekt.
 * Sichert die Integrität nach dem Review.
 */
export function generateHash(data: any): string {
    const serialized = JSON.stringify(data, Object.keys(data).sort());
    return 'sha256:' + createHash('sha256').update(serialized).digest('hex');
}
