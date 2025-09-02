from app.utils.portfolio import extract_portfolio_allocations, extract_portfolio_section


def test_extract_portfolio_allocations_parses_ranges_and_single_values():
    text = "Suggested Portfolio Allocation: 5-10% allocation of AAPL; 7% allocation to TSLA"
    out = extract_portfolio_allocations(text)
    # average of 5-10 is 7.5
    assert out["AAPL"] == 7.5
    assert out["TSLA"] == 7.0


def test_extract_portfolio_section_returns_only_section():
    text = (
        "Header\n\n"
        "Suggested Portfolio Allocation\nAAPL 5%\nTSLA 10%\n\n"
        "Footer"
    )
    section = extract_portfolio_section(text)
    assert "Suggested Portfolio Allocation" in section
    assert "Footer" not in section


def test_extract_portfolio_allocations_single_and_range():
    text = "Suggested Portfolio Allocation: 5-10% allocation of AAPL, 7% allocation to TSLA."
    allocations = extract_portfolio_allocations(text)
    assert allocations["AAPL"] == 7.5  # average of 5 and 10
    assert allocations["TSLA"] == 7.0


def test_extract_portfolio_section():
    text = (
        "Other text...\n\n"
        "Suggested Portfolio Allocation\n- 5% AAPL\n- 10% TSLA\n\n"
        "Footer"
    )
    section = extract_portfolio_section(text)
    assert "Suggested Portfolio Allocation" in section
    assert "5% AAPL" in section

