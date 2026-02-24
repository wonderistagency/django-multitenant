import operator
from functools import reduce

from django.db.models import Q

from .utils import get_current_tenant, get_tenant_filters


def related_objects(obj, related_model, related_fields, objs):
    """
    Override of Collector.related_objects. Returns the filter for the related objects
    Different from the original method, this method adds the tenant filters to the query.
    CAUTION: When Collector.related_objects is changed, this method should be updated accordingly.
    """
    filters = {}
    predicate = reduce(
        operator.or_,
        (Q(**{f"{related_field.name}__in": objs}) for related_field in related_fields),
    )

    if get_current_tenant():
        try:
            filters = get_tenant_filters(related_model)
        except ValueError:
            pass
    # pylint: disable=protected-access
    return related_model._base_manager.using(obj.using).filter(predicate, **filters)
