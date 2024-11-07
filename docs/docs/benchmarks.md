# Benchmarks

<div class='subtitle'>Submit your own AI agent to be included in a benchmark comparison</div>

Invariant Labs hosts and maintains a public registry of AI agent benchmarks, that you can use to compare and inspect different AI agents on tasks such as coding, web browsing, customer support or productivity automation.

This document outlines the datasets and benchmarks that are currently available, and how you can submit your own AI agent to be included in a benchmark comparison.

## Benchmarks and Datasets

A benchmark is a collection of tasks and environment of a particular domain, that can be used to evaluate the performance of an AI agent system. To enable comparison between different AI agents, benchmarks are typically designed to be reproducible and standardized.

To facilitate the comparison of AI agents, Invariant hosts a number of popular benchmarks and respective AI agent results on the <img class='inline-invariant' src="assets/logo.svg"/> [Invariant Explorer](https://explorer.invariantlabs.ai).

<figure>

<svg width="671px" height="321px" viewBox="0 0 671 321" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <title>Group 5</title>
    <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
        <g id="Group-5">
            <rect id="Rectangle" fill="#F4F4F4" x="0" y="0" width="671" height="321" rx="52"></rect>
            <g id="Group-4" transform="translate(36.000000, 83.000000)">
                <g id="Group">
                    <rect id="Rectangle-Copy" stroke="#979797" fill="#E9FFD6" x="0.5" y="0.5" width="192" height="202" rx="16"></rect>
                    <text id="Agent-#1-results" font-family="NeueMontreal-Regular, Neue Montreal, Helvetica" font-size="26.8876632" font-weight="normal" fill="#0C0C13">
                        <tspan x="46.8653737" y="60">Agent #1</tspan>
                        <tspan x="51" y="99.0706807">Dataset</tspan>
                    </text>
                    <text id="score-0.3" font-family="PTMono-Regular, PT Mono" font-size="21.5101306" font-weight="normal" fill="#0C0C13">
                        <tspan x="38.4226474" y="164">score 0.3</tspan>
                    </text>
                </g>
                <g id="Group-2" transform="translate(210.000000, 0.000000)">
                    <rect id="Rectangle-Copy-2" stroke="#979797" fill="#FFCFEF" x="0.5" y="0.5" width="192" height="202" rx="16"></rect>
                    <text id="Agent-#2-results" font-family="NeueMontreal-Regular, Neue Montreal, Helvetica" font-size="26.8876632" font-weight="normal" fill="#0C0C13">
                        <tspan x="46.0421691" y="60">Agent #2</tspan>
                        <tspan x="51.9968663" y="99.0706807">Dataset</tspan>
                    </text>
                </g>
                <text id="score-0.34" font-family="PTMono-Regular, PT Mono" font-size="21.5101306" font-weight="normal" fill="#0C0C13">
                    <tspan x="241.969608" y="164">score 0.34</tspan>
                </text>
                <g id="Group-3" transform="translate(420.000000, 0.000000)">
                    <rect id="Rectangle-Copy-3" stroke="#979797" fill="#CCF6FF" x="0.5" y="0.5" width="192" height="202" rx="16"></rect>
                    <text id="Agent-#3-results" font-family="NeueMontreal-Regular, Neue Montreal, Helvetica" font-size="26.8876632" font-weight="normal" fill="#0C0C13">
                        <tspan x="43.8673992" y="60">Agent #3</tspan>
                        <tspan x="51" y="99.0706807">Dataset</tspan>
                    </text>
                </g>
            </g>
            <text id="WebArena-Benchmark" font-family="NeueMontreal-Regular, Neue Montreal, Helvetica" font-size="26.8876632" font-weight="normal" fill="#0C0C13">
                <tspan x="36" y="47">WebArena Benchmark</tspan>
            </text>
            <text id="score-0.5" font-family="PTMono-Regular, PT Mono" font-size="21.5101306" font-weight="normal" fill="#0C0C13">
                <tspan x="494.422647" y="247">score 0.5</tspan>
            </text>
        </g>
    </g>
</svg>

</figure>

Individual runs of a benchmark with a specific AI agent are stored as a separate Explorer datasets, as accessible via a unique `<username>/<dataset>` identifier on the Explorer.

A dataset includes all of an agent's reasoning, actions and interactions with the environment.

## Submitting New Agent Results

After you have built and evaluated an AI agent on a given benchmark, you can submit the resulting agent traces to be available for comparison on the Explorer.

This document describes the steps to submit your AI agent to the benchmark registry.

### Step 1: Setup the Invariant SDK and Prepare Your Traces

First, you need to install the Invariant SDK and prepare your agent traces for submission. To do so, follow the [Getting Started](./index.md) guide, that will guide you through the process of setting up the SDK and ensuring that your agent traces are in a compatible format.

### Step 2: Upload Your Agent Traces to the Explorer

Once you have prepared and ensured that your agent traces are in a compatible format, you can upload them to the Explorer into a new dataset. Carefully note the `<username>/<dataset>` identifier of the dataset, as you will need it in the next steps.

### Step 3: Associate Your Agent Dataset with a Benchmark and Score

WIP: Instructions on updating the datasets's metadata to include the `benchmark` and `accuracy` fields, that will associate your agent dataset with a specific benchmark and score.

For instance, to associate your agent dataset with the `webarena` benchmark and an accuracy score of `0.5`, you can update the dataset's metadata as follows:

```json
{
    "benchmark": "webarena",
    "accuracy": 0.5
}
```

### Step 4: Submit Your Results to the Benchmark Registry

Submit your agent dataset to be included in the official benchmark registry by contacting the Invariant Labs team at [registry@invariantlabs.ai](mailto:registry@invariantlabs.ai).

The team will then review and verify your submission, and include your agent dataset in the benchmark registry for comparison once approved.