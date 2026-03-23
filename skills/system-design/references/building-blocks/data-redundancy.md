---
title: "Data Redundancy in Distributed Systems"
description: "Comprehensive guide to data redundancy strategies, implementation approaches, and best practices for ensuring data availability and integrity"
category: "Building Blocks"
tags: ["data-redundancy", "fault-tolerance", "availability", "backup", "disaster-recovery"]
difficulty: "intermediate"
last_updated: "2025-07-27"
---

# Data Redundancy in Distributed Systems

Data redundancy refers to the practice of storing the same piece of data in multiple places. It's not just about creating copies; it's about implementing a comprehensive strategy to ensure the availability, integrity, and recoverability of your digital assets.

## What is Data Redundancy?

Data redundancy is a fundamental principle in distributed systems that involves intentionally storing multiple copies of the same data across different locations, devices, or systems. This practice provides protection against data loss, improves availability, and can enhance performance.

### Core Principles

1. **Multiple Copies**: Maintain several instances of the same data
2. **Geographic Distribution**: Store copies in different physical locations
3. **Diverse Storage Methods**: Use different storage technologies and media
4. **Automated Management**: Implement systems to maintain redundancy automatically

### Redundancy vs. Replication

While related, redundancy and replication serve different purposes:

```
Redundancy: Focuses on data protection and availability
┌─────────────────────────────────────┐
│     Primary Data    │   Backup 1    │
│    (Active Use)     │  (Protection) │
├─────────────────────┼───────────────┤
│     Backup 2        │   Archive     │
│   (Protection)      │ (Long-term)   │
└─────────────────────────────────────┘

Replication: Focuses on performance and distribution
┌─────────────────────────────────────┐
│    Replica 1        │   Replica 2   │
│  (Active Reads)     │ (Active Reads)│
├─────────────────────┼───────────────┤
│    Replica 3        │   Replica 4   │
│  (Active Reads)     │ (Active Reads)│
└─────────────────────────────────────┘
```

## Types of Data Redundancy

### 1. Physical Redundancy

Storing copies on different physical devices to protect against hardware failures.

```python
import os
import shutil
import hashlib
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class StorageType(Enum):
    LOCAL_DISK = "local_disk"
    NETWORK_STORAGE = "network_storage"
    CLOUD_STORAGE = "cloud_storage"
    TAPE_STORAGE = "tape_storage"

@dataclass
class StorageDevice:
    device_id: str
    storage_type: StorageType
    capacity_gb: float
    used_gb: float
    mount_point: str
    is_healthy: bool = True

class PhysicalRedundancyManager:
    def __init__(self):
        self.storage_devices: Dict[str, StorageDevice] = {}
        self.redundancy_policies = {}
        self.file_locations = {}  # file_hash -> [device_ids]
        
    def register_storage_device(self, device: StorageDevice):
        """Register a storage device for redundancy"""
        self.storage_devices[device.device_id] = device
        print(f"Registered storage device: {device.device_id}")
    
    def set_redundancy_policy(self, file_pattern: str, min_copies: int, 
                            preferred_storage_types: List[StorageType]):
        """Set redundancy policy for specific file patterns"""
        self.redundancy_policies[file_pattern] = {
            'min_copies': min_copies,
            'preferred_storage_types': preferred_storage_types,
            'max_copies_per_device': 1  # Avoid single points of failure
        }
    
    async def store_with_redundancy(self, file_path: str, data: bytes) -> bool:
        """Store file with redundancy across multiple physical devices"""
        
        file_hash = hashlib.sha256(data).hexdigest()
        
        # Determine redundancy policy
        policy = self._get_policy_for_file(file_path)
        
        # Select storage devices
        target_devices = self._select_storage_devices(policy)
        
        if len(target_devices) < policy['min_copies']:
            raise Exception(f"Insufficient storage devices for redundancy policy")
        
        # Store on selected devices
        successful_stores = []
        
        for device_id in target_devices:
            device = self.storage_devices[device_id]
            
            try:
                target_path = os.path.join(device.mount_point, file_hash)
                
                # Create redundant copy
                await self._write_to_device(device, target_path, data)
                
                # Verify integrity
                if await self._verify_file_integrity(target_path, file_hash):
                    successful_stores.append(device_id)
                    print(f"Successfully stored {file_path} on {device_id}")
                
            except Exception as e:
                print(f"Failed to store on device {device_id}: {e}")
        
        # Update file location tracking
        if len(successful_stores) >= policy['min_copies']:
            self.file_locations[file_hash] = successful_stores
            return True
        else:
            # Cleanup partial stores
            await self._cleanup_partial_stores(file_hash, successful_stores)
            return False
    
    def _select_storage_devices(self, policy: Dict) -> List[str]:
        """Select storage devices based on policy"""
        
        # Filter healthy devices by preferred storage types
        eligible_devices = []
        
        for device_id, device in self.storage_devices.items():
            if (device.is_healthy and 
                device.storage_type in policy['preferred_storage_types'] and
                device.used_gb < device.capacity_gb * 0.9):  # Don't fill completely
                
                eligible_devices.append(device_id)
        
        # Sort by available space (prefer devices with more space)
        eligible_devices.sort(
            key=lambda device_id: self.storage_devices[device_id].capacity_gb - 
                                  self.storage_devices[device_id].used_gb,
            reverse=True
        )
        
        # Return required number of devices
        return eligible_devices[:policy['min_copies']]
    
    async def _write_to_device(self, device: StorageDevice, path: str, data: bytes):
        """Write data to specific storage device"""
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Write data
        with open(path, 'wb') as f:
            f.write(data)
        
        # Update device usage
        device.used_gb += len(data) / (1024 * 1024 * 1024)  # Convert to GB
    
    async def _verify_file_integrity(self, file_path: str, expected_hash: str) -> bool:
        """Verify file integrity using hash comparison"""
        
        try:
            with open(file_path, 'rb') as f:
                file_data = f.read()
                actual_hash = hashlib.sha256(file_data).hexdigest()
                return actual_hash == expected_hash
        except Exception:
            return False
    
    async def retrieve_file(self, file_hash: str) -> Optional[bytes]:
        """Retrieve file from any available redundant copy"""
        
        device_ids = self.file_locations.get(file_hash, [])
        
        for device_id in device_ids:
            device = self.storage_devices[device_id]
            
            if not device.is_healthy:
                continue
            
            try:
                file_path = os.path.join(device.mount_point, file_hash)
                
                with open(file_path, 'rb') as f:
                    data = f.read()
                
                # Verify integrity
                actual_hash = hashlib.sha256(data).hexdigest()
                if actual_hash == file_hash:
                    return data
                else:
                    print(f"Integrity check failed for {file_hash} on {device_id}")
                    
            except Exception as e:
                print(f"Failed to retrieve from device {device_id}: {e}")
        
        return None
    
    async def check_redundancy_health(self) -> Dict:
        """Check health of redundancy for all files"""
        
        health_report = {
            'healthy_files': 0,
            'at_risk_files': 0,
            'corrupted_files': 0,
            'device_failures': []
        }
        
        for file_hash, device_ids in self.file_locations.items():
            healthy_copies = 0
            
            for device_id in device_ids:
                device = self.storage_devices[device_id]
                
                if device.is_healthy:
                    file_path = os.path.join(device.mount_point, file_hash)
                    
                    if await self._verify_file_integrity(file_path, file_hash):
                        healthy_copies += 1
                else:
                    health_report['device_failures'].append(device_id)
            
            if healthy_copies == 0:
                health_report['corrupted_files'] += 1
            elif healthy_copies < 2:  # Assuming minimum 2 copies desired
                health_report['at_risk_files'] += 1
            else:
                health_report['healthy_files'] += 1
        
        return health_report

# Usage example
async def setup_physical_redundancy():
    manager = PhysicalRedundancyManager()
    
    # Register storage devices
    manager.register_storage_device(StorageDevice(
        device_id="local_ssd_1",
        storage_type=StorageType.LOCAL_DISK,
        capacity_gb=1000,
        used_gb=100,
        mount_point="/mnt/ssd1"
    ))
    
    manager.register_storage_device(StorageDevice(
        device_id="nas_storage_1",
        storage_type=StorageType.NETWORK_STORAGE,
        capacity_gb=5000,
        used_gb=500,
        mount_point="/mnt/nas1"
    ))
    
    manager.register_storage_device(StorageDevice(
        device_id="cloud_backup_1",
        storage_type=StorageType.CLOUD_STORAGE,
        capacity_gb=10000,
        used_gb=1000,
        mount_point="/mnt/cloud1"
    ))
    
    # Set redundancy policies
    manager.set_redundancy_policy(
        "*.critical",
        min_copies=3,
        preferred_storage_types=[StorageType.LOCAL_DISK, StorageType.NETWORK_STORAGE, StorageType.CLOUD_STORAGE]
    )
    
    manager.set_redundancy_policy(
        "*.important",
        min_copies=2,
        preferred_storage_types=[StorageType.LOCAL_DISK, StorageType.NETWORK_STORAGE]
    )
    
    # Store file with redundancy
    critical_data = b"This is critical business data"
    success = await manager.store_with_redundancy("backup.critical", critical_data)
    
    if success:
        print("Critical data stored with redundancy")
        
        # Check health
        health_report = await manager.check_redundancy_health()
        print(f"Redundancy health: {health_report}")
```

### 2. Geographic Redundancy

Storing data copies in different physical locations to protect against regional disasters.

```python
import asyncio
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

class RegionType(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    DR_SITE = "disaster_recovery"

@dataclass
class GeographicSite:
    site_id: str
    region: str
    country: str
    region_type: RegionType
    lat: float
    lon: float
    is_active: bool = True

class GeographicRedundancyManager:
    def __init__(self):
        self.sites: Dict[str, GeographicSite] = {}
        self.data_distribution = {}  # data_id -> [site_ids]
        self.replication_policies = {}
        
    def register_site(self, site: GeographicSite):
        """Register a geographic site"""
        self.sites[site.site_id] = site
        print(f"Registered site: {site.site_id} in {site.region}")
    
    def set_geographic_policy(self, data_category: str, min_regions: int, 
                            required_region_types: List[RegionType]):
        """Set geographic distribution policy"""
        self.replication_policies[data_category] = {
            'min_regions': min_regions,
            'required_region_types': required_region_types,
            'min_distance_km': 1000  # Minimum distance between sites
        }
    
    async def distribute_data_geographically(self, data_id: str, data_category: str, 
                                           data: bytes) -> bool:
        """Distribute data across geographic sites"""
        
        policy = self.replication_policies.get(data_category, {
            'min_regions': 2,
            'required_region_types': [RegionType.PRIMARY, RegionType.SECONDARY],
            'min_distance_km': 1000
        })
        
        # Select sites based on policy
        target_sites = self._select_geographic_sites(policy)
        
        if len(target_sites) < policy['min_regions']:
            raise Exception("Insufficient geographic sites for policy")
        
        # Distribute to selected sites
        successful_distributions = []
        
        for site_id in target_sites:
            try:
                await self._replicate_to_site(site_id, data_id, data)
                successful_distributions.append(site_id)
                print(f"Data {data_id} replicated to site {site_id}")
                
            except Exception as e:
                print(f"Failed to replicate to site {site_id}: {e}")
        
        # Verify minimum requirements met
        if len(successful_distributions) >= policy['min_regions']:
            self.data_distribution[data_id] = successful_distributions
            return True
        else:
            # Cleanup partial distributions
            await self._cleanup_failed_distribution(data_id, successful_distributions)
            return False
    
    def _select_geographic_sites(self, policy: Dict) -> List[str]:
        """Select sites based on geographic distribution policy"""
        
        available_sites = [
            site_id for site_id, site in self.sites.items()
            if site.is_active
        ]
        
        # Group sites by region type
        sites_by_type = {}
        for site_id in available_sites:
            site = self.sites[site_id]
            if site.region_type not in sites_by_type:
                sites_by_type[site.region_type] = []
            sites_by_type[site.region_type].append(site_id)
        
        selected_sites = []
        
        # First, select required region types
        for region_type in policy['required_region_types']:
            if region_type in sites_by_type and sites_by_type[region_type]:
                # Select site with best geographic distribution
                best_site = self._select_best_distributed_site(
                    sites_by_type[region_type], 
                    selected_sites,
                    policy['min_distance_km']
                )
                if best_site:
                    selected_sites.append(best_site)
        
        # Add additional sites if needed
        remaining_sites = [s for s in available_sites if s not in selected_sites]
        while len(selected_sites) < policy['min_regions'] and remaining_sites:
            best_site = self._select_best_distributed_site(
                remaining_sites,
                selected_sites,
                policy['min_distance_km']
            )
            if best_site:
                selected_sites.append(best_site)
                remaining_sites.remove(best_site)
            else:
                break
        
        return selected_sites
    
    def _select_best_distributed_site(self, candidate_sites: List[str], 
                                    existing_sites: List[str], 
                                    min_distance_km: float) -> Optional[str]:
        """Select site with best geographic distribution"""
        
        if not existing_sites:
            return candidate_sites[0] if candidate_sites else None
        
        best_site = None
        best_min_distance = 0
        
        for candidate_site_id in candidate_sites:
            candidate_site = self.sites[candidate_site_id]
            
            # Calculate minimum distance to existing sites
            min_distance = float('inf')
            
            for existing_site_id in existing_sites:
                existing_site = self.sites[existing_site_id]
                distance = self._calculate_distance(
                    candidate_site.lat, candidate_site.lon,
                    existing_site.lat, existing_site.lon
                )
                min_distance = min(min_distance, distance)
            
            # Select site with maximum minimum distance (best distribution)
            if min_distance > best_min_distance and min_distance >= min_distance_km:
                best_min_distance = min_distance
                best_site = candidate_site_id
        
        return best_site
    
    def _calculate_distance(self, lat1: float, lon1: float, 
                          lat2: float, lon2: float) -> float:
        """Calculate distance between two geographic points (Haversine formula)"""
        import math
        
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Radius of Earth in kilometers
        r = 6371
        
        return r * c
    
    async def _replicate_to_site(self, site_id: str, data_id: str, data: bytes):
        """Replicate data to specific geographic site"""
        
        # This would implement actual replication to the site
        # Could use various methods: API calls, file transfer, database replication, etc.
        
        site = self.sites[site_id]
        
        # Simulate network transfer with latency based on distance
        if site.region_type == RegionType.DR_SITE:
            await asyncio.sleep(2.0)  # Simulate longer transfer to DR site
        else:
            await asyncio.sleep(0.5)  # Simulate local/regional transfer
        
        print(f"Replicated {len(data)} bytes to site {site_id}")
    
    async def handle_site_failure(self, failed_site_id: str):
        """Handle failure of geographic site"""
        
        if failed_site_id not in self.sites:
            return
        
        # Mark site as inactive
        self.sites[failed_site_id].is_active = False
        
        # Find affected data
        affected_data = []
        for data_id, site_ids in self.data_distribution.items():
            if failed_site_id in site_ids:
                affected_data.append(data_id)
        
        # Re-replicate affected data to maintain redundancy
        for data_id in affected_data:
            remaining_sites = [
                site_id for site_id in self.data_distribution[data_id]
                if site_id != failed_site_id and self.sites[site_id].is_active
            ]
            
            if len(remaining_sites) < 2:  # Below minimum redundancy
                await self._emergency_replication(data_id, remaining_sites)
        
        print(f"Handled failure of site {failed_site_id}")
    
    async def _emergency_replication(self, data_id: str, remaining_sites: List[str]):
        """Emergency replication to maintain minimum redundancy"""
        
        if not remaining_sites:
            print(f"CRITICAL: No remaining sites for data {data_id}")
            return
        
        # Get data from remaining site
        source_site = remaining_sites[0]
        data = await self._retrieve_from_site(source_site, data_id)
        
        if data:
            # Find new target sites
            available_sites = [
                site_id for site_id, site in self.sites.items()
                if site.is_active and site_id not in remaining_sites
            ]
            
            if available_sites:
                target_site = available_sites[0]  # Choose first available
                await self._replicate_to_site(target_site, data_id, data)
                
                # Update distribution tracking
                self.data_distribution[data_id].append(target_site)
                
                print(f"Emergency replication of {data_id} to {target_site}")

# Usage example
async def setup_geographic_redundancy():
    manager = GeographicRedundancyManager()
    
    # Register geographic sites
    manager.register_site(GeographicSite(
        site_id="us_west_primary",
        region="US West",
        country="USA",
        region_type=RegionType.PRIMARY,
        lat=37.7749,
        lon=-122.4194
    ))
    
    manager.register_site(GeographicSite(
        site_id="us_east_secondary",
        region="US East",
        country="USA",
        region_type=RegionType.SECONDARY,
        lat=40.7128,
        lon=-74.0060
    ))
    
    manager.register_site(GeographicSite(
        site_id="eu_dr_site",
        region="Europe",
        country="Ireland",
        region_type=RegionType.DR_SITE,
        lat=53.3498,
        lon=-6.2603
    ))
    
    # Set geographic policies
    manager.set_geographic_policy(
        "critical_business_data",
        min_regions=3,
        required_region_types=[RegionType.PRIMARY, RegionType.SECONDARY, RegionType.DR_SITE]
    )
    
    # Distribute data geographically
    critical_data = b"Critical business operations data"
    success = await manager.distribute_data_geographically(
        "business_critical_001",
        "critical_business_data",
        critical_data
    )
    
    if success:
        print("Data distributed geographically")
        
        # Simulate site failure
        await manager.handle_site_failure("us_west_primary")
```

### 3. Logical Redundancy

Creating multiple data instances within a system using different data structures or representations.

```python
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import json
import pickle
import compression

@dataclass
class DataInstance:
    instance_id: str
    format_type: str  # json, pickle, avro, parquet, etc.
    compression: Optional[str]  # gzip, lz4, snappy, etc.
    data: bytes
    metadata: Dict
    created_at: float

class LogicalRedundancyManager:
    def __init__(self):
        self.data_instances: Dict[str, List[DataInstance]] = {}
        self.format_converters = {}
        self.register_default_converters()
    
    def register_default_converters(self):
        """Register default format converters"""
        
        self.format_converters['json'] = {
            'serialize': lambda obj: json.dumps(obj).encode('utf-8'),
            'deserialize': lambda data: json.loads(data.decode('utf-8'))
        }
        
        self.format_converters['pickle'] = {
            'serialize': lambda obj: pickle.dumps(obj),
            'deserialize': lambda data: pickle.loads(data)
        }
    
    async def store_with_logical_redundancy(self, data_key: str, data_object: Any,
                                          formats: List[str], 
                                          compression_methods: List[Optional[str]] = None) -> bool:
        """Store data object in multiple logical formats"""
        
        if compression_methods is None:
            compression_methods = [None] * len(formats)
        
        instances = []
        
        for i, format_type in enumerate(formats):
            compression_method = compression_methods[i] if i < len(compression_methods) else None
            
            try:
                # Convert to specified format
                if format_type not in self.format_converters:
                    raise ValueError(f"Unsupported format: {format_type}")
                
                serialized_data = self.format_converters[format_type]['serialize'](data_object)
                
                # Apply compression if specified
                if compression_method:
                    serialized_data = await self._compress_data(serialized_data, compression_method)
                
                # Create instance
                instance = DataInstance(
                    instance_id=f"{data_key}_{format_type}_{compression_method or 'none'}",
                    format_type=format_type,
                    compression=compression_method,
                    data=serialized_data,
                    metadata={
                        'original_size': len(serialized_data),
                        'compressed_size': len(serialized_data) if not compression_method else None
                    },
                    created_at=time.time()
                )
                
                instances.append(instance)
                
            except Exception as e:
                print(f"Failed to create instance in format {format_type}: {e}")
        
        if instances:
            self.data_instances[data_key] = instances
            return True
        
        return False
    
    async def retrieve_data(self, data_key: str, preferred_format: str = None) -> Optional[Any]:
        """Retrieve data, trying preferred format first"""
        
        instances = self.data_instances.get(data_key, [])
        
        if not instances:
            return None
        
        # Try preferred format first
        if preferred_format:
            for instance in instances:
                if instance.format_type == preferred_format:
                    try:
                        return await self._deserialize_instance(instance)
                    except Exception as e:
                        print(f"Failed to deserialize preferred format {preferred_format}: {e}")
        
        # Try other formats
        for instance in instances:
            if not preferred_format or instance.format_type != preferred_format:
                try:
                    return await self._deserialize_instance(instance)
                except Exception as e:
                    print(f"Failed to deserialize format {instance.format_type}: {e}")
        
        return None
    
    async def _deserialize_instance(self, instance: DataInstance) -> Any:
        """Deserialize data instance"""
        
        data = instance.data
        
        # Decompress if needed
        if instance.compression:
            data = await self._decompress_data(data, instance.compression)
        
        # Deserialize
        if instance.format_type in self.format_converters:
            return self.format_converters[instance.format_type]['deserialize'](data)
        else:
            raise ValueError(f"No deserializer for format: {instance.format_type}")
    
    async def _compress_data(self, data: bytes, method: str) -> bytes:
        """Compress data using specified method"""
        
        if method == 'gzip':
            import gzip
            return gzip.compress(data)
        elif method == 'lz4':
            import lz4.frame
            return lz4.frame.compress(data)
        elif method == 'snappy':
            import snappy
            return snappy.compress(data)
        else:
            raise ValueError(f"Unsupported compression method: {method}")
    
    async def _decompress_data(self, data: bytes, method: str) -> bytes:
        """Decompress data using specified method"""
        
        if method == 'gzip':
            import gzip
            return gzip.decompress(data)
        elif method == 'lz4':
            import lz4.frame
            return lz4.frame.decompress(data)
        elif method == 'snappy':
            import snappy
            return snappy.decompress(data)
        else:
            raise ValueError(f"Unsupported compression method: {method}")
    
    def get_redundancy_health(self) -> Dict:
        """Get health status of logical redundancy"""
        
        health_stats = {
            'total_data_keys': len(self.data_instances),
            'format_distribution': {},
            'compression_usage': {},
            'corrupted_instances': 0
        }
        
        for data_key, instances in self.data_instances.items():
            for instance in instances:
                # Count format usage
                format_type = instance.format_type
                health_stats['format_distribution'][format_type] = \
                    health_stats['format_distribution'].get(format_type, 0) + 1
                
                # Count compression usage
                compression = instance.compression or 'none'
                health_stats['compression_usage'][compression] = \
                    health_stats['compression_usage'].get(compression, 0) + 1
                
                # Check for corruption (basic validation)
                try:
                    # Attempt to read first few bytes
                    if len(instance.data) == 0:
                        health_stats['corrupted_instances'] += 1
                except Exception:
                    health_stats['corrupted_instances'] += 1
        
        return health_stats

# Usage example
async def demonstrate_logical_redundancy():
    manager = LogicalRedundancyManager()
    
    # Sample data object
    user_data = {
        'user_id': 12345,
        'name': 'John Doe',
        'email': 'john@example.com',
        'preferences': {
            'theme': 'dark',
            'notifications': True
        },
        'activity_log': [
            {'action': 'login', 'timestamp': '2023-07-27T10:00:00Z'},
            {'action': 'update_profile', 'timestamp': '2023-07-27T10:30:00Z'}
        ]
    }
    
    # Store with multiple formats and compression
    success = await manager.store_with_logical_redundancy(
        'user_12345',
        user_data,
        formats=['json', 'pickle'],
        compression_methods=['gzip', 'lz4']
    )
    
    if success:
        print("Data stored with logical redundancy")
        
        # Retrieve data (try JSON first)
        retrieved_data = await manager.retrieve_data('user_12345', 'json')
        print(f"Retrieved data: {retrieved_data}")
        
        # Get health stats
        health = manager.get_redundancy_health()
        print(f"Redundancy health: {health}")
```

### 4. Time-Based Redundancy

Creating copies at different time points for temporal protection.

```python
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class BackupType(Enum):
    FULL = "full"
    INCREMENTAL = "incremental"
    DIFFERENTIAL = "differential"
    SNAPSHOT = "snapshot"

@dataclass
class TimedBackup:
    backup_id: str
    data_key: str
    backup_type: BackupType
    timestamp: float
    data_hash: str
    size_bytes: int
    retention_until: float
    metadata: Dict

class TimeBasedRedundancyManager:
    def __init__(self):
        self.backups: Dict[str, List[TimedBackup]] = {}
        self.retention_policies = {}
        self.backup_schedules = {}
        
    def set_retention_policy(self, data_category: str, policy: Dict):
        """Set retention policy for data category"""
        self.retention_policies[data_category] = {
            'daily_retention_days': policy.get('daily_retention_days', 30),
            'weekly_retention_weeks': policy.get('weekly_retention_weeks', 12),
            'monthly_retention_months': policy.get('monthly_retention_months', 12),
            'yearly_retention_years': policy.get('yearly_retention_years', 7),
            'max_total_backups': policy.get('max_total_backups', 100)
        }
    
    async def create_timed_backup(self, data_key: str, data: bytes, 
                                backup_type: BackupType, 
                                data_category: str = 'default') -> str:
        """Create time-based backup"""
        
        current_time = time.time()
        data_hash = hashlib.sha256(data).hexdigest()
        
        # Calculate retention period
        retention_until = self._calculate_retention_period(
            current_time, backup_type, data_category
        )
        
        backup = TimedBackup(
            backup_id=f"{data_key}_{backup_type.value}_{int(current_time)}",
            data_key=data_key,
            backup_type=backup_type,
            timestamp=current_time,
            data_hash=data_hash,
            size_bytes=len(data),
            retention_until=retention_until,
            metadata={
                'created_by': 'system',
                'data_category': data_category
            }
        )
        
        # Store backup
        await self._store_backup(backup, data)
        
        # Add to tracking
        if data_key not in self.backups:
            self.backups[data_key] = []
        
        self.backups[data_key].append(backup)
        
        # Clean up old backups if needed
        await self._cleanup_expired_backups(data_key)
        
        return backup.backup_id
    
    def _calculate_retention_period(self, current_time: float, 
                                  backup_type: BackupType, 
                                  data_category: str) -> float:
        """Calculate when backup should be deleted"""
        
        policy = self.retention_policies.get(data_category, {
            'daily_retention_days': 30,
            'weekly_retention_weeks': 12,
            'monthly_retention_months': 12,
            'yearly_retention_years': 7
        })
        
        if backup_type == BackupType.FULL:
            # Keep full backups longer
            retention_days = policy['monthly_retention_months'] * 30
        elif backup_type == BackupType.INCREMENTAL:
            # Shorter retention for incremental
            retention_days = policy['daily_retention_days']
        elif backup_type == BackupType.DIFFERENTIAL:
            # Medium retention for differential
            retention_days = policy['weekly_retention_weeks'] * 7
        else:  # SNAPSHOT
            # Variable retention based on frequency
            retention_days = policy['daily_retention_days']
        
        return current_time + (retention_days * 24 * 60 * 60)
    
    async def _store_backup(self, backup: TimedBackup, data: bytes):
        """Store backup data"""
        
        # In production, this would store to persistent storage
        # For example: cloud storage, tape, distributed file system
        
        storage_path = f"/backups/{backup.data_key}/{backup.backup_id}"
        
        # Simulate storage operation
        print(f"Storing backup {backup.backup_id} to {storage_path}")
        
        # Could implement compression, encryption, etc.
        compressed_data = await self._compress_backup_data(data)
        
        # Store metadata and data
        # Implementation would depend on storage backend
    
    async def _compress_backup_data(self, data: bytes) -> bytes:
        """Compress backup data for storage efficiency"""
        import gzip
        return gzip.compress(data)
    
    async def restore_from_backup(self, data_key: str, 
                                target_timestamp: Optional[float] = None) -> Optional[bytes]:
        """Restore data from backup closest to target timestamp"""
        
        backups = self.backups.get(data_key, [])
        
        if not backups:
            return None
        
        # If no target timestamp, use most recent
        if target_timestamp is None:
            target_timestamp = time.time()
        
        # Find best backup (closest to target time, but not newer)
        best_backup = None
        best_diff = float('inf')
        
        for backup in backups:
            if backup.timestamp <= target_timestamp:
                diff = target_timestamp - backup.timestamp
                if diff < best_diff:
                    best_diff = diff
                    best_backup = backup
        
        if best_backup:
            return await self._retrieve_backup_data(best_backup)
        
        return None
    
    async def _retrieve_backup_data(self, backup: TimedBackup) -> bytes:
        """Retrieve data from backup"""
        
        storage_path = f"/backups/{backup.data_key}/{backup.backup_id}"
        
        # Simulate retrieval
        print(f"Retrieving backup {backup.backup_id} from {storage_path}")
        
        # In production, would read from actual storage
        # and decompress, decrypt as needed
        
        return b"restored_data"  # Placeholder
    
    async def _cleanup_expired_backups(self, data_key: str):
        """Clean up expired backups for data key"""
        
        if data_key not in self.backups:
            return
        
        current_time = time.time()
        backups = self.backups[data_key]
        
        # Identify expired backups
        expired_backups = [
            backup for backup in backups
            if backup.retention_until < current_time
        ]
        
        # Remove expired backups
        for backup in expired_backups:
            await self._delete_backup(backup)
            backups.remove(backup)
        
        if expired_backups:
            print(f"Cleaned up {len(expired_backups)} expired backups for {data_key}")
    
    async def _delete_backup(self, backup: TimedBackup):
        """Delete backup from storage"""
        
        storage_path = f"/backups/{backup.data_key}/{backup.backup_id}"
        print(f"Deleting expired backup {backup.backup_id}")
        
        # Implementation would delete from actual storage
    
    def get_backup_timeline(self, data_key: str) -> List[Dict]:
        """Get timeline of backups for data key"""
        
        backups = self.backups.get(data_key, [])
        
        timeline = []
        for backup in sorted(backups, key=lambda b: b.timestamp):
            timeline.append({
                'backup_id': backup.backup_id,
                'timestamp': datetime.fromtimestamp(backup.timestamp).isoformat(),
                'type': backup.backup_type.value,
                'size_mb': backup.size_bytes / (1024 * 1024),
                'expires': datetime.fromtimestamp(backup.retention_until).isoformat()
            })
        
        return timeline
    
    async def schedule_automated_backups(self, data_key: str, schedule: Dict):
        """Schedule automated backups"""
        
        self.backup_schedules[data_key] = schedule
        
        # Start backup scheduler task
        asyncio.create_task(self._backup_scheduler(data_key, schedule))
    
    async def _backup_scheduler(self, data_key: str, schedule: Dict):
        """Background task for scheduled backups"""
        
        while data_key in self.backup_schedules:
            try:
                # Check if backup is due
                last_backup_time = self._get_last_backup_time(data_key)
                current_time = time.time()
                
                should_backup = False
                backup_type = BackupType.INCREMENTAL
                
                # Daily backup check
                if current_time - last_backup_time > schedule.get('daily_interval', 86400):
                    should_backup = True
                    
                    # Weekly full backup
                    if current_time - self._get_last_full_backup_time(data_key) > 604800:  # 7 days
                        backup_type = BackupType.FULL
                
                if should_backup:
                    # Get current data (this would be implemented based on data source)
                    current_data = await self._get_current_data(data_key)
                    
                    if current_data:
                        await self.create_timed_backup(
                            data_key, 
                            current_data, 
                            backup_type
                        )
                
                # Sleep until next check
                await asyncio.sleep(schedule.get('check_interval', 3600))  # Check hourly
                
            except Exception as e:
                print(f"Backup scheduler error for {data_key}: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error

# Usage example
async def demonstrate_time_based_redundancy():
    manager = TimeBasedRedundancyManager()
    
    # Set retention policy
    manager.set_retention_policy('critical_data', {
        'daily_retention_days': 30,
        'weekly_retention_weeks': 12,
        'monthly_retention_months': 24,
        'yearly_retention_years': 10
    })
    
    # Create some backups
    data = b"Important business data version 1"
    
    backup_id1 = await manager.create_timed_backup(
        'business_data_001',
        data,
        BackupType.FULL,
        'critical_data'
    )
    
    # Simulate time passing and data changes
    await asyncio.sleep(1)
    
    data = b"Important business data version 2"
    backup_id2 = await manager.create_timed_backup(
        'business_data_001',
        data,
        BackupType.INCREMENTAL,
        'critical_data'
    )
    
    # Get backup timeline
    timeline = manager.get_backup_timeline('business_data_001')
    print("Backup timeline:")
    for entry in timeline:
        print(f"  {entry['timestamp']}: {entry['type']} backup ({entry['size_mb']:.2f} MB)")
    
    # Restore from backup
    restored_data = await manager.restore_from_backup('business_data_001')
    print(f"Restored data: {restored_data}")
    
    # Schedule automated backups
    await manager.schedule_automated_backups('business_data_001', {
        'daily_interval': 86400,  # 24 hours
        'check_interval': 3600    # Check every hour
    })
```

## Implementation Strategies

### RAID Systems

```python
from enum import Enum
from typing import List, Optional
import os

class RAIDLevel(Enum):
    RAID_0 = "raid_0"  # Striping
    RAID_1 = "raid_1"  # Mirroring
    RAID_5 = "raid_5"  # Striping with parity
    RAID_6 = "raid_6"  # Striping with double parity
    RAID_10 = "raid_10"  # Striping of mirrors

class RAIDManager:
    def __init__(self, raid_level: RAIDLevel, drives: List[str]):
        self.raid_level = raid_level
        self.drives = drives
        self.stripe_size = 64 * 1024  # 64KB stripe size
        
    async def write_data(self, data: bytes, block_address: int) -> bool:
        """Write data using RAID configuration"""
        
        if self.raid_level == RAIDLevel.RAID_0:
            return await self._write_raid_0(data, block_address)
        elif self.raid_level == RAIDLevel.RAID_1:
            return await self._write_raid_1(data, block_address)
        elif self.raid_level == RAIDLevel.RAID_5:
            return await self._write_raid_5(data, block_address)
        else:
            raise ValueError(f"RAID level {self.raid_level} not implemented")
    
    async def _write_raid_0(self, data: bytes, block_address: int) -> bool:
        """RAID 0: Stripe data across drives"""
        
        # No redundancy, but improved performance
        chunk_size = len(data) // len(self.drives)
        
        for i, drive in enumerate(self.drives):
            start_offset = i * chunk_size
            end_offset = start_offset + chunk_size if i < len(self.drives) - 1 else len(data)
            chunk = data[start_offset:end_offset]
            
            await self._write_to_drive(drive, block_address + i, chunk)
        
        return True
    
    async def _write_raid_1(self, data: bytes, block_address: int) -> bool:
        """RAID 1: Mirror data to all drives"""
        
        # Write identical copy to each drive
        successful_writes = 0
        
        for drive in self.drives:
            try:
                await self._write_to_drive(drive, block_address, data)
                successful_writes += 1
            except Exception as e:
                print(f"Write failed to drive {drive}: {e}")
        
        # Require at least one successful write
        return successful_writes > 0
    
    async def _write_raid_5(self, data: bytes, block_address: int) -> bool:
        """RAID 5: Striping with distributed parity"""
        
        if len(self.drives) < 3:
            raise ValueError("RAID 5 requires at least 3 drives")
        
        # Calculate parity
        chunk_size = len(data) // (len(self.drives) - 1)
        parity_drive = block_address % len(self.drives)
        
        # Write data chunks
        data_drive_index = 0
        for i, drive in enumerate(self.drives):
            if i == parity_drive:
                # Calculate and write parity
                parity_data = self._calculate_parity(data, chunk_size)
                await self._write_to_drive(drive, block_address, parity_data)
            else:
                # Write data chunk
                start_offset = data_drive_index * chunk_size
                end_offset = start_offset + chunk_size
                chunk = data[start_offset:end_offset]
                
                await self._write_to_drive(drive, block_address, chunk)
                data_drive_index += 1
        
        return True
    
    def _calculate_parity(self, data: bytes, chunk_size: int) -> bytes:
        """Calculate XOR parity for RAID 5"""
        
        parity = bytearray(chunk_size)
        
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]
            for j in range(len(chunk)):
                if j < len(parity):
                    parity[j] ^= chunk[j]
        
        return bytes(parity)
    
    async def _write_to_drive(self, drive: str, block_address: int, data: bytes):
        """Write data to specific drive"""
        
        # Simulate drive write operation
        print(f"Writing {len(data)} bytes to drive {drive} at block {block_address}")
        
        # In production, this would interface with actual storage hardware
        # or file system operations
```

### Cloud Storage Redundancy

```python
import asyncio
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class CloudProvider(Enum):
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    HYBRID = "hybrid"

@dataclass
class CloudStorageConfig:
    provider: CloudProvider
    region: str
    storage_class: str  # Standard, IA, Glacier, etc.
    encryption: bool
    replication_enabled: bool

class CloudRedundancyManager:
    def __init__(self):
        self.storage_configs: Dict[str, CloudStorageConfig] = {}
        self.cross_region_policies = {}
        
    def configure_storage_tier(self, tier_name: str, config: CloudStorageConfig):
        """Configure cloud storage tier"""
        self.storage_configs[tier_name] = config
    
    async def store_with_cloud_redundancy(self, data_key: str, data: bytes,
                                        redundancy_policy: Dict) -> bool:
        """Store data with cloud redundancy"""
        
        target_tiers = redundancy_policy.get('storage_tiers', ['primary'])
        min_successful_stores = redundancy_policy.get('min_successful_stores', 1)
        
        successful_stores = []
        
        for tier_name in target_tiers:
            if tier_name not in self.storage_configs:
                print(f"Storage tier {tier_name} not configured")
                continue
            
            try:
                config = self.storage_configs[tier_name]
                await self._store_to_cloud_tier(data_key, data, config)
                successful_stores.append(tier_name)
                
            except Exception as e:
                print(f"Failed to store to tier {tier_name}: {e}")
        
        return len(successful_stores) >= min_successful_stores
    
    async def _store_to_cloud_tier(self, data_key: str, data: bytes, 
                                 config: CloudStorageConfig):
        """Store data to specific cloud tier"""
        
        # Simulate cloud storage operation
        print(f"Storing {data_key} to {config.provider.value} "
              f"in {config.region} ({config.storage_class})")
        
        # In production, would use cloud SDKs:
        # - boto3 for AWS
        # - azure-storage for Azure
        # - google-cloud-storage for GCP
        
        if config.encryption:
            encrypted_data = await self._encrypt_data(data)
        else:
            encrypted_data = data
        
        # Simulate network transfer
        await asyncio.sleep(0.1 * len(data) / (1024 * 1024))  # Simulate based on size
        
        if config.replication_enabled:
            # Enable cross-region replication
            await self._enable_cross_region_replication(data_key, config)
    
    async def _encrypt_data(self, data: bytes) -> bytes:
        """Encrypt data for cloud storage"""
        
        # In production, would use proper encryption
        # e.g., AES-256, envelope encryption with KMS
        
        import base64
        return base64.b64encode(data)
    
    async def _enable_cross_region_replication(self, data_key: str, 
                                             config: CloudStorageConfig):
        """Enable cross-region replication for data"""
        
        # Configure automatic replication to other regions
        if config.provider == CloudProvider.AWS:
            # Configure S3 Cross-Region Replication
            pass
        elif config.provider == CloudProvider.AZURE:
            # Configure Azure Blob Storage replication
            pass
        elif config.provider == CloudProvider.GCP:
            # Configure Cloud Storage replication
            pass

# Usage example
async def setup_cloud_redundancy():
    manager = CloudRedundancyManager()
    
    # Configure storage tiers
    manager.configure_storage_tier('primary', CloudStorageConfig(
        provider=CloudProvider.AWS,
        region='us-west-2',
        storage_class='Standard',
        encryption=True,
        replication_enabled=True
    ))
    
    manager.configure_storage_tier('backup', CloudStorageConfig(
        provider=CloudProvider.AZURE,
        region='westus2',
        storage_class='Cool',
        encryption=True,
        replication_enabled=False
    ))
    
    manager.configure_storage_tier('archive', CloudStorageConfig(
        provider=CloudProvider.GCP,
        region='us-central1',
        storage_class='Nearline',
        encryption=True,
        replication_enabled=False
    ))
    
    # Store with redundancy policy
    data = b"Critical business data"
    
    redundancy_policy = {
        'storage_tiers': ['primary', 'backup', 'archive'],
        'min_successful_stores': 2
    }
    
    success = await manager.store_with_cloud_redundancy(
        'critical_data_001',
        data,
        redundancy_policy
    )
    
    print(f"Cloud redundancy storage: {'Success' if success else 'Failed'}")
```

## Best Practices

### 1. Redundancy Strategy Selection

```python
class RedundancyStrategySelector:
    def __init__(self):
        self.strategy_matrix = {
            'data_criticality': {
                'critical': ['physical', 'geographic', 'logical', 'time_based'],
                'important': ['physical', 'geographic', 'time_based'],
                'normal': ['physical', 'time_based'],
                'low': ['time_based']
            },
            'recovery_time_objective': {
                'immediate': ['physical', 'logical'],
                'minutes': ['physical', 'geographic'],
                'hours': ['geographic', 'time_based'],
                'days': ['time_based']
            },
            'budget_level': {
                'high': ['physical', 'geographic', 'logical', 'time_based'],
                'medium': ['physical', 'geographic'],
                'low': ['time_based']
            }
        }
    
    def recommend_redundancy_strategy(self, requirements: Dict) -> List[str]:
        """Recommend redundancy strategies based on requirements"""
        
        strategy_scores = {}
        
        for requirement, value in requirements.items():
            if requirement in self.strategy_matrix:
                strategies = self.strategy_matrix[requirement].get(value, [])
                
                for strategy in strategies:
                    strategy_scores[strategy] = strategy_scores.get(strategy, 0) + 1
        
        # Return strategies with score >= 2 (mentioned in at least 2 categories)
        recommended = [
            strategy for strategy, score in strategy_scores.items()
            if score >= 2
        ]
        
        return recommended if recommended else ['time_based']  # Minimum fallback

# Usage
selector = RedundancyStrategySelector()

requirements = {
    'data_criticality': 'critical',
    'recovery_time_objective': 'minutes',
    'budget_level': 'medium'
}

strategies = selector.recommend_redundancy_strategy(requirements)
print(f"Recommended strategies: {strategies}")
```

### 2. Monitoring and Alerting

```python
class RedundancyMonitor:
    def __init__(self):
        self.health_checks = {}
        self.alert_thresholds = {
            'redundancy_level_critical': 1,  # Only 1 copy remaining
            'redundancy_level_warning': 2,   # Only 2 copies remaining
            'corruption_rate_threshold': 0.01  # 1% corruption rate
        }
    
    async def monitor_redundancy_health(self, managers: Dict):
        """Monitor health of all redundancy managers"""
        
        health_report = {
            'timestamp': time.time(),
            'overall_health': 'healthy',
            'issues': [],
            'recommendations': []
        }
        
        # Check physical redundancy
        if 'physical' in managers:
            physical_health = await managers['physical'].check_redundancy_health()
            
            if physical_health['corrupted_files'] > 0:
                health_report['issues'].append({
                    'type': 'corruption',
                    'severity': 'critical',
                    'count': physical_health['corrupted_files'],
                    'description': f"{physical_health['corrupted_files']} corrupted files detected"
                })
                health_report['overall_health'] = 'critical'
            
            if physical_health['at_risk_files'] > 0:
                health_report['issues'].append({
                    'type': 'redundancy_low',
                    'severity': 'warning',
                    'count': physical_health['at_risk_files'],
                    'description': f"{physical_health['at_risk_files']} files with low redundancy"
                })
                
                if health_report['overall_health'] == 'healthy':
                    health_report['overall_health'] = 'warning'
        
        # Check geographic redundancy
        if 'geographic' in managers:
            # Implementation for geographic redundancy health checks
            pass
        
        # Generate recommendations
        if health_report['issues']:
            health_report['recommendations'] = self._generate_recommendations(health_report['issues'])
        
        return health_report
    
    def _generate_recommendations(self, issues: List[Dict]) -> List[str]:
        """Generate recommendations based on health issues"""
        
        recommendations = []
        
        for issue in issues:
            if issue['type'] == 'corruption':
                recommendations.append(
                    f"Immediately restore {issue['count']} corrupted files from backup"
                )
                recommendations.append("Run full integrity check on all storage devices")
            
            elif issue['type'] == 'redundancy_low':
                recommendations.append(
                    f"Increase redundancy for {issue['count']} at-risk files"
                )
                recommendations.append("Consider adding additional storage devices")
        
        return recommendations

async def run_redundancy_monitoring():
    monitor = RedundancyMonitor()
    
    # Set up managers (simplified)
    managers = {
        'physical': PhysicalRedundancyManager(),
        'geographic': GeographicRedundancyManager(),
        'logical': LogicalRedundancyManager(),
        'time_based': TimeBasedRedundancyManager()
    }
    
    while True:
        try:
            health_report = await monitor.monitor_redundancy_health(managers)
            
            if health_report['overall_health'] != 'healthy':
                print(f"REDUNDANCY ALERT: {health_report['overall_health']}")
                for issue in health_report['issues']:
                    print(f"  - {issue['description']}")
                
                print("Recommendations:")
                for rec in health_report['recommendations']:
                    print(f"  - {rec}")
            
            await asyncio.sleep(300)  # Check every 5 minutes
            
        except Exception as e:
            print(f"Monitoring error: {e}")
            await asyncio.sleep(60)  # Retry after 1 minute
```

## Conclusion

Data redundancy is essential for building resilient systems that can withstand various types of failures. Key takeaways include:

### Strategy Selection
- **Physical Redundancy**: Protection against hardware failures
- **Geographic Redundancy**: Protection against regional disasters
- **Logical Redundancy**: Protection against format-specific issues
- **Time-Based Redundancy**: Protection against logical errors and corruption

### Implementation Guidelines
1. **Assess Requirements**: Understand criticality, RTO, and budget constraints
2. **Layer Multiple Strategies**: Combine different redundancy types for comprehensive protection
3. **Automate Management**: Implement automated backup, replication, and cleanup processes
4. **Monitor Continuously**: Track redundancy health and integrity
5. **Test Recovery**: Regularly test restore and recovery procedures

### Best Practices
- **Diversify Storage**: Use different technologies, vendors, and locations
- **Implement Retention Policies**: Define appropriate data lifecycle management
- **Encrypt Sensitive Data**: Protect redundant copies with encryption
- **Document Procedures**: Maintain clear recovery procedures and contacts
- **Regular Testing**: Verify redundancy effectiveness through regular drills

Remember that redundancy involves trade-offs between cost, complexity, and protection level. The goal is to implement the right level of redundancy that matches your specific risk tolerance and business requirements while maintaining operational efficiency.