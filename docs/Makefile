SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

.PHONY: help clean html

html:
	@echo "🔄 Generating feeds directly into _build/html..."
	@python ../generate_feeds.py
	@echo "🔧 Building HTML with Sphinx..."
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

clean:
	rm -rf $(BUILDDIR)

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)