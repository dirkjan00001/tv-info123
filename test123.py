#!/usr/bin/env python

import info123

def log(s):
    print(s)

def get_program_title(channel):
    title = ""
    try:
        prog = tv.get_current_program(channel)
        title = prog['titel']
        # log("Nu op nederland 1: " + prog['titel'] + "\nvan: " + prog['datum_start'] + "\ntot: " + prog['datum_end'])
    except KeyError:
        log("Channel %s not found" %channel)
    except  Exception as e:
        log("Error obtaining the program on channel %s. %s" % (channel, e))
    return title



if __name__ == "__main__":
    tv = info123.info123()

    try:
        tv.update()
    except Exception as e:
        log("Unable to connect to the server. %s" %e)

    print(get_program_title("1"))
    print(get_program_title("2"))
    print(get_program_title("3"))
