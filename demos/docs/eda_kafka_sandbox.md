# Quick Setup to Experiment with Kafka and Event-Driven Ansible

The content provided in this document will enable you to quickly setup Kafka (on RHEL), create a topic, and integrate with Event-Driven Ansible to experiment with rulebooks that represent a real-world implementation. This setup could be used for individual test environments or simply to learn about the product.

## Pre-requisites

- Infrastructure (virtual or physical) to host a lightweight RHEL server
  - I am leveraging AWS to host a RHEL EC2
  - Specs: RHEL 9.3, 2 vCPU, 4GB memory
  - _Given the lightweight deployment, I expecte this would work with various setups having similar characteristics_
- Ability to manage network setup
  - The role installs Kafka listening on 9093 for external connections (9092 if you are testing locally)
  - Ensure firewall / security group rules are properly configured to enable connections with Kafka
- Self-hosting would require a Red Hat developer account to access RHEL images
  - You would likely have success with Fedora
- Event-Driven Ansible
  - If you have a deployment of Ansible Automation Platform including EDA, then you're in good shape!
  - You can test using ansible-rulebook if full EDA capabilities are not readily available

## Installing Kafka

The [playbook](../../playbooks/aws/install_apps.yml) to install Kafka is designed to fit into a workflow that supports an end-user choosing apps they would like to deploy. The bulk of the work is done via the [kafka role](../../roles/kafka/README.md), which currently supports the following configuration:
- Java 11
- Kafka 3.7.0
- Scala 2.13
- Zookeeper deployment

### Important Variables
| Variable | Purpose | Default |
| --- | --- | --- |
| _hosts | Used to target specific hosts within an inventory | **_user must provide_** |
| install_apps | Used to determine which apps are installed | kafka |
| _kafka_mode | Designed to support multiple deployment methods (only zookeeper tested) | zookeeper |
| demo_topic | Name of topic to be created after install | **_user must provide_** |

## Testing Kafka

The [Apache Kafka Quickstart](https://kafka.apache.org/quickstart) is a great resource for testing your newly stood up Kafka environment. In fact, some of the tasks in my kafka role are sourced directly from this guide.

### Suggested Tests

The kafka role completes the following actions:
- installs kafka
- starts the relevant services
- configures the firewall
- creates a demo topic (if provided)

A couple of notes for running tests:
1. The binaries referenced will exist on the kafka host or any box you have installed kafka. They will be located in the kafka installation directory (e.g. `/opt/kafka`).
1. If you run this command from a remote box, then modify the `bootstrap-server` argument and use port 9093.

#### Create a topic

If you did not provide a demo topic to the automation, then create one yourself using the following command:
```
bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server localhost:9092
```

#### Publish messages to a topic

```
bin/kafka-console-producer.sh --topic quickstart-events --bootstrap-server localhost:9092
>This is my first event
>This is my second event
```

#### Consume messages from a topic

I recommend having two terminals open to simultaneously produce messages and consume them and observe Kafka in action. If you add the argument `--from-beginning`, then any previous test messages you produced will be read by the consumer.

```
bin/kafka-console-consumer.sh --topic quickstart-events --bootstrap-server localhost:9092
This is my first event
This is my second event
```

## Testing Event-Driven Ansible

The [rulebook](https://github.com/zjleblanc/ansible-eda-demos/blob/master/rulebooks/demo_kafka.yml) I use to subscribe to my Kafka topic leverages the ansible.eda.kafka event source plugin. As is common in the Ansible ecosystem, I benefit from open-source plugins and support from Red Hat when I use certified collections. I provide the important variables:
- host
- port
- topics

... and let the plugin do it's magic. If you have a chance to watch my video, I will walk through this integration in Ansible Automation Platform. While I do not have an example using ansible-rulebook, you can certainly clone the repostiory containing the rulebook (linked above) and test locally using the CLI.