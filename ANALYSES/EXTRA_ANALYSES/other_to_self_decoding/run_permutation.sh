 #!/bin/bash
PERMS=1300
for i in $(seq 1 $PERMS); do
	python /home/lsnoek1/DecodingEmotions/PermutationStuff/REMOTE_SCRIPTS/ANALYSES/EXTRA_ANALYSES/other_to_self_decoding/permute_other_self_analysis.py $i
done
