import express from 'express';
import * as fs from 'fs';
import * as path from 'path';
import { buildSnapshot } from './build';
import { approveSnapshot } from './approve';

export const bridgeRouter = express.Router();
const PENDING_DIR = path.join(process.cwd(), '_TOOBIX_KNOWLEDGE_SPACE', 'bridge', 'pending');

// 1. Snapshot bauen (wird als Datei im pending/ Ordner abgelegt)
bridgeRouter.post('/build-snapshot', async (req, res) => {
    try {
        const filename = await buildSnapshot(req.body);
        res.json({ status: 'success', filename, message: 'Snapshot in pending/ abgelegt. Bereit für Review.' });
    } catch (error: any) {
        res.status(500).json({ error: error.message });
    }
});

// 2. Offene Snapshots auflisten
bridgeRouter.get('/pending', (req, res) => {
    try {
        if (!fs.existsSync(PENDING_DIR)) fs.mkdirSync(PENDING_DIR, { recursive: true });
        const files = fs.readdirSync(PENDING_DIR).filter(f => f.endsWith('.json'));
        res.json({ pending_files: files });
    } catch (error: any) {
        res.status(500).json({ error: error.message });
    }
});

// 3. Snapshot freigeben (signieren und in ready/ verschieben)
bridgeRouter.post('/approve-snapshot', async (req, res) => {
    try {
        const readyPath = await approveSnapshot(req.body);
        res.json({ 
            status: 'approved', 
            ready_path: readyPath,
            message: 'Snapshot signiert und in ready/ abgelegt. Manuelle Kopie ins public repo erforderlich!'
        });
    } catch (error: any) {
        res.status(500).json({ error: error.message });
    }
});

export default bridgeRouter;
