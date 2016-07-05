# WORK IN PROGRESS

## Short description

This project provides a worker for obtaining QOS information from Ceph storage system. It is designed to act as a QOS data source for  [**cdmi-s3-qos**](https://github.com/indigo-dc/cdmi-s3-qos) module, but it can also act as a standalone module.
This service supports two data sources:
* Ceph data source - data is obtained from configured Ceph storage system (life mode)
* Mock data source - data is obtained from configuration file (designed for testing purposes)

## Installation

### Requirements

Tools required to run the project:

* [git](https://git-scm.com/) (optionally, if you want to follow the bellow procedures literally)
* [python 3.x](https://www.python.org/)
* [only for Ceph data source] Linux user account with priviledges to run [**radosgw-admin**](http://docs.ceph.com/docs/hammer/man/8/radosgw-admin/) on Ceph cluster 

### Installation workflow

Clone cdmi-s3-qos-ceph-provider repository [cdmi-s3-qos-ceph-provider](https://github.com/indigo-dc/cdmi-s3-qos-ceph-provider.git)

## Usage

```
usage: cdmi-s3-qos-ceph-provider.py [-h] [-b BUCKET] [-a]
Returns capabilities information from CEPH server
optional arguments:
  -h, --help                    Show this help message and exit
  -b BUCKET, --bucket BUCKET    Get profile of given bucket                    
  -a, --all                     Get all profiles
```

## Configuration

### Data source

Data source is configured in `config.ini` file. The available values are:

* `ceph_source` to take advantage of Ceph data source
* `mock_source` to take advantage of Mock data source

### Mock data source

`cdmi-s3-qos-ceph-provider.py -b BUCKET` returns always:

```
{
   'type':'container',
   'metadata':{
      'cdmi_geographic_placement':[
         'PL',
         'GB'
      ],
      'cdmi_data_redundancy':'2',
      'cdmi_latency':'20'
   },
   'name':'Profile1',
   'allowed_profiles':[

   ],
   'pools':[
      '.rgw.buckets'
   ]
}
```

`cdmi-s3-qos-ceph-provider.py --all` returns always:

```
[
   {
      'metadata_provided':{
         'cdmi_latency_provided':'20',
         'cdmi_data_redundancy_provided':'2',
         'cdmi_geographic_placement_provided':[
            'PL',
            'GB'
         ]
      },
      'metadata':{
         'cdmi_latency':'20',
         'cdmi_data_redundancy':'2',
         'cdmi_geographic_placement':[
            'PL',
            'GB'
         ]
      },
      'pools':[
         '.rgw.buckets'
      ],
      'type':'container',
      'name':'Profile1',
      'allowed_profiles':[

      ]
   },
   {
      'metadata_provided':{
         'cdmi_latency_provided':'300',
         'cdmi_data_redundancy_provided':'2',
         'cdmi_geographic_placement_provided':[
            'DE',
            'CZ'
         ]
      },
      'metadata':{
         'cdmi_latency':'300',
         'cdmi_data_redundancy':'2',
         'cdmi_geographic_placement':[
            'DE',
            'CZ'
         ]
      },
      'pools':[
         '.rgw.buckets.cdmi2'
      ],
      'type':'dataobject',
      'name':'Profile2',
      'allowed_profiles':[

      ]
   }
]
```

### Ceph data source

Each Ceph pool has assigned some QoS profile. Each bucket resides wihtin single pool. Mapping between QoS profiles and Ceph pools is placed in `profile_config.ini` file. Relation between buckets and pools is determined on the fly with help of Ceph administrative tools.

QoS profiles are described by set of attributes (in key - value format). As not all QoS attributes can be get from Ceph tools, some of them are placed in `profile_config.ini` file. The other attributes are read dynamically from Ceph platform.

Data read directly from Ceph:

* data redundancy
* mapping between bucket and pool

Sample ``profile_config.ini`:
```
[Profile1]
pools=[".rgw.buckets"]
type: container
cdmi_latency: 20
cdmi_geographic_placement: PL, GB

[Profile2]
pools=[".rgw.buckets.cdmi2"]
type: dataobject
cdmi_latency: 300
cdmi_geographic_placement: DE, CZ

```
