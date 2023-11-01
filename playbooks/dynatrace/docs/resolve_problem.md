# Resolve Dynatrace Problems with Event-Driven Ansible

The Dynatrace Problems API can surface all sorts of issues detected by OneAgent in your environment. In this demo, I will walk through the steps needed to integrate Event-Driven Ansible (EDA) with the Problems API and incorporate automated Service Now incident management steps. Instead of diving into the realm of Dynatrace Problems, I will use a custom event to trigger my downstream remediation process, focusing on the **integration** points.

### how it works
- EDA rulebook activated to listen to the Problems API
- Dynatrace Problem is detected or ingested from an external source (us in this demo)
- The rulebook processes incoming Problem and takes an action to launch a remediation job template
- The job template gathers details about the problem, creates an incident, restarts a service, and closes the problem & incident if successful

### process diagram

![Resolve Problem Process Diagram](resolve_problem.png)