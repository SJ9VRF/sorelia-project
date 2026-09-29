from sorelia.doctor import doctor

def test_doctor_reports_core_runtime():
    r = doctor()
    assert r["ok_core"] is True
    assert "playwright" in r["packages"]
