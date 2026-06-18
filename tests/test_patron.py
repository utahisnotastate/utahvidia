
def test_patron_free_profiles():
    from utahvidia import UtahRealityEngine
    from utahvidia.patron import apply_gaming_profile, list_profiles

    assert "competitive" in list_profiles()
    engine = UtahRealityEngine()
    cfg = apply_gaming_profile(engine, "competitive")
    assert cfg["alpha"] == 0.75


def test_patron_locked_without_unlock():
    from utahvidia import UtahRealityEngine
    from utahvidia.patron import apply_gaming_profile, is_patron_unlocked
    import pytest

    if is_patron_unlocked():
        pytest.skip("patron already unlocked in environment")
    engine = UtahRealityEngine()
    with pytest.raises(PermissionError):
        apply_gaming_profile(engine, "patron_max")


def test_patron_status():
    from utahvidia.patron import patron_status

    s = patron_status()
    assert s.paypal_email == "utah@utahcreates.com"
    assert "competitive" in s.available_profiles
