#!/usr/bin/env python

from django.contrib.admin.templatetags.admin_list import items_for_result, result_headers
from django.template import Library
from django.utils.safestring import mark_safe
register = Library()


def results(cl, additional_links):
    """
    Rewrite of original function to add additional columns after each result
    in the change list.
    """
    for res in cl.result_list:
        rl = list(items_for_result(cl,res))
        for link in additional_links:
        rl.append(mark_safe(link['url_template'] % (VAR,))) # Make sure you have enough VARs for any %s's in your extra content. Note mark_safe
        yield rl

def extended_result_list(cl, additional_links):
    """
    Rewrite of original function to add an additional columns after each result
    in the change list.
    """
    headers = list(result_headers(cl))
    for header in additional_links:
        headers.append(header)

    return {
        'cl': cl,
        'result_headers': headers,
        'results': list(results(cl, additional_links))
    }

# This function is an example template tag for use in an overridden change_list.html template.
def my_model_result_list(cl):
    additional_links = (
        { 'text': 'Actions',
          'sortable': False,
          'url_template': '<td>YOUR ADDITIONAL CONTENT HERE</td>'
        },
    )

    return extended_result_list(cl, additional_links)
my_model_result_list = register.inclusion_tag("admin/change_list_results.html")(my_model_result_list)
