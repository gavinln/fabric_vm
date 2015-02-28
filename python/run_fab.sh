#!/bin/bash

fab -f fabfile.py -i ~/insecure_private_key -H localhost host_type
