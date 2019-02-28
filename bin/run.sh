#!/usr/bin/env bash

KC_CMD="kubectl"
if ! [ -x "$(command -v kubectl)" ]; then
    if ! [ -x "$(command -v microk8s.kubectl)" ]; then
        echo 'unable to find kubectl command. please ensure Kubenetes is properly installed'
        exit 1
    fi
    KC_CMD="microk8s.kubectl"
fi


$KC_CMD delete -f team-view.yaml --all
$KC_CMD create -f team-view.yaml
sleep 30
open http://team-view.reserolabs.science/lab