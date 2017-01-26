# Mac에서 Apache와 Tomcat 연동하기
mac환경에서 apache와 tomcat을 연동하고자 한다.

Apache를 별도로 설치하고자 했지만 Mac에는 이미 포함되어 있다.
> #### 세팅 환경
> MacOS Sierra 10.12
> 
> ```apachectl -v``` 명령어로 버전확인
> Apache 2.4.23
> Tomcat 8.5.11

**localhost:8080** 처럼 직접적으로 Tomcat을 띄우고 8080포트에 접근해서 웹을 개발해봤는데 특정 도메인을 local로 인식하도록 한 후 tomcat connector로 연동하는 작업을 해보자.

먼저 test.com 이라는 도메인을 127.0.0.1로 인식하도록 작업해보자

1) Apache Reverse Proxy 설정
**/etc/hosts 수정**
sudo vim /etc/hosts

```shell
##
# Host Database
#
# localhost is used to configure the loopback interface
# when the system is booting.  Do not change this entry.
##
127.0.0.1       localhost
127.0.0.1       test.com
255.255.255.255 broadcasthost
::1             localhost
```

```localhost:8080``` = ```test.com:8080```


2) tomcat connector(mod_jk) 빌드
http://tomcat.apache.org/download-connectors.cgi 에서 다운
빌드하여 mod_jk.so 파일을 받아야함

> 빌드과정
> 
> 1) 위 URL에서 소스를 받은 후 tar xvfz 로 압축해제
> 2) cd /:압축 푼 경로/native
> 3) ./configure --with-apxs=/home/kyu/apache2/bin/apxs
> 4) make
> 5) make install

3) httpd.conf
```LoadModule jk_module /etc/apache2/other/mod_jk.so```
추가

```
# Virtual hosts
Include /private/etc/apache2/extra/httpd-vhosts.conf
```
Include 부분 주석해제

```
<IfModule mod_jk.c>
   JkMount /jkmanager/* jkstatus
   JkLogFile "/var/log/apache2/mod_jk.log"
   JkWorkersFile "/etc/apache2/workers.properties"
   JkShmFile "/var/log/apache2/mod_jk.shm"
</IfModule>
```

4) workers.properties 생성
/etc/apache2/ 에 workers.properties 파일을 생성

```
worker.list=tomcat

worker.tomcat.type=ajp13
worker.tomcat.port=8009
worker.tomcat.socket_timeout=10
worker.tomcat.connection_pool_timeout=10
```

> Syntax Error Check
> ```sudo apachectl -t```

5) /etc/apache2/extra/httpd-vhost.conf 수정
```sudo vi /etc/apache2/extra/httpd-vhost.conf```

```
<VirtualHost *>
    ServerAdmin webmaster@dummy-host.example.com

    DocumentRoot "/Users/Naver/Desktop/07-NaIssueT/deploy"
    <Directory "/Users/Naver/Desktop/07-NaIssueT/deploy">
       Options FollowSymLinks
       AllowOverride None
       Order deny,allow
       Allow from all
       Require all granted
    </Directory>

    JkMount /* tomcat
    JkUnMount /resources/* tomcat
    ServerName localhost
    ServerAlias www.dummy-host.example.com
    ErrorLog "/private/var/log/apache2/dummy-host.example.com-error_log"
    CustomLog "/private/var/log/apache2/dummy-host.example.com-access_log" common
</VirtualHost>
```

### JkMount / JkUnMount 
HTML, CSS, IMAGE 등의 정적 리소스 파일들을 Apache에서 처리하기 위해 UnMount시킴
