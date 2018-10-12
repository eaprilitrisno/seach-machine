d=2018-09-01
end=2018-10-11
while [ "$d" != $end ]; do 
  echo $(date -d "$d" +%Y%m%d)
  python read_data_omega.py price $(date -d "$d" +%Y%m%d)
  python read_data_omega.py stock $(date -d "$d" +%Y%m%d)
  d=$(date -I -d "$d + 1 day")
done
