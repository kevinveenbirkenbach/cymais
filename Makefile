.PHONY: install deinstall refresh

install:
	$(MAKE) -C sphinx html
	$(MAKE) -C sphinx install

deinstall:
	$(MAKE) -C sphinx clean

refresh:
	$(MAKE) -C sphinx clean
	$(MAKE) -C sphinx html
