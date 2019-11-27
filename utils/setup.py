

##NOTE: You may need a session with at least 8GB memory to install requirements 

cd
!cp /home/cdsw/utils/cdsw-build.sh .
!chmod 755 /home/cdsw/cdsw-build.sh
!bash /home/cdsw/cdsw-build.sh
!Rscript /home/cdsw/utils/install.R

from distutils.core import setup
setup(name='cdsw_await_workers',
      version='1.0',
      py_modules=['cdsw_await_workers']
      )
