test:
	@if test -z "$(TESTCASE)"; then \
      echo "TESTCASE is not set"; \
      echo "e.g. make TESTCASE=src/test/testCli.py:Test.test_do_volume_show"; \
      exit 1; \
    fi;
	PYTHONPATH=./src:./python-lib nosetests -s -v -d -l=nose $(TESTCASE)

testall:
#	PYTHONPATH=./src:./python-lib nosetests src/test -v -s -d --with-xcover --cover-package=pddf
	PYTHONPATH=./src:./python-lib nosetests src/test -v -s

clean:
	echo "clean all pyc"
	rm -rf */*/*/*.pyc
	rm -rf */*/*.pyc
	rm -rf */*.pyc
