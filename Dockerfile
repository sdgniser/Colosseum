FROM archlinux:latest

RUN pacman -Sy && pacman -S --noconfirm openssh vim python python-pip kitty-terminfo

RUN ssh-keygen -A && \
    #echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config

RUN echo "test" | passwd --stdin root
RUN useradd colosseum -m
COPY *.py /home/colosseum/
COPY docs /home/colosseum/docs
RUN chmod 111 /home/colosseum/*.py
RUN chmod 777 /home/colosseum/player*.py


EXPOSE 22
#CMD ["/usr/bin/sshd", "-D"]
CMD ["sh", "-c", "echo colosseum:${COLOSSEUM_PASSWORD:-default_password} | chpasswd && /usr/bin/sshd -D"]
