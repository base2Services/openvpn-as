# Builds a docker image for a OpenVPN Access Server
FROM phusion/baseimage 
MAINTAINER Lew Shobbrook <l.shobbrook@base2services.com>


###############################################
##           ENVIRONMENTAL CONFIG            ##
###############################################
# Set correct environment variables
ENV DEBIAN_FRONTEND noninteractive
ENV HOME="/root" LC_ALL="C.UTF-8" LANG="en_AU.UTF-8" LANGUAGE="en_AU.UTF-8"

RUN apt-get update -qq && \
apt-get upgrade -yqq && \
apt-get install -qy net-tools iptables curl && apt-get clean
RUN mkdir -p /opt/base2/pkg
RUN cd /opt/base2/pkg && curl -O http://swupdate.openvpn.org/as/openvpn-as-2.5-Ubuntu16.amd_64.deb


# Use baseimage-docker's init system
CMD ["/sbin/my_init"]

###############################################
##   INTALL ENVIORMENT, INSTALL OPENVPN      ##
###############################################
COPY install.sh /tmp/
RUN chmod +x /tmp/install.sh && sleep 1 && /tmp/install.sh && rm /tmp/install.sh


###############################################
##             PORTS AND VOLUMES             ##
###############################################

#expose 9443/tcp
#expose 443/tcp
#expose 943/tcp
#expose 1194/udp
VOLUME /config
