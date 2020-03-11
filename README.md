# igvjs_auto_capture

AWS S3バケットにおいてあるbamに対してpresignを発行した後、igv.jsで描画して指定のポジションでcaptureします。

## Set up

用意するもの
 
 - AWS CLI が使用できるユーザアカウント
 - bam, bai が置いてある AWS S3 バケット

1. AWS S3バケットに対し、CORを設定

```
<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
<CORSRule>
    <AllowedOrigin>*</AllowedOrigin>
    <AllowedMethod>GET</AllowedMethod>
    <AllowedMethod>HEAD</AllowedMethod>
    <MaxAgeSeconds>3000</MaxAgeSeconds>
    <ExposeHeader>Content-Length</ExposeHeader>
    <ExposeHeader>Content-Type</ExposeHeader>
    <ExposeHeader>Content-Range</ExposeHeader>
    <AllowedHeader>*</AllowedHeader>
</CORSRule>
</CORSConfiguration>
```

2. docker イメージの取得とAWSアカウントの設定

```
$ docker pull aokad/igvjs_auto_capture
$ docker run -it --memory 1024mb --shm-size 2g igvjs_auto_capture bash
# (コンテナ内) aws configure
...
```

## How to use

run.sh を編集して使う

```
python3 /work/igvjs_auto_capture/headless.py \
--bucket sra-virginia \
--url analysis/DRP001919/DRR016715/irav/DRR016715.iravnet.filt.bam \
--index_url analysis/DRP001919/DRR016715/irav/DRR016715.iravnet.filt.bam.bai \
--genome hg38 \
--chrom chr3 \
--pos 49699104 \
--output ./capture/RNF123_chr3_49699104_DRP001919_DRR016715.png
```
