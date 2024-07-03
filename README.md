# FaaSTrainGym_v1
An open-source Gymnasium compatible Serverless/FaaS environment for Reinforcement Learning experiments

---

## Installation

To install the base Gymnasium library, use `pip install gymnasium` <br>
To install the official Kubernetes Python client, use `pip install kubernetes` <br>
To install the Prometheus Python client, use `pip install prometheus-api-client` <br>

## Current Python Support

Gymnasium API - Python 3.8+ on Linux and MacOS. For updates, please check the [official documentation](https://github.com/Farama-Foundation/Gymnasium) <br>
Kubernetes Python Client - Python 3.6+ on Linux and MacOS. For updates, please check the [official documentation](https://github.com/kubernetes-client/python)
Prometheus Python Client - For updates, please check the [official documentation](https://github.com/prometheus/client_python?tab=readme-ov-file)

---

## Gymnasium Environment for Serverless Reinforcement Learning Agents
The current implementation of the serverless environment is based on the OpenFaaS framework and the Kubernetes cluster. The serverless environment is compatible with the Gymnasium API and can be used to train and evaluate Reinforcement Learning agents in a practical serverless environment. The serverless environment is designed to be scalable and can be used to train multiple agents in parallel.

To illustrate the serverless/FaaS environment, we will use the Kubernetes cluster as the underlying infrastructure. OpenFaaS CLI will be used to deploy the functions to the Kubernetes cluster as Pods and will be managed internally by OpenFaaS API via the Kubernetes API. For the purpose of this illustration, we will use the Kubernetes Python client to interact with the Kubernetes API and therefore, other Kubernetes based serverless frameworks can be used as well.

### Serverless Function Auto-Scaling Scenario

The environment consists of the serverless functions, deployed as Kubernetes Pods, and expects a periodic user-requests pattern. These functions are designed to be stateless and can be scaled horizontally based on the user-requests pattern. The agent interacts with the environment by sending the __scale__ action to increase or decrease the number of serverless functions based on the current state of the environment. The goal of the agent is to maintain the optimal number of serverless functions to minimize the cost and maximize the performance of the environment/serverless functions.

#### Environment Configuration
The environment consists of the following components:
1. __State (S)__: The current state of the environment is represented by the number of serverless functions deployed as Kubernetes Pods, the performance metrics such as the average CPU and memory utilisation of the functions, the average response time of the functions, the number of user-requests, and the average throughput of the functions.
2. __Actions (A)__: The agent can take two `Discrete` actions: __scale-up__ and __scale-down__ to increase or decrease the number of serverless functions deployed as Kubernetes Pods.
3. __Rewards (R)__: The agent receives a reward based on the performance metrics of the functions. The goal is to minimize the number of function pods and maximize their performance such as improving the throughput, average CPU and memory utilisation.
4. __Observations (O)__: The agent receives the current state of the environment as an observation. The observation consists of the current state of the environment and the performance metrics of the serverless functions.
5. __Termination__: As the process of scaling is non-episodic/continuous, an episode terminates when the agent reaches the maximum number of episodes (`default 10` steps) and a `done` signal is sent to the agent.