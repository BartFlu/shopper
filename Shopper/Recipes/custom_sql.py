def chain_filters(cls, column, operator, value_list):
    """
    function to chain filters based on list of values.
    :param cls: model class
    :param column: column to perform filter on
    :param operator: lookup operator
    :param value_list: list of values to filter for
    :return:
    """
    myfilter = column + '__' + operator
    query = cls.objects
    for value in value_list:
        query = query.filter(**{myfilter:value})
    return query
