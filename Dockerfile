FROM 763104351884.dkr.ecr.eu-north-1.amazonaws.com/pytorch-training:1.12.1-gpu-py38-cu116-ubuntu20.04-ec2
RUN pip install coloredlogs
COPY workdir ./workdir
