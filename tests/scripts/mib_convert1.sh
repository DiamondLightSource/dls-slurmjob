#!/bin/bash
#SBATCH --mem=100G           # total memory per node
#SBATCH --partition=cs05r
#SBATCH --chdir=/dls/e02/data/2021/cm28158-4/processing/Merlin/test_dataset_convert/20230120_131936/mibconvert.2023-06-14.143038.452724/mib_convert

echo '-----------------' >> .bxflow/prepare_environment.txt
echo 'hostname: ' `hostname`>> .bxflow/prepare_environment.txt
echo 'uname: ' `uname -a` >> .bxflow/prepare_environment.txt
echo 'id: ' `id` >> .bxflow/prepare_environment.txt
echo 'date: ' `date +'%Y-%m-%d %H:%M:%S %z'` >> .bxflow/prepare_environment.txt
echo 'pwd: ' `pwd` >> .bxflow/prepare_environment.txt
echo 'MODULEPATH: ' $MODULEPATH >> .bxflow/prepare_environment.txt
echo 'MODULESHOME: ' $MODULESHOME >> .bxflow/prepare_environment.txt
echo '-----------------' >> .bxflow/prepare_environment.txt
# dls_bxflow_run.bx_tasks.module_classname specification prepare_environment:

t1=`date "+%s.%N"`
echo 'export USER=USER' >>.bxflow/prepare_environment.txt
export USER=USER >>.bxflow/prepare_environment.txt 2>&1
rc=$?
t2=`date "+%s.%N"`
echo '-----------------' `echo $t1 $t2 | awk '{printf "%0.3f", $2-$1}'` seconds >> .bxflow/prepare_environment.txt
if [ $rc -ne 0 ]
then
  echo 252 >> .bxflow/exit_code.txt
  >&2 echo error doing: export USER=USER
  >&2 echo see /dls/e02/data/2021/cm28158-4/processing/Merlin/test_dataset_convert/20230120_131936/mibconvert.2023-06-14.143038.452724/mib_convert/.bxflow/prepare_environment.txt
  exit $((252))
fi

t1=`date "+%s.%N"`
echo 'source /etc/profile.d/modules.sh' >>.bxflow/prepare_environment.txt
source /etc/profile.d/modules.sh >>.bxflow/prepare_environment.txt 2>&1
rc=$?
t2=`date "+%s.%N"`
echo '-----------------' `echo $t1 $t2 | awk '{printf "%0.3f", $2-$1}'` seconds >> .bxflow/prepare_environment.txt
if [ $rc -ne 0 ]
then
  echo 252 >> .bxflow/exit_code.txt
  >&2 echo error doing: source /etc/profile.d/modules.sh
  >&2 echo see /dls/e02/data/2021/cm28158-4/processing/Merlin/test_dataset_convert/20230120_131936/mibconvert.2023-06-14.143038.452724/mib_convert/.bxflow/prepare_environment.txt
  exit $((252))
fi

t1=`date "+%s.%N"`
echo 'module load python/epsic3.10' >>.bxflow/prepare_environment.txt
module load python/epsic3.10 >>.bxflow/prepare_environment.txt 2>&1
rc=$?
t2=`date "+%s.%N"`
echo '-----------------' `echo $t1 $t2 | awk '{printf "%0.3f", $2-$1}'` seconds >> .bxflow/prepare_environment.txt
if [ $rc -ne 0 ]
then
  echo 252 >> .bxflow/exit_code.txt
  >&2 echo error doing: module load python/epsic3.10
  >&2 echo see /dls/e02/data/2021/cm28158-4/processing/Merlin/test_dataset_convert/20230120_131936/mibconvert.2023-06-14.143038.452724/mib_convert/.bxflow/prepare_environment.txt
  exit $((252))
fi

t1=`date "+%s.%N"`
echo 'export BXFLOW_PYTHONPATH=/dls_sw/apps/bxflow/taskpath/dls-bxflow-epsic/1.1.3' >>.bxflow/prepare_environment.txt
export BXFLOW_PYTHONPATH=/dls_sw/apps/bxflow/taskpath/dls-bxflow-epsic/1.1.3 >>.bxflow/prepare_environment.txt 2>&1
rc=$?
t2=`date "+%s.%N"`
echo '-----------------' `echo $t1 $t2 | awk '{printf "%0.3f", $2-$1}'` seconds >> .bxflow/prepare_environment.txt
if [ $rc -ne 0 ]
then
  echo 252 >> .bxflow/exit_code.txt
  >&2 echo error doing: export BXFLOW_PYTHONPATH=/dls_sw/apps/bxflow/taskpath/dls-bxflow-epsic/1.1.3
  >&2 echo see /dls/e02/data/2021/cm28158-4/processing/Merlin/test_dataset_convert/20230120_131936/mibconvert.2023-06-14.143038.452724/mib_convert/.bxflow/prepare_environment.txt
  exit $((252))
fi

t1=`date "+%s.%N"`
echo 'export EPSIC_PYTHONPATH=/dls_sw/e02/software' >>.bxflow/prepare_environment.txt
export EPSIC_PYTHONPATH=/dls_sw/e02/software >>.bxflow/prepare_environment.txt 2>&1
rc=$?
t2=`date "+%s.%N"`
echo '-----------------' `echo $t1 $t2 | awk '{printf "%0.3f", $2-$1}'` seconds >> .bxflow/prepare_environment.txt
if [ $rc -ne 0 ]
then
  echo 252 >> .bxflow/exit_code.txt
  >&2 echo error doing: export EPSIC_PYTHONPATH=/dls_sw/e02/software
  >&2 echo see /dls/e02/data/2021/cm28158-4/processing/Merlin/test_dataset_convert/20230120_131936/mibconvert.2023-06-14.143038.452724/mib_convert/.bxflow/prepare_environment.txt
  exit $((252))
fi

t1=`date "+%s.%N"`
echo 'export PYTHONPATH=$EPSIC_PYTHONPATH:$BXFLOW_PYTHONPATH:/dls_sw/e02/software:/dls_sw/apps/bxflow/runtime/dls-bxflow-epsic/1.1.3' >>.bxflow/prepare_environment.txt
export PYTHONPATH=$EPSIC_PYTHONPATH:$BXFLOW_PYTHONPATH:/dls_sw/e02/software:/dls_sw/apps/bxflow/runtime/dls-bxflow-epsic/1.1.3 >>.bxflow/prepare_environment.txt 2>&1
rc=$?
t2=`date "+%s.%N"`
echo '-----------------' `echo $t1 $t2 | awk '{printf "%0.3f", $2-$1}'` seconds >> .bxflow/prepare_environment.txt
if [ $rc -ne 0 ]
then
  echo 252 >> .bxflow/exit_code.txt
  >&2 echo error doing: export PYTHONPATH=$EPSIC_PYTHONPATH:$BXFLOW_PYTHONPATH:/dls_sw/e02/software:/dls_sw/apps/bxflow/runtime/dls-bxflow-epsic/1.1.3
  >&2 echo see /dls/e02/data/2021/cm28158-4/processing/Merlin/test_dataset_convert/20230120_131936/mibconvert.2023-06-14.143038.452724/mib_convert/.bxflow/prepare_environment.txt
  exit $((252))
fi
echo '-----------------' >> .bxflow/prepare_environment.txt
echo 'env:' >> .bxflow/prepare_environment.txt
env | sort >> .bxflow/prepare_environment.txt

t1=`date "+%s.%N"`
echo 'python3 -m dls_bxflow_run.main_isolated' >>.bxflow/prepare_environment.txt
python3 -m dls_bxflow_run.main_isolated
exit_code=$?
t2=`date "+%s.%N"`
echo '-----------------' `echo $t1 $t2 | awk '{printf "%0.3f", $2-$1}'` seconds >> .bxflow/prepare_environment.txt

echo $exit_code > /dls/e02/data/2021/cm28158-4/processing/Merlin/test_dataset_convert/20230120_131936/mibconvert.2023-06-14.143038.452724/mib_convert/.bxflow/exit_code.txt
exit $exit_code
