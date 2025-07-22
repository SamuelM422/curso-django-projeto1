from unittest import TestCase
from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range = list(range(1, 21)),
            qty_pages = 5,
            current_page = 2,
        )

        self.assertEqual([1, 2, 3, 4, 5], pagination['pagination'])

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=5,
        )

        self.assertEqual([3, 4, 5, 6, 7], pagination['pagination'])

    def test_make_sure_middle_ranges_are_correct(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=10,
        )

        self.assertEqual([8, 9, 10, 11, 12], pagination['pagination'])

    def test_make_sure_last_range_is_correct(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=19,
        )

        self.assertEqual([16, 17, 18, 19, 20], pagination['pagination'])