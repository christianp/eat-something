LESSC=lessc
LESS_DIR=recipes/static/less
CSS_DIR=recipes/static/css

CSS_FILENAMES = base meal random_meal index
CSS_FILES = $(foreach css,$(CSS_FILENAMES),$(CSS_DIR)/$(css).css)

$(CSS_DIR)/%.css: $(LESS_DIR)/%.less
	$(LESSC) $? > $@

default: $(CSS_FILES)

clean:
	rm $(CSS_DIR)/*.css

watch:
	ls -d recipes/static/less/* | entr make
