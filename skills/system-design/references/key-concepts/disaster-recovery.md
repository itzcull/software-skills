---
title: Disaster Recovery
description: Strategies and processes for recovering systems and data after catastrophic failures
source: Manual creation due to inaccessible source URL
tags: [disaster-recovery, business-continuity, backup, resilience, system-design]
category: key-concepts
---

# Disaster Recovery

## Definition

> Disaster Recovery (DR) is a set of policies, tools, and procedures designed to enable the recovery of vital technology infrastructure and systems following a natural or human-induced disaster.

Disaster recovery ensures business continuity by providing strategies to restore critical systems, data, and operations when primary infrastructure becomes unavailable due to catastrophic events.

## Key Concepts

### Disaster Types

#### Natural Disasters
- **Earthquakes**: Physical damage to data centers and infrastructure
- **Floods**: Water damage to equipment and facilities
- **Fires**: Destruction of hardware and buildings
- **Hurricanes/Tornadoes**: Wind and water damage
- **Power Grid Failures**: Extended power outages

#### Human-Induced Disasters
- **Cyberattacks**: Ransomware, data breaches, DDoS attacks
- **Human Error**: Accidental deletion, misconfiguration
- **Terrorism**: Physical or cyber attacks on infrastructure
- **Equipment Failures**: Hardware malfunctions, software bugs
- **Data Corruption**: Database corruption, file system failures

### Recovery Objectives

#### Recovery Time Objective (RTO)
- **Definition**: Maximum acceptable time to restore service after disruption
- **Measurement**: Hours, minutes, or seconds of downtime
- **Business Impact**: Directly affects revenue and customer experience
- **Example**: E-commerce site with RTO of 1 hour loses $100K per hour of downtime

#### Recovery Point Objective (RPO)
- **Definition**: Maximum acceptable data loss measured in time
- **Measurement**: How much data can be lost (minutes, hours, days)
- **Data Protection**: Determines backup frequency and replication strategy
- **Example**: Financial system with RPO of 15 minutes can lose maximum 15 minutes of transactions

#### Maximum Tolerable Downtime (MTD)
- **Definition**: Longest time business can survive without critical systems
- **Business Continuity**: Point where business viability is threatened
- **Strategic Planning**: Influences DR investment and strategy decisions
- **Example**: Online bank with MTD of 4 hours before customer defection

## Disaster Recovery Strategies

### Backup and Restore (Cold Site)

**Approach:**
- Regular backups stored off-site
- Manual restoration process when disaster occurs
- No pre-provisioned infrastructure at recovery site

**Characteristics:**
- **RTO**: Days to weeks
- **RPO**: Hours to days
- **Cost**: Lowest initial investment
- **Complexity**: Simple to implement

**Use Cases:**
- Non-critical systems
- Small businesses with limited budgets
- Systems with high tolerance for downtime

**Implementation:**
```bash
# Example backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="production_db"
BACKUP_DIR="/backups"
S3_BUCKET="s3://company-backups"

# Create database backup
pg_dump $DB_NAME > $BACKUP_DIR/db_backup_$DATE.sql

# Backup application files
tar -czf $BACKUP_DIR/app_backup_$DATE.tar.gz /var/www/html

# Upload to cloud storage
aws s3 cp $BACKUP_DIR/ $S3_BUCKET/ --recursive --include "*$DATE*"

# Cleanup local backups older than 7 days
find $BACKUP_DIR -type f -mtime +7 -delete
```

### Warm Site

**Approach:**
- Pre-configured infrastructure with basic systems
- Data synchronized periodically
- Manual activation and scaling required

**Characteristics:**
- **RTO**: Hours to days
- **RPO**: Minutes to hours
- **Cost**: Moderate investment
- **Complexity**: Medium complexity

**Use Cases:**
- Mid-tier applications
- Companies with moderate recovery requirements
- Systems requiring faster recovery than cold site

### Hot Site (Active-Passive)

**Approach:**
- Fully configured and operational standby environment
- Real-time or near-real-time data replication
- Automatic or manual failover procedures

**Characteristics:**
- **RTO**: Minutes to hours
- **RPO**: Seconds to minutes
- **Cost**: High investment
- **Complexity**: High complexity

**Use Cases:**
- Critical business applications
- High-availability requirements
- Customer-facing systems

**Architecture Example:**
```yaml
# Kubernetes disaster recovery configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: dr-config
data:
  primary_region: "us-east-1"
  dr_region: "us-west-2"
  failover_threshold: "5m"
  health_check_interval: "30s"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-primary
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
      region: primary
  template:
    metadata:
      labels:
        app: web-app
        region: primary
    spec:
      containers:
      - name: web-app
        image: myapp:latest
        env:
        - name: DATABASE_URL
          value: "postgresql://primary-db:5432/app"
```

### Active-Active (Multi-Site)

**Approach:**
- Multiple active sites serving traffic simultaneously
- Load balancing across geographical regions
- Shared or replicated data across sites

**Characteristics:**
- **RTO**: Seconds to minutes (automatic failover)
- **RPO**: Seconds (real-time replication)
- **Cost**: Highest investment
- **Complexity**: Highest complexity

**Use Cases:**
- Mission-critical systems
- Global applications
- Zero-downtime requirements

## Implementation Components

### Data Backup Strategies

#### Full Backups
- **Definition**: Complete copy of all data
- **Frequency**: Weekly or monthly
- **Advantages**: Simple restore process, complete data protection
- **Disadvantages**: Time-consuming, storage-intensive

#### Incremental Backups
- **Definition**: Only changes since last backup (any type)
- **Frequency**: Daily or hourly
- **Advantages**: Fast backup, efficient storage
- **Disadvantages**: Complex restore (requires full + all incrementals)

#### Differential Backups
- **Definition**: Changes since last full backup
- **Frequency**: Daily
- **Advantages**: Faster than full, simpler restore than incremental
- **Disadvantages**: Growing size over time

#### Continuous Data Protection (CDP)
- **Definition**: Real-time backup of every change
- **Frequency**: Continuous
- **Advantages**: Minimal data loss, point-in-time recovery
- **Disadvantages**: High resource requirements, complex implementation

### Replication Technologies

#### Database Replication

**Master-Slave Replication:**
```sql
-- MySQL master configuration
[mysqld]
server-id = 1
log-bin = mysql-bin
binlog-format = ROW
binlog-do-db = production_db

-- MySQL slave configuration
[mysqld]
server-id = 2
relay-log = relay-bin
read-only = 1
```

**Master-Master Replication:**
```sql
-- Node 1 configuration
[mysqld]
server-id = 1
auto-increment-increment = 2
auto-increment-offset = 1
log-bin = mysql-bin

-- Node 2 configuration
[mysqld]
server-id = 2
auto-increment-increment = 2
auto-increment-offset = 2
log-bin = mysql-bin
```

#### File System Replication

**DRBD (Distributed Replicated Block Device):**
```bash
# DRBD configuration
resource r0 {
    protocol C;
    device /dev/drbd0;
    disk /dev/sdb1;
    meta-disk internal;
    
    on primary-server {
        address 192.168.1.10:7789;
    }
    
    on backup-server {
        address 192.168.1.20:7789;
    }
}
```

#### Application-Level Replication

**Message Queue Replication:**
```yaml
# RabbitMQ cluster configuration
rabbitmq_clustering:
  cluster_nodes:
    - rabbit@node1
    - rabbit@node2
    - rabbit@node3
  cluster_partition_handling: autoheal
  ha_mode: all
  ha_sync_mode: automatic
```

### Network and Infrastructure

#### DNS Failover
```json
{
  "type": "A",
  "name": "api.company.com",
  "ttl": 60,
  "failover": {
    "primary": "203.0.113.10",
    "secondary": "198.51.100.20",
    "health_check": {
      "url": "https://api.company.com/health",
      "interval": 30,
      "timeout": 5,
      "retries": 3
    }
  }
}
```

#### Load Balancer Configuration
```nginx
# NGINX load balancer with failover
upstream backend {
    server primary.company.com:80 weight=3;
    server secondary.company.com:80 weight=1 backup;
    server dr.company.com:80 weight=1 backup;
}

server {
    listen 80;
    server_name api.company.com;
    
    location / {
        proxy_pass http://backend;
        proxy_connect_timeout 1s;
        proxy_timeout 3s;
        proxy_next_upstream error timeout;
    }
}
```

## Cloud-Based Disaster Recovery

### AWS Disaster Recovery

#### Multi-AZ Deployments
```yaml
# RDS Multi-AZ configuration
Resources:
  Database:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceClass: db.t3.medium
      Engine: postgres
      MultiAZ: true
      BackupRetentionPeriod: 7
      DeletionProtection: true
      StorageEncrypted: true
```

#### Cross-Region Replication
```yaml
# S3 Cross-Region Replication
Resources:
  ReplicationConfiguration:
    Type: AWS::S3::Bucket
    Properties:
      ReplicationConfiguration:
        Role: !GetAtt ReplicationRole.Arn
        Rules:
          - Id: ReplicateToWest
            Status: Enabled
            Prefix: critical-data/
            Destination:
              Bucket: !Sub "arn:aws:s3:::${BackupBucket}"
              StorageClass: STANDARD_IA
```

### Azure Site Recovery

```json
{
  "properties": {
    "friendlyName": "DR-Protection-Plan",
    "primaryFabric": "azure-eastus2",
    "recoveryFabric": "azure-westus2",
    "failoverDeploymentModel": "ResourceManager",
    "replicationProviders": ["InMage"],
    "allowedOperations": ["Failover", "TestFailover"]
  }
}
```

### Google Cloud Disaster Recovery

```yaml
# Cloud SQL High Availability
apiVersion: sql.cnrm.cloud.google.com/v1beta1
kind: SQLInstance
metadata:
  name: production-db
spec:
  databaseVersion: POSTGRES_13
  region: us-central1
  settings:
    tier: db-custom-2-7680
    availabilityType: REGIONAL
    backupConfiguration:
      enabled: true
      pointInTimeRecoveryEnabled: true
      transactionLogRetentionDays: 7
```

## Disaster Recovery Testing

### Testing Types

#### Tabletop Exercises
- **Definition**: Discussion-based simulation of disaster scenarios
- **Participants**: Key stakeholders and technical teams
- **Frequency**: Quarterly or semi-annually
- **Benefits**: Low cost, identifies process gaps, team training

#### Walkthrough Tests
- **Definition**: Step-by-step review of recovery procedures
- **Process**: Manual verification of documented procedures
- **Frequency**: Monthly or quarterly
- **Benefits**: Validates documentation, identifies missing steps

#### Simulation Tests
- **Definition**: Actual execution of recovery procedures in test environment
- **Scope**: Partial system recovery without affecting production
- **Frequency**: Monthly
- **Benefits**: Validates technical procedures, measures RTO/RPO

#### Full Interruption Tests
- **Definition**: Complete failover to disaster recovery site
- **Scope**: Production systems switched to DR environment
- **Frequency**: Annually
- **Benefits**: Complete validation, realistic testing, team training

### Testing Automation

```python
# Automated DR testing script
import boto3
import time
import requests

class DRTester:
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.rds = boto3.client('rds')
        self.elb = boto3.client('elbv2')
    
    def test_rds_failover(self, db_identifier):
        """Test RDS Multi-AZ failover"""
        print("Starting RDS failover test...")
        
        # Initiate failover
        response = self.rds.reboot_db_instance(
            DBInstanceIdentifier=db_identifier,
            ForceFailover=True
        )
        
        # Monitor failover completion
        while True:
            db_status = self.rds.describe_db_instances(
                DBInstanceIdentifier=db_identifier
            )
            status = db_status['DBInstances'][0]['DBInstanceStatus']
            
            if status == 'available':
                print("RDS failover completed successfully")
                break
            
            time.sleep(30)
    
    def test_application_health(self, health_url):
        """Test application health after failover"""
        try:
            response = requests.get(health_url, timeout=10)
            if response.status_code == 200:
                print("Application health check passed")
                return True
        except Exception as e:
            print(f"Application health check failed: {e}")
            return False
    
    def run_dr_test(self):
        """Execute complete DR test"""
        try:
            # Test database failover
            self.test_rds_failover('production-db')
            
            # Wait for DNS propagation
            time.sleep(60)
            
            # Test application health
            health_passed = self.test_application_health(
                'https://api.company.com/health'
            )
            
            # Generate test report
            self.generate_report(health_passed)
            
        except Exception as e:
            print(f"DR test failed: {e}")
    
    def generate_report(self, health_passed):
        """Generate DR test report"""
        report = {
            'test_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'database_failover': 'PASSED',
            'application_health': 'PASSED' if health_passed else 'FAILED',
            'overall_status': 'PASSED' if health_passed else 'FAILED'
        }
        
        print(f"DR Test Report: {report}")
```

## Monitoring and Alerting

### Key Metrics

#### Availability Metrics
- **System Uptime**: Percentage of time system is operational
- **Response Time**: Application response latency
- **Error Rate**: Percentage of failed requests
- **Recovery Time**: Time to restore service after failure

#### Data Protection Metrics
- **Backup Success Rate**: Percentage of successful backups
- **Replication Lag**: Delay in data replication
- **Data Integrity**: Consistency checks and validation
- **Storage Utilization**: Backup storage consumption

### Alerting Configuration

```yaml
# Prometheus alerting rules for DR
groups:
- name: disaster-recovery
  rules:
  - alert: BackupFailed
    expr: backup_success == 0
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "Backup process failed"
      description: "Database backup has failed for {{ $labels.database }}"
  
  - alert: ReplicationLagHigh
    expr: mysql_slave_lag_seconds > 300
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: "Database replication lag is high"
      description: "Replication lag is {{ $value }} seconds"
  
  - alert: PrimarySiteDown
    expr: up{job="primary-site"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Primary site is unreachable"
      description: "Primary site health check has failed"
```

## Cost Optimization

### Tiered Recovery Strategy

#### Tier 1: Critical Systems
- **RTO**: < 1 hour
- **RPO**: < 15 minutes
- **Strategy**: Hot site or active-active
- **Cost**: High

#### Tier 2: Important Systems
- **RTO**: 4-24 hours
- **RPO**: 1-4 hours
- **Strategy**: Warm site
- **Cost**: Medium

#### Tier 3: Standard Systems
- **RTO**: 24-72 hours
- **RPO**: 4-24 hours
- **Strategy**: Cold site
- **Cost**: Low

### Cloud Cost Management

```yaml
# AWS cost-optimized DR configuration
Resources:
  DRInstance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t3.micro  # Minimal instance for standby
      ImageId: ami-12345678
      Tags:
        - Key: Environment
          Value: DR
        - Key: AutoShutdown
          Value: "true"  # Automatically shutdown when not needed
  
  DRStorage:
    Type: AWS::S3::Bucket
    Properties:
      LifecycleConfiguration:
        Rules:
          - Status: Enabled
            Transitions:
              - StorageClass: STANDARD_IA
                TransitionInDays: 30
              - StorageClass: GLACIER
                TransitionInDays: 90
```

## Compliance and Governance

### Regulatory Requirements

#### SOX (Sarbanes-Oxley)
- **Data Retention**: 7 years for financial records
- **Backup Validation**: Regular testing and verification
- **Access Controls**: Audit trails for data access

#### HIPAA (Healthcare)
- **Data Encryption**: All backups must be encrypted
- **Access Logging**: Detailed audit logs required
- **Business Associate Agreements**: Third-party DR providers

#### GDPR (General Data Protection Regulation)
- **Data Minimization**: Only backup necessary personal data
- **Right to be Forgotten**: Ability to delete personal data
- **Cross-Border Transfers**: Compliance for international DR sites

### Documentation Requirements

#### DR Plan Documentation
- **Recovery Procedures**: Step-by-step instructions
- **Contact Information**: Key personnel and vendors
- **System Dependencies**: Application and service relationships
- **Network Diagrams**: Infrastructure topology and connections

#### Test Documentation
- **Test Results**: Detailed results from DR tests
- **Lessons Learned**: Improvements identified during testing
- **Training Records**: Staff training and certification
- **Vendor Agreements**: SLAs and support contracts

## Best Practices

### 1. Regular Testing and Validation
- Conduct regular DR tests at different levels
- Automate testing procedures where possible
- Document and analyze test results
- Update procedures based on test findings

### 2. Comprehensive Documentation
- Maintain detailed recovery procedures
- Keep contact information current
- Document system dependencies and configurations
- Create runbooks for common scenarios

### 3. Staff Training and Awareness
- Train key personnel on DR procedures
- Conduct regular tabletop exercises
- Cross-train team members on critical systems
- Maintain 24/7 on-call coverage

### 4. Multi-Layered Approach
- Implement multiple recovery strategies
- Use different backup methods and locations
- Diversify technology stack and vendors
- Plan for various disaster scenarios

### 5. Continuous Improvement
- Regular review and update of DR plans
- Incorporate lessons learned from incidents
- Stay current with technology and best practices
- Benchmark against industry standards

## Common Pitfalls

### Inadequate Testing
- **Problem**: DR plans not regularly tested
- **Risk**: Procedures may not work when needed
- **Solution**: Implement regular testing schedule

### Single Point of Failure
- **Problem**: DR solution has its own dependencies
- **Risk**: DR site fails when primary site fails
- **Solution**: Design for redundancy at all levels

### Outdated Documentation
- **Problem**: Procedures don't reflect current systems
- **Risk**: Recovery attempts may fail
- **Solution**: Regular documentation reviews and updates

### Insufficient Monitoring
- **Problem**: Backup and replication failures go unnoticed
- **Risk**: Data protection gaps discovered during disaster
- **Solution**: Comprehensive monitoring and alerting

Disaster recovery is essential for maintaining business continuity and protecting against various types of failures. A well-designed DR strategy balances recovery objectives, cost constraints, and operational complexity to ensure systems can be restored quickly and reliably when disasters occur.