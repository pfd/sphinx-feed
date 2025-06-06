SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

FEEDGEN       = python ../generate_feeds.py

.PHONY: help clean html

html:
	@echo "🔄 Generating feeds..."
	@$(FEEDGEN)
	@echo "🔧 Building HTML with Sphinx..."
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

clean:
	rm -rf $(BUILDDIR)

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)