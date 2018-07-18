#!/usr/bin/env bash

kubectl delete -f team-viewer.yaml
kubectl create -f team-viewer.yaml
sleep 30
export NODE_PORT=$(kubectl get services/team-viewer -o go-template='{{(index .spec.ports 0).nodePort}}')
open http://localhost:$NODE_PORT/lab