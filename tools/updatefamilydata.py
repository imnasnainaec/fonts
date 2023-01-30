#!/usr/bin/python3
__doc__ = '''Recreate families.json from base files and font manifests'''
__url__ = 'http://github.com/silnrsi/fonts'
__copyright__ = 'Copyright (c) 2023 SIL International (http://www.sil.org)'
__license__ = 'Released under the MIT License (http://opensource.org/licenses/MIT)'
__author__ = 'David Raymond'

import os
from silfont.gfr import gfr_base, gfr_manifest, gfr_family, setpaths
from silfont.core import execute

argspec = [('-l','--log',{'help': 'Log file'}, {'type': 'outfile', 'def': 'updatefamily.log'})]

'''

'''

headers = ['type', 'familyid', 'family', 'fallback', 'version', 'siteurl', 'packageurl', 'source', 'license', 'status', 'defaults/ttf', 'defaults/woff', 'defaults/woff2', 'hosturl', 'filesroot']
fields =          ['familyid', 'family', 'fallback', 'version', 'siteurl', 'packageurl', 'source', 'license', 'status', 'defaults',                                        'hosturl', 'filesroot']

def doit(args):
    logger = args.logger
    (repopath, silpath, otherpath, basespath) = setpaths(logger)
    silfamilies = os.listdir(silpath)
    otherfamilies = os.listdir(otherpath)

    familydata = {}

    for basename in sorted(os.listdir(basespath)):
        (dummy, ext) = os.path.splitext(basename)
        if ext != ".json": continue
        basepath = os.path.join(basespath, basename)
        base = gfr_base(filename=basepath, logger=logger)
        base.read()
        (valid, logs) = base.validate()
        if not valid:
            for logmess in logs:
                logger.log(logmess[0], logmess[1])
            logger.log(f'{basename} invalid so skipped')
            continue
        familyid = base.id
        fdata = {x: base.data[x] for x in base.data}
        logger.log(f'Processing {familyid}', "P")
        if familyid in silfamilies + otherfamilies: # Has folder in the fonts repo so font manifest is required
            if familyid in silfamilies:
                manifestpath = os.path.join(silpath, familyid,"fontmanifest.json")
            else:
                manifestpath = os.path.join(otherpath, familyid, "fontmanifest.json")
            if os.path.isfile(manifestpath):
                manifest = gfr_manifest(filename=manifestpath, logger=logger)
                manifest.read()
                (valid, logs) = manifest.validate()
                if not valid:
                    for logmess in logs:
                        logger.log(logmess[0], logmess[1])
                    logger.log(f'{manifestname} invalid so {familyid} skipped')
                    continue
            else:
                logger.log(f'{manifestname} missing so {familyid} skipped')
                continue
            # Update fdata with data from manifest file
            for field in manifest.data:
                fdata[field] = manifest.data[field]

        # Add to familydata
        familydata[familyid] = fdata

    familyfile = gfr_family(data=familydata)
    familyfile.write(os.path.join(repopath, "fonts", "families.json"))

    return






    # Write the base file out
    bname = os.path.join(outdir, familyid + "_base" + bext)
    basefile.write(bname)

    # Write results summary to file
    filename = os.path.join(fontspath, "local", "createbasefilesresults.csv")
    with open(filename, "w", encoding="utf-8") as outf:
        for line in resultssummary: outf.write(line + "\n")

    return


def cmd(): execute("", doit, argspec)

if __name__ == "__main__": cmd()
