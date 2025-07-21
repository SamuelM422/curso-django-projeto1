import math

def make_pagination_range(page_range, qty_pages, current_page):
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
