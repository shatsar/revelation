#
# Revelation 0.3.3 - a password manager for GNOME 2
# http://oss.codepoet.no/revelation/
# $Id$
#
# Module containing entry information
#
#
# Copyright (c) 2003-2004 Erik Grinaker
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#

from revelation import stock

import copy, time


DATATYPE_FILE		= "file"
DATATYPE_EMAIL		= "email"
DATATYPE_PASSWORD	= "password"
DATATYPE_STRING		= "string"
DATATYPE_URL		= "url"



class EntryFieldError(Exception):
	"Exception for invalid entry fields"
	pass


class EntryTypeError(Exception):
	"Exception for invalid entry types"
	pass



class Entry(object):
	"An entry object"

	id		= None
	typename	= ""
	icon		= None

	def __init__(self):
		self.name		= ""
		self.description	= ""
		self.updated		= int(time.time())
		self.fields		= []


	def __getitem__(self, key):
		return self.get_field(key).value


	def __setitem__(self, key, value):
		self.get_field(key).value = value


	def copy(self):
		"Create a copy of the entry"

		return copy.deepcopy(self)


	def get_field(self, fieldtype):
		"Get one of the entrys fields"

		for field in self.fields:
			if type(field) == fieldtype:
				return field

		else:
			raise EntryFieldError


	def has_field(self, fieldtype):
		"Check if the entry has a field"

		try:
			self.get_field(fieldtype)
			return True

		except EntryFieldError:
			return False


	def mirror(self, entry):
		"Makes this entry mirror a different entry (same data)"

		if type(self) != type(entry):
			raise EntryTypeError

		self.name		= entry.name
		self.description	= entry.description
		self.updated		= entry.updated

		for field in entry.fields:
			self[type(field)] = field.value



class FolderEntry(Entry):

	id		= "folder"
	typename	= "Folder"
	icon		= stock.STOCK_ENTRY_FOLDER

	def __init__(self):
		Entry.__init__(self)



class CreditcardEntry(Entry):

	id		= "creditcard"
	typename	= "Creditcard"
	icon		= stock.STOCK_ENTRY_CREDITCARD

	def __init__(self):
		Entry.__init__(self)

		self.fields = [
			CardtypeField(),
			CardnumberField(),
			ExpirydateField(),
			CCVField(),
			PINField()
		]



class CryptoKeyEntry(Entry):

	id		= "cryptokey"
	typename	= "Crypto Key"
	icon		= stock.STOCK_ENTRY_CRYPTOKEY

	def __init__(self):
		Entry.__init__(self)

		self.fields = [
			HostnameField(),
			CertificateField(),
			KeyfileField(),
			PasswordField()
		]



class DatabaseEntry(Entry):

	id		= "database"
	typename	= "Database"
	icon		= stock.STOCK_ENTRY_DATABASE

	def __init__(self):
		Entry.__init__(self)

		self.fields = [
			HostnameField(),
			UsernameField(),
			PasswordField(),
			DatabaseField()
		]



class DoorEntry(Entry):

	id		= "door"
	typename	= "Door lock"
	icon		= stock.STOCK_ENTRY_DOOR

	def __init__(self):
		Entry.__init__(self)

		self.fields = [
			LocationField(),
			CodeField()
		]



class EmailEntry(Entry):

	id		= "email"
	typename	= "Email"
	icon		= stock.STOCK_ENTRY_EMAIL

	def __init__(self):
		Entry.__init__(self)

		self.fields = [
			EmailField(),
			HostnameField(),
			UsernameField(),
			PasswordField()
		]



class FTPEntry(Entry):

	id		= "ftp"
	typename	= "FTP"
	icon		= stock.STOCK_ENTRY_FTP

	def __init__(self):
		Entry.__init__(self)

		self.fields = [
			HostnameField(),
			PortField(),
			UsernameField(),
			PasswordField()
		]



class GenericEntry(Entry):

	id		= "generic"
	typename	= "Generic"
	icon		= stock.STOCK_ENTRY_GENERIC

	def __init__(self):
		Entry.__init__(self)

		self.fields = [
			HostnameField(),
			UsernameField(),
			PasswordField()
		]



class PhoneEntry(Entry):

	id		= "phone"
	typename	= "Phone"
	icon		= stock.STOCK_ENTRY_PHONE

	def __init__(self):
		Entry.__init__(self)

		self.fields = [
			PhonenumberField(),
			PINField()
		]



class ShellEntry(Entry):

	id		= "shell"
	typename	= "Shell"
	icon		= stock.STOCK_ENTRY_SHELL

	def __init__(self):
		Entry.__init__(self)

		self.fields = [
			HostnameField(),
			DomainField(),
			UsernameField(),
			PasswordField()
		]



class WebEntry(Entry):

	id		= "website"
	typename	= "Website"
	icon		= stock.STOCK_ENTRY_WEBSITE

	def __init__(self):
		Entry.__init__(self)

		self.fields = [
			URLField(),
			UsernameField(),
			PasswordField()
		]



ENTRYLIST = [
	FolderEntry,
	CreditcardEntry,
	CryptoKeyEntry,
	DatabaseEntry,
	DoorEntry,
	EmailEntry,
	FTPEntry,
	GenericEntry,
	PhoneEntry,
	ShellEntry,
	WebEntry
]



class Field(object):
	"An entry field object"

	id		= None
	name		= ""
	description	= ""
	symbol		= None

	datatype	= None
	value		= None

	def __init__(self, value = ""):
		self.value = value


	def __str__(self):
		return self.value is not None and self.value or ""



class CardnumberField(Field):

	id		= "creditcard-cardnumber"
	name		= "Card number"
	description	= "The number of a creditcard, usually a 16-digit number"
	symbol		= "N"
	datatype	= DATATYPE_STRING



class CardtypeField(Field):

	id		= "creditcard-cardtype"
	name		= "Card type"
	description	= "The type of creditcard, like MasterCard or VISA"
	symbol		= "C"
	datatype	= DATATYPE_STRING



class CCVField(Field):

	id		= "creditcard-ccv"
	name		= "CCV number"
	description	= "A Credit Card Verification number, normally a 3-digit code found on the back of a card"
	symbol		= "V"
	datatype	= DATATYPE_STRING



class CertificateField(Field):

	id		= "generic-certificate"
	name		= "Certificate"
	description	= "A certificate, such as an X.509 SSL Certificate"
	symbol		= "x"
	datatype	= DATATYPE_FILE



class CodeField(Field):

	id		= "generic-code"
	name		= "Code"
	description	= "A code used to provide access to something"
	symbol		= "c"
	datatype	= DATATYPE_PASSWORD



class DatabaseField(Field):

	id		= "generic-database"
	name		= "Database"
	description	= "A database name"
	symbol		= "D"
	datatype	= DATATYPE_STRING



class DomainField(Field):

	id		= "generic-domain"
	name		= "Domain"
	description	= "An Internet or logon domain, like amazon.com or a Windows logon domain"
	symbol		= "d"
	datatype	= DATATYPE_STRING



class EmailField(Field):

	id		= "generic-email"
	name		= "Email"
	description	= "An email address"
	symbol		= "e"
	datatype	= DATATYPE_EMAIL



class ExpirydateField(Field):

	id		= "creditcard-expirydate"
	name		= "Expiry date"
	description	= "The month that the credit card validity expires"
	symbol		= "E"
	datatype	= DATATYPE_STRING



class HostnameField(Field):

	id		= "generic-hostname"
	name		= "Hostname"
	description	= "The name of a computer, like computer.domain.com or MYCOMPUTER"
	symbol		= "h"
	datatype	= DATATYPE_STRING



class KeyfileField(Field):

	id		= "generic-keyfile"
	name		= "Key File"
	description	= "A key file, used for authentication for example via ssh or to encrypt X.509 certificates"
	symbol		= "f"
	datatype	= DATATYPE_FILE



class LocationField(Field):

	id		= "generic-location"
	name		= "Location"
	description	= "A physical location, like office entrance"
	symbol		= "L"
	datatype	= DATATYPE_STRING



class PasswordField(Field):

	id		= "generic-password"
	name		= "Password"
	description	= "A secret word or character combination used for proving you have access"
	symbol		= "p"
	datatype	= DATATYPE_PASSWORD



class PhonenumberField(Field):

	id		= "phone-phonenumber"
	name		= "Phone number"
	description	= "A telephone number"
	symbol		= "n"
	datatype	= DATATYPE_STRING



class PINField(Field):

	id		= "generic-pin"
	name		= "PIN"
	description	= "A Personal Identification Number, a numeric code used for credit cards, phones etc"
	symbol		= "P"
	datatype	= DATATYPE_PASSWORD



class PortField(Field):

	id		= "generic-port"
	name		= "Port number"
	description	= "A network port number, used to access network services directly"
	symbol		= "o"
	datatype	= DATATYPE_STRING



class URLField(Field):

	id		= "generic-url"
	name		= "URL"
	description	= "A Uniform Resource Locator, such as a web-site address"
	symbol		= "U"
	datatype	= DATATYPE_URL



class UsernameField(Field):

	id		= "generic-username"
	name		= "Username"
	description	= "A name or other identification used to identify yourself"
	symbol		= "u"
	datatype	= DATATYPE_STRING

