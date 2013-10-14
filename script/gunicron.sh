#!/bin/bash
set -x 

. /root/djaong15/bin/activate

mkdir -p /data/www/raspberry/run/

USER="nobody"
WORK_DIR="/data/www/raspberry/"
#PYTHON="/usr/bin/python"
PID="/data/www/raspberry/run/gunicorn.pid"
Gunicorn_OPT="-D -w 17 -k sync -u ${USER} -p ${PID} --max-requests=1024 -b 10.0.2.218:10080"

if test -d ${WORK_DIR}; then
	cd ${WORK_DIR};
fi

start_work() {
	python manage.py run_gunicorn ${Gunicorn_OPT}
}

stop_work() {
	cat ${PID} | xargs kill -9
}

reload_work() {
	cat ${PID} | xargs kill -HUP
}

case "$1" in
	start)
		start_work
	;;
	stop)
		stop_work
	;;
	reload)
		reload_work
	;;
	*)
		echo "Usage: gunicorn {start|stop|reload}"
		exit 1;
esac

exit 01;
