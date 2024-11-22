import random
import time

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
]

headers = {"User-Agent": random.choice(user_agents)}

skills = [
    "802.11",
    "aix",
    "airflow",
    "alpine",
    "amazon",
    "ansible",
    "apache",
    "arangodb",
    "argo",
    "avro",
    "aws",
    "azure",
    "bash",
    "bamboo",
    "bazaar",
    "beam",
    "bigquery",
    "bitbucket",
    "blob",
    "bolt",
    "buddy",
    "buildkite",
    "c#",
    "c++",
    "cassandara",
    "ceph",
    "chef",
    "ci/cd",
    "circleci",
    "clickhouse",
    "cluster",
    "codepipeline",
    "codeship",
    "concourse",
    "containerd",
    "controlm",
    "cosmosdb",
    "couchbase",
    "couchdb",
    "cri-o",
    "csv",
    "dask",
    "databricks",
    "datalake",
    "datadog",
    "dart",
    "db2",
    "debian",
    "devops",
    "dhcp",
    "dns",
    "dnssec",
    "docker",
    "dynamodb",
    "elasticsearch",
    "elixir",
    "english",
    "esxi",
    "etf",
    "fabfile",
    "fedora",
    "firestore",
    "flink",
    "fortran",
    "fossil",
    "ftp",
    "german",
    "github",
    "gitlab",
    "gitops",
    "gpfs",
    "grafana",
    "haskell",
    "helm",
    "hive",
    "hbase",
    "hyper-v",
    "hyperv",
    "hyper v",
    "hypertable",
    "ibm_db2",
    "icinga",
    "icmp",
    "imap",
    "influxdb",
    "infrastructure as code",
    "iptables",
    "istio",
    "italian",
    "itil",
    "java",
    "janusgraph",
    "jenkins",
    "javascript",
    "json",
    "kafka",
    "kdb+",
    "kibana",
    "kinesis",
    "kotlin",
    "kudu",
    "kubernetes",
    "kvm",
    "lxd",
    "lxc",
    "linkerd",
    "linux",
    "logstash",
    "longhorn",
    "lxd",
    "matlab",
    "marklogic",
    "mariadb",
    "maven",
    "mercurial",
    "mesos",
    "mongodb",
    "nagios",
    "neo4j",
    "newrelic",
    "nfs",
    "nifi",
    "nomad",
    "openshift",
    "openstack",
    "orientdb",
    "osfp",
    "packer",
    "pandas",
    "parquet",
    "perl",
    "perforce",
    "podman",
    "portainer",
    "postgres",
    "powershell",
    "presto",
    "prometheus",
    "proxmox",
    "proxy",
    "puppet",
    "python",
    "rabbitmq",
    "rancher",
    "realm",
    "red hat",
    "redhat",
    "redis",
    "redshift",
    "rhel",
    "riak",
    "rundeck",
    "ruby",
    "rust",
    "salt",
    "samba",
    "sensu",
    "singularity",
    "siem",
    "sles",
    "snmp",
    "solaris",
    "solr",
    "spark",
    "spinnaker",
    "splunk",
    "sql",
    "ssh",
    "storm",
    "subnetting",
    "suse",
    "swift",
    "s3",
    "terraform",
    "tcp",
    "tcp/ip",
    "teamcity",
    "tekton",
    "teradata",
    "terraform",
    "travis",
    "travisci",
    "typescript",
    "ubuntu",
    "vagrant",
    "virtualbox",
    "vlan",
    "vmware",
    "voltdb",
    "vpn",
    "werf",
    "windows",
    "wireless",
    "xen",
    "zabbix",
    "zookeeper",
]

skills_ww = [
    "orc",
    "san",
    "nas",
    "go",
    "lan",
    "wan",
    "hana",
    "ecs",
    "nat",
    "elk",
    "scala",
    "shell",
    "udp",
    "cloud",
    "git",
]

replacement_map = {
    "aws": ["amazon", "s3"],
    "ci/cd": ["bitbucket", "concourse", "teamcity", "tekton", "werf", "bamboo"],
    "elk": ["elasticsearch", "logstash", "kibana"],
    "hyper-v": ["hyper v", "hyperv"],
    "IaC": ["infrastructure as code"],
    "linux": ["red hat", "rhel", "redhat", "ubuntu", "sles", "suse", "debian"],
    "lxc": ["lxd"],
    "sql": ["mariadb", "postgres"],
    "tcp/ip": ["tcp", "udp"],
    "vmware": ["esxi"],    
}

replacement_ww_map = {
    "bash": ["shell"],
    "tcp/ip": ["tcp", "udp"],
}

def wait_a_sec(s1, s2):
    delay = random.uniform(s1, s2)
    time.sleep(delay)
