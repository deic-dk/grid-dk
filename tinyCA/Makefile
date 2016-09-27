# (c) Original: http://sial.org/howto/openssl/ca/
# (c) changes and extensions:
#     03/2009 Jost Berthold, grid.dk
#
# NOTE If running OpenSSL 0.9.8a or higher, see -newkey, below.
#
# Automates the setup of a custom Certificate Authority and provides
# routines for signing and revocation of certificates. To use, first
# customize the commands in this file and the settings in openssl.cnf,
# then run:
#
# make init
#
# Then, copy in certificate signing requests, and ensure their suffix is
# .csr before signing them with the following command:
#
# make sign
#
# To revoke a key, name the certificate file with the cert option
# as shown below:
#
# make revoke cert=foo.cert
#
# This will revoke the certificate and call gencrl; the revocation list
# will then need to be copied somehow to the various systems that use
# your CA cert.


# configuration resides in this file, added everywhere
CONFIG=custom.cnf

# items to put in the distinguished name (DN)
# in general:
SUBJECTSTRING=/C=DK/ST=Denmark/O=GRIDDK
# for the CA, we will add this:
CASUBJECT="$(SUBJECTSTRING)/CN=amazonARC-ca"

# File suffix we expect and generate.
keysuffix=key
certsuffix=cert
reqsuffix=certreq
# For certificate requests, signing happens in
# the main directory, so files will need to be copied here anyway.
requests = *.${reqsuffix}

##############################################
######                                  ######
###### items for configuration end here ######
######                                  ######
##############################################


ifeq ($(strip $(HOST)),)
  # (bash-centric) find out where we live
  HOST=`hostname`.`dnsdomainname` 
endif
#for the host certificate, we will add this:
HOSTSUBJECT="$(SUBJECTSTRING)/CN=$(HOST)"

CONFIGFLAG=-config $(CONFIG)

# to be set when generating user certificates 
# use like this: #>make usercert NAME="John Doe" FILE=filename
ifeq ($(strip $(NAME)),)
  CN=/CN=unknown
  FILE=unknown
else
  CN=/CN=$(NAME)
  ifeq ($(strip $(FILE)),)
# weird make hack
    EMPTY:=
    SPACE:=$(EMPTY) $(EMPTY)
    FILE=$(subst $(SPACE),_,$(NAME))
  endif
endif

default: help

sign: ${requests} serial

# remove -batch option if want chance to not certify a particular request
${requests}: FORCE
	@openssl ca -batch $(CONFIGFLAG) -in $@ -out ${@:.certreq=.${certsuffix}}
	@[ -f ${@:.certreq=.${certsuffix}} ] && rm $@

revoke: serial
	@test $${cert:?"usage: make revoke cert=certificate"}
	@openssl ca $(CONFIGFLAG) -revoke $(cert)
	@$(MAKE) gencrl

gencrl:
	@openssl ca $(CONFIGFLAG) -gencrl -out ca-crl.pem

clean:
	@rm ${requests} *.${keysuffix} *.${certsuffix} *.p12 -f

init: serial

# creates required supporting files, CA key and certificate
init_: config
	@test ! -f serial #|| echo "Already initialised, clean first!";exit 1	 
	@mkdir crl newcerts private 
	@chmod go-rwx private
	@echo '01' > serial
	@touch index
# NOTE use "-newkey rsa:2048" if running OpenSSL 0.9.8a or higher
	@openssl req -nodes $(CONFIGFLAG) -days 1825 -x509 -subj $(CASUBJECT) -newkey rsa:2048 -out ca-cert.pem -outform PEM
# and now, we hash the certificate to deploy it into /etc/grid-security
	@cp ca-cert.pem `openssl x509 -hash -noout -in ca-cert.pem`.0

wipe:	
	@test -f serial || (echo "Nothing to wipe";exit 1)
	@echo "Wiping the whole CA, are you sure? (press return or ^C)"
	@read INPUT
	@make clean
	@rm -Rf crl newcerts private serial* index* ca-cert.pem *.0 $(CONFIG)

hostcert: serial
	@openssl req $(CONFIGFLAG) -newkey 2048:rsa -keyout host.${keysuffix} -out host.certreq  -subj $(HOSTSUBJECT) 
	@make sign
	 # and decrypt the key (remove password)
	@mv host.$(keysuffix) host.tmp
	@openssl rsa -in host.tmp -out host.${keysuffix} -passin pass:amazonARC
	@rm host.tmp

usercert: serial
	openssl req $(CONFIGFLAG) -newkey 2048:rsa -keyout $(FILE).${keysuffix} \
        -out $(FILE).certreq  -subj "$(SUBJECTSTRING)$(CN)" -text
	@make sign
	@mv $(FILE).$(keysuffix) $(FILE).tmp
	@openssl rsa -in $(FILE).tmp -out $(FILE).${keysuffix} -passin pass:amazonARC
	@rm $(FILE).tmp
	 # and make a p12 bundle from it...
	@openssl pkcs12 -export -in $(FILE).$(certsuffix) -inkey $(FILE).$(keysuffix) -out $(FILE).p12 -password pass:


help:
	@echo make sign
	@echo '  - signs all *.certreq files in this directory'
	@echo make hostcert
	@echo '  - generates and signs a host certificate for the current host'
	@echo '    The hostname can be set by variable HOST:'
	@echo '    #>make hostcert HOST=shiny-new.host.dk'
	@echo make usercert
	@echo '  - generates and signs a user certificate request, using'
	@echo '    the NAME variable content as the Common Name.'
	@echo '    FILE variable gives the basename for the file to save in.'
	@echo '    Use it like this:'
	@echo '    #>make request NAME="John Doe" FILE=filename'
	@echo make revoke cert=filename
	@echo '  - revokes certificate in named file and calls gencrl'
	@echo make gencrl
	@echo '  - updates Certificate Revocation List (CRL)'
	@echo make clean
	@echo '  - removes *.${reqsuffix}, *.${certsuffix} and *.${keysuffix} files in this directory'
	@echo make init
	@echo '  - required initial setup command for new CA'
	@echo make wipe
	@echo '  - removes the entire thing (after asking you)'


config:	$(CONFIG)

$(CONFIG): $(CONFIG).in
#	cpp -traditional -D__CAHOME_REPLACE__=`pwd` $(CONFIG).in > $(CONFIG)
	@echo Generating $(CONFIG) file
	@sed -e s%__CAHOME_REPLACE__%`pwd`%g $(CONFIG).in > $(CONFIG)

# dummy target to ensure init
serial:	
	make init_

# for legacy make support
FORCE:
