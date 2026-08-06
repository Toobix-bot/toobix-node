export type SnapshotType = 
    | 'principle' 
    | 'architecture' 
    | 'module' 
    | 'manifest' 
    | 'project_status' 
    | 'scarcity' 
    | 'abundance' 
    | 'resource' 
    | 'release';

export interface SnapshotItem {
    id: string;
    type: SnapshotType;
    category: string;
    title: string;
    description: string;
    content?: string; // Optional full markdown or text content
}

export interface PublicSnapshot {
    schema_version: "1.0";
    source_system: "TOOBIX_PRIVATE";
    visibility: "public";
    truth_status: "verified" | "prototype" | "idea";
    contains_personal_data: false;
    items: SnapshotItem[];
    approved_by?: string;
    approved_at?: string;
    snapshot_hash?: string;
    // Added during prepare for chronicle:
    summary?: string;
    published_at?: string;
    tags?: string[];
}

export interface BuildSnapshotRequest {
    items: SnapshotItem[];
    truth_status: "verified" | "prototype" | "idea";
}

export interface ApproveSnapshotRequest {
    filename: string;
    approver_name: string; // "Micha"
}
