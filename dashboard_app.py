
import json, time
from pathlib import Path
import pandas as pd
import streamlit as st

OUT = Path("interview_monitor_output")
st.set_page_config(page_title="Interview Monitoring Dashboard", layout="wide")
st.title("Interview Monitoring Dashboard")
st.caption("Photo-based review signals. Flags are heuristic and require human review.")

def read_jsonl(path):
    if not path.exists(): return []
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            try: rows.append(json.loads(line))
            except json.JSONDecodeError: continue
    return rows

observations = read_jsonl(OUT / "observations.jsonl")
batches = read_jsonl(OUT / "batches.jsonl")
latest = observations[-1] if observations else None
c1, c2, c3, c4 = st.columns(4)
c1.metric("Photos analyzed", len(observations))
c2.metric("Batches", len(batches))
c3.metric("Review flags", sum(bool(b.get("review_flag")) for b in batches))
c4.metric("Latest cue count", len(latest.get("cues", [])) if latest else 0)

if latest:
    st.subheader("Latest analyzed photo")
    left, right = st.columns([1.2, 1])
    with left:
        img = latest.get("annotated_path")
        if img and Path(img).exists(): st.image(img, caption=latest.get("captured_at", ""), width="stretch")
    with right:
        st.write("**Face present:**", latest.get("face_present"))
        st.write("**Face count:**", latest.get("face_count"))
        st.write("**Person count:**", latest.get("person_count"))
        st.write("**Gaze direction (approx.):**", latest.get("gaze_direction"))
        st.write("**Head direction (approx.):**", latest.get("head_direction"))
        st.write("**Detected devices:**", latest.get("devices", []))
        st.write("**Current cues:**", latest.get("cues", []))

st.subheader("5-second batch review")
if batches:
    bdf = pd.DataFrame(batches)
    batch_cols = [c for c in [
        "created_at", "photos_analyzed", "face_present_photos", "face_missing_photos",
        "gaze_away_photos", "head_turned_photos", "multiple_face_photos",
        "additional_person_photos", "device_photo_counts", "gaze_directions",
        "head_directions", "persistent_cues", "review_reasons", "review_flag", "status"
    ] if c in bdf.columns]
    st.dataframe(bdf[batch_cols].iloc[::-1], width="stretch", hide_index=True)
    if batches:
        latest_batch = batches[-1]
        st.write("**Latest batch review reasons:**", latest_batch.get("review_reasons", []))
        st.caption("The batch checks whether gaze/head deviations persist across photos; it does not verify identity across frames or prove cheating.")
else: st.info("No batch results yet. Start the notebook pipeline and wait for a batch window.")

st.subheader("Photo observations")
if observations:
    odf = pd.DataFrame(observations)
    cols = [c for c in ["captured_at", "index", "face_present", "face_count", "person_count", "gaze_direction", "head_direction", "devices", "cues"] if c in odf]
    st.dataframe(odf[cols].iloc[::-1], width="stretch", hide_index=True)

if st.button("Refresh dashboard"):
    st.rerun()
time.sleep(2)
st.rerun()
