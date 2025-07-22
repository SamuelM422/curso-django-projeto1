import math
from typing import Dict, Tuple, Any
from django.core.paginator import Paginator, Page
from django.http import HttpRequest
from django.db.models.query import QuerySet


def make_pagination_range(page_range: range, qty_pages: int, current_page: int) -> Dict[str, Any]:
    total_pages = len(page_range)
    middle_range = math.ceil(qty_pages / 2)
    start_range = current_page - middle_range
    stop_range = current_page + middle_range - 1

    if start_range < 0:
        start_range = 0
        stop_range = qty_pages

    if stop_range >= total_pages:
        stop_range = total_pages
        start_range = stop_range - qty_pages

    return {
        'pagination': page_range[start_range:stop_range],
        'page_range': page_range,
        'qtd_pages': qty_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > middle_range,
        'last_page_out_of_range': stop_range < total_pages
    }


def make_pagination(request: HttpRequest, recipes: QuerySet, per_page: int) -> Tuple[Dict[str, Any], Page]:
    """
    Handles pagination for a list of recipes, dividing them into pages and creating
    a range of numbers for the pagination display.

    This function retrieves the current page number from the request object,
    handles any errors from invalid page numbers, and then paginates the list
    of recipes. It also creates a customized pagination range to improve
    the user interface.

    Arguments:
        request: The HTTP request object containing query parameters.
        recipes: A list of recipes to be paginated.
        per_page: The number of recipes to display per page.

    Returns:
        A tuple containing:
        - pagination_range: A range object representing the customized pagination
          range to display.
        - page_object: The page object for the current page of recipes.
    """
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(recipes, per_page)
    page_object = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        5,
        current_page
    )
    
    return pagination_range, page_object