import pulumi
import pulumi_observe as observe
from provider import observe_provider


# Attach the provider explicitly to get_workspace
workspace = observe.get_workspace(
    name="Default",
    opts=pulumi.InvokeOptions(provider=observe_provider)
)

pulumi.export("workspace_id", workspace.oid)



# Lookup the usage metrics dataset
usage_dataset = observe.get_dataset(
    name="usage/Observe Usage Metrics",
    workspace=workspace.oid,  # exact name from UI
    opts=pulumi.InvokeOptions(provider=observe_provider)
)

# Create a usage-based threshold monitor

workspace_id = workspace.oid
dataset_id = usage_dataset.oid

monitor = observe.MonitorV2("usage-pulumi-monitor",
    name="Usage Pulumi Monitor",
    description="",
    workspace=workspace.oid,
    inputs={
        "credits_adhoc_query_from_usage/Observe Usage Metrics": usage_dataset.oid
    },
    custom_variables='{"message": "", "title": ""}',
    data_stabilization_delay="0s",
    disabled=False,
    lookback_time="10m0s",
    rule_kind="threshold",
    groupings=[
        observe.MonitorV2GroupingArgs(
            link_column=observe.MonitorV2GroupingLinkColumnArgs(
                name="User"
            )
        )
    ],
    rules=[
        observe.MonitorV2RuleArgs(
            level="error",
            threshold=observe.MonitorV2RuleThresholdArgs(
                aggregation="all_of",
                value_column_name="A_credits_adhoc_query_avg",
                compare_values=[
                    observe.MonitorV2RuleThresholdCompareValueArgs(
                        compare_fn="greater",
                        value_float64s=[10.0]
                    )
                ]
            )
        )
    ],
    stages=[
        observe.MonitorV2StageArgs(
            output_stage=False,
            pipeline="""
                align 1m, frame(back: 2m), A_credits_adhoc_query_avg:avg(m("credits_adhoc_query"))
                aggregate A_credits_adhoc_query_avg:avg(A_credits_adhoc_query_avg), group_by(^User...)
            """
        )
    ],
    opts=pulumi.ResourceOptions(provider=observe_provider)
)
