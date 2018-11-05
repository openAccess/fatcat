#!/usr/bin/env python3

import sys
import argparse
from fatcat.changelog_workers import FatcatChangelogWorker, FatcatEntityUpdatesWorker

def run_changelog_worker(args):
    topic = "fatcat-{}.changelog".format(args.env)
    worker = FatcatChangelogWorker(args.api_host_url, args.kafka_hosts, topic,
        args.poll_interval)
    worker.run()

def run_entity_updates_worker(args):
    changelog_topic = "fatcat-{}.changelog".format(args.env)
    release_topic = "fatcat-{}.release-updates".format(args.env)
    worker = FatcatEntityUpdatesWorker(args.api_host_url, args.kafka_hosts,
        changelog_topic, release_topic)
    worker.run()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug',
        action='store_true',
        help="enable debug logging")
    parser.add_argument('--api-host-url',
        default="http://localhost:9411/v0",
        help="fatcat API host/port to use")
    parser.add_argument('--kafka-hosts',
        default="localhost:9092",
        help="list of Kafka brokers (host/port) to use")
    parser.add_argument('--env',
        default="qa",
        help="Kafka topic namespace to use (eg, prod, qa)")
    subparsers = parser.add_subparsers()

    sub_changelog = subparsers.add_parser('changelog')
    sub_changelog.set_defaults(func=run_changelog_worker)
    sub_changelog.add_argument('--poll-interval',
        help="how long to wait between polling (seconds)",
        default=10.0, type=float)

    sub_entity_updates = subparsers.add_parser('entity-updates')
    sub_entity_updates.set_defaults(func=run_entity_updates_worker)

    args = parser.parse_args()
    if not args.__dict__.get("func"):
        print("tell me what to do!")
        sys.exit(-1)
    args.func(args)

if __name__ == '__main__':
    main()
