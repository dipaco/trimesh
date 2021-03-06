set -xe
apt-get update -qq
apt-get upgrade -y -qq --no-install-recommends
apt-get install -y -qq --no-install-recommends wget bzip2 supervisor \
	libgl1-mesa-glx libgl1-mesa-dri xvfb xauth \
	libassimp-dev ca-certificates zstd unzip \
	freeglut3-dev

# remove garbage
apt-get clean -qq
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
