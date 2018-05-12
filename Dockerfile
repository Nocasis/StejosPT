FROM ubuntu:16.04
RUN apt-get -qq update && apt-get install -qq -y python3
RUN apt-get update && apt-get install -y openssh-server iproute2
RUN mkdir /var/run/sshd
RUN echo 'root:ssh_test' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN echo "The Best" > Sibears

RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

CMD ["/bin/bash", "-l"]

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
