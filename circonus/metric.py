"""

circonus.metric
~~~~~~~~~~~~~~~

Manipulate check metrics.

"""

from collections import OrderedDict

from circonus.util import colors


def get_metrics(check_bundle, metric_re):
    """Get a list of metrics from ``check_bundle``.

    :param dict check_bundle: A check bundle with metrics.
    :param re metric_re: Regular expression matching metrics to return.
    :rtype: :py:class:`list`

    """
    return [m for m in check_bundle["metrics"] if metric_re.match(m["name"])]


def get_metrics_sorted_by_suffix(metrics, suffixes):
    """Get a list of metrics sorted by suffix from the list of metrics.

    :param list metrics: Metrics to sort.
    :param list suffixes: Sorted list of suffixes used to sort the return metrics list.
    :rtype: :py:class:`list`

    Sort the ``metrics`` list by metric names ending with values in the ``suffixes`` list.  When creating graphs with
    stacked metrics the order in which metrics are stacked affects the manner in which they are displayed, e.g.,
    perhaps "free" memory makes the most sense when it is at the top of a memory graph.

    """
    metrics_map = OrderedDict.fromkeys(suffixes)
    for m in metrics:
        for s in suffixes:
            if m["name"].endswith(s):
                metrics_map[s] = m
                break
    return metrics_map.values()


def get_datapoints(check_id, metrics, custom=None):
    """Get a list of datapoints for ``check_id`` from ``metrics``.

    :param str check_id: The check id.
    :param list metrics: The metrics.
    :param dict custom: (optional) The custom datapoint attributes used to update each datapoint.
    :rtype: :py:class:`list`

    Datapoints determine how ``metrics`` are rendered on a `graph
    <https://login.circonus.com/resources/api/calls/graph>`_.  This function merges values from metrics with a few
    default values of required datapoint attributes.  Datapoint attributes can be overridden with the ``custom``
    parameter.  The ``custom`` :py:class:`dict` is used to :py:meth:`~dict.update` each datapoint as it is created.

    """
    if custom is None:
        custom = {}

    c = colors(metrics)
    datapoints = []
    for m in metrics:
        dp = {"alpha": m.get("alpha"),
              "axis": "l",
              "check_id": check_id,
              "color": c.next().get_hex_l(),
              "data_formula": m.get("data_formula"),
              "hidden": m.get("hidden", False),
              "legend_formula": m.get("legend_formula"),
              "metric_name": m.get("name"),
              "metric_type": m.get("type"),
              "name": m.get("name"),
              "stack": m.get("stack")}
        dp.update(custom)
        datapoints.append(dp)
    return datapoints