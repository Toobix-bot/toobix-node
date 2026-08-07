import { validateSnapshotData } from './validate';

const validRequest = {
    truth_status: 'verified',
    items: [
        { id: '1', type: 'principle', title: 'Test', description: 'Valid' }
    ]
};

const evilRequests = [
    { name: "E-Mail (Standard)", payload: { ...validRequest, summary: "Kontakt: max@example.com" } },
    { name: "E-Mail (Markdown/Unicode)", payload: { ...validRequest, summary: "Kontakt: max\u200B@\u202Fexample.com" } },
    { name: "Telefon (Standard)", payload: { ...validRequest, summary: "Ruf an: +49 151 12345678" } },
    { name: "Telefon (Markdown)", payload: { ...validRequest, summary: "Ruf an: +49&nbsp;151-12345678" } },
    { name: "API Key", payload: { ...validRequest, summary: "Mein token: sk-1234567890abcdef" } },
    { name: "Adresse", payload: { ...validRequest, summary: "Musterstraße 12" } },
    { name: "Überlanger Titel", payload: { truth_status: 'verified', items: [{ id: '1', type: 'principle', title: 'a'.repeat(121), description: 'Valid' }] } },
    { name: "Zu viele Tags", payload: { ...validRequest, tags: Array.from({length: 11}, (_, i) => `tag${i}`) } },
    { name: "Falscher Typ", payload: { truth_status: 'verified', items: [{ id: '1', type: 'invalid_type', title: 'Test', description: 'Valid' }] } }
];

let failedTests = 0;

console.log("=== Starte Zoll-Prüfstand (validate.ts) ===");

// Positiv-Test
try {
    validateSnapshotData(validRequest);
    console.log("✅ Positiv-Test bestanden: Valider Request wurde akzeptiert.");
} catch (e: any) {
    console.error("❌ Positiv-Test fehlgeschlagen! Valider Request wurde blockiert:", e.message);
    failedTests++;
}

// Negativ-Tests
for (const test of evilRequests) {
    try {
        validateSnapshotData(test.payload);
        console.error(`❌ Negativ-Test fehlgeschlagen: '${test.name}' wurde durchgelassen! (MUSS BLOCKIERT WERDEN)`);
        failedTests++;
    } catch (e: any) {
        console.log(`✅ Negativ-Test bestanden: '${test.name}' erfolgreich blockiert. (${e.message.split(':')[0]})`);
    }
}

console.log("===========================================");
if (failedTests > 0) {
    console.error(`🚨 ERGEBNIS: ${failedTests} Tests fehlgeschlagen! Zoll ist undicht.`);
    process.exit(1);
} else {
    console.log("🎉 ERGEBNIS: Alle Tests bestanden. Zoll ist dicht.");
    process.exit(0);
}
