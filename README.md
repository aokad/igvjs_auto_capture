# igvjs_auto_capture

AWS S3バケットにおいてあるbamに対してpresignを発行した後、igv.jsで描画して指定のポジションでcaptureします。

## Set up

用意するもの
 
 - AWS CLI が使用できるユーザアカウント
 - bam, bai が置いてある AWS S3 バケット

1. AWS S3バケットに対し、CORを設定

```
[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "GET",
            "HEAD"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": [
            "Content-Length",
            "Content-Type",
            "Content-Range"
        ],
        "MaxAgeSeconds": 3000
    }
]
```

2. docker イメージの取得とAWSアカウントの設定

```
$ docker pull aokad/igvjs_auto_capture
$ docker run -it --memory 1024mb --shm-size 2g aokad/igvjs_auto_capture bash
# (コンテナ内) aws configure
...
```

## How to use

（コンテナ内で実行）  
コンテナにおいてある run.sh を編集して実行する  
/work/igvjs_auto_capture/run.sh
```
python3 /work/igvjs_auto_capture/headless.py \
--bucket sra-virginia \
--url path/to/bam/file.bam \
--index_url path/to/bam/file.bam.bai \
--genome hg38 \
--chrom chr3 \
--pos 49699104 \
--output ./capture.png
```

※ `--url`, `--index_url` は `s3://bucket-name/` 不要  
`s3://bucket-name/dir/file.bam` の場合、`dir/file.bam` を入力する
