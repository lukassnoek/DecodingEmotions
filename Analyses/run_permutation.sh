 #!/bin/bash
PERMS=1000
for i in $(seq 1 $PERMS); do 
	python /home/lukas/Dropbox/PhD_projects/DecodingEmotions_SCAN/Analyses/permute_main_analysis.py $i
done