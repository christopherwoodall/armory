From: poetry-cover
SHELL                           := $(shell which bash) -e
POETRY_BIN                      ?= $(shell which poetry)
PYTHON_BIN                      ?= $(shell /usr/bin/env python)

MAKEFILE_PATH                   := $(abspath $(lastword $(MAKEFILE_LIST)))
ROOT_DIR                        := $(patsubst %/,%,$(dir $(MAKEFILE_PATH)))

VENDOR_SRC                      := $(ROOT_DIR)/vendors
VENDOR_DIR                      := $(ROOT_DIR)/src/poetry/core/_vendor
VENDOR_TXT                      := $(VENDOR_DIR)/vendor.txt

# set markdown input format to "markdown-smart" for pandoc version 2 and to "markdown" for pandoc prior to version 2
MARKDOWN = $(shell if [ `pandoc -v | head -n1 | cut -d" " -f2 | head -c1` = "2" ]; then echo markdown-smart; else echo markdown; fi)


.PHONY: all clean install test build bash-completion ot offlinetest codetest

clean:
	rm -rf youtube-dl.1.temp.md youtube-dl.1 youtube-dl.bash-completion README.txt MANIFEST build/ dist/ .coverage cover/ youtube-dl.tar.gz youtube-dl.zsh youtube-dl.fish youtube_dl/extractor/lazy_extractors.py *.dump *.part* *.ytdl *.info.json *.mp4 *.m4a *.flv *.mp3 *.avi *.mkv *.webm *.3gp *.wav *.ape *.swf *.jpg *.png CONTRIBUTING.md.tmp youtube-dl youtube-dl.exe
	find . -name "*.pyc" -delete
	find . -name "*.class" -delete


.PHONY: vendor/lock
vendor/lock: $(VENDOR_LOCK)
	# regenerate lock file
	@pushd $(VENDOR_SRC) && $(POETRY_BIN) lock --no-update

.PHONY: vendor/sync
vendor/sync:
	# regenerate vendor.txt file (exported from lockfile)
	@pushd $(VENDOR_SRC) && $(POETRY_BIN) export --without-hashes 2> /dev/null \
			| egrep -v "(importlib|zipp)" \
			| sort > $(VENDOR_TXT)

	# vendor packages
	@vendoring sync

	# strip out *.pyi stubs
	@find "$(VENDOR_DIR)" -type f -name "*.pyi" -exec rm {} \;

.PHONY: vendor/update
vendor/update: | vendor/lock vendor/sync
	@:



# From youtube-dl: https://github.com/ytdl-org/youtube-dl/blob/master/Makefile

install: youtube-dl youtube-dl.1 youtube-dl.bash-completion youtube-dl.zsh youtube-dl.fish
	install -d $(DESTDIR)$(BINDIR)
	install -m 755 youtube-dl $(DESTDIR)$(BINDIR)
	install -d $(DESTDIR)$(MANDIR)/man1
	install -m 644 youtube-dl.1 $(DESTDIR)$(MANDIR)/man1
	install -d $(DESTDIR)$(SYSCONFDIR)/bash_completion.d
	install -m 644 youtube-dl.bash-completion $(DESTDIR)$(SYSCONFDIR)/bash_completion.d/youtube-dl
	install -d $(DESTDIR)$(SHAREDIR)/zsh/site-functions
	install -m 644 youtube-dl.zsh $(DESTDIR)$(SHAREDIR)/zsh/site-functions/_youtube-dl
	install -d $(DESTDIR)$(SYSCONFDIR)/fish/completions
	install -m 644 youtube-dl.fish $(DESTDIR)$(SYSCONFDIR)/fish/completions/youtube-dl.fish

codetest:
	flake8 .

test:
	#nosetests --with-coverage --cover-package=youtube_dl --cover-html --verbose --processes 4 test
	nosetests --verbose test
	$(MAKE) codetest

ot: offlinetest

# Keep this list in sync with devscripts/run_tests.sh
offlinetest: codetest
	$(PYTHON) -m nose --verbose test \
		--exclude test_age_restriction.py \
		--exclude test_download.py \
		--exclude test_iqiyi_sdk_interpreter.py \
		--exclude test_socks.py \
		--exclude test_subtitles.py \
		--exclude test_write_annotations.py \
		--exclude test_youtube_lists.py \
		--exclude test_youtube_signature.py


README.txt: README.md
	pandoc -f $(MARKDOWN) -t plain README.md -o README.txt


youtube-dl: youtube_dl/*.py youtube_dl/*/*.py
	mkdir -p zip
	for d in youtube_dl youtube_dl/downloader youtube_dl/extractor youtube_dl/postprocessor ; do \
	  mkdir -p zip/$$d ;\
	  cp -pPR $$d/*.py zip/$$d/ ;\
	done
	touch -t 200001010101 zip/youtube_dl/*.py zip/youtube_dl/*/*.py
	mv zip/youtube_dl/__main__.py zip/
	cd zip ; zip -q ../youtube-dl youtube_dl/*.py youtube_dl/*/*.py __main__.py
	rm -rf zip
	echo '#!$(PYTHON)' > youtube-dl
	cat youtube-dl.zip >> youtube-dl
	rm youtube-dl.zip
	chmod a+x youtube-dl


