#!/bin/bash
curl -X POST "http://localhost:3333/api/pcap/file" \
	-H "Content-Type: application/json" \
	-d '{"file":"/home/capture.pcap","flush_all":false,"delete_original_file":false}'
