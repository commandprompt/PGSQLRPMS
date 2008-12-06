# $Header: /cvsroot/pgsqlrpms/patches/8.0/acinclude.m4,v 1.1 2006/10/14 08:19:17 devrim Exp $

# This file defines new macros to process configure command line
# arguments, to replace the brain-dead AC_ARG_WITH and AC_ARG_ENABLE.
# The flaw in these is particularly that they only differentiate
# between "given" and "not given" and do not provide enough help to
# process arguments that only accept "yes/no", that require an
# argument (other than "yes/no"), etc.
#
# The point of this implementation is to reduce code size and
# redundancy in configure.in and to improve robustness and consistency
# in the option evaluation code.


# Convert type and name to shell variable name (e.g., "enable_long_strings")
m4_define([pgac_arg_to_variable],
          [$1[]_[]patsubst($2, -, _)])


# PGAC_ARG(TYPE, NAME, HELP-STRING,
#          [ACTION-IF-YES], [ACTION-IF-NO], [ACTION-IF-ARG],
#          [ACTION-IF-OMITTED])
# ----------------------------------------------------------
# This is the base layer. TYPE is either "with" or "enable", depending
# on what you like. NAME is the rest of the option name, HELP-STRING
# as usual. ACTION-IF-YES is executed if the option is given without
# and argument (or "yes", which is the same); similar for ACTION-IF-NO.

AC_DEFUN([PGAC_ARG],
[
m4_case([$1],

enable, [
AC_ARG_ENABLE([$2], [$3], [
  case [$]enableval in
    yes)
      m4_default([$4], :)
      ;;
    no)
      m4_default([$5], :)
      ;;
    *)
      $6
      ;;
  esac
],
[$7])[]dnl AC_ARG_ENABLE
],

with, [
AC_ARG_WITH([$2], [$3], [
  case [$]withval in
    yes)
      m4_default([$4], :)
      ;;
    no)
      m4_default([$5], :)
      ;;
    *)
      $6
      ;;
  esac
],
[$7])[]dnl AC_ARG_WITH
],

[m4_fatal([first argument of $0 must be 'enable' or 'with', not '$1'])]
)
])# PGAC_ARG


# PGAC_ARG_BOOL(TYPE, NAME, DEFAULT, HELP-STRING, 
#               [ACTION-IF-YES], [ACTION-IF-NO])
# -----------------------------------------------
# Accept a boolean option, that is, one that only takes yes or no.
# ("no" is equivalent to "disable" or "without"). DEFAULT is what
# should be done if the option is omitted; it should be "yes" or "no".
# (Consequently, one of ACTION-IF-YES and ACTION-IF-NO will always
# execute.)

AC_DEFUN([PGAC_ARG_BOOL],
[PGAC_ARG([$1], [$2], [$4], [$5], [$6], 
          [AC_MSG_ERROR([no argument expected for --$1-$2 option])],
          [m4_case([$3],
                   yes, [pgac_arg_to_variable([$1], [$2])=yes
$5],
                   no,  [pgac_arg_to_variable([$1], [$2])=no
$6],
                   [m4_fatal([third argument of $0 must be 'yes' or 'no', not '$3'])])])[]dnl
])# PGAC_ARG_BOOL


# PGAC_ARG_REQ(TYPE, NAME, HELP-STRING, [ACTION-IF-GIVEN], [ACTION-IF-NOT-GIVEN])
# -------------------------------------------------------------------------------
# This option will require an argument; "yes" or "no" will not be
# accepted.

AC_DEFUN([PGAC_ARG_REQ],
[PGAC_ARG([$1], [$2], [$3],
          [AC_MSG_ERROR([argument required for --$1-$2 option])],
          [AC_MSG_ERROR([argument required for --$1-$2 option])],
          [$4],
          [$5])])# PGAC_ARG_REQ


# PGAC_ARG_OPTARG(TYPE, NAME, HELP-STRING, [DEFAULT-ACTION], [ARG-ACTION]
#                 [ACTION-ENABLED], [ACTION-DISABLED])
# -----------------------------------------------------------------------
# This will create an option that behaves as follows: If omitted, or
# called with "no", then set the enable_variable to "no" and do
# nothing else. If called with "yes", then execute DEFAULT-ACTION. If
# called with argument, set enable_variable to "yes" and execute
# ARG-ACTION. Additionally, execute ACTION-ENABLED if we ended up with
# "yes" either way, else ACTION-DISABLED.
#
# The intent is to allow enabling a feature, and optionally pass an
# additional piece of information.

AC_DEFUN([PGAC_ARG_OPTARG],
[PGAC_ARG([$1], [$2], [$3], [$4], [],
          [pgac_arg_to_variable([$1], [$2])=yes
$5],
          [pgac_arg_to_variable([$1], [$2])=no])
dnl Add this code only if there's a ACTION-ENABLED or ACTION-DISABLED.
m4_ifval([$6[]$7],
[
if test "[$]pgac_arg_to_variable([$1], [$2])" = yes; then
  m4_default([$6], :)
m4_ifval([$7],
[else
  $7
])[]dnl
fi
])[]dnl
])# PGAC_ARG_OPTARG

# Macros that test various C library quirks
# $Header: /cvsroot/pgsqlrpms/patches/8.0/acinclude.m4,v 1.1 2006/10/14 08:19:17 devrim Exp $


# PGAC_VAR_INT_TIMEZONE
# ---------------------
# Check if the global variable `timezone' exists. If so, define
# HAVE_INT_TIMEZONE.
AC_DEFUN([PGAC_VAR_INT_TIMEZONE],
[AC_CACHE_CHECK(for int timezone, pgac_cv_var_int_timezone,
[AC_TRY_LINK([#include <time.h>
int res;],
  [res = timezone / 60;],
  [pgac_cv_var_int_timezone=yes],
  [pgac_cv_var_int_timezone=no])])
if test x"$pgac_cv_var_int_timezone" = xyes ; then
  AC_DEFINE(HAVE_INT_TIMEZONE,, [Set to 1 if you have the global variable timezone])
fi])# PGAC_VAR_INT_TIMEZONE


# PGAC_FUNC_GETTIMEOFDAY_1ARG
# ---------------------------
# Check if gettimeofday() has only one arguments. (Normal is two.)
# If so, define GETTIMEOFDAY_1ARG.
AC_DEFUN([PGAC_FUNC_GETTIMEOFDAY_1ARG],
[AC_CACHE_CHECK(whether gettimeofday takes only one argument,
pgac_cv_func_gettimeofday_1arg,
[AC_TRY_COMPILE([#include <sys/time.h>],
[struct timeval *tp;
struct timezone *tzp;
gettimeofday(tp,tzp);],
[pgac_cv_func_gettimeofday_1arg=no],
[pgac_cv_func_gettimeofday_1arg=yes])])
if test x"$pgac_cv_func_gettimeofday_1arg" = xyes ; then
  AC_DEFINE(GETTIMEOFDAY_1ARG,, [Set to 1 if gettimeofday() takes only 1 argument])
fi])# PGAC_FUNC_GETTIMEOFDAY_1ARG


# PGAC_UNION_SEMUN
# ----------------
# Check if `union semun' exists. Define HAVE_UNION_SEMUN if so.
# If it doesn't then one could define it as
# union semun { int val; struct semid_ds *buf; unsigned short *array; }
AC_DEFUN([PGAC_UNION_SEMUN],
[AC_CHECK_TYPES([union semun], [], [],
[#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>])])# PGAC_UNION_SEMUN


# PGAC_STRUCT_SOCKADDR_UN
# -----------------------
# If `struct sockaddr_un' exists, define HAVE_STRUCT_SOCKADDR_UN. If
# it is missing then one could define it as { short int sun_family;
# char sun_path[108]; }. (Requires test for <sys/un.h>!)
AC_DEFUN([PGAC_STRUCT_SOCKADDR_UN],
[AC_CHECK_TYPES([struct sockaddr_un], [], [],
[#include <sys/types.h>
#ifdef HAVE_SYS_UN_H
#include <sys/un.h>
#endif
])])# PGAC_STRUCT_SOCKADDR_UN


# PGAC_FUNC_POSIX_SIGNALS
# -----------------------
# Check to see if the machine has the POSIX signal interface. Define
# HAVE_POSIX_SIGNALS if so. Also set the output variable HAVE_POSIX_SIGNALS
# to yes or no.
#
# Note that this test only compiles a test program, it doesn't check
# whether the routines actually work. If that becomes a problem, make
# a fancier check.
AC_DEFUN([PGAC_FUNC_POSIX_SIGNALS],
[AC_CACHE_CHECK(for POSIX signal interface, pgac_cv_func_posix_signals,
[AC_TRY_LINK([#include <signal.h>
],
[struct sigaction act, oact;
sigemptyset(&act.sa_mask);
act.sa_flags = SA_RESTART;
sigaction(0, &act, &oact);],
[pgac_cv_func_posix_signals=yes],
[pgac_cv_func_posix_signals=no])])
if test x"$pgac_cv_func_posix_signals" = xyes ; then
  AC_DEFINE(HAVE_POSIX_SIGNALS,, [Set to 1 if you have the POSIX signal interface])
fi
HAVE_POSIX_SIGNALS=$pgac_cv_func_posix_signals
AC_SUBST(HAVE_POSIX_SIGNALS)])# PGAC_FUNC_POSIX_SIGNALS

