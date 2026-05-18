# Retrieval Benchmark: Strategy A vs Strategy B

> **Strategy A** — Raw Vector Search: embed the query as-is and retrieve nearest neighbors.
> **Strategy B** — AI-Enhanced Retrieval: expand the query via a generative model first, then retrieve.

---

## Query 1

**Input:** `How does the system handle peak load?`

### A - Raw Vector Search
| Rank | Doc ID | Cosine Score | Snippet |
|:----:|:------:|:------------:|---------|
| 1 | 0 | 0.6127 | The system employs a multi-tier load balancer using consistent hashing to distribute incoming HTTP traffic across a pool of stateless application servers. Durin... |
| 2 | 1 | 0.4986 | Horizontal autoscaling is triggered when average CPU utilization exceeds 70% across the server fleet for more than 2 consecutive minutes. The autoscaling policy... |
| 3 | 3 | 0.3722 | The system uses event-driven architecture with Apache Kafka as the message broker. During high throughput scenarios, producers batch messages to reduce round-tr... |

### B - AI-Enhanced Retrieval
> **Expanded query:**  
> _Describe the autoscaling policies, load balancing algorithms, and traffic management strategies used during high-traffic events and peak load conditions, including horizontal scaling, request queuing, circuit breaker activation, and Kafka consumer group rebalancing._

| Rank | Doc ID | Cosine Score | Snippet |
|:----:|:------:|:------------:|---------|
| 1 | 1 | 0.6742 | Horizontal autoscaling is triggered when average CPU utilization exceeds 70% across the server fleet for more than 2 consecutive minutes. The autoscaling policy... |
| 2 | 0 | 0.6273 | The system employs a multi-tier load balancer using consistent hashing to distribute incoming HTTP traffic across a pool of stateless application servers. Durin... |
| 3 | 3 | 0.6236 | The system uses event-driven architecture with Apache Kafka as the message broker. During high throughput scenarios, producers batch messages to reduce round-tr... |

---

## Query 2

**Input:** `What caching mechanisms are used to improve performance?`

### A - Raw Vector Search
| Rank | Doc ID | Cosine Score | Snippet |
|:----:|:------:|:------------:|---------|
| 1 | 2 | 0.5167 | A distributed Redis cluster is deployed as the primary caching layer, storing session tokens, frequently accessed API responses, and computed aggregations with ... |
| 2 | 3 | 0.3930 | The system uses event-driven architecture with Apache Kafka as the message broker. During high throughput scenarios, producers batch messages to reduce round-tr... |
| 3 | 8 | 0.3849 | Database read replicas are provisioned across three availability zones to support read-heavy workloads without impacting primary write throughput. Replication l... |

### B - AI-Enhanced Retrieval
> **Expanded query:**  
> _Explain the distributed caching strategies including Redis TTL configuration, write-through cache invalidation, in-memory cache layers, and how caching reduces PostgreSQL pressure and improves response latency for frequently accessed API responses and session tokens._

| Rank | Doc ID | Cosine Score | Snippet |
|:----:|:------:|:------------:|---------|
| 1 | 2 | 0.8655 | A distributed Redis cluster is deployed as the primary caching layer, storing session tokens, frequently accessed API responses, and computed aggregations with ... |
| 2 | 8 | 0.5010 | Database read replicas are provisioned across three availability zones to support read-heavy workloads without impacting primary write throughput. Replication l... |
| 3 | 3 | 0.4557 | The system uses event-driven architecture with Apache Kafka as the message broker. During high throughput scenarios, producers batch messages to reduce round-tr... |

---

## Query 3

**Input:** `How is data consistency maintained across distributed nodes?`

### A - Raw Vector Search
| Rank | Doc ID | Cosine Score | Snippet |
|:----:|:------:|:------------:|---------|
| 1 | 4 | 0.6730 | Data consistency across distributed nodes is enforced through a two-phase commit (2PC) protocol for critical financial transactions. For non-critical data paths... |
| 2 | 8 | 0.5483 | Database read replicas are provisioned across three availability zones to support read-heavy workloads without impacting primary write throughput. Replication l... |
| 3 | 2 | 0.4828 | A distributed Redis cluster is deployed as the primary caching layer, storing session tokens, frequently accessed API responses, and computed aggregations with ... |

### B - AI-Enhanced Retrieval
> **Expanded query:**  
> _Describe the consistency models (eventual consistency, strong consistency via 2PC), distributed transaction strategies, vector clock conflict resolution, database read replica replication lag handling, and last-write-wins approaches across distributed nodes._

| Rank | Doc ID | Cosine Score | Snippet |
|:----:|:------:|:------------:|---------|
| 1 | 4 | 0.7532 | Data consistency across distributed nodes is enforced through a two-phase commit (2PC) protocol for critical financial transactions. For non-critical data paths... |
| 2 | 8 | 0.6610 | Database read replicas are provisioned across three availability zones to support read-heavy workloads without impacting primary write throughput. Replication l... |
| 3 | 2 | 0.4884 | A distributed Redis cluster is deployed as the primary caching layer, storing session tokens, frequently accessed API responses, and computed aggregations with ... |

---
