#/bin/bash
echo '-----------------' >> .bxflow/prepare_environment.txt
echo 'hostname: ' `hostname`>> .bxflow/prepare_environment.txt
echo 'uname: ' `uname -a` >> .bxflow/prepare_environment.txt
echo 'id: ' `id` >> .bxflow/prepare_environment.txt
echo 'date: ' `date +'%Y-%m-%d %H:%M:%S %z'` >> .bxflow/prepare_environment.txt
echo 'pwd: ' `pwd` >> .bxflow/prepare_environment.txt
echo '-----------------' >> .bxflow/prepare_environment.txt
# dls_bxflow_run.bx_tasks.jupyter specification prepare_environment:

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
  >&2 echo see /home/kbp43231/22/dls-bxflow-exemplar-workflows/nodata.bxflows/hello.007794/hello/.bxflow/prepare_environment.txt
  exit $((252))
fi

t1=`date "+%s.%N"`
echo 'export PYTHONPATH=/dls_sw/apps/bxflow/runtime/dls-bxflow-epsic/edge:PYTHONPATH' >>.bxflow/prepare_environment.txt
export PYTHONPATH=/dls_sw/apps/bxflow/runtime/dls-bxflow-epsic/edge:PYTHONPATH >>.bxflow/prepare_environment.txt 2>&1
rc=$?
t2=`date "+%s.%N"`
echo '-----------------' `echo $t1 $t2 | awk '{printf "%0.3f", $2-$1}'` seconds >> .bxflow/prepare_environment.txt
if [ $rc -ne 0 ]
then
  echo 252 >> .bxflow/exit_code.txt
  >&2 echo error doing: export PYTHONPATH=/dls_sw/apps/bxflow/runtime/dls-bxflow-epsic/edge:PYTHONPATH
  >&2 echo see /home/kbp43231/22/dls-bxflow-exemplar-workflows/nodata.bxflows/hello.007794/hello/.bxflow/prepare_environment.txt
  exit $((252))
fi

t1=`date "+%s.%N"`
echo 'export PYTHONPATH=/dls_sw/e02/software:PYTHONPATH' >>.bxflow/prepare_environment.txt
export PYTHONPATH=/dls_sw/e02/software:PYTHONPATH >>.bxflow/prepare_environment.txt 2>&1
rc=$?
t2=`date "+%s.%N"`
echo '-----------------' `echo $t1 $t2 | awk '{printf "%0.3f", $2-$1}'` seconds >> .bxflow/prepare_environment.txt
if [ $rc -ne 0 ]
then
  echo 252 >> .bxflow/exit_code.txt
  >&2 echo error doing: export PYTHONPATH=/dls_sw/e02/software:PYTHONPATH
  >&2 echo see /home/kbp43231/22/dls-bxflow-exemplar-workflows/nodata.bxflows/hello.007794/hello/.bxflow/prepare_environment.txt
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

echo $exit_code > /home/kbp43231/22/dls-bxflow-exemplar-workflows/nodata.bxflows/hello.007794/hello/.bxflow/exit_code.txt
exit $exit_code
