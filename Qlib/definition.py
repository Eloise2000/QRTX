# Simple sequantial run of knob values
name = "Q-RTX"

execution_strategy = {
    "ignore_first_n_results": 100,
    "sample_size": 100,
    "type": "sequential",
    "knobs": [
        {" average_edge_duration_factor": 1},
        {" average_edge_duration_factor": 1.2},
        {" average_edge_duration_factor": 1.7},
        {" average_edge_duration_factor": 2.5}
    ]
}


def primary_data_reducer(state, newData, wf):
    cnt = state["count"]
    state["avg_overhead"] = (state["avg_overhead"] * cnt + newData["overhead"]) / (cnt + 1)
    state["count"] = cnt + 1
    return state


primary_data_provider = {
    "type": "kafka_consumer",
    "kafka_uri": "kafka:9092",
    "topic": "crowd-nav-trips",
    "serializer": "JSON",
    "data_reducer": primary_data_reducer
}

change_provider = {
    "type": "kafka_producer",
    "kafka_uri": "kafka:9092",
    "topic": "crowd-nav-commands",
    "serializer": "JSON",
}


def evaluator(resultState, wf):
    return resultState["avg_overhead"]


def state_initializer(state, wf):
    state["count"] = 0
    state["avg_overhead"] = 0
    return state
