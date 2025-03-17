.PHONY: install deinstall refresh

install:
	$(MAKE) -C sphinx html $(MAKEFLAGS)
	$(MAKE) -C sphinx install $(MAKEFLAGS)

deinstall:
	$(MAKE) -C sphinx clean $(MAKEFLAGS)

refresh:
	$(MAKE) -C sphinx clean $(MAKEFLAGS)
	$(MAKE) -C sphinx html $(MAKEFLAGS)
