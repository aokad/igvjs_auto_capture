#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 16:15:42 2020

@author: aokada
@version: 20200228.1617
"""

import os

CURRENT = os.path.dirname(os.path.abspath(__file__))
IGVJS_PATH = CURRENT + "/igv.js"
TEMPLATE_PATH = CURRENT + "/template.html"

def create_presigned_url(bucket_name, object_name, expiration=3600):
    import boto3
    
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_name
            },
            ExpiresIn=expiration
        )
    except Exception as e:
        print(e)
        return None

    # The response contains the presigned URL
    return response

def write_html(url, indexURL, output_html, args):
    
    track_name = args.track_name
    if track_name == "":
        track_name = os.path.splitext(os.path.basename(args.url))[0]
    
    start = args.pos - args.read_width
    if start < 1:
        start = 1
        
    template = open(TEMPLATE_PATH).read()
    data = template.format(
        genome = args.genome,
        chrom = args.chrom,
        start = start,
        end = args.pos + args.read_width,
        name = track_name,
        url = url,
        indexURL = indexURL,
        height = args.track_height
    )
    open(output_html, "w").write(data)
    
    js_path = os.path.dirname(output_html) + "/igv.js"
    if not os.path.exists(js_path):
        import shutil
        shutil.copy(IGVJS_PATH, js_path)
        
def capture(html, args):
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    # ブラウザのオプションにヘッドレスモードを指定
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')

    # 設定したオプションでブラウザオブジェクトの生成
    browser = webdriver.Firefox(options=options)
    browser.set_window_size(args.img_height, args.img_width)

    #browser.implicitly_wait(20)
    
    browser.get('file://' + os.path.abspath(html))
    #browser.get('file:///home/ubuntu/environment/igvjs.html')
    #WebDriverWait(browser, 20).until(EC.visibility_of_element_located)
    
    import time
    time.sleep(args.wait_time)
    
    browser.save_screenshot(args.output)
    # ブラウザ操作終了
    browser.quit()
    
def main():
    import sys
    import argparse
    
    prog = "igvjs_capture"
    parser = argparse.ArgumentParser(prog = prog)
    parser.add_argument("--version", action = "version", version = prog + "-0.0.1")
    
    parser.add_argument("--bucket", metavar = "YOUR-BUCKET", help = "aws s3 bucket name for bam/bai file", type = str, required = True)
    parser.add_argument("--url", metavar = "/path/to/file.bam", help = "aws s3 path to bam file (without bucket-name)", type = str, required = True)
    parser.add_argument("--index_url", metavar = "/path/to/file.bam.bai", help = "aws s3 path to bai file (without bucket-name)", type = str, required = True)

    parser.add_argument("--genome", metavar = "hg19", help = "see, https://github.com/igvteam/igv.js/wiki/Reference-Genome#genome-property", type = str, required = True)
    parser.add_argument("--chrom", metavar = "chr12", help = "chromosome", type = str, required = True)
    parser.add_argument("--pos", metavar = "123456", help = "center position for capture", type = int, required = True)

    parser.add_argument("--output", metavar = "/path/to/capture.png", help = "path to output capture file", type = str, required = True)

    parser.add_argument("--track_name", metavar = "5929Tumor", help = "track name, fefault: bam_file name", type = str, default = "")
    parser.add_argument("--img_height", metavar = "2560", help = "height(px) for image file", type = int, default = 2560)
    parser.add_argument("--img_width", metavar = "1600", help = "width(px) for image file", type = int, default = 1600)
    parser.add_argument("--track_height", metavar = "1200", help = "height(px) for igv.js drowing read track.", type = int, default = 1200)
    parser.add_argument("--read_width", metavar = "300", help = "capture range(bps). If setting width=300, capture size = 601bps. (300(left) + 1(center) + 300(right))", type = int, default = 300)
    parser.add_argument("--wait_time", metavar = "30", help = "aws s3 path to bam file (without bucket-name)", type = int, default = 30)
    
    argv = sys.argv[1:]
    if len(argv) < 1:
        argv = [""]
        
    args = parser.parse_args(argv)

    url = create_presigned_url(args.bucket, args.url)
    indexURL = create_presigned_url(args.bucket, args.index_url)
    html = os.path.splitext(args.output)[0] + ".html"
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    write_html(url, indexURL, html, args)
    capture(html, args)
    
if __name__ == '__main__':
    main()
