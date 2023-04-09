from main import set_page_return_current_page

def test_set_page_return_current_page():
    assert set_page_return_current_page(3) == 3
    assert set_page_return_current_page(10) == 10
    assert set_page_return_current_page(5) == 5
