#!/usr/bin/env python3

from presenter import Presenter

import gettext
import locale
from pathlib import Path


if __name__ == '__main__':
    mytextdomain = 'CheatShDesktop'
    locale.setlocale(locale.LC_ALL, '')
    # The i18n files should be copied to ./locale/LANGUAGE_CODE/LC_MESSAGES/
    LOCALE_DIR = Path(__file__).parent / "locale"
    locale.bindtextdomain(mytextdomain, LOCALE_DIR)
    gettext.bindtextdomain(mytextdomain, LOCALE_DIR)
    gettext.textdomain(mytextdomain)

    presenter = Presenter()
    presenter.run()
