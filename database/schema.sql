-- Draft SQLite schema for the Blenrep NZ CSP Portal prototype.
-- This schema is for local proof-of-concept use only and is not production-ready.

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    display_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL,
    organisation TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Future users detail: identity provider subject, MFA status, and professional registration checks.

CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clinic_patient_code TEXT NOT NULL UNIQUE,
    site_name TEXT,
    treating_hcp_name TEXT,
    first_paid_dose_date TEXT,
    current_status TEXT NOT NULL,
    created_by_user_id INTEGER,
    created_by_role TEXT,
    haematologist_user_id INTEGER,
    pharmacist_user_id INTEGER,
    site_code TEXT,
    free_dose_start_date TEXT,
    free_dose_end_date TEXT,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by_user_id) REFERENCES users(id),
    FOREIGN KEY (haematologist_user_id) REFERENCES users(id),
    FOREIGN KEY (pharmacist_user_id) REFERENCES users(id)
);

-- Future patients detail: confirm minimal patient fields, retention, and privacy requirements.

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    order_sequence INTEGER,
    order_type TEXT NOT NULL,
    order_status TEXT NOT NULL DEFAULT 'draft',
    requested_date TEXT,
    submitted_by_user_id INTEGER,
    non_sensitive_reference TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (submitted_by_user_id) REFERENCES users(id)
);

-- Future orders detail: final reorder approval model and external communication references.

CREATE TABLE IF NOT EXISTS paid_dose_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    dose_number INTEGER NOT NULL,
    dose_date TEXT,
    funding_type TEXT NOT NULL DEFAULT 'private_paid',
    attested_by_user_id INTEGER,
    attestation_status TEXT NOT NULL DEFAULT 'pending',
    verified_by_user_id INTEGER,
    verified_at TEXT,
    evidence_reference TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (attested_by_user_id) REFERENCES users(id),
    FOREIGN KEY (verified_by_user_id) REFERENCES users(id)
);

-- Future paid dose detail: decide whether evidence uploads are required and how they are stored.

CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT,
    recipient_role TEXT,
    recipient_email TEXT,
    message TEXT,
    status TEXT NOT NULL DEFAULT 'simulated',
    recipient_role_key TEXT,
    recipient_user_id INTEGER,
    patient_id INTEGER,
    milestone_key TEXT,
    subject TEXT,
    delivery_channel TEXT NOT NULL DEFAULT 'in_app_simulated',
    delivery_status TEXT NOT NULL DEFAULT 'queued',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    sent_at TEXT,
    FOREIGN KEY (recipient_user_id) REFERENCES users(id),
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

-- Future notifications detail: approved message templates and no-sensitive-info email rules.

CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_action TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id TEXT,
    performed_by_user_id INTEGER,
    performed_by_display_name TEXT,
    performed_by_role TEXT,
    details TEXT,
    actor_user_id INTEGER,
    actor_role_key TEXT,
    details_json TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (performed_by_user_id) REFERENCES users(id),
    FOREIGN KEY (actor_user_id) REFERENCES users(id)
);

-- Future audit log detail: immutability controls, request IDs, IP/user-agent capture, and retention policy.
