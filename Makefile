.PHONY: install deinstall refresh

install:
	$(MAKE) -C docs html $(MAKEFLAGS)
	$(MAKE) -C docs install $(MAKEFLAGS)

deinstall:
	$(MAKE) -C docs clean $(MAKEFLAGS)

refresh:
	$(MAKE) -C docs clean $(MAKEFLAGS)
	$(MAKE) -C docs html $(MAKEFLAGS)
