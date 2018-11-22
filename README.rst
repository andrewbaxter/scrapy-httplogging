Logs http requests and responses.  Make sure LOG_LEVEL is set to DEBUG.

Installation
############

Run::

   pip install git+https://github.com/andrewbaxter/scrapy-httplogging

Add this to ``settings.py``::

   EXTENSIONS = {
       'httplogging.HttpLogging': 100
   }

To disable colors and box lines, also add this::

    HTTPLOGGING_NOCOLORS = True
