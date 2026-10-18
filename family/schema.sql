-- Family Line initial schema (v1)
CREATE TABLE IF NOT EXISTS records (
          id TEXT PRIMARY KEY, kind TEXT NOT NULL, title TEXT NOT NULL, body TEXT NOT NULL,
          source TEXT NOT NULL, demo INTEGER NOT NULL DEFAULT 0, version INTEGER NOT NULL DEFAULT 1,
          created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS resources (
          id TEXT PRIMARY KEY, title TEXT NOT NULL, mime TEXT, path TEXT, url TEXT,
          text TEXT NOT NULL, status TEXT NOT NULL, error TEXT, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS conversations (
          id TEXT PRIMARY KEY, role TEXT NOT NULL, channel TEXT NOT NULL, state TEXT NOT NULL,
          summary TEXT NOT NULL DEFAULT '', demo INTEGER DEFAULT 0, started_at TEXT, ended_at TEXT);
        CREATE TABLE IF NOT EXISTS messages (
          id INTEGER PRIMARY KEY AUTOINCREMENT, conversation_id TEXT NOT NULL REFERENCES conversations(id),
          speaker TEXT NOT NULL, text TEXT NOT NULL, utterance_id TEXT, created_at TEXT,
          UNIQUE(conversation_id, utterance_id));
        CREATE TABLE IF NOT EXISTS issues (
          id TEXT PRIMARY KEY, topic TEXT NOT NULL, title TEXT NOT NULL, status TEXT NOT NULL,
          owner TEXT NOT NULL DEFAULT '', created_at TEXT, updated_at TEXT);
        CREATE TABLE IF NOT EXISTS occurrences (
          id TEXT PRIMARY KEY, issue_id TEXT NOT NULL REFERENCES issues(id),
          conversation_id TEXT NOT NULL REFERENCES conversations(id), evidence TEXT, created_at TEXT,
          UNIQUE(issue_id, conversation_id));
        CREATE TABLE IF NOT EXISTS events (
          id TEXT PRIMARY KEY, title TEXT, detail TEXT, source TEXT, ref TEXT, created_at TEXT);
        CREATE TABLE IF NOT EXISTS jobs (
          id TEXT PRIMARY KEY, title TEXT NOT NULL, payload TEXT NOT NULL, due_at TEXT NOT NULL,
          status TEXT NOT NULL, mode TEXT NOT NULL, dedup_key TEXT UNIQUE,
          attempts INTEGER DEFAULT 0, result TEXT DEFAULT '', created_at TEXT);
        CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS proposals (
          id TEXT PRIMARY KEY, conversation_id TEXT, changes TEXT NOT NULL, status TEXT NOT NULL, created_at TEXT);
        CREATE TABLE IF NOT EXISTS operations (key TEXT PRIMARY KEY, result TEXT NOT NULL);
        CREATE INDEX IF NOT EXISTS ix_messages_conversation ON messages(conversation_id,id);
        CREATE INDEX IF NOT EXISTS ix_jobs_due ON jobs(status,due_at);
PRAGMA user_version=1;

CREATE TABLE IF NOT EXISTS conversation_resources (
 conversation_id TEXT NOT NULL REFERENCES conversations(id),
 resource_id TEXT NOT NULL REFERENCES resources(id) ON DELETE CASCADE,
 PRIMARY KEY(conversation_id,resource_id));
CREATE TABLE IF NOT EXISTS proposal_resources (
 proposal_id TEXT NOT NULL REFERENCES proposals(id),
 resource_id TEXT NOT NULL REFERENCES resources(id) ON DELETE CASCADE,
 text TEXT NOT NULL, expected_text TEXT NOT NULL,
 PRIMARY KEY(proposal_id,resource_id));
CREATE TABLE IF NOT EXISTS issue_notes (
 id TEXT PRIMARY KEY, issue_id TEXT NOT NULL REFERENCES issues(id),
 author TEXT NOT NULL, text TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS call_outcomes (
 conversation_id TEXT PRIMARY KEY REFERENCES conversations(id),
 topic TEXT NOT NULL, outcome TEXT NOT NULL, summary TEXT NOT NULL);
