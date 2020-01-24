
#Run this if you are not using a custom docker image
#To build a custom docker image for this project run commands like in build-engine.sh

##NOTE: You need a session with at least 8GB memory to install the python libs

cd
!cp /home/cdsw/utils/cdsw-build.sh .
!chmod 755 /home/cdsw/cdsw-build.sh
!bash /home/cdsw/cdsw-build.sh
!pip3 install -r utils/requirements3.txt
#!Rscript /home/cdsw/utils/install.R
