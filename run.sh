#export PATH=$HOME/environment:$PATH

python3 /work/igvjs_auto_capture/headless.py \
--bucket sra-virginia \
--url analysis/DRP001919/DRR016715/irav/DRR016715.iravnet.filt.bam \
--index_url analysis/DRP001919/DRR016715/irav/DRR016715.iravnet.filt.bam.bai \
--genome hg38 \
--chrom chr3 \
--pos 49699104 \
--output ./capture/RNF123_chr3_49699104_DRP001919_DRR016715.png
