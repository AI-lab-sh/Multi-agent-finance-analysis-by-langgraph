import app.graph.nodes.recommend as rec


def test_highlight_recommendation_buy():
    html = rec.highlight_recommendation("Strong BUY for AAPL")
    assert "BUY" in html and "background-color:green" in html


def test_highlight_recommendation_hold():
    html = rec.highlight_recommendation("We suggest to HOLD")
    assert "HOLD" in html and "background-color:yellow" in html


def test_highlight_recommendation_sell():
    html = rec.highlight_recommendation("Time to SELL")
    assert "SELL" in html and "background-color:red" in html


