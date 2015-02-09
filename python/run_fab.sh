#!/bin/bash

fab -f fabfile1.py -i ~/insecure_private_key -H localhost host_type
