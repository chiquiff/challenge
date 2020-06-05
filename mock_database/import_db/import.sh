#!/bin/bash
echo "**************************************************"
echo "*                                                *"
echo "*                                                *"
echo "* STARTING DB POPULATION. THIS MIGHT TAKE A BIT  *"
echo "*     (one time only, but needs to happen!)      *"
echo "*                                                *"
echo "*                                                *"
echo "**************************************************"
mysql -uroot -psecret < /test_db/employees.sql
exit_status=$?
if [ $exit_status -eq 0 ]; then
  echo "**************************************************"
  echo "*                                                *"
  echo "*                                                *"
  echo "*        POPULATION ENDED SUCCESFULLY!!          *"
  echo "*     Now you can open a new terminal and run:   *"
  echo "*       curl localhost:8080/employees | jq .     *"
  echo "*                                                *"
  echo "**************************************************"
else
  echo "**************************************************"
  echo "*                                                *"
  echo "*                                                *"
  echo "*          SOMETHING WENT WRONG!! =( =(          *"
  echo "*        I'd rather open a hotdogs place..       *"
  echo "*                                                *"
  echo "*                                                *"
  echo "**************************************************"
fi
