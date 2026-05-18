# data/corpus.py

CORPUS = [
    # Doc 0 – Load balancing
    "The system employs a multi-tier load balancer using consistent hashing to distribute incoming "
    "HTTP traffic across a pool of stateless application servers. During peak load events, the load "
    "balancer automatically routes traffic away from overloaded nodes and activates standby replicas "
    "within 30 seconds using health-check polling intervals.",

    # Doc 1 – Autoscaling
    "Horizontal autoscaling is triggered when average CPU utilization exceeds 70% across the server "
    "fleet for more than 2 consecutive minutes. The autoscaling policy adds instances in batches of "
    "three, with a cooldown period of 5 minutes to prevent thrashing. A predictive scaling model "
    "trained on historical traffic patterns pre-warms instances before anticipated peak hours.",

    # Doc 2 – Caching (Redis)
    "A distributed Redis cluster is deployed as the primary caching layer, storing session tokens, "
    "frequently accessed API responses, and computed aggregations with configurable TTLs ranging from "
    "60 seconds to 24 hours. Cache invalidation follows a write-through strategy to maintain "
    "consistency between the cache and the underlying PostgreSQL database.",

    # Doc 3 – Message queues
    "The system uses event-driven architecture with Apache Kafka as the message broker. During high "
    "throughput scenarios, producers batch messages to reduce round-trip latency. Consumer groups "
    "scale horizontally, and partition rebalancing ensures no single consumer becomes a bottleneck "
    "under peak load conditions.",

    # Doc 4 – Data consistency / distributed transactions
    "Data consistency across distributed nodes is enforced through a two-phase commit (2PC) protocol "
    "for critical financial transactions. For non-critical data paths, eventual consistency is "
    "accepted, and conflict resolution uses a last-write-wins (LWW) strategy with vector clocks to "
    "detect and reconcile divergent replicas.",

    # Doc 5 – Circuit breaker
    "The circuit breaker pattern is implemented using Resilience4j to protect downstream services "
    "from cascading failures. When the error rate of a service exceeds 50% within a 10-second "
    "sliding window, the circuit opens and requests are redirected to a fallback handler, preventing "
    "resource exhaustion during system-wide overload events.",

    # Doc 6 – Rate limiting / API gateway
    "Rate limiting is enforced at the API gateway using a token bucket algorithm, allowing a burst "
    "capacity of 500 requests before throttling individual clients. The gateway also performs "
    "request coalescing to merge identical concurrent requests into a single upstream call, "
    "significantly reducing backend pressure during flash traffic spikes.",

    # Doc 7 – Observability
    "Observability is achieved through a three-pillar stack: Prometheus collects time-series metrics, "
    "Jaeger handles distributed tracing across microservice boundaries, and the ELK stack aggregates "
    "structured logs. Alerting rules fire when P99 latency exceeds 500ms or error rates cross 1% "
    "of total request volume.",

    # Doc 8 – Database replication
    "Database read replicas are provisioned across three availability zones to support read-heavy "
    "workloads without impacting primary write throughput. Replication lag is monitored continuously, "
    "and queries are automatically redirected to the primary node if replica lag exceeds 100ms, "
    "ensuring data freshness for time-sensitive operations.",

    # Doc 9 – Disaster recovery / failover
    "The disaster recovery plan specifies an RTO of 15 minutes and an RPO of 5 minutes. Continuous "
    "backups are streamed to object storage using WAL archiving for PostgreSQL. In the event of "
    "a primary region failure, automated failover promotes a warm standby replica in the secondary "
    "region and updates DNS routing within the defined RTO window.",
]
