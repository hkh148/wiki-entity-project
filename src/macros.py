import string
# some macros
USER_NAME = "root"
PASSWORD = "203761333"
DB_NAME = "wiki-project-db"

SQL_FILE = "hewiki-20180201-page.sql"
XML_FILE = "hewiki-20180201-pages-articles.xml"

TITLE_TAG = "{http://www.mediawiki.org/xml/export-0.10/}title"
TEXT_TAG = "{http://www.mediawiki.org/xml/export-0.10/}text"

BASE_URL = 'https://he.wikipedia.org/wiki/'

PUNCTUATION = set(string.punctuation)
PUNCTUATION.remove("'")

ABBREVIATIONS = {"ר'":"רבי","דר'":"דרבי","ור'":"ורבי"}

ENGINE_URL = "mysql+mysqlconnector://" + USER_NAME + ":" + PASSWORD + "@127.0.0.1:3306/" + DB_NAME

#stam comment

