# THIS MAKFILE IS GENERATED

PACKAGES = bgpflowspec

NETWORK = 

.PHONY: netsim netsim-clean netsim-start netsim-stop
netsim:

netsim-clean:

netsim-start:

netsim-stop:

.PHONY: packages packages-clean
packages:
	(for i in $(PACKAGES); do \
	        $(MAKE) -C packages/$${i}/src all || exit 1; \
	done)

packages-clean:
	(for i in $(PACKAGES); do \
	        $(MAKE) -C packages/$${i}/src clean || exit 1; \
	done)

