param([string]$img_version='v1.0.0',[int]$e=0,[string]$img_name='stock-quotations-gateway')
$build_dir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$proj_dir = Split-Path -Parent $build_dir
docker login --username=ohsaly --password=lgb2536807 registry.cn-shanghai.aliyuncs.com
if(${e} -eq 1)
{
Copy-Item $build_dir'\Dockerfile-Environment' $proj_dir'\Dockerfile'
docker build -t $img_name-environment .
}
Copy-Item $build_dir'\Dockerfile-Executable' $proj_dir'\Dockerfile'
docker build -t $img_name-executable .
docker tag $img_name-executable registry.cn-shanghai.aliyuncs.com/ohs-sys-stage/$img_name-executable:$img_version
docker push registry.cn-shanghai.aliyuncs.com/ohs-sys-stage/$img_name-executable:$img_version
del $proj_dir'\Dockerfile'
