FROM ubuntu:trusty
ADD . /opt/crawler
WORKDIR /
RUN sudo apt-get update
RUN sudo apt-get install software-properties-common wget debconf-utils -y
RUN bash /opt/crawler/tools/install_python.sh
RUN bash /opt/crawler/tools/install_circus.sh
RUN bash /opt/crawler/tools/install_pip.sh
RUN bash /opt/crawler/tools/install_zeromq.sh
RUN bash /opt/crawler/tools/install_tor.sh
RUN bash /opt/crawler/tools/install_packages_docker.sh
RUN bash /opt/crawler/tools/install_mysql-5.6_docker.sh
EXPOSE 3306
EXPOSE 8050
CMD ["bash", "/opt/crawler/HIVE_docker.sh"]