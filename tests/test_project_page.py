from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def test_flagship_project_page_contract():
    page = (ROOT / "website" / "index.html").read_text()
    required = [
        "01 · Hero",
        "02 · Why this problem matters",
        "03 · Core idea",
        "04 · Architecture",
        "05 · My contribution",
        "06 · Experiments",
        "07 · Results",
        "08 · Failure analysis",
        "09 · Interactive demo",
        "10 · Scaling",
        "11 · Safety / limitations",
        "12 · Technical deep dive",
        "13 · Artifacts",
        "14 · Citation",
    ]
    for heading in required:
        assert heading in page
    for label in ["Paper", "Code", "Demo", "Benchmark", "Video"]:
        assert label in page
    assert "Aura Yavary" in page
    assert "1.33×" in page
    assert "engineering smoke" in page.lower()
    assert "sorelia-demo.mp4" in page
    assert "architecture.svg" in page
    assert "failure-frontier.svg" in page


def test_project_page_local_links_exist():
    page_path = ROOT / "website" / "index.html"
    page = page_path.read_text()
    hrefs = re.findall(r'href="([^"]+)"', page)
    for href in hrefs:
        if href.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target = (page_path.parent / href).resolve()
        assert target.exists(), f"missing local artifact link: {href}"


def test_interactive_demo_is_retained_fixture_not_marketing_claim():
    demo = (ROOT / "website" / "demo.html").read_text()
    assert "browser-real-0001" in demo
    assert "artifacts/browser_smoke.json" in demo
    assert "engineering demo, not a frontier-model result" in demo
    assert "Failure: memory" in demo
    assert "Recovery succeeded" in demo


def test_project_page_has_exactly_fourteen_numbered_sections():
    page = (ROOT / "website" / "index.html").read_text()
    assert "01 · Hero" in page
    numbers = re.findall(r'class="section-kicker">(\d{2}) ·', page)
    assert numbers == [f"{i:02d}" for i in range(2, 15)]


def test_public_visual_assets_and_video_exist():
    assets = ROOT / "website" / "assets"
    for name in ["architecture.svg", "architecture.png", "failure-frontier.svg", "failure-frontier.png", "project-card.png", "sorelia-demo.mp4"]:
        p = assets / name
        assert p.exists(), name
        assert p.stat().st_size > 1000, name


def test_public_hiring_artifacts_exist():
    for name in ["PROJECT_CARD.md", "INTERVIEW_TALK_TRACKS.md", "DEMO_NARRATION.md", "PUBLIC_RELEASE_CHECKLIST.md", "RESUME_BULLETS.md"]:
        assert (ROOT / "docs" / name).exists(), name


def test_video_is_evidence_labeled_not_screen_recording_claim():
    page = (ROOT / "website" / "index.html").read_text().lower()
    assert "trajectory replay visualization" in page
    assert "not a fabricated browser recording" in page
