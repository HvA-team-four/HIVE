FROM ubuntu:trusty
ADD . /opt/crawler
RUN sudo apt-get update
RUN sudo apt-get install software-properties-common wget debconf-utils -y
RUN bash /opt/crawler/tools/install_python.sh
RUN bash /opt/crawler/tools/install_circus.sh
RUN bash /opt/crawler/tools/install_pip.sh
RUN bash /opt/crawler/tools/install_zeromq.sh
RUN bash /opt/crawler/tools/install_tor.sh
RUN bash /opt/crawler/tools/install_packages_docker.sh
RUN bash /opt/crawler/tools/install_mysql-5.6_docker.sh

CMD ["mysql", "--version"]