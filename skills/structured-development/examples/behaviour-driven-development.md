# Behaviour-driven development

## Source and scope

- [Cucumber: Behaviour-Driven Development](https://cucumber.io/docs/bdd/).

The source describes discovery, formulation, and automation: collaborate on concrete examples, document them in an automatable form, then implement the behaviour starting with an automated test. It explicitly positions BDD as an enhancement to an existing agile process, not a replacement for it.

## Mapping to the abstract procedure

This is our interpretation using the [contract and evidence labels](../SKILL.md#researched-examples).

| Responsibility | Mapping and limits |
| --- | --- |
| [1. Intent and boundaries](../SKILL.md#1-establish-intent-and-boundaries) | **Partial:** discovery develops shared understanding of needs, rules, and scope. Decision authority still needs to be specified. |
| [2. Structure the work](../SKILL.md#2-structure-the-work) | **Supported:** small stories and concrete examples break problems into manageable pieces; discovery can expose lower-priority functionality to defer. |
| [3. Prepare the next increment](../SKILL.md#3-select-and-prepare-the-next-increment) | **Partial:** formulate a valuable example and check agreement before automation. The surrounding process must address dependencies and material risks. |
| [4. Execute](../SKILL.md#4-execute-the-increment) | **Supported:** automate an example, observe its failure, and implement the described behaviour. |
| [5. Evaluate](../SKILL.md#5-evaluate-the-result) | **Partial:** automated examples check behaviour; collaboration checks shared understanding. Broader quality and integration criteria need suitable evidence. |
| [6. Reconcile and adapt](../SKILL.md#6-reconcile-and-adapt) | **Supported:** move back to discovery when more information is needed, evolve shared understanding, and respond to feedback after each example. |
| [7. Close the scope](../SKILL.md#7-close-the-agreed-scope) | **Partial:** accumulated examples preserve an executable account of behaviour. Overall acceptance and handoff remain responsibilities of the enclosing process. |

## What remains implementation-specific

Collaborative discovery, executable examples, and test-first automation are the source's practices. They need not be imposed on every structured-development implementation. Gherkin and Cucumber are not requirements of the abstract contract.

**Lesson for the abstraction:** discovering what is needed, agreeing what should happen, and observing what actually happens are distinct responsibilities with feedback between them.
