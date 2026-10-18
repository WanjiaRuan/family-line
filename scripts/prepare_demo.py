"""Prepare the fictional TV case in a new data directory; never replace call history."""
import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def prepare(data_dir):
    from family import store, demo

    target = Path(data_dir).expanduser().resolve()
    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        raise ValueError("Choose an empty directory. Existing data, credentials and calls are never overwritten.")
    source_dir = ROOT / "examples" / "tv-demo"
    names = ("roku-tv-remote.jpg", "household-note.txt", "source-notes.md")
    for name in names:
        if not (source_dir / name).is_file():
            raise ValueError(f"Missing bundled example: {name}")
    store.DATA = target
    store.init()
    uploads = target / "uploads"
    uploads.mkdir(exist_ok=True)
    for name in names:
        shutil.copy2(source_dir / name, uploads / name)
    note = (source_dir / "household-note.txt").read_text()
    source_notes = (source_dir / "source-notes.md").read_text()
    photo_note = (
        "Black Roku remote with a purple directional pad and OK in the middle. "
        "The house-shaped Home button is at the top right. The white Netflix button "
        "has red lettering, below playback controls and to the left of Disney+. "
        "This reference photo does not establish the caller's current screen. "
        "Photo: Texas Lane, Wikimedia Commons, CC BY-SA 4.0, unchanged. "
        + demo.PHOTO_SOURCE
    )
    with store.db() as conn:
        # Only this newly created fixture is touched: omit legacy scripted calls.
        conn.execute("DELETE FROM occurrences")
        conn.execute("DELETE FROM issues")
        conn.execute("DELETE FROM messages")
        conn.execute("DELETE FROM conversations")
        ids = store.apply_changes_in(conn, [{
            "kind": "device", "title": "June's Roku streaming setup and remote", "body": note
        }], "prepared-demo")
        conn.execute("UPDATE records SET demo=1 WHERE id=?", (ids[0],))
        for name, mime, text, url in (
            (names[0], "image/jpeg", photo_note, demo.PHOTO_SOURCE),
            (names[1], "text/plain", note, None),
            (names[2], "text/markdown", source_notes, None),
        ):
            conn.execute("INSERT INTO resources VALUES(?,?,?,?,?,?,?,?,?)", (
                store.ident("res"), name, mime, str(uploads / name), url,
                text, "ready", None, store.now(),
            ))
        store.event(conn, "Prepared household loaded", "Fictional TV context and attributed sources; no real call or AI request was made.", "prepared-demo")
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", required=True, type=Path, help="New or empty directory for the fictional household.")
    args = parser.parse_args()
    try:
        target = prepare(args.data_dir)
    except ValueError as exc:
        parser.error(str(exc))
    print(f"Prepared fictional household: {target}")
    print("The Roku setup and three source files are ready. No API calls, phone calls or real transcripts were created.")
    print("Set FAMILY_DATA_DIR to this directory when launching if it is not the default data/ folder.")


if __name__ == "__main__":
    main()
