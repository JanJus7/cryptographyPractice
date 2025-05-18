#!/bin/bash

OUTPUT="hash.txt"

md5sum personal.txt >> $OUTPUT
sha1sum personal.txt >> $OUTPUT
sha224sum personal.txt >> $OUTPUT
sha256sum personal.txt >> $OUTPUT
sha384sum personal.txt >> $OUTPUT
sha512sum personal.txt >> $OUTPUT
b2sum personal.txt >> $OUTPUT

cat hash-.pdf personal.txt | md5sum >> $OUTPUT
cat hash-.pdf personal.txt | sha1sum >> $OUTPUT
cat hash-.pdf personal.txt | sha224sum >> $OUTPUT
cat hash-.pdf personal.txt | sha256sum >> $OUTPUT
cat hash-.pdf personal.txt | sha384sum >> $OUTPUT
cat hash-.pdf personal.txt | sha512sum >> $OUTPUT
cat hash-.pdf personal.txt | b2sum >> $OUTPUT

cat hash-.pdf personal_.txt | md5sum >> $OUTPUT
cat hash-.pdf personal_.txt | sha1sum >> $OUTPUT
cat hash-.pdf personal_.txt | sha224sum >> $OUTPUT
cat hash-.pdf personal_.txt | sha256sum >> $OUTPUT
cat hash-.pdf personal_.txt | sha384sum >> $OUTPUT
cat hash-.pdf personal_.txt | sha512sum >> $OUTPUT
cat hash-.pdf personal_.txt | b2sum >> $OUTPUT
