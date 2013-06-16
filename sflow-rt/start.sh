#!/bin/sh

HOME=`dirname $0`
cd $HOME

JAR="./lib/sflowrt.jar"
JVM_OPTS=""

exec java ${JVM_OPTS} -jar ${JAR}

