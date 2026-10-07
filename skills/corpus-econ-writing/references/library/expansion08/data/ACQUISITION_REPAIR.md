# Acquisition Receipt Repair

The first sandboxed attempt could not resolve hosts and obtained no files. A
permitted network attempt through the old shared downloader obtained public PDFs
but failed while building receipts: that helper requires an `index` field even
when a direct primary-source PDF URL is supplied. It had already written bytes.

The new edition's downloader does not overwrite these files or invent acquisition
receipts. It redownloads the configured public URLs, requires exact byte hashes
for unrecorded files, and records the verification time and recovered-receipt
status. Any differing download stops. Existing earlier editions are unchanged.
