#!/usr/bin/env bash

kubectl delete -f team-view.yaml
kubectl create -f team-view.yaml
sleep 30
export NODE_PORT=$(kubectl get services/team-view -o go-template='{{(index .spec.ports 0).nodePort}}')
open http://localhost:$NODE_PORT/lab