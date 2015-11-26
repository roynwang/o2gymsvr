kill -9 $(cat run.pid) 
nohup uwsgi --ini o2fit_uwsgi.ini & echo $! > run.pid
