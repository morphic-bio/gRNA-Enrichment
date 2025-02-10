#! /bin/bash
docker run --rm -p 6080:6080 -v /workspace/gRNA-Enrichment/:/data -v /var/run/docker.sock:/var/run/docker.sock -v /tmp/.X11-unix:/tmp/.X11-unix --privileged --group-add root -e STARTING_WORKFLOW=/data/workflow/mageck_count/mageck_count.ows biodepot/bwb
