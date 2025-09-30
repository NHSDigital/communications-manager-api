###################################################################################
#
# Uses git secrets scanner to scan raw source code for secrets
# Same framework in the nhsd-git-secrets folder, but wrapped up in a docker image
#
# How to use:
# 1. Create yourself a ".gitallowed" file in the root of your project.
# 2. Add an allowed patterns to there
# 3. Add an additional providers that you want to use - uses AWS by default
# 4. "docker build" this docker file as part of your pipeline
#
# What is does:
# 1. Copies your source code into a docker image
# 2. Downloads latest version of the secret scanner tool
# 3. Downloads latest regex patterns from software-engineering-quality-framework
# 4. Runs a scan
#
##################################################################################

FROM ubuntu:24.10

RUN echo "Installing required modules" \
  && apt-get update \
  && apt-get -y install build-essential curl git \
  && apt-get clean \
  && echo "Copying source files"

# By default, we copy the entire project into the dockerfile for secret scanning
# Tweak that COPY if you only want some of the source
WORKDIR /secrets-scanner
COPY . source
RUN ls -l source \
  && echo "Downloading secrets scanner" \
  && curl https://codeload.github.com/awslabs/git-secrets/tar.gz/master | tar -xz --strip=1 git-secrets-master \
  && RUN echo "Installing secrets scanner" \
  && RUN make install \
  && echo "Configuring git"

# even though running secrets scanner on a folder, must still be in some kind of git repo
# for the git-secrets config to attach to something
# so init an empty git repo here
WORKDIR /secrets-scanner/source
RUN git init \
  && echo "Downloading regex files from engineering-framework" \
  && curl https://codeload.github.com/NHSDigital/software-engineering-quality-framework/tar.gz/main | tar -xz --strip=3 software-engineering-quality-framework-main/tools/nhsd-git-secrets/nhsd-rules-deny.txt \
  && echo "Copying allowed secrets list"

COPY .gitallowed .
RUN echo .gitallowed \
  # Register additional providers: adds AWS by default
  && echo "Configuring secrets scanner" \
  && /secrets-scanner/git-secrets --register-aws \
  && /secrets-scanner/git-secrets --add-provider -- cat nhsd-rules-deny.txt \
  # build will fail here, if secrets are found
  && echo "Running scan..." \
  && /secrets-scanner/git-secrets --scan -r .
