---
document_id: EXT-KAFKA-001
title: Apache Kafka — Operations Monitoring
document_type: public_reference
service: event-streaming
version: current
product: upstream-technology
created_at: 2026-09-25
updated_at: 2026-09-25
environment: [staging, production]
tags: [kafka, consumer-lag, monitoring]
publisher: Apache Software Foundation
source_url: https://kafka.apache.org/43/operations/monitoring/
license: Apache-2.0
---

# Apache Kafka — Operations Monitoring

> Official upstream documentation imported for operational reference. Always verify the linked current documentation before making production changes.

**Publisher:** Apache Software Foundation  
**Official source:** https://kafka.apache.org/43/operations/monitoring/  
**License:** Apache-2.0

## Imported reference content

Monitoring | Apache Kafka

View page source

Edit this page

Create child page

Create documentation issue

Print entire section

Tag Cloud

Apis 1

Configuration 34

Connect 34

Design 34

Developer-Guide 34

Docs 2106

Getting-Started 34

Implementation 34

Kafka 2106

Ops 34

Security 34

Streams 68

Monitoring

Monitoring

Tags:

Kafka

Docs

Kafka uses Yammer Metrics for metrics reporting in the server. The Java clients use Kafka Metrics, a built-in metrics registry that minimizes transitive dependencies pulled into client applications. Both expose metrics via JMX and can be configured to report stats using pluggable stats reporters to hook up to your monitoring system.

All Kafka rate metrics have a corresponding cumulative count metric with suffix

-total

. For example,

records-consumed-rate

has a corresponding metric named

records-consumed-total

The easiest way to see the available metrics is to fire up jconsole and point it at a running kafka client or server; this will allow browsing all metrics with JMX.

Security Considerations for Remote Monitoring using JMX

Apache Kafka disables remote JMX by default. You can enable remote monitoring using JMX by setting the environment variable

JMX_PORT

for processes started using the CLI or standard Java system properties to enable remote JMX programmatically. You must enable security when enabling remote JMX in production scenarios to ensure that unauthorized users cannot monitor or control your broker or application as well as the platform on which these are running. Note that authentication is disabled for JMX by default in Kafka and security configs must be overridden for production deployments by setting the environment variable

KAFKA_JMX_OPTS

for processes started using the CLI or by setting appropriate Java system properties. See Monitoring and Management Using JMX Technology for details on securing JMX.

We do graphing and alerting on the following metrics:

Description

Mbean name

Normal value

Message in rate

kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec,topic=([-.\w]+)

Incoming message rate per topic. Omitting ’topic=(…)’ will yield the all-topic rate.

Byte in rate from clients

kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec,topic=([-.\w]+)

Byte in (from the clients) rate per topic. Omitting ’topic=(…)’ will yield the all-topic rate.

Byte in rate from other brokers

kafka.server:type=BrokerTopicMetrics,name=ReplicationBytesInPerSec

Byte in (from the other brokers) rate across all topics.

Controller Request rate from Broker

kafka.controller:type=ControllerChannelManager,name=RequestRateAndQueueTimeMs,brokerId=([0-9]+)

The rate (requests per second) at which the ControllerChannelManager takes requests from the queue of the given broker. And the time it takes for a request to stay in this queue before it is taken from the queue.

Controller Event queue size

kafka.controller:type=ControllerEventManager,name=EventQueueSize

Size of the ControllerEventManager’s queue.

Controller Event queue time

kafka.controller:type=ControllerEventManager,name=EventQueueTimeMs

Time that takes for any event (except the Idle event) to wait in the ControllerEventManager’s queue before being processed

Request rate

kafka.network:type=RequestMetrics,name=RequestsPerSec,request={Produce|FetchConsumer|FetchFollower},version=([0-9]+)

Error rate

kafka.network:type=RequestMetrics,name=ErrorsPerSec,request=([-.\w]+),error=([-.\w]+)

Number of errors in responses counted per-request-type, per-error-code. If a response contains multiple errors, all are counted. error=NONE indicates successful responses.

Produce request rate

kafka.server:type=BrokerTopicMetrics,name=TotalProduceRequestsPerSec,topic=([-.\w]+)

Produce request rate per topic. Omitting ’topic=(…)’ will yield the all-topic rate.

Fetch request rate

kafka.server:type=BrokerTopicMetrics,name=TotalFetchRequestsPerSec,topic=([-.\w]+)

Fetch request (from clients or followers) rate per topic. Omitting ’topic=(…)’ will yield the all-topic rate.

Failed produce request rate

kafka.server:type=BrokerTopicMetrics,name=FailedProduceRequestsPerSec,topic=([-.\w]+)

Failed Produce request rate per topic. Omitting ’topic=(…)’ will yield the all-topic rate.

Failed fetch request rate

kafka.server:type=BrokerTopicMetrics,name=FailedFetchRequestsPerSec,topic=([-.\w]+)

Failed Fetch request (from clients or followers) rate per topic. Omitting ’topic=(…)’ will yield the all-topic rate.

Request size in bytes

kafka.network:type=RequestMetrics,name=RequestBytes,request=([-.\w]+)

Size of requests for each request type.

Temporary memory size in bytes

kafka.network:type=RequestMetrics,name=TemporaryMemoryBytes,request={Produce|Fetch}

Temporary memory used for message format conversions and decompression.

Message conversion time

kafka.network:type=RequestMetrics,name=MessageConversionsTimeMs,request={Produce|Fetch}

Time in milliseconds spent on message format conversions.

Message conversion rate

kafka.server:type=BrokerTopicMetrics,name={Produce|Fetch}MessageConversionsPerSec,topic=([-.\w]+)

Message format conversion rate, for Produce or Fetch requests, per topic. Omitting ’topic=(…)’ will yield the all-topic rate.

Request Queue Size

kafka.network:type=RequestChannel,name=RequestQueueSize

Size of the request queue.

Byte out rate to clients

kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec,topic=([-.\w]+)

Byte out (to the clients) rate per topic. Omitting ’topic=(…)’ will yield the all-topic rate.

Byte out rate to other brokers

kafka.server:type=BrokerTopicMetrics,name=ReplicationBytesOutPerSec

Byte out (to the other brokers) rate across all topics

Rejected byte rate

kafka.server:type=BrokerTopicMetrics,name=BytesRejectedPerSec,topic=([-.\w]+)

Rejected byte rate per topic, due to the record batch size being greater than max.message.bytes configuration. Omitting ’topic=(…)’ will yield the all-topic rate.

Message validation failure rate due to no key specified for compacted topic

kafka.server:type=BrokerTopicMetrics,name=NoKeyCompactedTopicRecordsPerSec

Message validation failure rate due to invalid magic number

kafka.server:type=BrokerTopicMetrics,name=InvalidMagicNumberRecordsPerSec

Message validation failure rate due to incorrect crc checksum

kafka.server:type=BrokerTopicMetrics,name=InvalidMessageCrcRecordsPerSec

Message validation failure rate due to non-continuous offset or sequence number in batch

kafka.server:type=BrokerTopicMetrics,name=InvalidOffsetOrSequenceRecordsPerSec

Log flush rate and time

kafka.log:type=LogFlushStats,name=LogFlushRateAndTimeMs

# of offline log directories

kafka.log:type=LogManager,name=OfflineLogDirectoryCount

Leader election rate

kafka.controller:type=ControllerStats,name=LeaderElectionRateAndTimeMs

non-zero when there are broker failures

Unclean leader election rate

kafka.controller:type=ControllerStats,name=UncleanLeaderElectionsPerSec

Election from Eligible leader replicas rate

kafka.controller:type=ControllerStats,name=ElectionFromEligibleLeaderReplicasPerSec

Is controller active on broker

kafka.controller:type=KafkaController,name=ActiveControllerCount

only one broker in the cluster should have 1

Pending topic deletes

kafka.controller:type=KafkaController,name=TopicsToDeleteCount

Pending replica deletes

kafka.controller:type=KafkaController,name=ReplicasToDeleteCount

Ineligible pending topic deletes

kafka.controller:type=KafkaController,name=TopicsIneligibleToDeleteCount

Ineligible pending replica deletes

kafka.controller:type=KafkaController,name=ReplicasIneligibleToDeleteCount

# of under replicated partitions (|ISR| < |all replicas|)

kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions

# of under minIsr partitions (|ISR| < min.insync.replicas)

kafka.server:type=ReplicaManager,name=UnderMinIsrPartitionCount

# of at minIsr partitions (|ISR| = min.insync.replicas)

kafka.server:type=ReplicaManager,name=AtMinIsrPartitionCount

Producer Id counts

kafka.server:type=ReplicaManager,name=ProducerIdCount

Count of all producer ids created by transactional and idempotent producers in each replica on the broker

Partition counts

kafka.server:type=ReplicaManager,name=PartitionCount

mostly even across brokers

Offline Replica counts

kafka.server:type=ReplicaManager,name=OfflineReplicaCount

Leader replica counts

kafka.server:type=ReplicaManager,name=LeaderCount

mostly even across brokers

ISR shrink rate

kafka.server:type=ReplicaManager,name=IsrShrinksPerSec

If a broker goes down, ISR for some of the partitions will shrink. When that broker is up again, ISR will be expanded once the replicas are fully caught up. Other than that, the expected value for both ISR shrink rate and expansion rate is 0.

ISR expansion rate

kafka.server:type=ReplicaManager,name=IsrExpandsPerSec

See above

Failed ISR update rate

kafka.server:type=ReplicaManager,name=FailedIsrUpdatesPerSec

Max lag in messages btw follower and leader replicas

kafka.server:type=ReplicaFetcherManager,name=MaxLag,clientId=Replica

lag should be proportional to the maximum batch size of a produce request.

Lag in messages per follower replica

kafka.server:type=FetcherLagMetrics,name=ConsumerLag,clientId=([-.\w]+),topic=([-.\w]+),partition=([0-9]+)

lag should be proportional to the maximum batch size of a produce request.

Requests waiting in the producer purgatory

kafka.server:type=DelayedOperationPurgatory,name=PurgatorySize,delayedOperation=Produce

non-zero if ack=-1 is used

Requests waiting in the fetch purgatory

kafka.server:type=DelayedOperationPurgatory,name=PurgatorySize,delayedOperation=Fetch

size depends on fetch.wait.max.ms in the consumer

Request total time

kafka.network:type=RequestMetrics,name=TotalTimeMs,request={Produce|FetchConsumer|FetchFollower}

broken into queue, local, remote and response send time

Time the request waits in the request queue

kafka.network:type=RequestMetrics,name=RequestQueueTimeMs,request={Produce|FetchConsumer|FetchFollower}

Time the request is processed at the leader

kafka.network:type=RequestMetrics,name=LocalTimeMs,request={Produce|FetchConsumer|FetchFollower}

Time the request waits for the follower

kafka.network:type=RequestMetrics,name=RemoteTimeMs,request={Produce|FetchConsumer|FetchFollower}

non-zero for produce requests when ack=-1

Time the request waits in the response queue

kafka.network:type=RequestMetrics,name=ResponseQueueTimeMs,request={Produce|FetchConsumer|FetchFollower}

Time to send the response

kafka.network:type=RequestMetrics,name=ResponseSendTimeMs,request={Produce|FetchConsumer|FetchFollower}

Number of messages the consumer lags behind the producer by. Published by the consumer, not broker.

kafka.consumer:type=consumer-fetch-manager-metrics,client-id={client-id} Attribute: records-lag-max

The average fraction of time the network processors are idle

kafka.network:type=SocketServer,name=NetworkProcessorAvgIdlePercent

between 0 and 1, ideally > 0.3

The number of connections disconnected on a processor due to a client not re-authenticating and then using the connection beyond its expiration time for anything other than re-authentication

kafka.server:type=socket-server-metrics,listener=[SASL_PLAINTEXT|SASL_SSL],networkProcessor=<#>,name=expired-connections-killed-count

ideally 0 when re-authentication is enabled, implying there are no longer any older, pre-2.2.0 clients connecting to this (listener, processor) combination

The total number of connections disconnected, across all processors, due to a client not re-authenticating and then using the connection beyond its expiration time for anything other than re-authentication

kafka.network:type=SocketServer,name=ExpiredConnectionsKilledCount

ideally 0 when re-authentication is enabled, implying there are no longer any older, pre-2.2.0 clients connecting to this broker

The average fraction of time the request handler threads are idle

kafka.server:type=KafkaRequestHandlerPool,name=RequestHandlerAvgIdlePercent

between 0 and 1, ideally > 0.3

Bandwidth quota metrics per (user, client-id), user or client-id

kafka.server:type={Produce|Fetch},user=([-.\w]+),client-id=([-.\w]+)

Two attributes. throttle-time indicates the amount of time in ms the client was throttled. Ideally = 0. byte-rate indicates the data produce/consume rate of the client in bytes/sec. For (user, client-id) quotas, both user and client-id are specified. If per-client-id quota is applied to the client, user is not specified. If per-user quota is applied, client-id is not specified.

Request quota metrics per (user, client-id), user or client-id

kafka.server:type=Request,user=([-.\w]+),client-id=([-.\w]+)

Two attributes. throttle-time indicates the amount of time in ms the client was throttled. Ideally = 0. request-time indicates the percentage of time spent in broker network and I/O threads to process requests from client group. For (user, client-id) quotas, both user and client-id are specified. If per-client-id quota is applied to the client, user is not specified. If per-user quota is applied, client-id is not specified.

Requests exempt from throttling

kafka.server:type=Request

exempt-throttle-time indicates the percentage of time spent in broker network and I/O threads to process requests that are exempt from throttling.

Max time to load group metadata

kafka.server:type=group-coordinator-metrics,name=partition-load-time-max

maximum time, in milliseconds, it took to load offsets and group metadata from the consumer offset partitions loaded in the last 30 seconds (including time spent waiting for the loading task to be scheduled)

Avg time to load group metadata

kafka.server:type=group-coordinator-metrics,name=partition-load-time-avg

average time, in milliseconds, it took to load offsets and group metadata from the consumer offset partitions loaded in the last 30 seconds (including time spent waiting for the loading task to be scheduled)

Max time to load transaction metadata

kafka.server:type=transaction-coordinator-metrics,name=partition-load-time-max

maximum time, in milliseconds, it took to load transaction metadata from the consumer offset partitions loaded in the last 30 seconds (including time spent waiting for the loading task to be scheduled)

Avg time to load transaction metadata

kafka.server:type=transaction-coordinator-metrics,name=partition-load-time-avg

average time, in milliseconds, it took to load transaction metadata from the consumer offset partitions loaded in the last 30 seconds (including time spent waiting for the loading task to be scheduled)

Rate of transactional verification errors

kafka.server:type=AddPartitionsToTxnManager,name=VerificationFailureRate

Rate of verifications that returned in failure either from the AddPartitionsToTxn API response or through errors in the AddPartitionsToTxnManager. In steady state 0, but transient errors are expected during rolls and reassignments of the transactional state partition.

Time to verify a transactional request

kafka.server:type=AddPartitionsToTxnManager,name=VerificationTimeMs

The amount of time queueing while a possible previous request is in-flight plus the round trip to the transaction coordinator to verify (or not verify)

Number of reassigning partitions

kafka.server:type=ReplicaManager,name=ReassigningPartitions

The number of reassigning leader partitions on a broker.

Outgoing byte rate of reassignment traffic

kafka.server:type=BrokerTopicMetrics,name=ReassignmentBytesOutPerSec

0; non-zero when a partition reassignment is in progress.

Incoming byte rate of reassignment traffic

kafka.server:type=BrokerTopicMetrics,name=ReassignmentBytesInPerSec

0; non-zero when a partition reassignment is in progress.

Size of a partition on disk (in bytes)

kafka.log:type=Log,name=Size,topic=([-.\w]+),partition=([0-9]+)

The size of a partition on disk, measured in bytes.

Partition size as a percentage of retention bytes limit

kafka.log:type=Log,name=RetentionSizeInPercent,topic=([-.\w]+),partition=([0-9]+)

The partition size expressed as a percentage of the configured retention.bytes limit. Returns 0 for topics with tiered storage enabled (where the metric is reported by RemoteLogManager) or when retention bytes is unlimited. May exceed 100% if retention cleanup is delayed.

Number of log segments in a partition

kafka.log:type=Log,name=NumLogSegments,topic=([-.\w]+),partition=([0-9]+)

The number of log segments in a partition.

First offset in a partition

kafka.log:type=Log,name=LogStartOffset,topic=([-.\w]+),partition=([0-9]+)

The first offset in a partition.

Last offset in a partition

kafka.log:type=Log,name=LogEndOffset,topic=([-.\w]+),partition=([0-9]+)

The last offset in a partition.

Remaining logs to recover

kafka.log:type=LogManager,name=remainingLogsToRecover

The number of remaining logs for each log.dir to be recovered.This metric provides an overview of the recovery progress for a given log directory.

Remaining segments to recover for the current recovery thread

kafka.log:type=LogManager,name=remainingSegmentsToRecover

The number of remaining segments assigned to the currently active recovery thread.

Log directory offline status

kafka.log:type=LogManager,name=LogDirectoryOffline

Indicates if a log directory is offline (1) or online (0).

Group Coordinator Monitoring

The following set of metrics are available for monitoring the group coordinator:

The Partition Count, per State

kafka.server:type=group-coordinator-metrics,name=num-partitions,state={loading|active|failed}

The number of

__consumer_offsets

partitions hosted by the broker, broken down by state

Partition Maximum Loading Time

kafka.server:type=group-coordinator-metrics,name=partition-load-time-max

The maximum loading time needed to read the state from the

__consumer_offsets

partitions

Partition Average Loading Time

kafka.server:type=group-coordinator-metrics,name=partition-load-time-avg

The average loading time needed to read the state from the

__consumer_offsets

partitions

Average Thread Idle Ratio

kafka.server:type=group-coordinator-metrics,name=thread-idle-ratio-avg

The average idle ratio of the coordinator threads

Event Queue Size

kafka.server:type=group-coordinator-metrics,name=event-queue-size

The number of events waiting to be processed in the queue

Event Queue Time (Ms)

kafka.server:type=group-coordinator-metrics,name=event-queue-time-ms-[max|p50|p95|p99|p999]

The time that an event spent waiting in the queue to be processed

Event Processing Time (Ms)

kafka.server:type=group-coordinator-metrics,name=event-processing-time-ms-[max|p50|p95|p99|p999]

The time that an event took to be processed

Event Purgatory Time (Ms)

kafka.server:type=group-coordinator-metrics,name=event-purgatory-time-ms-[max|p50|p95|p99|p999]

The time that an event waited in the purgatory before being completed

Batch Linger Time (Ms)

kafka.server:type=group-coordinator-metrics,name=batch-linger-time-ms-[max|p50|p95|p99|p999]

The effective linger time of a batch before being flushed to the local partition

Batch Flush Time (Ms)

kafka.server:type=group-coordinator-metrics,name=batch-flush-time-ms-[max|p50|p95|p99|p999]

The time that a batch took to be flushed to the local partition

Batch Flush Rate

kafka.server:type=group-coordinator-metrics,name=batch-flush-rate

The number of batches flushed per second

Batch Buffer Cache Size

kafka.server:type=group-coordinator-metrics,name=batch-buffer-cache-size-bytes

The total size in bytes of append buffers currently held in the coordinator’s cache

Batch Buffer Cache Discard Count

kafka.server:type=group-coordinator-metrics,name=batch-buffer-cache-discard-count

The total number of over-sized append buffers that were discarded upon release

Group Count, per group type

kafka.server:type=group-coordinator-metrics,name=group-count,protocol={consumer|classic|streams}

Total number of group per group type: Classic, Consumer or Streams

Consumer Group Count, per state

kafka.server:type=group-coordinator-metrics,name=consumer-group-count,state=[empty|assigning|reconciling|stable|dead]

Total number of Consumer Groups in each state: Empty, Assigning, Reconciling, Stable, Dead

Consumer Group Rebalance Rate

kafka.server:type=group-coordinator-metrics,name=consumer-group-rebalance-rate

The rebalance rate of consumer groups

Consumer Group Rebalance Count

kafka.server:type=group-coordinator-metrics,name=consumer-group-rebalance-count

Total number of Consumer Group Rebalances

Streams Group Count, per state

kafka.server:type=group-coordinator-metrics,name=streams-group-count,state=[empty|not_ready|assigning|reconciling|stable|dead]

Total number of Streams Groups in each state: Empty, Not Ready, Assigning, Reconciling, Stable, Dead

Streams Group Rebalance Rate

kafka.server:type=group-coordinator-metrics,name=streams-group-rebalance-rate

The rebalance rate of streams groups

Streams Group Rebalance Count

kafka.server:type=group-coordinator-metrics,name=streams-group-rebalance-count

Total number of Streams Group Rebalances

Classic Group Count

kafka.server:type=GroupMetadataManager,name=NumGroups

Total number of Classic Groups

Classic Group Count, per State

kafka.server:type=GroupMetadataManager,name=NumGroups[PreparingRebalance,CompletingRebalance,Empty,Stable,Dead]

The number of Classic Groups in each state: PreparingRebalance, CompletingRebalance, Empty, Stable, Dead

Classic Group Completed Rebalance Rate

kafka.server:type=group-coordinator-metrics,name=group-completed-rebalance-rate

The rate of classic group completed rebalances

Classic Group Completed Rebalance Count

kafka.server:type=group-coordinator-metrics,name=group-completed-rebalance-count

The total number of classic group completed rebalances

Group Offset Count

kafka.server:type=GroupMetadataManager,name=NumOffsets

Total number of committed offsets for Classic and Consumer Groups

Offset Commit Rate

kafka.server:type=group-coordinator-metrics,name=offset-commit-rate

The rate of committed offsets

Offset Commit Count

kafka.server:type=group-coordinator-metrics,name=offset-commit-count

The total number of committed offsets

Offset Expiration Rate

kafka.server:type=group-coordinator-metrics,name=offset-expiration-rate

The rate of expired offsets

Offset Expiration Count

kafka.server:type=group-coordinator-metrics,name=offset-expiration-count

The total number of expired offsets

Offset Deletion Rate

kafka.server:type=group-coordinator-metrics,name=offset-deletion-rate

The rate of administrative deleted offsets

Offset Deletion Count

kafka.server:type=group-coordinator-metrics,name=offset-deletion-count

The total number of administrative deleted offsets

Tiered Storage Monitoring

The following set of metrics are available for monitoring of the tiered storage feature:

Metric/Attribute name

Description

Mbean name

Remote Fetch Bytes Per Sec

Rate of bytes read from remote storage per topic. Omitting ’topic=(…)’ will yield the all-topic rate

kafka.server:type=BrokerTopicMetrics,name=RemoteFetchBytesPerSec,topic=([-.\w]+)

Remote Fetch Requests Per Sec

Rate of read requests from remote storage per topic. Omitting ’topic=(…)’ will yield the all-topic rate

kafka.server:type=BrokerTopicMetrics,name=RemoteFetchRequestsPerSec,topic=([-.\w]+)

Remote Fetch Errors Per Sec

Rate of read errors from remote storage per topic. Omitting ’topic=(…)’ will yield the all-topic rate

kafka.server:type=BrokerTopicMetrics,name=RemoteFetchErrorsPerSec,topic=([-.\w]+)

Remote Copy Bytes Per Sec

Rate of bytes copied to remote storage per topic. Omitting ’topic=(…)’ will yield the all-topic rate

kafka.server:type=BrokerTopicMetrics,name=RemoteCopyBytesPerSec,topic=([-.\w]+)

Remote Copy Requests Per Sec

Rate of write requests to remote storage per topic. Omitting ’topic=(…)’ will yield the all-topic rate

kafka.server:type=BrokerTopicMetrics,name=RemoteCopyRequestsPerSec,topic=([-.\w]+)

Remote Copy Errors Per Sec

Rate of write errors from remote storage per topic. Omitting ’topic=(…)’ will yield the all-topic rate

kafka.server:type=BrokerTopicMetrics,name=RemoteCopyErrorsPerSec,topic=([-.\w]+)

Remote Copy Lag Bytes

Bytes which are eligible for tiering, but are not in remote storage yet. Omitting ’topic=(…)’ will yield the all-topic sum

kafka.server:type=BrokerTopicMetrics,name=RemoteCopyLagBytes,topic=([-.\w]+)

Remote Copy Lag Segments

Segments which are eligible for tiering, but are not in remote storage yet. Omitting ’topic=(…)’ will yield the all-topic count

kafka.server:type=BrokerTopicMetrics,name=RemoteCopyLagSegments,topic=([-.\w]+)

Remote Delete Requests Per Sec

Rate of delete requests to remote storage per topic. Omitting ’topic=(…)’ will yield the all-topic rate

kafka.server:type=BrokerTopicMetrics,name=RemoteDeleteRequestsPerSec,topic=([-.\w]+)

Remote Delete Errors Per Sec

Rate of delete errors from remote storage per topic. Omitting ’topic=(…)’ will yield the all-topic rate

kafka.server:type=BrokerTopicMetrics,name=RemoteDeleteErrorsPerSec,topic=([-.\w]+)

Remote Delete Lag Bytes

Tiered bytes which are eligible for deletion, but have not been deleted yet. Omitting ’topic=(…)’ will yield the all-topic sum

kafka.server:type=BrokerTopicMetrics,name=RemoteDeleteLagBytes,topic=([-.\w]+)

Remote Delete Lag Segments

Tiered segments which are eligible for deletion, but have not been deleted yet. Omitting ’topic=(…)’ will yield the all-topic count

kafka.server:type=BrokerTopicMetrics,name=RemoteDeleteLagSegments,topic=([-.\w]+)

Build Remote Log Aux State Requests Per Sec

Rate of requests for rebuilding the auxiliary state from remote storage per topic. Omitting ’topic=(…)’ will yield the all-topic rate

kafka.server:type=BrokerTopicMetrics,name=BuildRemoteLogAuxStateRequestsPerSec,topic=([-.\w]+)

Build Remote Log Aux State Errors Per Sec

Rate of errors for rebuilding the auxiliary state from remote storage per topic. Omitting ’topic=(…)’ will yield the all-topic rate

kafka.server:type=BrokerTopicMetrics,name=BuildRemoteLogAuxStateErrorsPerSec,topic=([-.\w]+)

Remote Log Size Computation Time

The amount of time needed to compute the size of the remote log. Omitting ’topic=(…)’ will yield the all-topic time

kafka.server:type=BrokerTopicMetrics,name=RemoteLogSizeComputationTime,topic=([-.\w]+)

Remote Log Size Bytes

The total size of a remote log in bytes. Omitting ’topic=(…)’ will yield the all-topic sum

kafka.server:type=BrokerTopicMetrics,name=RemoteLogSizeBytes,topic=([-.\w]+)

Remote Log Metadata Count

The total number of metadata entries for remote storage. Omitting ’topic=(…)’ will yield the all-topic count

kafka.server:type=BrokerTopicMetrics,name=RemoteLogMetadataCount,topic=([-.\w]+)

Delayed Remote Fetch Expires Per Sec

The number of expired remote fetches per second. Omitting ’topic=(…)’ will yield the all-topic rate

kafka.server:type=DelayedRemoteFetchMetrics,name=ExpiresPerSec,topic=([-.\w]+)

RemoteLogReader Task Queue Size

Size of the queue holding remote storage read tasks

org.apache.kafka.storage.internals.log:type=RemoteStorageThreadPool,name=RemoteLogReaderTaskQueueSize

RemoteLogReader Avg Idle Percent

Average idle percent of thread pool for processing remote storage read tasks

org.apache.kafka.storage.internals.log:type=RemoteStorageThreadPool,name=RemoteLogReaderAvgIdlePercent

RemoteLogManager Tasks Avg Idle Percent

Average idle percent of thread pool for copying data to remote storage

kafka.log.remote:type=RemoteLogManager,name=RemoteLogManagerTasksAvgIdlePercent

RemoteLogManager Avg Broker Fetch Throttle Time

The average time in millis remote fetches was throttled by a broker

kafka.server:type=RemoteLogManager, name=remote-fetch-throttle-time-avg

RemoteLogManager Max Broker Fetch Throttle Time

The max time in millis remote fetches was throttled by a broker

kafka.server:type=RemoteLogManager, name=remote-fetch-throttle-time-max

RemoteLogManager Avg Broker Copy Throttle Time

The average time in millis remote copies was throttled by a broker

kafka.server:type=RemoteLogManager, name=remote-copy-throttle-time-avg

RemoteLogManager Max Broker Copy Throttle Time

The max time in millis remote copies was throttled by a broker

kafka.server:type=RemoteLogManager, name=remote-copy-throttle-time-max

RemoteLogReader Fetch Rate And Time

The time to read data from remote storage by a broker

kafka.log.remote:type=RemoteLogManager,name=RemoteLogReaderFetchRateAndTimeMs

Retention Size In Percent

Total partition size (local + remote) as a percentage of the configured retention.bytes limit. Available for tiered storage topics. May exceed 100% if retention cleanup is delayed. Returns 0 when retention bytes is unlimited.

kafka.log.remote:type=RemoteLogManager,name=RetentionSizeInPercent,topic=([-.\w]+),partition=([0-9]+)

Local Retention Size In Percent

Local log size as a percentage of the configured local.retention.bytes limit. Available for tiered storage topics. Helps operators monitor pressure on local disks independently of remote storage. May exceed 100% if retention cleanup is delayed. Returns 0 when local retention bytes is unlimited.

kafka.log.remote:type=RemoteLogManager,name=LocalRetentionSizeInPercent,topic=([-.\w]+),partition=([0-9]+)

Delayed Remote List Offsets Expires Per Sec

The number of expired remote list offsets per second. Omitting ’topic=(…), partition=(…)’ will yield the all-topic rate

kafka.server:type=DelayedRemoteListOffsetsMetrics,name=ExpiresPerSec,topic=([-.\w]+),partition=([0-9]+)

KRaft Monitoring Metrics

The set of metrics that allow monitoring of the KRaft quorum and the metadata log. Note that some exposed metrics depend on the role of the node as defined by

process.roles

KRaft Quorum Monitoring Metrics

These metrics are reported on both Controllers and Brokers in a KRaft Cluster

Metric/Attribute name

Description

Mbean name

Current State

The current state of this member; possible values are leader, candidate, voted, follower, unattached, observer.

kafka.server:type=raft-metrics

Current Leader

The current quorum leader’s id; -1 indicates unknown.

kafka.server:type=raft-metrics

Current Voted

The current voted leader’s id; -1 indicates not voted for anyone.

kafka.server:type=raft-metrics

Current Epoch

The current quorum epoch.

kafka.server:type=raft-metrics

High Watermark

The high watermark maintained on this member; -1 if it is unknown.

kafka.server:type=raft-metrics

Log End Offset

The current raft log end offset.

kafka.server:type=raft-metrics

Number of Unknown Voter Connections

Number of unknown voters whose connection information is not cached. This value of this metric is always 0.

kafka.server:type=raft-metrics

Average Commit Latency

The average time in milliseconds to commit an entry in the raft log.

kafka.server:type=raft-metrics

Maximum Commit Latency

The maximum time in milliseconds to commit an entry in the raft log.

kafka.server:type=raft-metrics

Average Election Latency

The average time in milliseconds spent on electing a new leader.

kafka.server:type=raft-metrics

Maximum Election Latency

The maximum time in milliseconds spent on electing a new leader.

kafka.server:type=raft-metrics

Fetch Records Rate

The average number of records fetched from the leader of the raft quorum.

kafka.server:type=raft-metrics

Append Records Rate

The average number of records appended per sec by the leader of the raft quorum.

kafka.server:type=raft-metrics

Average Poll Idle Ratio

The ratio of time the Raft IO thread is idle as opposed to doing work (e.g. handling requests or replicating from the leader)

kafka.server:type=raft-metrics

Current Metadata Version

Outputs the feature level of the current effective metadata version.

kafka.server:type=MetadataLoader,name=CurrentMetadataVersion

Metadata Snapshot Load Count

The total number of times we have loaded a KRaft snapshot since the process was started.

kafka.server:type=MetadataLoader,name=HandleLoadSnapshotCount

Latest Metadata Snapshot Size

The total size in bytes of the latest snapshot that the node has generated. If none have been generated yet, this is the size of the latest snapshot that was loaded. If no snapshots have been generated or loaded, this is 0.

kafka.server:type=SnapshotEmitter,name=LatestSnapshotGeneratedBytes

Latest Metadata Snapshot Age

The interval in milliseconds since the latest snapshot that the node has generated. If none have been generated yet, this is approximately the time delta since the process was started.

kafka.server:type=SnapshotEmitter,name=LatestSnapshotGeneratedAgeMs

KRaft Controller Monitoring Metrics

Metric/Attribute name

Description

Mbean name

Active Controller Count

The number of Active Controllers on this node. Valid values are ‘0’ or ‘1’.

kafka.controller:type=KafkaController,name=ActiveControllerCount

Event Queue Time Ms

A Histogram of the time in milliseconds that requests spent waiting in the Controller Event Queue.

kafka.controller:type=ControllerEventManager,name=EventQueueTimeMs

Event Queue Processing Time Ms

A Histogram of the time in milliseconds that requests spent being processed in the Controller Event Queue.

kafka.controller:type=ControllerEventManager,name=EventQueueProcessingTimeMs

Fenced Broker Count

The number of fenced brokers as observed by this Controller.

kafka.controller:type=KafkaController,name=FencedBrokerCount

Active Broker Count

The number of active brokers as observed by this Controller.

kafka.controller:type=KafkaController,name=ActiveBrokerCount

Global Topic Count

The number of global topics as observed by this Controller.

kafka.controller:type=KafkaController,name=GlobalTopicCount

Global Partition Count

The number of global partitions as observed by this Controller.

kafka.controller:type=KafkaController,name=GlobalPartitionCount

Offline Partition Count

The number of offline topic partitions (non-internal) as observed by this Controller.

kafka.controller:type=KafkaController,name=OfflinePartitionsCount

Preferred Replica Imbalance Count

The count of topic partitions for which the leader is not the preferred leader.

kafka.controller:type=KafkaController,name=PreferredReplicaImbalanceCount

Metadata Error Count

The number of times this controller node has encountered an error during metadata log processing.

kafka.controller:type=KafkaController,name=MetadataErrorCount

Last Applied Record Offset

The offset of the last record from the cluster metadata partition that was applied by the Controller.

kafka.controller:type=KafkaController,name=LastAppliedRecordOffset

Last Committed Record Offset

The offset of the last record committed to this Controller.

kafka.controller:type=KafkaController,name=LastCommittedRecordOffset

Last Applied Record Timestamp

The timestamp of the last record from the cluster metadata partition that was applied by the Controller.

kafka.controller:type=KafkaController,name=LastAppliedRecordTimestamp

Last Applied Record Lag Ms

The difference between now and the timestamp of the last record from the cluster metadata partition that was applied by the controller. For active Controllers the value of this lag is always zero.

kafka.controller:type=KafkaController,name=LastAppliedRecordLagMs

Timed-out Broker Heartbeat Count

The number of broker heartbeats that timed out on this controller since the process was started. Note that only active controllers handle heartbeats, so only they will see increases in this metric.

kafka.controller:type=KafkaController,name=TimedOutBrokerHeartbeatCount

Number Of Operations Started In Event Queue

The total number of controller event queue operations that were started. This includes deferred operations.

kafka.controller:type=KafkaController,name=EventQueueOperationsStartedCount

Number of Operations Timed Out In Event Queue

The total number of controller event queue operations that timed out before they could be performed.

kafka.controller:type=KafkaController,name=EventQueueOperationsTimedOutCount

Number Of New Controller Elections

Counts the number of times this node has seen a new controller elected. A transition to the “no leader” state is not counted here. If the same controller as before becomes active, that still counts.

kafka.controller:type=KafkaController,name=NewActiveControllersCount

KRaft Broker Monitoring Metrics

Metric/Attribute name

Description

Mbean name

Last Applied Record Offset

The offset of the last record from the cluster metadata partition that was applied by the broker

kafka.server:type=broker-metadata-metrics

Last Applied Record Timestamp

The timestamp of the last record from the cluster metadata partition that was applied by the broker.

kafka.server:type=broker-metadata-metrics

Last Applied Record Lag Ms

The difference between now and the timestamp of the last record from the cluster metadata partition that was applied by the broker

kafka.server:type=broker-metadata-metrics

Metadata Load Error Count

The number of errors encountered by the BrokerMetadataListener while loading the metadata log and generating a new MetadataDelta based on it.

kafka.server:type=broker-metadata-metrics

Metadata Apply Error Count

The number of errors encountered by the BrokerMetadataPublisher while applying a new MetadataImage based on the latest MetadataDelta.

kafka.server:type=broker-metadata-metrics

Common monitoring metrics for producer/consumer/connect/streams

The following metrics are available on producer/consumer/connector/streams instances. For specific metrics, please see following sections.

Metric/Attribute name

Description

Mbean name

connection-close-rate

Connections closed per second in the window.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

connection-close-total

Total connections closed in the window.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

connection-creation-rate

New connections established per second in the window.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

connection-creation-total

Total new connections established in the window.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

network-io-rate

The average number of network operations (reads or writes) on all connections per second.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

network-io-total

The total number of network operations (reads or writes) on all connections.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

outgoing-byte-rate

The average number of outgoing bytes sent per second to all servers.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

outgoing-byte-total

The total number of outgoing bytes sent to all servers.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

request-rate

The average number of requests sent per second.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

request-total

The total number of requests sent.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

request-size-avg

The average size of all requests in the window.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

request-size-max

The maximum size of any request sent in the window.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

incoming-byte-rate

Bytes/second read off all sockets.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

incoming-byte-total

Total bytes read off all sockets.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

response-rate

Responses received per second.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

response-total

Total responses received.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

select-rate

Number of times the I/O layer checked for new I/O to perform per second.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

select-total

Total number of times the I/O layer checked for new I/O to perform.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

io-wait-time-ns-avg

The average length of time the I/O thread spent waiting for a socket ready for reads or writes in nanoseconds.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

io-wait-time-ns-total

The total time the I/O thread spent waiting in nanoseconds.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

io-wait-ratio

The fraction of time the I/O thread spent waiting.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

io-time-ns-avg

The average length of time for I/O per select call in nanoseconds.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

io-time-ns-total

The total time the I/O thread spent doing I/O in nanoseconds.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

io-ratio

The fraction of time the I/O thread spent doing I/O.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

connection-count

The current number of active connections.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

successful-authentication-rate

Connections per second that were successfully authenticated using SASL or SSL.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

successful-authentication-total

Total connections that were successfully authenticated using SASL or SSL.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

failed-authentication-rate

Connections per second that failed authentication.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

failed-authentication-total

Total connections that failed authentication.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

successful-reauthentication-rate

Connections per second that were successfully re-authenticated using SASL.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

successful-reauthentication-total

Total connections that were successfully re-authenticated using SASL.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

reauthentication-latency-max

The maximum latency in ms observed due to re-authentication.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

reauthentication-latency-avg

The average latency in ms observed due to re-authentication.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

failed-reauthentication-rate

Connections per second that failed re-authentication.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

failed-reauthentication-total

Total connections that failed re-authentication.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

successful-authentication-no-reauth-total

Total connections that were successfully authenticated by older, pre-2.2.0 SASL clients that do not support re-authentication. May only be non-zero.

kafka.[producer|consumer|connect]:type=[producer|consumer|connect]-metrics,client-id=([-.\w]+)

Common Per-broker metrics for producer/consumer/connect/streams

The following metrics are available on producer/consumer/connector/streams instances. For specific metrics, please see following sections.

Metric/Attribute name

Description

Mbean name

outgoing-byte-rate

The average number of outgoing bytes sent per second for a node.

kafka.[producer|consumer|connect]:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)

outgoing-byte-total

The total number of outgoing bytes sent for a node.

kafka.[producer|consumer|connect]:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)

request-rate

The average number of requests sent per second for a node.

kafka.[producer|consumer|connect]:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)

request-total

The total number of requests sent for a node.

kafka.[producer|consumer|connect]:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)

request-size-avg

The average size of all requests in the window for a node.

kafka.[producer|consumer|connect]:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)

request-size-max

The maximum size of any request sent in the window for a node.

kafka.[producer|consumer|connect]:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)

incoming-byte-rate

The average number of bytes received per second for a node.

kafka.[producer|consumer|connect]:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)

incoming-byte-total

The total number of bytes received for a node.

kafka.[producer|consumer|connect]:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)

request-latency-avg

The average request latency in ms for a node.

kafka.[producer|consumer|connect]:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)

request-latency-max

The maximum request latency in ms for a node.

kafka.[producer|consumer|connect]:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)

response-rate

Responses received per second for a node.

kafka.[producer|consumer|connect]:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)

response-total

Total responses received for a node.

kafka.[producer|consumer|connect]:type=[consumer|producer|connect]-node-metrics,client-id=([-.\w]+),node-id=([0-9]+)

Producer monitoring

The following metrics are available on producer instances.

Metric/Attribute name

Description

Mbean name

waiting-threads

The number of user threads blocked waiting for buffer memory to enqueue their records.

kafka.producer:type=producer-metrics,client-id=([-.\w]+)

buffer-total-bytes

The maximum amount of buffer memory the client can use (whether or not it is currently used).

kafka.producer:type=producer-metrics,client-id=([-.\w]+)

buffer-available-bytes

The total amount of buffer memory that is not being used (either unallocated or in the free list).

kafka.producer:type=producer-metrics,client-id=([-.\w]+)

buffer-exhausted-rate

The average per-second number of record sends that are dropped due to buffer exhaustion

kafka.producer:type=producer-metrics,client-id=([-.\w]+)

buffer-exhausted-total

The total number of record sends that are dropped due to buffer exhaustion

kafka.producer:type=producer-metrics,client-id=([-.\w]+)

bufferpool-wait-time

The fraction of time an appender waits for space allocation.

kafka.producer:type=producer-metrics,client-id=([-.\w]+)

bufferpool-wait-ratio

The fraction of time an appender waits for space allocation.

kafka.producer:type=producer-metrics,client-id=([-.\w]+)

bufferpool-wait-time-ns-total

The total time an appender waits for space allocation in nanoseconds.

kafka.producer:type=producer-metrics,client-id=([-.\w]+)

flush-time-ns-total

The total time the Producer spent in Producer.flush in nanoseconds.

kafka.producer:type=producer-metrics,client-id=([-.\w]+)

txn-init-time-ns-total

The total time the Producer spent initializing transactions in nanoseconds (for EOS).

kafka.producer:type=producer-metrics,client-id=([-.\w]+)

txn-begin-time-ns-total

The total time the Producer spent in beginTransaction in nanoseconds (for EOS).

kafka.producer:type=producer-metrics,client-id=([-.\w]+)

txn-send-offsets-time-ns-total

The total time the Producer spent sending offsets to transactions in nanoseconds (for EOS).

kafka.producer:type=producer-metrics,client-id=([-.\w]+)

txn-commit-time-ns-total

The total time the Producer spent committing transactions in nanoseconds (for EOS).

kafka.producer:type=producer-metrics,client-id=([-.\w]+)

txn-abort-time-ns-total

The total time the Producer spent aborting transactions in nanoseconds (for EOS).

kafka.producer:type=producer-metrics,client-id=([-.\w]+)

metadata-wait-time-ns-total

the total time in nanoseconds that has spent waiting for metadata from the Kafka broker

kafka.producer:type=producer-metrics,client-id=([-.\w]+)

Producer Sender Metrics

Metric/Attribute name Description Mbean name

batch-size-avg The average number of bytes sent per partition per-request. kafka.producer:type=producer-metrics,client-id="{client-id}"

batch-size-max The max number of bytes sent per partition per-request. kafka.producer:type=producer-metrics,client-id="{client-id}"

batch-split-rate The average number of batch splits per second kafka.producer:type=producer-metrics,client-id="{client-id}"

batch-split-total The total number of batch splits kafka.producer:type=producer-metrics,client-id="{client-id}"

compression-rate-avg The average compression rate of record batches, defined as the average ratio of the compressed batch size over the uncompressed size. kafka.producer:type=producer-metrics,client-id="{client-id}"

metadata-age The age in seconds of the current producer metadata being used. kafka.producer:type=producer-metrics,client-id="{client-id}"

produce-throttle-time-avg The average time in ms a request was throttled by a broker kafka.producer:type=producer-metrics,client-id="{client-id}"

produce-throttle-time-max The maximum time in ms a request was throttled by a broker kafka.producer:type=producer-metrics,client-id="{client-id}"

record-error-rate The average per-second number of record sends that resulted in errors kafka.producer:type=producer-metrics,client-id="{client-id}"

record-error-total The total number of record sends that resulted in errors kafka.producer:type=producer-metrics,client-id="{client-id}"

record-queue-time-avg The average time in ms record batches spent in the send buffer. kafka.producer:type=producer-metrics,client-id="{client-id}"

record-queue-time-max The maximum time in ms record batches spent in the send buffer. kafka.producer:type=producer-metrics,client-id="{client-id}"

record-retry-rate The average per-second number of retried record sends kafka.producer:type=producer-metrics,client-id="{client-id}"

record-retry-total The total number of retried record sends kafka.producer:type=producer-metrics,client-id="{client-id}"

record-send-rate The average number of records sent per second. kafka.producer:type=producer-metrics,client-id="{client-id}"

record-send-total The total number of records sent. kafka.producer:type=producer-metrics,client-id="{client-id}"

record-size-avg The average record size kafka.producer:type=producer-metrics,client-id="{client-id}"

record-size-max The maximum record size kafka.producer:type=producer-metrics,client-id="{client-id}"

records-per-request-avg The average number of records per request. kafka.producer:type=producer-metrics,client-id="{client-id}"

request-latency-avg The average request latency in ms kafka.producer:type=producer-metrics,client-id="{client-id}"

request-latency-max The maximum request latency in ms kafka.producer:type=producer-metrics,client-id="{client-id}"

requests-in-flight The current number of in-flight requests awaiting a response. kafka.producer:type=producer-metrics,client-id="{client-id}"

byte-rate The average number of bytes sent per second for a topic. kafka.producer:type=producer-topic-metrics,client-id="{client-id}",topic="{topic}"

byte-total The total number of bytes sent for a topic. kafka.producer:type=producer-topic-metrics,client-id="{client-id}",topic="{topic}"

compression-rate The average compression rate of record batches for a topic, defined as the average ratio of the compressed batch size over the uncompressed size. kafka.producer:type=producer-topic-metrics,client-id="{client-id}",topic="{topic}"

record-error-rate The average per-second number of record sends that resulted in errors for a topic kafka.producer:type=producer-topic-metrics,client-id="{client-id}",topic="{topic}"

record-error-total The total number of record sends that resulted in errors for a topic kafka.producer:type=producer-topic-metrics,client-id="{client-id}",topic="{topic}"

record-retry-rate The average per-second number of retried record sends for a topic kafka.producer:type=producer-topic-metrics,client-id="{client-id}",topic="{topic}"

record-retry-total The total number of retried record sends for a topic kafka.producer:type=producer-topic-metrics,client-id="{client-id}",topic="{topic}"

record-send-rate The average number of records sent per second for a topic. kafka.producer:type=producer-topic-metrics,client-id="{client-id}",topic="{topic}"

record-send-total The total number of records sent for a topic. kafka.producer:type=producer-topic-metrics,client-id="{client-id}",topic="{topic}"

Consumer monitoring

The following metrics are available on consumer instances.

Metric/Attribute name

Description

Mbean name

time-between-poll-avg

The average delay between invocations of poll().

kafka.consumer:type=consumer-metrics,client-id=([-.\w]+)

time-between-poll-max

The max delay between invocations of poll().

kafka.consumer:type=consumer-metrics,client-id=([-.\w]+)

last-poll-seconds-ago

The number of seconds since the last poll() invocation.

kafka.consumer:type=consumer-metrics,client-id=([-.\w]+)

poll-idle-ratio-avg

The average fraction of time the consumer’s poll() is idle as opposed to waiting for the user code to process records.

kafka.consumer:type=consumer-metrics,client-id=([-.\w]+)

committed-time-ns-total

The total time the Consumer spent in committed in nanoseconds.

kafka.consumer:type=consumer-metrics,client-id=([-.\w]+)

commit-sync-time-ns-total

The total time the Consumer spent committing offsets in nanoseconds (for AOS).

kafka.consumer:type=consumer-metrics,client-id=([-.\w]+)

Consumer Group Metrics

Metric/Attribute name

Description

Mbean name

commit-latency-avg

The average time taken for a commit request

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

commit-latency-max

The max time taken for a commit request

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

commit-rate

The number of commit calls per second

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

commit-total

The total number of commit calls

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

assigned-partitions

The number of partitions currently assigned to this consumer

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

heartbeat-response-time-max

The max time taken to receive a response to a heartbeat request

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

heartbeat-rate

The average number of heartbeats per second

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

heartbeat-total

The total number of heartbeats

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

join-time-avg

The average time taken for a group rejoin

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

join-time-max

The max time taken for a group rejoin

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

join-rate

The number of group joins per second

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

join-total

The total number of group joins

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

sync-time-avg

The average time taken for a group sync

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

sync-time-max

The max time taken for a group sync

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

sync-rate

The number of group syncs per second

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

sync-total

The total number of group syncs

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

rebalance-latency-avg

The average time taken for a group rebalance

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

rebalance-latency-max

The max time taken for a group rebalance

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

rebalance-latency-total

The total time taken for group rebalances so far

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

rebalance-total

The total number of group rebalances participated

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

rebalance-rate-per-hour

The number of group rebalance participated per hour

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

failed-rebalance-total

The total number of failed group rebalances

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

failed-rebalance-rate-per-hour

The number of failed group rebalance event per hour

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

last-rebalance-seconds-ago

The number of seconds since the last rebalance event

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

last-heartbeat-seconds-ago

The number of seconds since the last controller heartbeat

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

partitions-revoked-latency-avg

The average time taken by the on-partitions-revoked rebalance listener callback

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

partitions-revoked-latency-max

The max time taken by the on-partitions-revoked rebalance listener callback

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

partitions-assigned-latency-avg

The average time taken by the on-partitions-assigned rebalance listener callback

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

partitions-assigned-latency-max

The max time taken by the on-partitions-assigned rebalance listener callback

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

partitions-lost-latency-avg

The average time taken by the on-partitions-lost rebalance listener callback

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

partitions-lost-latency-max

The max time taken by the on-partitions-lost rebalance listener callback

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

Consumer Fetch Metrics

Metric/Attribute name Description Mbean name

bytes-consumed-rate The average number of bytes consumed per second kafka.consumer:type=consumer-fetch-manager-metrics,client-id="{client-id}"

bytes-consumed-total The total number of bytes consumed kafka.consumer:type=consumer-fetch-manager-metrics,client-id="{client-id}"

fetch-latency-avg The average time taken for a fetch request. kafka.consumer:type=consumer-fetch-manager-metrics,client-id="{client-id}"

fetch-latency-max The max time taken for any fetch request. kafka.consumer:type=consumer-fetch-manager-metrics,client-id="{client-id}"

fetch-rate The number of fetch requests per second. kafka.consumer:type=consumer-fetch-manager-metrics,client-id="{client-id}"

fetch-size-avg The average number of bytes fetched per request kafka.consumer:type=consumer-fetch-manager-metrics,client-id="{client-id}"

fetch-size-max The maximum number of bytes fetched per request kafka.consumer:type=consumer-fetch-manager-metrics,client-id="{client-id}"

fetch-throttle-time-avg The average throttle time in ms kafka.consumer:type=consumer-fetch-manager-metrics,client-id="{client-id}"

fetch-throttle-time-max The maximum throttle time in ms kafka.consumer:type=consumer-fetch-manager-metrics,client-id="{client-id}"

fetch-total The total number of fetch requests. kafka.consumer:type=consumer-fetch-manager-metrics,client-id="{client-id}"

records-consumed-rate The average number of records consumed per second kafka.consumer:type=consumer-fetch-manager-metrics,client-id="{client-id}"

records-consumed-total The total number of records consumed kafka.consumer:type=consumer-fetch-manager-metrics,client-id="{client-id}"

records-lag-max The maximum lag in terms of number of records for any partition in this window. NOTE: This is based on current offset and not committed offset kafka.consumer:type=consumer-fetch-manager-metrics,client-id="{client-id}"

records-lead-min The minimum lead in terms of number of records for any partition in this window kafka.consumer:type=consumer-fetch-manager-metrics,client-id="{client-id}"

records-per-request-avg The average number of records in each request kafka.consumer:type=consumer-fetch-manager-metrics,client-id="{client-id}"

bytes-consumed-rate The average number of bytes consumed per second for a topic. Note: For topic names with periods (.), an additional metric with underscores is emitted. However, the periods replaced metric is deprecated. Please use the metric with actual topic name instead. kafka.consumer:type=consumer-fetch-manager-metrics,client-id="{client-id}",topic="{topic}"

bytes-consumed-total The total number of bytes consumed for a topic. Note: For topic names with periods (.), an additional metric with underscores is emitted. However, the periods replaced metric is deprecated. Please use the metric with actual topic name instead. kafka.consumer:type=consumer-fetch-manager-metrics,client-id="{client-id}",topic="{topic}"

fetch-size-avg The average number of bytes fetched per request for a topic. Note: For topic names with periods (.), an additional metric with underscores is emitted. However, the periods replaced metric is deprecated. Please use the metric with actual topic name instead. kafka.consumer:type=consumer-fetch-manager-metrics,client-id="{client-id}",topic="{topic}"

fetch-size-max The maximum number of bytes fetched per request for a topic. Note: For topic names with periods (.), an additional metric with underscores is emitted. However, the periods replaced metric is deprecated. Please use the metric with actual topic name instead. kafka.consumer:type=consumer-fetch-manager-metrics,client-id="{client-id}",topic="{topic}"

records-consumed-rate The average number of records consumed per second for a topic. Note: For topic names with periods (.), an additional metric with underscores is emitted. However, the periods replaced metric is deprecated. Please use the metric with actual topic name instead. kafka.consumer:type=consumer-fetch-manager-metrics,client-id="{client-id}",topic="{topic}"

records-consumed-total The total number of records consumed for a topic. Note: For topic names with periods (.), an additional metric with underscores is emitted. However, the periods replaced metric is deprecated. Please use the metric with actual topic name instead. kafka.consumer:type=consumer-fetch-manager-metrics,client-id="{client-id}",topic="{topic}"

records-per-request-avg The average number of records in each request for a topic. Note: For topic names with periods (.), an additional metric with underscores is emitted. However, the periods replaced metric is deprecated. Please use the metric with actual topic name instead. kafka.consumer:type=consumer-fetch-manager-metrics,client-id="{client-id}",topic="{topic}"

preferred-read-replica The current read replica for the partition, or -1 if reading from leader. Note: For topic names with periods (.), an additional metric with underscores is emitted. However, the periods replaced metric is deprecated. Please use the metric with actual topic name instead. kafka.consumer:type=consumer-fetch-manager-metrics,partition="{partition}",topic="{topic}",client-id="{client-id}"

records-lag The latest lag of the partition. Note: For topic names with periods (.), an additional metric with underscores is emitted. However, the periods replaced metric is deprecated. Please use the metric with actual topic name instead. kafka.consumer:type=consumer-fetch-manager-metrics,partition="{partition}",topic="{topic}",client-id="{client-id}"

records-lag-avg The average lag of the partition. Note: For topic names with periods (.), an additional metric with underscores is emitted. However, the periods replaced metric is deprecated. Please use the metric with actual topic name instead. kafka.consumer:type=consumer-fetch-manager-metrics,partition="{partition}",topic="{topic}",client-id="{client-id}"

records-lag-max The max lag of the partition. Note: For topic names with periods (.), an additional metric with underscores is emitted. However, the periods replaced metric is deprecated. Please use the metric with actual topic name instead. kafka.consumer:type=consumer-fetch-manager-metrics,partition="{partition}",topic="{topic}",client-id="{client-id}"

records-lead The latest lead of the partition. Note: For topic names with periods (.), an additional metric with underscores is emitted. However, the periods replaced metric is deprecated. Please use the metric with actual topic name instead. kafka.consumer:type=consumer-fetch-manager-metrics,partition="{partition}",topic="{topic}",client-id="{client-id}"

records-lead-avg The average lead of the partition. Note: For topic names with periods (.), an additional metric with underscores is emitted. However, the periods replaced metric is deprecated. Please use the metric with actual topic name instead. kafka.consumer:type=consumer-fetch-manager-metrics,partition="{partition}",topic="{topic}",client-id="{client-id}"

records-lead-min The min lead of the partition. Note: For topic names with periods (.), an additional metric with underscores is emitted. However, the periods replaced metric is deprecated. Please use the metric with actual topic name instead. kafka.consumer:type=consumer-fetch-manager-metrics,partition="{partition}",topic="{topic}",client-id="{client-id}"

Connect Monitoring

A Connect worker process contains all the producer and consumer metrics as well as metrics specific to Connect. The worker process itself has a number of metrics, while each connector and task have additional metrics.

Metric/Attribute name Description Mbean name

connector-count The number of connectors run in this worker. kafka.connect:type=connect-worker-metrics

connector-startup-attempts-total The total number of connector startups that this worker has attempted. kafka.connect:type=connect-worker-metrics

connector-startup-failure-percentage The average percentage of this worker's connectors starts that failed. kafka.connect:type=connect-worker-metrics

connector-startup-failure-total The total number of connector starts that failed. kafka.connect:type=connect-worker-metrics

connector-startup-success-percentage The average percentage of this worker's connectors starts that succeeded. kafka.connect:type=connect-worker-metrics

connector-startup-success-total The total number of connector starts that succeeded. kafka.connect:type=connect-worker-metrics

task-count The number of tasks run in this worker. kafka.connect:type=connect-worker-metrics

task-startup-attempts-total The total number of task startups that this worker has attempted. kafka.connect:type=connect-worker-metrics

task-startup-failure-percentage The average percentage of this worker's tasks starts that failed. kafka.connect:type=connect-worker-metrics

task-startup-failure-total The total number of task starts that failed. kafka.connect:type=connect-worker-metrics

task-startup-success-percentage The average percentage of this worker's tasks starts that succeeded. kafka.connect:type=connect-worker-metrics

task-startup-success-total The total number of task starts that succeeded. kafka.connect:type=connect-worker-metrics

connector-destroyed-task-count The number of destroyed tasks of the connector on the worker. kafka.connect:type=connect-worker-metrics,connector="{connector}"

connector-failed-task-count The number of failed tasks of the connector on the worker. kafka.connect:type=connect-worker-metrics,connector="{connector}"

connector-paused-task-count The number of paused tasks of the connector on the worker. kafka.connect:type=connect-worker-metrics,connector="{connector}"

connector-restarting-task-count The number of restarting tasks of the connector on the worker. kafka.connect:type=connect-worker-metrics,connector="{connector}"

connector-running-task-count The number of running tasks of the connector on the worker. kafka.connect:type=connect-worker-metrics,connector="{connector}"

connector-total-task-count The number of tasks of the connector on the worker. kafka.connect:type=connect-worker-metrics,connector="{connector}"

connector-unassigned-task-count The number of unassigned tasks of the connector on the worker. kafka.connect:type=connect-worker-metrics,connector="{connector}"

completed-rebalances-total The total number of rebalances completed by this worker. kafka.connect:type=connect-worker-rebalance-metrics

connect-protocol The Connect protocol used by this cluster kafka.connect:type=connect-worker-rebalance-metrics

epoch The epoch or generation number of this worker. kafka.connect:type=connect-worker-rebalance-metrics

leader-name The name of the group leader. kafka.connect:type=connect-worker-rebalance-metrics

rebalance-avg-time-ms The average time in milliseconds spent by this worker to rebalance. kafka.connect:type=connect-worker-rebalance-metrics

rebalance-max-time-ms The maximum time in milliseconds spent by this worker to rebalance. kafka.connect:type=connect-worker-rebalance-metrics

rebalancing Whether this worker is currently rebalancing. kafka.connect:type=connect-worker-rebalance-metrics

time-since-last-rebalance-ms The time in milliseconds since this worker completed the most recent rebalance. kafka.connect:type=connect-worker-rebalance-metrics

connector-class The name of the connector class. kafka.connect:type=connector-metrics,connector="{connector}"

connector-type The type of the connector. One of 'source' or 'sink'. kafka.connect:type=connector-metrics,connector="{connector}"

connector-version The version of the connector class, as reported by the connector. kafka.connect:type=connector-metrics,connector="{connector}"

status The status of the connector. One of 'unassigned', 'running', 'paused', 'stopped', 'failed', or 'restarting'. kafka.connect:type=connector-metrics,connector="{connector}"

predicate-class The class name of the predicate class kafka.connect:type=connector-predicate-metrics,connector="{connector}",task="{task}",predicate="{predicate}"

predicate-version The version of the predicate class kafka.connect:type=connector-predicate-metrics,connector="{connector}",task="{task}",predicate="{predicate}"

batch-size-avg The average number of records in the batches the task has processed so far. kafka.connect:type=connector-task-metrics,connector="{connector}",task="{task}"

batch-size-max The number of records in the largest batch the task has processed so far. kafka.connect:type=connector-task-metrics,connector="{connector}",task="{task}"

connector-class The name of the connector class. kafka.connect:type=connector-task-metrics,connector="{connector}",task="{task}"

connector-type The type of the connector. One of 'source' or 'sink'. kafka.connect:type=connector-task-metrics,connector="{connector}",task="{task}"

connector-version The version of the connector class, as reported by the connector. kafka.connect:type=connector-task-metrics,connector="{connector}",task="{task}"

header-converter-class The fully qualified class name from header.converter kafka.connect:type=connector-task-metrics,connector="{connector}",task="{task}"

header-converter-version The version instantiated for header.converter. May be undefined kafka.connect:type=connector-task-metrics,connector="{connector}",task="{task}"

key-converter-class The fully qualified class name from key.converter kafka.connect:type=connector-task-metrics,connector="{connector}",task="{task}"

key-converter-version The version instantiated for key.converter. May be undefined kafka.connect:type=connector-task-metrics,connector="{connector}",task="{task}"

offset-commit-avg-time-ms The average time in milliseconds taken by this task to commit offsets. kafka.connect:type=connector-task-metrics,connector="{connector}",task="{task}"

offset-commit-failure-percentage The average percentage of this task's offset commit attempts that failed. kafka.connect:type=connector-task-metrics,connector="{connector}",task="{task}"

offset-commit-max-time-ms The maximum time in milliseconds taken by this task to commit offsets. kafka.connect:type=connector-task-metrics,connector="{connector}",task="{task}"

offset-commit-success-percentage The average percentage of this task's offset commit attempts that succeeded. kafka.connect:type=connector-task-metrics,connector="{connector}",task="{task}"

pause-ratio The fraction of time this task has spent in the pause state. kafka.connect:type=connector-task-metrics,connector="{connector}",task="{task}"

running-ratio The fraction of time this task has spent in the running state. kafka.connect:type=connector-task-metrics,connector="{connector}",task="{task}"

status The status of the connector task. One of 'unassigned', 'running', 'paused', 'failed', or 'restarting'. kafka.connect:type=connector-task-metrics,connector="{connector}",task="{task}"

task-class The class name of the task. kafka.connect:type=connector-task-metrics,connector="{connector}",task="{task}"

task-version The version of the task. kafka.connect:type=connector-task-metrics,connector="{connector}",task="{task}"

value-converter-class The fully qualified class name from value.converter kafka.connect:type=connector-task-metrics,connector="{connector}",task="{task}"

value-converter-version The version instantiated for value.converter. May be undefined kafka.connect:type=connector-task-metrics,connector="{connector}",task="{task}"

transform-class The class name of the transformation class kafka.connect:type=connector-transform-metrics,connector="{connector}",task="{task}",transform="{transform}"

transform-version The version of the transformation class kafka.connect:type=connector-transform-metrics,connector="{connector}",task="{task}",transform="{transform}"

offset-commit-completion-rate The average per-second number of offset commit completions that were completed successfully. kafka.connect:type=sink-task-metrics,connector="{connector}",task="{task}"

offset-commit-completion-total The total number of offset commit completions that were completed successfully. kafka.connect:type=sink-task-metrics,connector="{connector}",task="{task}"

offset-commit-seq-no The current sequence number for offset commits. kafka.connect:type=sink-task-metrics,connector="{connector}",task="{task}"

offset-commit-skip-rate The average per-second number of offset commit completions that were received too late and skipped/ignored. kafka.connect:type=sink-task-metrics,connector="{connector}",task="{task}"

offset-commit-skip-total The total number of offset commit completions that were received too late and skipped/ignored. kafka.connect:type=sink-task-metrics,connector="{connector}",task="{task}"

partition-count The number of topic partitions assigned to this task belonging to the named sink connector in this worker. kafka.connect:type=sink-task-metrics,connector="{connector}",task="{task}"

put-batch-avg-time-ms The average time taken by this task to put a batch of sinks records. kafka.connect:type=sink-task-metrics,connector="{connector}",task="{task}"

put-batch-max-time-ms The maximum time taken by this task to put a batch of sinks records. kafka.connect:type=sink-task-metrics,connector="{connector}",task="{task}"

sink-record-active-count The number of records that have been read from Kafka but not yet completely committed/flushed/acknowledged by the sink task. kafka.connect:type=sink-task-metrics,connector="{connector}",task="{task}"

sink-record-active-count-avg The average number of records that have been read from Kafka but not yet completely committed/flushed/acknowledged by the sink task. kafka.connect:type=sink-task-metrics,connector="{connector}",task="{task}"

sink-record-active-count-max The maximum number of records that have been read from Kafka but not yet completely committed/flushed/acknowledged by the sink task. kafka.connect:type=sink-task-metrics,connector="{connector}",task="{task}"

sink-record-lag-max The maximum lag in terms of number of records that the sink task is behind the consumer's position for any topic partitions. kafka.connect:type=sink-task-metrics,connector="{connector}",task="{task}"

sink-record-read-rate The average per-second number of records read from Kafka for this task belonging to the named sink connector in this worker. This is before transformations are applied. kafka.connect:type=sink-task-metrics,connector="{connector}",task="{task}"

sink-record-read-total The total number of records read from Kafka by this task belonging to the named sink connector in this worker, since the task was last restarted. kafka.connect:type=sink-task-metrics,connector="{connector}",task="{task}"

sink-record-send-rate The average per-second number of records output from the transformations and sent/put to this task belonging to the named sink connector in this worker. This is after transformations are applied and excludes any records filtered out by the transformations. kafka.connect:type=sink-task-metrics,connector="{connector}",task="{task}"

sink-record-send-total The total number of records output from the transformations and sent/put to this task belonging to the named sink connector in this worker, since the task was last restarted. kafka.connect:type=sink-task-metrics,connector="{connector}",task="{task}"

poll-batch-avg-time-ms The average time in milliseconds taken by this task to poll for a batch of source records. kafka.connect:type=source-task-metrics,connector="{connector}",task="{task}"

poll-batch-max-time-ms The maximum time in milliseconds taken by this task to poll for a batch of source records. kafka.connect:type=source-task-metrics,connector="{connector}",task="{task}"

source-record-active-count The number of records that have been produced by this task but not yet completely written to Kafka. kafka.connect:type=source-task-metrics,connector="{connector}",task="{task}"

source-record-active-count-avg The average number of records that have been produced by this task but not yet completely written to Kafka. kafka.connect:type=source-task-metrics,connector="{connector}",task="{task}"

source-record-active-count-max The maximum number of records that have been produced by this task but not yet completely written to Kafka. kafka.connect:type=source-task-metrics,connector="{connector}",task="{task}"

source-record-poll-rate The average per-second number of records produced/polled (before transformation) by this task belonging to the named source connector in this worker. kafka.connect:type=source-task-metrics,connector="{connector}",task="{task}"

source-record-poll-total The total number of records produced/polled (before transformation) by this task belonging to the named source connector in this worker. kafka.connect:type=source-task-metrics,connector="{connector}",task="{task}"

source-record-write-rate The average per-second number of records written to Kafka for this task belonging to the named source connector in this worker, since the task was last restarted. This is after transformations are applied, and excludes any records filtered out by the transformations. kafka.connect:type=source-task-metrics,connector="{connector}",task="{task}"

source-record-write-total The number of records output written to Kafka for this task belonging to the named source connector in this worker, since the task was last restarted. This is after transformations are applied, and excludes any records filtered out by the transformations. kafka.connect:type=source-task-metrics,connector="{connector}",task="{task}"

transaction-size-avg The average number of records in the transactions the task has committed so far. kafka.connect:type=source-task-metrics,connector="{connector}",task="{task}"

transaction-size-max The number of records in the largest transaction the task has committed so far. kafka.connect:type=source-task-metrics,connector="{connector}",task="{task}"

transaction-size-min The number of records in the smallest transaction the task has committed so far. kafka.connect:type=source-task-metrics,connector="{connector}",task="{task}"

deadletterqueue-produce-failures The number of failed writes to the dead letter queue. kafka.connect:type=task-error-metrics,connector="{connector}",task="{task}"

deadletterqueue-produce-requests The number of attempted writes to the dead letter queue. kafka.connect:type=task-error-metrics,connector="{connector}",task="{task}"

last-error-timestamp The epoch timestamp when this task last encountered an error. kafka.connect:type=task-error-metrics,connector="{connector}",task="{task}"

total-errors-logged The number of errors that were logged. kafka.connect:type=task-error-metrics,connector="{connector}",task="{task}"

total-record-errors The number of record processing errors in this task. kafka.connect:type=task-error-metrics,connector="{connector}",task="{task}"

total-record-failures The number of record processing failures in this task. kafka.connect:type=task-error-metrics,connector="{connector}",task="{task}"

total-records-skipped The number of records skipped due to errors. kafka.connect:type=task-error-metrics,connector="{connector}",task="{task}"

total-retries The number of operations retried. kafka.connect:type=task-error-metrics,connector="{connector}",task="{task}"

Streams Monitoring

A Kafka Streams instance contains all the producer and consumer metrics as well as additional metrics specific to Streams. The metrics have three recording levels:

info

debug

, and

trace

Note that the metrics have a 4-layer hierarchy. At the top level there are client-level metrics for each started Kafka Streams client. Each client has stream threads, with their own metrics. Each stream thread has tasks, with their own metrics. Each task has a number of processor nodes, with their own metrics. Each task also has a number of state stores and record caches, all with their own metrics.

Use the following configuration option to specify which metrics you want collected:

metrics.recording.level = "info"

Client Metrics

All the following metrics have a recording level of

info

Metric/Attribute name

Description

Mbean name

version

The version of the Kafka Streams client.

kafka.streams:type=stream-metrics,client-id=([-.\w]+)

commit-id

The version control commit ID of the Kafka Streams client.

kafka.streams:type=stream-metrics,client-id=([-.\w]+)

application-id

The application ID of the Kafka Streams client.

kafka.streams:type=stream-metrics,client-id=([-.\w]+)

topology-description

The description of the topology executed in the Kafka Streams client.

kafka.streams:type=stream-metrics,client-id=([-.\w]+)

state

The state of the Kafka Streams client as a string.

kafka.streams:type=stream-metrics,client-id=([-.\w]+)

client-state

The state of the Kafka Streams client as a number (

ordinal()

of the corresponding enum).

kafka.streams:type=stream-metrics,client-id=([-.\w]+),process-id=([-.\w]+),application-id=([-.\w]+)

alive-stream-threads

The current number of alive stream threads that are running or participating in rebalance.

kafka.streams:type=stream-metrics,client-id=([-.\w]+)

failed-stream-threads

The number of failed stream threads since the start of the Kafka Streams client.

kafka.streams:type=stream-metrics,client-id=([-.\w]+)

recording-level

The metric recording level as a number (0 = INFO, 1 = DEBUG, 2 = TRACE).

kafka.streams:type=stream-metrics,client-id=([-.\w]+),process-id=([-.\w]+)

Thread Metrics

All the following metrics have a recording level of

info

Metric/Attribute name

Description

Mbean name

state

The state of the thread as a string.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

thread-state

The state of the thread as a number (

ordinal()

of the corresponding enum).

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+),process-id=([-.\w]+)

commit-latency-avg

The average execution time in ms, for committing, across all running tasks of this thread.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

commit-latency-max

The maximum execution time in ms, for committing, across all running tasks of this thread.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

poll-latency-avg

The average execution time in ms, for consumer polling.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

poll-latency-max

The maximum execution time in ms, for consumer polling.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

process-latency-avg

The average execution time in ms, for processing.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

process-latency-max

The maximum execution time in ms, for processing.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

punctuate-latency-avg

The average execution time in ms, for punctuating.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

punctuate-latency-max

The maximum execution time in ms, for punctuating.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

commit-ratio

The fraction of time the thread spent on committing all tasks

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

commit-rate

The average number of commits per sec.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

commit-total

The total number of commit calls.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

poll-ratio

The fraction of time the thread spent on polling records from consumer

kafka.consumer:type=consumer-coordinator-metrics,client-id=([-.\w]+)

poll-rate

The average number of consumer poll calls per sec.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

poll-total

The total number of consumer poll calls.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

poll-records-avg

The average number of records polled from consumer within an iteration.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

poll-records-max

The maximum number of records polled from consumer within an iteration.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

process-ratio

The fraction of time the thread spent on processing active tasks

kafka.streams:type=type=stream-thread-metrics,client-id=([-.\w]+)

process-rate

The average number of processed records per sec.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

process-total

The total number of processed records.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

process-records-avg

The average number of records processed within an iteration (total count of processed records over total number of iterations).

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

process-records-max

The maximum number of records processed within an iteration.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

punctuate-ratio

The fraction of time the thread spends performing punctuating actions on active tasks

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

punctuate-rate

The average number of punctuate calls per sec.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

punctuate-total

The total number of punctuate calls.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

task-created-rate

The average number of tasks created per sec.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

task-created-total

The total number of tasks created.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

task-closed-rate

The average number of tasks closed per sec.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

task-closed-total

The total number of tasks closed.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

blocked-time-ns-total

The total time in ns the thread spent blocked on Kafka brokers.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

thread-start-time

The system timestamp in ms that the thread was started.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

tasks-revoked-latency-avg

The average time in ms taken for tasks-revoked rebalance listener callback.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

tasks-revoked-latency-max

The maximum time in ms taken for tasks-revoked rebalance listener callback.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

tasks-assigned-latency-avg

The average time in ms taken for tasks-assigned rebalance listener callback.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

tasks-assigned-latency-max

The maximum time in ms taken for tasks-assigned rebalance listener callback.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

tasks-lost-latency-avg

The average time in ms taken for tasks-lost rebalance listener callback.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

tasks-lost-latency-max

The maximum time in ms taken for tasks-lost rebalance listener callback.

kafka.streams:type=stream-thread-metrics,thread-id=([-.\w]+)

Task Metrics

All the following metrics have a recording level of

debug

, except for the dropped-records-* and active-process-ratio metrics which have a recording level of

info

Metric/Attribute name

Description

Mbean name

process-latency-avg

The average execution time in ns, for processing.

kafka.streams:type=stream-task-metrics,thread-id=([-.\w]+),task-id=([-.\w]+)

process-latency-max

The maximum execution time in ns, for processing.

kafka.streams:type=stream-task-metrics,thread-id=([-.\w]+),task-id=([-.\w]+)

process-rate

The average number of processed records per sec across all source processor nodes of this task.

kafka.streams:type=stream-task-metrics,thread-id=([-.\w]+),task-id=([-.\w]+)

process-total

The total number of processed records across all source processor nodes of this task.

kafka.streams:type=stream-task-metrics,thread-id=([-.\w]+),task-id=([-.\w]+)

punctuate-latency-avg

The average amount of time taken to execute periodic tasks per call to punctuate

kafka.streams:type=stream-task-metrics,thread-id=([-.\w]+),task-id=([-.\w]+)

punctuate-latency-max

The maximum amount of time taken for any single call to punctuate to complete.

kafka.streams:type=stream-task-metrics,thread-id=([-.\w]+),task-id=([-.\w]+)

punctuate-total

The total number of times the punctuate method was called to trigger periodic actions during task processing.

kafka.streams:type=stream-task-metrics,thread-id=([-.\w]+),task-id=([-.\w]+)

punctuate-rate

The average number of calls to punctuate per second.

kafka.streams:type=stream-task-metrics,thread-id=([-.\w]+),task-id=([-.\w]+)

record-lateness-avg

The average observed lateness in ms of records (stream time - record timestamp).

kafka.streams:type=stream-task-metrics,thread-id=([-.\w]+),task-id=([-.\w]+)

record-lateness-max

The max observed lateness in ms of records (stream time - record timestamp).

kafka.streams:type=stream-task-metrics,thread-id=([-.\w]+),task-id=([-.\w]+)

enforced-processing-rate

The average number of enforced processings per sec.

kafka.streams:type=stream-task-metrics,thread-id=([-.\w]+),task-id=([-.\w]+)

enforced-processing-total

The total number enforced processings.

kafka.streams:type=stream-task-metrics,thread-id=([-.\w]+),task-id=([-.\w]+)

dropped-records-rate

The average number of records dropped per sec within this task.

kafka.streams:type=stream-task-metrics,thread-id=([-.\w]+),task-id=([-.\w]+)

dropped-records-total

The total number of records dropped within this task.

kafka.streams:type=stream-task-metrics,thread-id=([-.\w]+),task-id=([-.\w]+)

active-process-ratio

The fraction of time the stream thread spent on processing this task among all assigned active tasks.

kafka.streams:type=stream-task-metrics,thread-id=([-.\w]+),task-id=([-.\w]+)

active-buffer-count

The count of buffered records that are polled from consumer and not yet processed for this active task.

kafka.streams:type=stream-task-metrics,thread-id=([-.\w]+),task-id=([-.\w]+)

input-buffer-bytes-total

The total number of bytes accumulated by this task,

kafka.streams:type=stream-task-metrics,thread-id=([-.\w]+),task-id=([-.\w]+)

cache-size-bytes-total

The cache size in bytes accumulated by this task.

kafka.streams:type=stream-task-metrics,thread-id=([-.\w]+),task-id=([-.\w]+)

record-rate

The average number of records restored per second.

kafka.streams:type=stream-task-metrics,thread-id=([-.\w]+),task-id=([-.\w]+)

record-total

The total number of records restored

kafka.streams:type=stream-task-metrics,thread-id=([-.\w]+),task-id=([-.\w]+)

update-rate

The average number of records updated per second.

kafka.streams:type=stream-task-metrics,thread-id=([-.\w]+),task-id=([-.\w]+)

update-total

The total number of records updated

kafka.streams:type=stream-task-metrics,thread-id=([-.\w]+),task-id=([-.\w]+)

Processor Node Metrics

The following metrics are only available on certain types of nodes, i.e., the process-* metrics are only available for source processor nodes, the

suppression-emit-*

metrics are only available for suppression operation nodes,

emit-final-*

metrics are only available for windowed aggregations nodes, and the

record-e2e-latency-*

metrics are only available for source processor nodes and terminal nodes (nodes without successor nodes). All the metrics have a recording level of

debug

, except for the

record-e2e-latency-*

metrics which have a recording level of

info

Metric/Attribute name

Description

Mbean name

bytes-consumed-total

The total number of bytes consumed by a source processor node.

kafka.streams:type=stream-topic-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+),topic=([-.\w]+)

bytes-produced-total

The total number of bytes produced by a sink processor node.

kafka.streams:type=stream-topic-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+),topic=([-.\w]+)

process-rate

The average number of records processed by a source processor node per sec.

kafka.streams:type=stream-processor-node-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)

process-total

The total number of records processed by a source processor node per sec.

kafka.streams:type=stream-processor-node-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)

suppression-emit-rate

The rate of records emitted per sec that have been emitted downstream from suppression operation nodes.

kafka.streams:type=stream-processor-node-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)

suppression-emit-total

The total number of records that have been emitted downstream from suppression operation nodes.

kafka.streams:type=stream-processor-node-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)

emit-final-latency-max

The max latency in ms to emit final records when a record could be emitted.

kafka.streams:type=stream-processor-node-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)

emit-final-latency-avg

The avg latency in ms to emit final records when a record could be emitted.

kafka.streams:type=stream-processor-node-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)

emit-final-records-rate

The rate of records emitted per sec when records could be emitted.

kafka.streams:type=stream-processor-node-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)

emit-final-records-total

The total number of records emitted.

kafka.streams:type=stream-processor-node-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)

record-e2e-latency-avg

The average end-to-end latency in ms of a record, measured by comparing the record timestamp with the system time when it has been fully processed by the node.

kafka.streams:type=stream-processor-node-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)

record-e2e-latency-max

The maximum end-to-end latency in ms of a record, measured by comparing the record timestamp with the system time when it has been fully processed by the node.

kafka.streams:type=stream-processor-node-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)

record-e2e-latency-min

The minimum end-to-end latency in ms of a record, measured by comparing the record timestamp with the system time when it has been fully processed by the node.

kafka.streams:type=stream-processor-node-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+)

records-consumed-total

The total number of records consumed by a source processor node.

kafka.streams:type=stream-topic-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+),topic=([-.\w]+)

records-produced-total

The total number of records produced by a sink processor node.

kafka.streams:type=stream-topic-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+),topic=([-.\w]+)

Idempotent-update-skip-rate

The average number of skipped idempotent updates per second.

kafka.streams:type=stream-topic-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+),topic=([-.\w]+)

Idempotent-update-skip-total

The total number of skipped updates.

kafka.streams:type=stream-topic-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),processor-node-id=([-.\w]+),topic=([-.\w]+)

State Store Metrics

All the following metrics have a recording level of

debug

, except for the

record-e2e-latency-*

metrics which have a recording level

trace

and

num-open-iterators

and

num-keys

which have recording level

info

. Note that the

store-scope

value is specified in

StoreSupplier#metricsScope()

for user’s customized state stores; for built-in state stores, currently we have:

in-memory-state

in-memory-lru-state

in-memory-window-state

in-memory-suppression

(for suppression buffers)

rocksdb-state

(for RocksDB backed key-value store)

rocksdb-window-state

(for RocksDB backed window store)

rocksdb-session-state

(for RocksDB backed session store)

Metrics suppression-buffer-size-avg, suppression-buffer-size-max, suppression-buffer-count-avg, and suppression-buffer-count-max are only available for suppression buffers. All other metrics are not available for suppression buffers.

Metric/Attribute name

Description

Mbean name

put-latency-avg

The average put execution time in ns.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

put-latency-max

The maximum put execution time in ns.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

put-if-absent-latency-avg

The average put-if-absent execution time in ns.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

put-if-absent-latency-max

The maximum put-if-absent execution time in ns.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

get-latency-avg

The average get execution time in ns.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

get-latency-max

The maximum get execution time in ns.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

delete-latency-avg

The average delete execution time in ns.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

delete-latency-max

The maximum delete execution time in ns.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

put-all-latency-avg

The average put-all execution time in ns.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

put-all-latency-max

The maximum put-all execution time in ns.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

all-latency-avg

The average execution time in ns, from iterator create to close time.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

all-latency-max, from iterator create to close time.

The maximum all operation execution time in ns.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

range-latency-avg, from iterator create to close time.

The average range execution time in ns, from iterator create to close time.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

range-latency-max, from iterator create to close time.

The maximum range execution time in ns.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

prefix-scan-latency-avg

The average prefix-scan execution time in ns, from iterator create to close time.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

prefix-scan-latency-max

The maximum prefix-scan execution time in ns, from iterator create to close time.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

flush-latency-avg (deprecated)

The average flush execution time in ns. Deprecated: use commit-latency-avg instead.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

flush-latency-max (deprecated)

The maximum flush execution time in ns. Deprecated: use commit-latency-max instead.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

commit-latency-avg

The average commit execution time in ns.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

commit-latency-max

The maximum commit execution time in ns.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

restore-latency-avg

The average restore execution time in ns.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

restore-latency-max

The maximum restore execution time in ns.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

put-rate

The average put rate per sec for this store.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

put-if-absent-rate

The average put-if-absent rate per sec for this store.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

get-rate

The average get rate per sec for this store.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

delete-rate

The average delete rate per sec for this store.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

put-all-rate

The average put-all rate per sec for this store.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

all-rate

The average all operation rate per sec for this store.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

range-rate

The average range rate per sec for this store.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

prefix-scan-rate

The average prefix-scan rate per sec for this store.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

flush-rate (deprecated)

The average flush rate for this store. Deprecated: use commit-rate instead.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

commit-rate

The average commit rate for this store.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

restore-rate

The average restore rate for this store.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

suppression-buffer-size-avg

The average total size in bytes of the buffered data over the sampling window.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),in-memory-suppression-id=([-.\w]+)

suppression-buffer-size-max

The maximum total size, in bytes, of the buffered data over the sampling window.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),in-memory-suppression-id=([-.\w]+)

suppression-buffer-count-avg

The average number of records buffered over the sampling window.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),in-memory-suppression-id=([-.\w]+)

suppression-buffer-count-max

The maximum number of records buffered over the sampling window.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),in-memory-suppression-id=([-.\w]+)

record-e2e-latency-avg

The average end-to-end latency in ms of a record, measured by comparing the record timestamp with the system time when it has been fully processed by the node.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

record-e2e-latency-max

The maximum end-to-end latency in ms of a record, measured by comparing the record timestamp with the system time when it has been fully processed by the node.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

record-e2e-latency-min

The minimum end-to-end latency in ms of a record, measured by comparing the record timestamp with the system time when it has been fully processed by the node.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

num-open-iterators

The current number of iterators on the store that have been created, but not yet closed.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

num-keys

The current number of keys in the in-memory state store. Only reported for in-memory state stores; not available for RocksDB-backed stores.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

iterator-duration-avg

The average time in ns spent between creating an iterator and closing it.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

iterator-duration-max

The maximum time in ns spent between creating an iterator and closing it.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

oldest-iterator-open-since-ms

The system timestamp in ms the oldest still open iterator was created.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

RocksDB Metrics

RocksDB metrics are grouped into statistics-based metrics and properties-based metrics. The former are recorded from statistics that a RocksDB state store collects whereas the latter are recorded from properties that RocksDB exposes. Statistics collected by RocksDB provide cumulative measurements over time, e.g. bytes written to the state store. Properties exposed by RocksDB provide current measurements, e.g., the amount of memory currently used. Note that the

store-scope

for built-in RocksDB state stores are currently the following:

rocksdb-state

(for RocksDB backed key-value store)

rocksdb-window-state

(for RocksDB backed window store)

rocksdb-session-state

(for RocksDB backed session store)

RocksDB Statistics-based Metrics: All the following statistics-based metrics have a recording level of

debug

because collecting statistics in RocksDB may have an impact on performance . Statistics-based metrics are collected every minute from the RocksDB state stores. If a state store consists of multiple RocksDB instances, as is the case for WindowStores and SessionStores, each metric reports an aggregation over the RocksDB instances of the state store.

Metric/Attribute name

Description

Mbean name

bytes-written-rate

The average number of bytes written per sec to the RocksDB state store.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

bytes-written-total

The total number of bytes written to the RocksDB state store.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

bytes-read-rate

The average number of bytes read per second from the RocksDB state store.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

bytes-read-total

The total number of bytes read from the RocksDB state store.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

memtable-bytes-flushed-rate

The average number of bytes flushed per sec from the memtable to disk.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

memtable-bytes-flushed-total

The total number of bytes flushed from the memtable to disk.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

memtable-hit-ratio

The ratio of memtable hits relative to all lookups to the memtable.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

memtable-flush-time-avg

The average duration in ms of memtable flushes to disc.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

memtable-flush-time-min

The minimum duration of memtable flushes to disc in ms.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

memtable-flush-time-max

The maximum duration in ms of memtable flushes to disc.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

block-cache-data-hit-ratio

The ratio of block cache hits for data blocks relative to all lookups for data blocks to the block cache.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

block-cache-index-hit-ratio

The ratio of block cache hits for index blocks relative to all lookups for index blocks to the block cache.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

block-cache-filter-hit-ratio

The ratio of block cache hits for filter blocks relative to all lookups for filter blocks to the block cache.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

write-stall-duration-avg

The average duration in ms of write stalls.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

write-stall-duration-total

The total duration in ms of write stalls.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

bytes-read-compaction-rate

The average number of bytes read per sec during compaction.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

bytes-written-compaction-rate

The average number of bytes written per sec during compaction.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

compaction-time-avg

The average duration in ms of disc compactions.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

compaction-time-min

The minimum duration of disc compactions in ms.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

compaction-time-max

The maximum duration in ms of disc compactions.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

number-open-files

This metric will return constant -1 because the RocksDB’s counter NO_FILE_CLOSES has been removed in RocksDB 9.7.3

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

number-file-errors-total

The total number of file errors occurred.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

**RocksDB Properties-based Metrics:** All the following properties-based metrics have a recording level of `info` and are recorded when the metrics are accessed. If a state store consists of multiple RocksDB instances, as is the case for WindowStores and SessionStores, each metric reports the sum over all the RocksDB instances of the state store, except for the block cache metrics `block-cache-*`. The block cache metrics report the sum over all RocksDB instances if each instance uses its own block cache, and they report the recorded value from only one instance if a single block cache is shared among all instances.

Metric/Attribute name

Description

Mbean name

num-immutable-mem-table

The number of immutable memtables that have not yet been flushed.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

cur-size-active-mem-table

The approximate size in bytes of the active memtable.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

cur-size-all-mem-tables

The approximate size in bytes of active and unflushed immutable memtables.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

size-all-mem-tables

The approximate size in bytes of active, unflushed immutable, and pinned immutable memtables.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

num-entries-active-mem-table

The number of entries in the active memtable.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

num-entries-imm-mem-tables

The number of entries in the unflushed immutable memtables.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

num-deletes-active-mem-table

The number of delete entries in the active memtable.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

num-deletes-imm-mem-tables

The number of delete entries in the unflushed immutable memtables.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

mem-table-flush-pending

This metric reports 1 if a memtable flush is pending, otherwise it reports 0.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

num-running-flushes

The number of currently running flushes.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

compaction-pending

This metric reports 1 if at least one compaction is pending, otherwise it reports 0.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

num-running-compactions

The number of currently running compactions.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

estimate-pending-compaction-bytes

The estimated total number of bytes a compaction needs to rewrite on disk to get all levels down to under target size (only valid for level compaction).

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

total-sst-files-size

The total size in bytes of all SST files.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

live-sst-files-size

The total size in bytes of all SST files that belong to the latest LSM tree.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

num-live-versions

Number of live versions of the LSM tree.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

block-cache-capacity

The capacity in bytes of the block cache.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

block-cache-usage

The memory size in bytes of the entries residing in block cache.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

block-cache-pinned-usage

The memory size in bytes for the entries being pinned in the block cache.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

estimate-num-keys

The estimated number of keys in the active and unflushed immutable memtables and storage.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

estimate-table-readers-mem

The estimated memory in bytes used for reading SST tables, excluding memory used in block cache.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

background-errors

The total number of background errors.

kafka.streams:type=stream-state-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),[store-scope]-id=([-.\w]+)

Record Cache Metrics

All the following metrics have a recording level of

debug

Metric/Attribute name

Description

Mbean name

hit-ratio-avg

The average cache hit ratio defined as the ratio of cache read hits over the total cache read requests.

kafka.streams:type=stream-record-cache-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),record-cache-id=([-.\w]+)

hit-ratio-min

The minimum cache hit ratio.

kafka.streams:type=stream-record-cache-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),record-cache-id=([-.\w]+)

hit-ratio-max

The maximum cache hit ratio.

kafka.streams:type=stream-record-cache-metrics,thread-id=([-.\w]+),task-id=([-.\w]+),record-cache-id=([-.\w]+)

Share Group Monitoring

The following set of metrics are available for monitoring the share group:

Metric/Attribute name

Mbean name

Description

TotalShareFetchRequestsPerSec

kafka.server:type=BrokerTopicMetrics,name=TotalShareFetchRequestsPerSec,topic=([-.\w]+)

The fetch request rate per second.

FailedShareFetchRequestsPerSec

kafka.server:type=BrokerTopicMetrics,name=FailedShareFetchRequestsPerSec,topic=([-.\w]+)

The share fetch request rate for requests that failed.

TotalShareAcknowledgementRequestsPerSec

kafka.server:type=BrokerTopicMetrics,name=TotalShareAcknowledgementRequestsPerSec,topic=([-.\w]+)

The acknowledgement request rate per second.

FailedShareAcknowledgementRequestsPerSec

kafka.server:type=BrokerTopicMetrics,name=FailedShareAcknowledgementRequestsPerSec,topic=([-.\w]+)

The share acknowledgement request rate for requests that failed.

RecordAcknowledgementsPerSec

kafka.server:type=ShareGroupMetrics,name=RecordAcknowledgementsPerSec,ackType={Accept|Release|Reject|Renew}

The rate per second of records acknowledged per acknowledgement type.

PartitionLoadTimeMs

kafka.server:type=ShareGroupMetrics,name=PartitionLoadTimeMs

The time taken to load the share partitions.

RequestTopicPartitionsFetchRatio

kafka.server:type=ShareGroupMetrics,name=RequestTopicPartitionsFetchRatio,group=([-.\w]+)

The ratio of topic-partitions acquired to the total number of topic-partitions in share fetch request.

TopicPartitionsAcquireTimeMs

kafka.server:type=ShareGroupMetrics,name=TopicPartitionsAcquireTimeMs,group=([-.\w]+)

The time elapsed (in millisecond) to acquire any topic partition for fetch.

AcquisitionLockTimeoutPerSec

kafka.server:type=SharePartitionMetrics,name=AcquisitionLockTimeoutPerSec,group=([-.\w]+),topic=([-.\w]+),partition=([0-9]+)

The rate of acquisition locks for records which are not acknowledged within the timeout.

InFlightMessageCount

kafka.server:type=SharePartitionMetrics,name=InFlightMessageCount,group=([-.\w]+),topic=([-.\w]+),partition=([0-9]+)

The number of in-flight messages for the share partition.

InFlightBatchCount

kafka.server:type=SharePartitionMetrics,name=InFlightBatchCount,group=([-.\w]+),topic=([-.\w]+),partition=([0-9]+)

The number of in-flight batches for the share partition.

InFlightBatchMessageCount

kafka.server:type=SharePartitionMetrics,name=InFlightBatchMessageCount,group=([-.\w]+),topic=([-.\w]+),partition=([0-9]+)

The number of messages in the in-flight batch.

FetchLockTimeMs

kafka.server:type=SharePartitionMetrics,name=FetchLockTimeMs,group=([-.\w]+),topic=([-.\w]+),partition=([0-9]+)

The time elapsed (in milliseconds) while a share partition is held under lock for fetching messages.

FetchLockRatio

kafka.server:type=SharePartitionMetrics,name=FetchLockRatio,group=([-.\w]+),topic=([-.\w]+),partition=([0-9]+)

The fraction of time that share partition is held under lock.

ShareSessionEvictionsPerSec

kafka.server:type=ShareSessionCache,name=ShareSessionEvictionsPerSec

The share session eviction rate per second.

SharePartitionsCount

kafka.server:type=ShareSessionCache,name=SharePartitionsCount

The number of cached share partitions.

ShareSessionsCount

kafka.server:type=ShareSessionCache,name=ShareSessionsCount

The number of cached share sessions.

NumDelayedOperations (ShareFetch)

kafka.server:type=DelayedOperationPurgatory,name=NumDelayedOperations,delayedOperation=ShareFetch

The number of delayed operations for share fetch purgatory.

PurgatorySize (ShareFetch)

kafka.server:type=DelayedOperationPurgatory,name=PurgatorySize,delayedOperation=ShareFetch

The number of requests waiting in the share fetch purgatory. This is high if share consumers use a large value for fetch.wait.max.ms.

ExpiresPerSec

kafka.server:type=DelayedShareFetchMetrics,name=ExpiresPerSec

The expired delayed share fetch operation rate per second.

Coordinator Metrics

Metric/Attribute name

Mbean name

Description

group-count

kafka.server:type=group-coordinator-metrics,name=group-count,protocol=share

The total number of share groups managed by group coordinator.

share-group-rebalance-rate

kafka.server:type=group-coordinator-metrics,name=share-group-rebalance-rate

The total number of share group rebalances.

share-group-rebalance-count

kafka.server:type=group-coordinator-metrics,name=share-group-rebalance-count

The total number of share group rebalances.

group-count

kafka.server:type=group-coordinator-metrics,name=group-count,protocol=share

The total number of share groups managed by group coordinator.

partition-load-time-max

kafka.server:type=share-coordinator-metrics,name=partition-load-time-max

The maximum time taken in milliseconds to load the share-group state from the share-group state partitions.

partition-load-time-avg

kafka.server:type=share-coordinator-metrics,name=partition-load-time-avg

The average time taken in milliseconds to load the share-group state from the share-group state partitions.

thread-idle-ratio-min

kafka.server:type=share-coordinator-metrics,name=thread-idle-ratio-min

The minimum fraction of time the share coordinator thread is idle.

thread-idle-ratio-avg

kafka.server:type=share-coordinator-metrics,name=thread-idle-ratio-avg

The average fraction of time the share coordinator thread is idle.

write-rate

kafka.server:type=share-coordinator-metrics,name=write-rate

The number of share-group state write calls per second.

write-total

kafka.server:type=share-coordinator-metrics,name=write-total

The total number of share-group state write calls.

write-latency-avg

kafka.server:type=share-coordinator-metrics,name=write-latency-avg

The average time taken for a share-group state write call, including the time to write to the share-group state topic.

write-latency-max

kafka.server:type=share-coordinator-metrics,name=write-latency-max

The maximum time taken for a share-group state write call, including the time to write to the share-group state topic.

num-partitions

kafka.server:type=share-coordinator-metrics,name=num-partitions,state={loading|active|failed}

The number of partitions in the share-state topic in each state.

last-pruned-offset

kafka.server:type=share-coordinator-metrics,name=last-pruned-offset,topic=([-.\w]+),partition=([0-9]+)

The offset at which the share-group state topic was last pruned.

batch-buffer-cache-size-bytes

kafka.server:type=share-coordinator-metrics,name=batch-buffer-cache-size-bytes

The total size in bytes of append buffers currently held in the share coordinator’s cache

batch-buffer-cache-discard-count

kafka.server:type=share-coordinator-metrics,name=batch-buffer-cache-discard-count

The total number of over-sized append buffers that were discarded upon release

Client Metrics

The following metrics are available on share consumer instances:

Metric/Attribute name

Mbean name

Description

last-poll-seconds-ago

kafka.consumer:type=consumer-share-metrics,name=last-poll-seconds-ago,client-id=([-.\w]+)

The number of seconds since the last poll() invocation.

time-between-poll-avg

kafka.consumer:type=consumer-share-metrics,name=time-between-poll-avg,client-id=([-.\w]+)

The average delay between invocations of poll() in milliseconds.

time-between-poll-max

kafka.consumer:type=consumer-share-metrics,name=time-between-poll-max,client-id=([-.\w]+)

The maximum delay between invocations of poll() in milliseconds.

poll-idle-ratio-avg

kafka.consumer:type=consumer-share-metrics,name=poll-idle-ratio-avg,client-id=([-.\w]+)

The average fraction of time the consumer’s poll() is idle as opposed to waiting for the user code to process records.

heartbeat-response-time-max

kafka.consumer:type=consumer-share-coordinator-metrics,name=heartbeat-response-time-max,client-id=([-.\w]+)

The maximum time taken to receive a response to a heartbeat request in milliseconds.

heartbeat-rate

kafka.consumer:type=consumer-share-coordinator-metrics,name=heartbeat-rate,client-id=([-.\w]+)

The number of heartbeats per second.

heartbeat-total

kafka.consumer:type=consumer-share-coordinator-metrics,name=heartbeat-total,client-id=([-.\w]+)

The total number of heartbeats.

last-heartbeat-seconds-ago

kafka.consumer:type=consumer-share-coordinator-metrics,name=last-heartbeat-seconds-ago,client-id=([-.\w]+)

The number of seconds since the last coordinator heartbeat was sent.

rebalance-total

kafka.consumer:type=consumer-share-coordinator-metrics,name=rebalance-total,client-id=([-.\w]+)

The total number of share group rebalances count.

rebalance-rate-per-hour

kafka.consumer:type=consumer-share-coordinator-metrics,name=rebalance-rate-per-hour,client-id=([-.\w]+)

The number of share group rebalances event per hour.

fetch-size-avg

kafka.consumer:type=consumer-share-fetch-manager-metrics,name=fetch-size-avg,client-id=([-.\w]+)

The average number of bytes fetched per request.

fetch-size-max

kafka.consumer:type=consumer-share-fetch-manager-metrics,name=fetch-size-max,client-id=([-.\w]+)

The maximum number of bytes fetched per request.

records-per-request-avg

kafka.consumer:type=consumer-share-fetch-manager-metrics,name=records-per-request-avg,client-id=([-.\w]+)

The average number of records in each request.

records-per-request-max

kafka.consumer:type=consumer-share-fetch-manager-metrics,name=records-per-request-max,client-id=([-.\w]+)

The maximum number of records in a request.

bytes-consumed-rate

kafka.consumer:type=consumer-share-fetch-manager-metrics,name=bytes-consumed-rate,client-id=([-.\w]+)

The average number of bytes consumed per second.

bytes-consumed-total

kafka.consumer:type=consumer-share-fetch-manager-metrics,name=bytes-consumed-total,client-id=([-.\w]+)

The total number of bytes consumed.

records-consumed-rate

kafka.consumer:type=consumer-share-fetch-manager-metrics,name=records-consumed-rate,client-id=([-.\w]+)

The average number of records fetched per second.

records-consumed-total

kafka.consumer:type=consumer-share-fetch-manager-metrics,name=records-consumed-total,client-id=([-.\w]+)

The total number of records fetched.

acknowledgements-send-rate

kafka.consumer:type=consumer-share-fetch-manager-metrics,name=acknowledgements-send-rate,client-id=([-.\w]+)

The average number of record acknowledgements sent per second.

acknowledgements-send-total

kafka.consumer:type=consumer-share-fetch-manager-metrics,name=acknowledgements-send-total,client-id=([-.\w]+)

The total number of record acknowledgements sent.

acknowledgements-error-rate

kafka.consumer:type=consumer-share-fetch-manager-metrics,name=acknowledgements-error-rate,client-id=([-.\w]+)

The average number of record acknowledgements that resulted in errors per second.

acknowledgements-error-total

kafka.consumer:type=consumer-share-fetch-manager-metrics,name=acknowledgements-error-total,client-id=([-.\w]+)

The total number of record acknowledgements that resulted in errors.

fetch-latency-avg

kafka.consumer:type=consumer-share-fetch-manager-metrics,name=fetch-latency-avg,client-id=([-.\w]+)

The average time taken for a fetch request.

fetch-latency-max

kafka.consumer:type=consumer-share-fetch-manager-metrics,name=fetch-latency-max,client-id=([-.\w]+)

The maximum time taken for any fetch request.

fetch-rate

kafka.consumer:type=consumer-share-fetch-manager-metrics,name=fetch-rate,client-id=([-.\w]+)

The number of fetch requests per second.

fetch-total

kafka.consumer:type=consumer-share-fetch-manager-metrics,name=fetch-total,client-id=([-.\w]+)

The total number of fetch requests.

fetch-throttle-time-avg

kafka.consumer:type=consumer-share-fetch-manager-metrics,name=fetch-throttle-time-avg,client-id=([-.\w]+)

The average throttle time in milliseconds.

fetch-throttle-time-max

kafka.consumer:type=consumer-share-fetch-manager-metrics,name=fetch-throttle-time-max,client-id=([-.\w]+)

The maximum throttle time in milliseconds.

Others

We recommend monitoring GC time and other stats and various server stats such as CPU utilization, I/O service time, etc. On the client side, we recommend monitoring the message/byte rate (global and per topic), request rate/size/time, and on the consumer side, max lag in messages among all partitions and min fetch request rate. For a consumer to keep up, max lag needs to be less than a threshold and min fetch rate needs to be larger than 0.

Last modified June 25, 2026: Update docs for 4.3.1 release (#886) (43d2ba2ab1)
