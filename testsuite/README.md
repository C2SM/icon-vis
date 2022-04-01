# testsuite

**Description**

This folder contains files for testing if all provided scripts are running. Three different config files are tested together with two differnt netcdf files. This test is done automatically once a week and an email is sent to _annika.lauber@c2sm.ethz.ch_ in case a test fails. You can run the tests yourself from the main folder (make sure all requirements are installed first):

    pytest testsuite/test*

It is also possible to just test single scripts like mapplot.py by running

    pytest testsuite/test_mapplot.py
