#!/bin/bash
#
# Mega service init script
#
#
#
#Xchliu
#2014-06-20
###END

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
NAME=mega
DESC='Mega service '
#APP_DIR='/export/servers/script/mega-master/src/'
APP_DIR='..'

MAIN_PWD=$APP_DIR/mega_service/daemon.py
LOG_DIR=''
PID_FILE=/var/run/$NAME.pid

function is_alive()
{
	PID=$1
	PSTATE=`ps -p "$PID" -o s=`
	if [ "D" = "$PSTATE" -o "R" = "$PSTATE" -o "S" = "$PSTATE" ]; then
		# Process is alive
		echo 'A'
	else
		# Process is dead
		echo 'D'
	fi
}

function stop_mega()
{
#	if [ -f "${PID_FILE}" ];then
#		PID=`CAT $PID_FILE`
#		if [ 'A' = "`is_alive $PID`" ];then
#			kill -INT $PID
#		fi
#		rm "$PID_FILE"
#	fi
	sudo python $MAIN_PWD stop
#echo "${NAME} stop/waiting."
}

function start_mega()
{
	sudo python $MAIN_PWD start
}
case "$1" in
	start)
		echo -n "Starting $DESC..."
		start_mega
		echo "Done."
		;;
	stop)
		echo -n "Stopping $DESC..."
		stop_mega
		echo "Done."
		;;
	restart)
		echo -n "Restarting $DESC..."
		stop_mega
		sleep 6
		start_mega
		echo "Done."
		;;
	status)
		status_of_proc -p $PID_FILE "$DAEMON" uwsgi && exit 0 || exit $?
		;;
	*)
		echo "Usage: $NAME {start|stop|restart|status}" >&2
		exit 1
		;;
esac

exit 0