from rtxlib.executionstrategy.ForeverStrategy import start_forever_strategy
from rtxlib.executionstrategy.StepStrategy import start_step_strategy
from rtxlib.executionstrategy.SelfOptimizerStrategy import start_self_optimizer_strategy
from rtxlib.executionstrategy.SequencialStrategy import start_sequential_strategy
# from rtxlib.executionstrategy.SeqRuntimeStrategy import start_seq_runtime_stategy
# from rtxlib.executionstrategy.DiscreteOptimizer import start_discrete_optimizer_strategy
# from rtxlib.executionstrategy.UCB1 import start_mab_ucb1_strategy
# from rtxlib.executionstrategy.DiscountUCB import start_mab_discount_ucb_strategy
# from rtxlib.executionstrategy.SWUCB import start_mab_sw_ucb_strategy
from rtxlib.executionstrategy.SimpleAdaptationManager import start_simple_am
from rtxlib import log_results, error, info

from rtxlib.executionstrategy.UncorrelatedSelfOptimizerStrategy import start_uncorrelated_self_optimizer_strategy


def run_execution_strategy(wf):
    """ we run the correct execution strategy """
    applyInitKnobs(wf)
    print(wf.execution_strategy["type"])
    try:
        # start the right execution strategy
        if wf.execution_strategy["type"] == "sequential":
            log_results(wf.folder, list(wf.execution_strategy["knobs"][0].keys()) + ["result"], append=False)
            start_sequential_strategy(wf)

        elif wf.execution_strategy["type"] == "self_optimizer":
            log_results(wf.folder, list(wf.execution_strategy["knobs"].keys()) + ["result"], append=False)
            start_self_optimizer_strategy(wf)

        # elif wf.execution_strategy["type"] == "discrete_optimizer":
        #     log_results(wf.folder, wf.execution_strategy["knobs"] + ["result"], append=False)
        #     start_discrete_optimizer_strategy(wf)

        elif wf.execution_strategy["type"] == "uncorrelated_self_optimizer":
            log_results(wf.folder, list(wf.execution_strategy["knobs"].keys()) + ["result"], append=False)
            start_uncorrelated_self_optimizer_strategy(wf)

        elif wf.execution_strategy["type"] == "step_explorer":
            log_results(wf.folder, list(wf.execution_strategy["knobs"].keys()) + ["result"], append=False)
            start_step_strategy(wf)
    
        elif wf.execution_strategy["type"] == "forever":
            start_forever_strategy(wf)

        elif wf.execution_strategy["type"] == "simple_am":
            start_simple_am(wf)

        # elif wf.execution_strategy["type"] == "sequential_runtime":
        #     print("got here")
        #     log_results(wf.folder, wf.execution_strategy["knobs"] + ["result"], append=False)
        #     start_seq_runtime_stategy(wf)
            
        # elif wf.execution_strategy["type"] == "mabandit_ucb1":
        #     print(type(wf.execution_strategy["knobs"]))
        #     log_results(wf.folder, wf.execution_strategy["knobs"] + ["result"], append=False)
        #     start_mab_ucb1_strategy(wf)

        # elif wf.execution_strategy["type"] == "discount_ucb":
            
        #     log_results(wf.folder, wf.execution_strategy["knobs"] + ["result"], append=False)
        #     start_mab_discount_ucb_strategy(wf)

        # elif wf.execution_strategy["type"] == "sliding_ucb":
            
        #     log_results(wf.folder, wf.execution_strategy["knobs"] + ["result"], append=False)
        #     start_mab_sw_ucb_strategy(wf)
            
    except RuntimeError:
        error("Stopped the whole workflow as requested by a RuntimeError")
    # finished
    info(">")
    applyDefaultKnobs(wf)


def applyInitKnobs(wf):
    """ we are done, so revert to default if given """
    if "pre_workflow_knobs" in wf.execution_strategy:
        try:
            info("> Applied the pre_workflow_knobs")
            wf.change_provider["instance"] \
                .applyChange(wf.change_event_creator(wf.execution_strategy["pre_workflow_knobs"]))
        except:
            error("apply changes did not work")


def applyDefaultKnobs(wf):
    """ we are done, so revert to default if given """
    if "post_workflow_knobs" in wf.execution_strategy:
        try:
            info("> Applied the post_workflow_knobs")
            wf.change_provider["instance"] \
                .applyChange(wf.change_event_creator(wf.execution_strategy["post_workflow_knobs"]))
        except:
            error("apply changes did not work")
