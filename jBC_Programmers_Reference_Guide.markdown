# jBC Programmers Reference Guide

## Preface

jBC is a programming language that is used in jBASE post-relational
(multi-value) DBMS. Syntax is Basic-like; compilation process firstly
converts the source code to C which in turn is compiled for the target platform
with the usage of standard C compiler.

For TAFJ it is converted to Java code rather than to C.

This is unofficial document; use it at your own risk - like TAFC :)) .. no, no joke - read its license agreement carefully.

### Latest changes

Saturday, 16 Jul 2022. Made available via github.io.

Tuesday, 30 Sep 2014. Another example for [@](#@) function.

## What is TAFC

TAFC stands for "Temenos application framework for C". This name was adopted to
differentiate the database (jBASE) from development tools that are used for it.
Full installation package is called "jBASE" for the non-T24 customers and "TAFC" for
T24-based ones.

## TAFC releases

TAFC release number normally reflects T24 release for which it is intended to
be used, e.g. R10 or R22.

## What is T24

T24 is the core banking system developed by Temenos company. The system
extensions can be developed in (but not limited to) jBC.

## jBC/jBASE features

- Case sensitive keywords and variable names.
- Optional statement labels.
- Code sections accessed by GOSUB.
- IF...THEN..ELSE conditional statement.
- BEGIN CASE...CASE...END CASE conditional statement.
- FOR...NEXT loop.
- DO..WHILE/UNTIL...REPEAT loop.
- External subroutines and functions.
- Weak variables typing; implicit types conversion.
- Dimensioned and dynamic arrays.
- String, number, and date data conversion.
- Patterns matching.
- Unary operators support.
- Single- and multi-byte character sets support.
- Bitwise operations.
- Standard industry encryption algorithms support.
- Named and unnamed COMMON areas.
- Operations with SELECT lists.
- File and record level locking capability; distributed lock system.
- Text files processing.
- Functions for XML processing.
- Manipulations with environment variables.
- Emulation modes for compatibility with numerous MV platforms.
- Practically unlimited data file size (OS limits apply).
- Data files distribution.
- Transactions support.
- Transparent access to jBASE data and dictionary files converted to Oracle, DB2 or MS SQL.
- Possibility to call C or Java code.
- Possibility to execute any jBASE, system or database enquiry command.
- Source code editor - JED (also capable of editing data files).
- Debugger.

# Introduction to some jBC syntax features

## Note

In examples presented here and below deleting and creation of temporary file
called F.TEMP is often used, so if you have such file with something valuable
in it in your current directory, backup it first.

## Note 2

OCONV() or FMT() with second parameter 'MCP' is often used; its only purpose is
to convert FM, VM and SM delimiters to a printable form, e.g.:

       V.ARRAY = 1 :@FM: 2 :@VM: 3 :@FM: 4 :@SM: 5
       CRT FMT(V.ARRAY, 'MCP')                ;*   1^2]3^4\5

Where possible, the output is shown in a comment (as it is in the example above).

## Variables visibility and lifetime

Variable is visible throughout the program or its subroutine (i.e. in
the bounds of particular source code file). To share a variable between
different programs/subroutines pass them as parameters in [CALL](#CALL)
statement or use a named or unnamed [COMMON](#COMMON).

All variables (except ones in COMMON areas) are reset (i.e. become unassigned) upon program end.

See also: [SUBROUTINE](#SUBROUTINE), [ASSIGNED](#ASSIGNED), [UNASSIGNED](#UNASSIGNED).

## To wrap a long line

Use a backslash:

       V.LINE = 'The report for the year ' :@FM: V.YEAR : ', prepared at ' \
            : TIMEDATE()

Or - if line ends with a comma - that's not necessary:

       V.STAT = IOCTL(F.TEST.FILE,
             JIOCTL_COMMAND_FINDRECORD_EXTENDED, V.NAME)

## Several statements on the same line

Use semicolon to delimit several statements on the same line; don't forget about
code readability. You can combine statements with comments (though as soon as
you have a comment, the following statements turn to comments as well):

    V.VAR = 1  ;  V.VAR++  ;  CRT V.VAR
    V.VAR-- ;* comment starts here so no "1" in the output ; CRT V.VAR
    V.VAR-- ; CRT V.VAR  ;* 0 will be displayed

Conditional statements are also supported (though code readability suffers in
the following example):

    var_1 = 1 ; var_2 = 2 ; IF var_1 + var_2 EQ 3 THEN
       CRT var_1, '+', var_2, '= 3'
    END

## Comments

Comments can be defined in different ways:

    * This is a comment
    ! And this is a comment
    REM This is also a comment
    // Even this is a comment
       CRT '1'    ;* this is a comment sharing the same line with some code
       CRT '2'    // yet another way to define a comment
       CRT '3'

## String variables

Strings can be delimited with single quotes, double quotes or backslashes:

       CRT 'QWERTZ'    ;* this is a string
       CRT "QWERTZ"    ;* this is also a string
       CRT 'QWE"RTZ'   ;* and even this is a string
       CRT \QWERTZ\    ;* still this is a string
       * and here a backslash means line continuation
       CRT 'QWE'  \
          : 'RTZ'

To concatenate strings (you could see it in one of examples above), use a
colon:

       a_line = 'QWE' : 'RT'
       CRT a_line                               ;*  QWERT
       * unary concatenation
       a_line := 'Y'
       CRT a_line                               ;*  QWERTY

String can be concatenated with a number without explicit conversion:

       a_line = 'QWERTY'
       a_line := 123
       CRT a_line                               ;*  QWERTY123

To extract a substring from a string use square brackets:

       a_line = 'QWERTY'
       CRT a_line[1,2]                          ;*  QW
       CRT a_line[2]                            ;*  TY
       CRT a_line[-4,2]                         ;*  ER

It's possible to reassign parts of a string using that notation:

       a_string = 'ABC'
       a_string[2,1] = 'Q'
       CRT a_string                             ;* AQC
       a_string[2,1] = 'WER'
       CRT a_string                             ;* AWERC

Strings comparison is done from left to right:

       a_string = 'ABC'
       char_a = 'A'
       char_b = 'B'
       CRT a_string GT char_a       ;* 1
       CRT a_string GT char_b       ;* 0

Other common string operations:

       a_line = 'QWERTY'
       * add quotes around a string
       CRT SQUOTE(a_line[4,999])                ;*  'RTY'
       CRT QUOTE(a_line)                        ;*  "QWERTY"
       * change case
       CRT DOWNCASE(a_line)                     ;*  qwerty
       CRT UPCASE('do it now!')                 ;*  DO IT NOW!
       * get length of a string
       CRT LEN(a_line)                          ;*  6
       * get length of i18n string - number of characters and number of bytes
       a_line := CHAR(353)
       CRT LEN(a_line)                          ;*  7
       CRT BYTELEN(a_line)                      ;*  8
       * repeat string several times
       CRT STR('QWE', 5)                        ;*  QWEQWEQWEQWEQWE
       * dynamic array is also a string
       dyn_array = 'qwe' : @FM : "rty" : @VM : \xYZ\
       CRT LEN(dyn_array)                       ;*  11
       CRT FMT( UPCASE(dyn_array), 'MCP' )      ;*  QWE^RTY]XYZ
       * pad a string
       a_string = 'AWERC'
       CRT '/' : FMT(a_string, '25R') : '/'     ;* /                    AWERC/
       * get ASCII value of a character
       CRT SEQ(a_string[1,1])                   ;* 65 (ASCII code of "A")

## Numeric variables

       V.VAR = 5            ;   CRT V.VAR           ;* 5
       CRT ISDIGIT(V.VAR)                           ;* 1
       V.VAR = V.VAR + 1    ;   CRT V.VAR           ;* 6
       V.VAR ++             ;   CRT V.VAR           ;* 7
       V.VAR += 1           ;   CRT V.VAR           ;* 8
       V.VAR -= 1           ;   CRT V.VAR           ;* 7
       V.VAR =- 1           ;   CRT V.VAR           ;* -1... easy to make a mistake
       CRT ISDIGIT(V.VAR)                           ;* 0 (we have minus now)
       CLEAR
       CRT V.VAR                                    ;* 0
       V.VAR2 = V.VAR++     ; CRT V.VAR2            ;* 0 - old value of V.VAR
       V.VAR3 = ++V.VAR     ; CRT V.VAR3            ;* 2 - value of V.VAR (1) + 1
    * other operators
       CRT 2 * 3                                    ;* 6
       CRT 2 ** 10                                  ;* power of 2 (1024)
       CRT 2 ^ 10                                   ;* same as above
       CRT 7 / 2                                    ;* 3.5
       CRT SQRT(144)                                ;* 12
    * precedence is quite expected
       CRT 7 / 2 + 3                                ;* 6.5
       CRT 7 / (2 + 3)                              ;* 1.4
    * Dot, plus, minus are considered non-numeric - in all emulations
    * dot_not_numeric = true:
       CRT ISDIGIT(-1)                         ;* 0
       CRT ISDIGIT(1.234)                      ;* 0

## Boolean variables

Boolean variables as such don't exist in jBC; the result of a statement like IF (VAR) THEN...
depends on that variable contents:

       IF NOT(unassigned_var) THEN CRT 'Unassigned var is false'
       true_var = 1  ;  false_var = 0
       IF true_var THEN CRT '1 is true'
       IF NOT(false_var) THEN CRT '0 is false'
       a_string = 'YES'
       IF a_string THEN CRT 'Non-empty string is true'
       IF NOT('0.00') THEN CRT '0.00 is false'
       IF NOT('-0.00') THEN CRT '"-0.00" is still false - treated as numeric'
    * and this test depends on PRECISION
       PRECISION 9
       IF NOT('0.00000000000001') THEN CRT '0.00000000000001 is false'  \
             ELSE CRT '0.00000000000001 is true'
       PRECISION 17
       IF NOT('0.00000000000001') THEN CRT '0.00000000000001 is false' \
             ELSE CRT '0.00000000000001 is true with PRECISION 17'
       *------------------------------------------------------------------------
    ANOTHER.METHOD:
    *
      CRT @TRUE
      CRT @FALSE

Compiler warning:

<pre>
    Warning: Variable unassigned_var is never assigned!</pre>

Runtime:

<pre>
    Non-numeric value -- ZERO USED ,
    Variable 'unassigned_var' , Line 1 , Source test.b
    Unassigned var is false
    1 is true
    0 is false
    Non-empty string is true
    0.00 is false
    "-0.00" is still false - treated as numeric
    0.00000000000001 is false
    0.00000000000001 is true with PRECISION 17
    1
    0</pre>

## Dynamic arrays

To assign or extract a field/value/subvalue from a dynamic array,
use string concatenation method (**:**) or angle brackets:

       V.ARRAY = 1 :@FM: 2 :@FM: 3 :@FM: 4 :@VM: 5 :@VM: 6 :@SM: 7
       CRT V.ARRAY<2>               ;* 2
       CRT V.ARRAY<4,3,1>           ;* 6
       V.ARRAY<2> += 1
       CRT V.ARRAY<2>               ;* 3
       V.ARRAY<-1> = 10             ;* adds an element to the end
    * Nesting is allowed:
       V.CNT = 1 :@FM: 3 :@FM: 5
       V.ARRAY<V.CNT<2>> = 77
       CRT FMT(V.ARRAY, 'MCP')      ;* 1^3^77^4]5]6\7^10

Note that array elements are numbered starting from 1 rather that 0.

## Dimensioned arrays

Dimensioned arrays use parentheses:

       DIM V.VALUES(30000)            ;* size it
       MAT V.VALUES = 0               ;* assign 0 to all elements
       V.X = SYSTEM(2) - 15  ; V.Y = SYSTEM(3) - 5
       DIM V.SCREEN(V.X, V.Y)         ;* can be 2-dimensional
       V.SCREEN(1, 1) = 123           ;* here goes assignment

## Other notes

"=" character can be used both for assignment and for a comparison,
though it's possible to use "EQ" in the latter case:

       V.STRING = 'ABC'
       IF V.STRING = 'ABC' THEN CRT 'YES'
       IF V.STRING EQ 'ABC' THEN CRT 'YES AGAIN'

"Non-equal" can either be "#", "!", "<>" or "NE":

       a_string = 'ABC'
       IF a_string #  'A' THEN CRT 'Not an "A"'
       IF a_string NE 'B' THEN CRT 'Not a "B"'
       IF a_string ! 'C' THEN CRT 'Not even a "C"'
       IF a_string <> 'D' THEN CRT 'Surprisingly, but neither a "D"'

IF...ELSE construct can be used without THEN:

       V.STRING = 'ABC'
       IF V.STRING NE 'ABC' ELSE CRT 'YES'

### Differences between emulations

For T24 emulation should always be **prime**, however for porting the code it's
crucial to understand the differences.

See several examples below.

The following
code will run successfully under **prime** emulation and will fail under **ros**:

       ret_code = GETENV('JBCEMULATE', jbc_emu)   ;   CRT jbc_emu
       dyn_array = 3 :@AM: 7
       dyn_array += 4
       CRT FMT(dyn_array, 'MCP')

Runtime:

<pre>
    prime
    7^7</pre>

<pre>
    ros
    Non-numeric value -- ZERO USED ,
    Variable 'dyn_array' , Line     3 , Source test.b
    Trap from an error message, error message name = NON_NUMERIC</pre>

*Setting in Config_EMULATE: ***no_value_maths = false|true**

Next program outputs *<>* under **prime** and *<0>* under **seq**
emulation. In the latter case there will be zero-sized file *report.txt* after
program termination. So if, for example, nothing was written to a report
under **prime** emulation (or, in fact, any other except **seq**),
there will be no output file left after that.

Source code:

       dir_name = '.'
       file_name = 'report.txt'
       DELETESEQ dir_name, file_name ELSE NULL
       *
       OPENSEQ dir_name, file_name TO f_report THEN NULL
       CRT '<' : DIR(file_name)<1> : '>'

*Setting in Config_EMULATE: ***openseq_creates = false|true**

The following program outputs *1* under **prime** emulation and *0*
under **r83**, thus showing that common variables can be assigned or
unassigned upon declaration of COMMON area:

       COMMON /MY.COMM/ var_1, var_2
       *
       CRT ASSIGNED(var_1)

*Setting in Config_EMULATE: ***named_common = unassigned|null|zero**

The next program outputs *A^1^2^3^4^5* under **seq** or **r83**
emulations; under others (that do add additional
delimiter even if one exists at the end of an array in question) the output
will be: *A^^1^2^3^4^5*.

Source code:

       dyn_array = 'A' : @FM
       FOR i = 1 TO 5
          dyn_array<-1> = i
       NEXT i
       CRT OCONV(dyn_array, 'MCP')

*Setting in Config_EMULATE: ***no_extra_delimiter = false|true**

The following *READV* example outputs *REC1* (i.e. record key) when is
run under **jbase** emulation and *3* (i.e. fields count) under, e.g.,
**ap** or **r83**:

       OPEN 'F.TEMP' TO f_temp THEN
          ret_error = ''
          CLEARFILE f_temp SETTING ret_error
          IF ret_error NE '' THEN
             CRT 'ERROR ' : ret_error
             STOP
          END
       END ELSE
          EXECUTE 'CREATE-FILE DATA F.TEMP 1 101 TYPE=J4'
          OPEN 'F.TEMP' TO f_temp ELSE ABORT 201, 'F.TEMP'
       END
       *
       out_record = 'LINE 1' :@FM: 'LINE 2' :@FM: 'LINE 3'
       WRITE out_record TO f_temp, 'REC1'
       *
       READV in_record FROM f_temp, 'REC1', 0 ELSE
          CRT 'Read error'
          STOP
       END
       *
       CRT in_record

*Setting in Config_EMULATE: ***readv0 = key|dcount|binary**

Some settings are effective at runtime, others apply during compilation.
For example, the following program compiles successfully under **prime**
emulation and runs successfully after that under all emulations.
However, it's not possible to compile it under, say, **jbase** emulation.
Reason of error - redimensioning of an array.

Code:

       DIMENSION dyn_array(10)
       MAT dyn_array = '!'
       dyn_array(5) = '?'
       FOR i = 1 TO 10
          CRT dyn_array(i):          ;* !!!!?!!!!!
       NEXT i
       DIM dyn_array(15)
       dyn_array(15) = '...'
       CRT dyn_array(15)

Compilation under **jbase** emulation:

<pre>
    [error 1        (32)] "test.b", 7 (offset 18)  near ")":
    Array dyn_array has already been DIMensioned
    &nbsp;
    1 error was found</pre>

*Setting in Config_EMULATE: ***resize_array = false|true**

Another example:

    * number of seconds past midnight
       CRT SYSTEM(12)   ;* e.g. 30938703.4097 under prime, 309387 under ros

For more settings see *Config_EMULATE* and *Config_EMULATE.txt*
files in your TAFC/config folder.

# Guidelines for writing the source code

## Recommendations (not rules)

*Note: some examples in this documentation don't fully follow these rules - they were taken from other sources or it's done intentionally to illustrate some language features.*

- All variables are to be in lower case and in the lower_case_and_underscore_naming style.

- Use only one style of quotes for strings, e.g.: "QWERT" (double quotes, preferable) or 'QWERT' (single quotes). Mix them only if it's really required, e.g.:

       CRT '"Yes Minister", ' : "that's what I said."

- Always use one space after the comma and never before the comma.

- Never use space after '(' and before ')' (exception is when code is more readable with it).

- Never put multiple commands on a single line and separate them by ";", except for short similar statements, like:

       var_1 = 1  ;  var_2 = 2  ;  var_3 = 3

- Don't put trailing ';' at the end of the lines.

- Never convert ints to boolean implicitly:

Instead of:

       IF INDEX(...) THEN

always write:

       IF INDEX(...) NE 0 THEN

Same goes for strings. Instead of:

       var = 'ABC'
       IF var THEN  ;* code continues here

Use:

       IF var NE '' THEN  ;* code continues here

- Never hardcode program or subroutine name in error messages etc. Use SYSTEM(40) instead.

- Always supply meaningful error messages with sufficient additional information.

- Don't comment what you do; comment why.

- Don't mix tabs with spaces, use either former or latter.

- Don't use characters with ASCII code above 126 in the source. To form strings with such characters use CHAR() or load them from external file or table.

- Use CR (ASCII 10) for line ends rather than CR+LF.

- For statements like INCLUDE, $INSERT use zero indent; for all other code - 3 spaces of initial indent and 3 spaces to indent each FOR...NEXT, LOOP...REPEAT contents etc.

- Wrap lines that are longer than 80 characters (use a backslash or comma at the end where the latter is applicable). It's a good idea to move line continuation(s) even more than 3 positions to the right, e.g.:

       current_date = DATE()
       current_day = OCONV(current_date, 'DD')
       current_month = OCONV(current_date, 'DM')
       ansi_date =  OCONV(current_date, 'DY') : '-'    \
             : FMT(current_month, 'R0%2' )   : '-'     \
             : FMT(current_day, 'R0%2' )
       CRT ansi_date                             ;* e.g. 2013-03-08

- Use spaces around "=":  not "var=1" but "var = 1".

- Use "=" for assignment only; for comparisons use "EQ".

- Don't use IF..ELSE without THEN.

- Avoid GOTO, RETURN TO as much as possible.

- Use named COMMON rather than unnamed.

- Don't use numeric line labels like:

       001 A = 0
       002 A += 1
       003 IF A LT 5 THEN GOTO 002 ELSE CRT A

- Avoid ambiguity with IF...AND...OR, use parentheses. In the following example code lines 2, 3 and 4 are the same (except parentheses); only second IF is true:

       var_1 = 1  ; var_2 = 2  ; var_3 = 3 ; var_4 = 4
       IF var_1 EQ 1 OR var_2 EQ 20 AND var_3 EQ 30 OR var_4 EQ 40 THEN CRT 1
       IF var_1 EQ 1 OR (var_2 EQ 20 AND var_3 EQ 30 OR var_4 EQ 40) THEN CRT 2
       IF (var_1 EQ 1 OR var_2 EQ 20) AND (var_3 EQ 30 OR var_4 EQ 40) THEN CRT 3

- Use only one method of writing "not equal" (preferably "NE").

(See the second example in chapter ["Other notes"](#Other_notes).)

# Environment variables relevant to jBC programming

## Minimum set of variables necessary to start development

Windows:

<pre>
    set TAFC_HOME=[path to installed TAFC]
    set JBCGLOBALDIR=%TAFC_HOME%
    set PATH=%TAFC_HOME%\bin;[path to C Compiler]\bin;%PATH%
    set JBCEMULATE=[your emulation; for T24 should be prime]
    set INCLUDE=[path to C Compiler]\include;%INCLUDE%
    set LIB=[path to C Compiler]\lib;%LIB%
    set JBCBASETMP=tmp_workfile</pre>

Unix/Linux:

<pre>
    export TAFC_HOME=[path to installed TAFC]
    export JBCGLOBALDIR=$TAFC_HOME
    export PATH=$TAFC_HOME/bin:$PATH
    export JBCEMULATE=[your emulation; for T24 should be prime]
    TTYNO=`tty | cut  -f4 -d\/`
    export JBCBASETMP=$HOME/jBASEWORK/tmp_$TTYNO
    export LD_LIBRARY_PATH=$TAFC_HOME/lib:/usr/ccs/lib:/usr/lib:/lib
    (Linux)
    export LIBPATH=$TAFC_HOME/lib:/usr/ccs/lib:/usr/lib
    (AIX)
    export SHLIB_PATH=$TAFC_HOME/lib:${SHLIB_PATH:-/usr/lib:/lib}
    (HP-UX)</pre>

## Customize work folders and files location

Main dictionary location (usually points to VOC file):

<pre>
    JEDIFILENAME_MD</pre>

Path to SYSTEM file (normally located in [path to installed TAFC]/src):

<pre>
    JEDIFILENAME_SYSTEM</pre>

Default path to jBASE data files:

<pre>
    JEDIFILEPATH</pre>

Location where programs will be put after compilation:

<pre>
    JBCDEV_BIN</pre>

The folder where shared libraries for compiled subroutines are located:

<pre>
    JBCDEV_LIB</pre>

Path to jBASE spooler folder:

<pre>
    JBCSPOOLERDIR</pre>

The folder where saved lists are placed:

<pre>
    JBCLISTFILE</pre>

Where to look for libraries containing compiled subroutines:

<pre>
    JBCOBJECTLIST</pre>

Could be several entries, e.g.:

Windows:

<pre>
    set JBCOBJECTLIST=%HOME%\lib;%HOME%\t24lib</pre>

Unix/Linux:

<pre>
    export JBCOBJECTLIST=$HOME/lib:$HOME/t24lib</pre>

If a subroutine presents in more than one location (which can be caused by
changing JBCDEV_LIB environment variable or accidental duplication of a
subroutine name) then the earlier location has the preference. See jshow output:

<pre>
    jshow -c ACCOUNT
    Subroutine:          C:\r11\bnk\bnk.run\lib\lib2.dll
                         jBC ACCOUNT version 11.0 Thu Sep 06 22:09:46 2012
                         jBC ACCOUNT source file ETC.BP
    Subroutine (DUP!!):  C:\r11\bnk\bnk.run\t24lib\acm_accountopening\lib0.dll
                         jBC ACCOUNT version 11.0 Fri Apr 29 14:43:35 2011
                         jBC ACCOUNT source file source/R11.000/win32_TAFCR11GA</pre>

In situation like that DECATALOG is to be used:

<pre>
    DECATALOG ETC.BP ACCOUNT
    Object ACCOUNT decataloged successfully
    Library C:\r11\bnk\bnk.run\lib\lib2.dll rebuild okay</pre>

<pre>
    jshow -c ACCOUNT
    Subroutine:          C:\r11\bnk\bnk.run\t24lib\acm_accountopening\lib0.dll
                         jBC ACCOUNT version 11.0 Fri Apr 29 14:43:35 2011
                         jBC ACCOUNT source file source/R11.000/win32_TAFCR11GA</pre>

## Runtime errors handling

This variable allows to suppress error messages and/or a program entering the debugger when divide by
zero is encountered:

<pre>
    JBASE_ERRMSG_DIVIDE_BY_ZERO</pre>

This variable allows to suppress error messages and/or a program entering the debugger when non-numeric
variable is used in an equation:

<pre>
    JBASE_ERRMSG_NON_NUMERIC</pre>

This variable allows to suppress error messages and/or a program entering the debugger when uninitialized
variable is used in an equation:

<pre>
    JBASE_ERRMSG_ZERO_USED</pre>

## Regional settings

Locale setting:

<pre>
    JBASE_LOCALE</pre>

In which codepage data is displayed (e.g. utf8, windows-1251 etc;
doesn't apply to how data is stored):

<pre>
    JBASE_CODEPAGE</pre>

Time zone:

<pre>
    JBASE_TIMEZONE
    E.g. Europe/London.</pre>

Setting this variable to 1 means utf-8 environment
(requires data files conversion when changed):

<pre>
    JBASE_I18N</pre>

## Diagnostics and tracing

Being set to 1 redirects stderr to stdout (useful to catch errors to COMO output):

<pre>
    JBC_STDERR</pre>

Being set to 1 stipulates creation of a core dump when the session crashes:

<pre>
    JBC_CORE_DUMP</pre>

jBASE tracing options:

<pre>
    JDIAG</pre>

E.g.:

<pre>
    set JDIAG=trace=JVM,CALLJ
    set JDIAG=TRACE=INDEX</pre>

## Other

Being set to 1 improves performance when distributed files are used:

<pre>
    JBASE_DISTRIB_FASTSCAN</pre>

Being set to 1 prevents all parts of a distributed file to be opened as soon as the stub had
been:

<pre>
    JEDI_DISTRIB_DEFOPEN</pre>

Terminal type (e.g. ntcon, vt220 etc):

<pre>
    TERM</pre>

# Compilation

## Introduction to BASIC...CATALOG and jcompile

<pre>
    BASIC MY.BP TEST.SUB
    &nbsp;
    TEST.SUB
    BASIC_1.c
    Source file TEST.SUB compiled successfully</pre>

<pre>
    CATALOG MY.BP TEST.SUB
    &nbsp;
    TEST.SUB
    Object TEST.SUB cataloged successfully
    Library $HOME\lib\lib0.dll rebuild okay</pre>

<pre>
    jcompile test.b
    &nbsp;
    Warning: Variable DIV.AMT2 is never assigned!
    test.c</pre>

Compilation results in appearance of an object and executable files
(sample for Windows):

<pre>
    test.obj
    test.dll
    test.exe</pre>

**See program information**:

<pre>
    jshow -c test
    &nbsp;
    Executable:          C:\r11\BATfiles\test.dll
                         jBC main() version 11.0 Thu Dec 06 23:35:34 2012
                         jBC main() source file unknown
    Executable (DUP!!):  C:\r11\BATfiles\test.exe
                         jBC main() version 11.0 Thu Dec 06 23:35:34 2012
                         jBC main() source file unknown</pre>

If the code is recompiled very often then it might happen that the older version
of executable code
still resides in shared memory and the result of changes wouldn't be seen immediately.
In this case "-E" option of jcompile can be used to build executable only
and not the shared library, e.g.:

<pre>
    jcompile -E test.b</pre>

And then test.dll isn't created. The final compilation is of course to be done
without "-E" option. Also - without shared library CHAIN statement might work
not as expected and persistence of COMMON areas won't be supported.

**See commands** used by compiler:

<pre>
    jcompile -v test.b
    &nbsp;
    cl /nologo /DWIN32 /MD /W2 /GR /EHa -c -IC:\TAFC\include -DJBC_OPTLEVEL2 test.c
    ...
    cl /nologo /DWIN32 /MD /W3 /GR /EHa /GF /Zi /F5000000 -D_LARGEFILE_SOURCE ...</pre>

**Conditional compilation**:

       V.VAR = 1
       CRT 'Version ':
    #ifdef VER1
       CRT V.VAR:
    #else
       CRT V.VAR + 1:
    #endif
       CRT ' finished'

<pre>
    jcompile -DVER1 test.b
    test.c
    &nbsp;
    test
    Version 1 finished</pre>

<pre>
    jcompile test.b
    test.c
    &nbsp;
    test
    Version 2 finished</pre>

**To look at C code** rather than to create executables "-S" option can be used
(files test.c and test.j will be created for test.b source).

Full information about jcompile options - "jcompile -H".

# Data files

## Introduction to jBASE/TAFC data files

The most widely used formats for data files nowadays are "J4" and "JR".
The former has size limitation (up to 2Gb if OS-level limits allow that)
and needs resizing on regular basis though when it's properly sized it's
faster. "JR" - "resilient" - doesn't have size limitation and
doesn't need resizing.

The following examples serve as a brief introduction to jBASE data storage.
They can be executed in jshell prompt or (except JED - it makes no sense)
in a jBC program or subroutine (using EXECUTE/PERFORM).

## Create/delete hashed file

Create both data and dictionary:

<pre>
    CREATE-FILE F.SAMPLE 101 1
    &nbsp;
    [ 417 ] File F.SAMPLE]D created , type = J4
    [ 417 ] File F.SAMPLE created , type = J4</pre>

If the file already exists, the error message appears:

<pre>
    [ 413 ] File name DICT F.SAMPLE already exists</pre>

Delete hashed file (both data and dictionary):

<pre>
    DELETE-FILE F.SAMPLE</pre>

Create hashed file (data only):

<pre>
    CREATE-FILE DATA F.SAMPLE 101 1
    &nbsp;
    [ 417 ] File F.SAMPLE created , type = J4</pre>

Create hashed file (dictionary only):

<pre>
    CREATE-FILE DICT F.SAMPLE 101 1
    &nbsp;
    [ 417 ] File F.SAMPLE]D created , type = J4</pre>

## Create and list the data

Put some data to file:

<pre>
    JED F.SAMPLE REC1
    &nbsp;
    0001 Field one
    0002 Field two
    0003 Field three</pre>

Press Esc; then type FI to save the record.

List file contents:

<pre>
    LIST F.SAMPLE
    &nbsp;
    F.SAMPLE......
    &nbsp;
    REC1
    &nbsp;
    1 Records Listed</pre>

No dictionary; we see only @ID. Raw output:

<pre>
    CT F.SAMPLE
    &nbsp;
    REC1
    001 Field one
    002 Field two
    003 Field three</pre>

As an alternative, we can use standard correlatives:

<pre>
    LIST F.SAMPLE &lowast;A1 &lowast;A2 &lowast;A3
    &nbsp;
    F.SAMPLE......   &lowast;A1...........   &lowast;A2...........   &lowast;A3...........
    &nbsp;
    REC1             Field one        Field two         Field three</pre>

## Adding dictionary items

Add a dictionary item to assign the name to a field:

<pre>
    JED DICT F.SAMPLE FLD1
    &nbsp;
    0001 D
    0002 1
    0003
    0004 FIELD 1 HEADER
    0005 10L
    0006 S
    0007</pre>

Use field name in a query:

<pre>
    LIST F.SAMPLE FLD1
    &nbsp;
    F.SAMPLE......   FIELD 1 HEADER
    &nbsp;
    REC1             Field one
    &nbsp;
    1 Records Listed</pre>

<pre>
    LIST F.SAMPLE WITH FLD1 EQ ''
    &nbsp;
     No Records Listed</pre>

In default view we still dont have it:

<pre>
    LIST F.SAMPLE
    &nbsp;
    F.SAMPLE......
    &nbsp;
    REC1</pre>

Set the field to be seen by default:

<pre>
    JED DICT F.SAMPLE @
    &nbsp;
    0001 PH
    0002 @ID FLD1</pre>

See the result:

<pre>
    LIST F.SAMPLE
    &nbsp;
    F.SAMPLE......   ID..................   FIELD 1 HEADER
    &nbsp;
    REC1             REC1                   Field one</pre>

## Change of size and format, statistics, properties

See file statistics:

<pre>
    jstat -v F.SAMPLE
    &nbsp;
    File C:\r11\bnk\bnk.run\F.SAMPLE
    Type=J4 , Hash method = 5
    Created at Tue Nov 20 19:38:25 2012
    Groups = 101 , Frame size = 4096 bytes , Secondary Record Size = 8192 bytes
    Restore re-size parameters : (none)
    File size = 417792 bytes , Inode = 29838 , Device = Id 24915
    Last Accessed Tue Nov 20 19:50:30 2012 , Last Modified Tue Nov 20 19:50:30 2012
    Backup = YES , Log = YES , Rollback = YES , Network = NO
    Record Count = 1 , Record Bytes = 45
    Bytes/Record = 45 , Bytes/Group = 0
    Primary file space:   Total Frames = 101 , Total Bytes = 45
    Secondary file space: Total Frames = 0 , Total Bytes = 0</pre>

### NOTE

101 - number of groups - was defined when file was created.

Add more records:

<pre>
    COPY FROM F.SAMPLE REC1,REC2
    &nbsp;
    1 records copied</pre>

Try to resize the file:

<pre>
    jrf -V F.SAMPLE
    &nbsp;
    ...
    Downsizing skipped from modulo 101 to 3.</pre>

Resize it anyway:

<pre>
    jrf -VD F.SAMPLE
    &nbsp;
    ...
    Downsizing from modulo 101 to 3</pre>

Change file type to JR:

<pre>
    jrf -H6 F.SAMPLE</pre>

See statistics now:

<pre>
    jstat -v F.SAMPLE
    &nbsp;
    File Type       = JR,        Hash method = 5, Created = Tue Nov 20 19:56:00 2012
    Frame size      = 4096,        OOG Threshold   = 2048
    File size       = 8192, Freespace       = 0 frames
    Internal Modulo = 3/7/11,      External Modulo = 13
    Inode no.       = 29838,       Device no.      = 24915
    Accessed        = Tue Nov 20 19:56:13 2012, Modified  = Tue Nov 20 19:56:13 2012
    Backup  = YES, Log      = YES, Rollback        = YES,  Secure updates  = NO
    Deallocate pointers : NO       Deallocate frames NO
    Revision level  = 2
    Record Bytes    = 82,   Record Count    = 2
    Bytes/Record    = 41,   Bytes/Group     = 82
    Data Frames     = 1,    Ptr Frames      = 0
    OOG Bytes       = 0,    OOG Frames      = 0
    Sum Squares     = 3362, Std Dev Mean    = 41</pre>

Turn on secure updates:

<pre>
    jchmod +S F.SAMPLE</pre>

Check the result:

<pre>
    jstat -v F.SAMPLE
    &nbsp;
    ...
    Backup  = YES, Log      = YES,  Rollback        = YES,  Secure updates  = YES
    ...</pre>

Delete a record:

<pre>
    DELETE F.SAMPLE REC2
    &nbsp;
    1 record(s) deleted.</pre>

Add data sections:

<pre>
    CREATE-FILE F.SAMPLE,TWO TYPE=JR
    &nbsp;
    [ 417 ] File F.SAMPLE]MTWO created , type = JR</pre>

<pre>
    CREATE-FILE F.SAMPLE,THREE TYPE=JR
    &nbsp;
    [ 417 ] File F.SAMPLE]MTHREE created , type = JR</pre>

Create a record in a section:

<pre>
    JED F.SAMPLE,TWO REC5
    &nbsp;
    0001 Section 2/1
    0002 Section 2/2
    0003 Section 2/3</pre>

See that all sections use the same dictionary:

<pre>
    LIST F.SAMPLE,TWO
    &nbsp;
    F.SAMPLE,TWO..    ID..................    FIELD 1 HEADER
    &nbsp;
    REC5              REC5                    Section 2/1</pre>

<pre>
    LIST F.SAMPLE,THREE
    &nbsp;
    F.SAMPLE,THREE    ID..................    FIELD 1 HEADER
    &nbsp;
     No Records Listed</pre>

### NOTE

File F.SAMPLE still reports 1 record in it; here's the difference
between having several data sections and a distributed file.

## UD type

Folders are also treated like data files (type UD); flat files in them -
like records. This allows, for example, use JED to edit source code.
Data can be copied transparently between hashed
files and folders. Some examples:

Create the folder:

<pre>
    CREATE-FILE DATA TEST.BP TYPE=UD
    &nbsp;
    [ 417 ] File TEST.BP created , type = UD</pre>

Create a program:

<pre>
    JED TEST.BP PROG1
    &nbsp;
    0001 CRT 2*2</pre>

Save file. Compile and run it:

<pre>
    BASIC TEST.BP PROG1
    &nbsp;
    PROG1
    BASIC_3.c
    Source file PROG1 compiled successfully</pre>

<pre>
    CATALOG TEST.BP PROG1
    &nbsp;
    PROG1
    Object PROG1 cataloged successfully</pre>

<pre>
    PROG1
    &nbsp;
    4</pre>

Copy data:

<pre>
    COPY FROM F.SAMPLE TO TEST.BP REC1
    &nbsp;
    1 records copied</pre>

Edit file REC1 in TEST.BP folder with any text editor so it now looks like:

<pre>
    Field one - updated
    Field two
    Field three</pre>

Copy it back to hashed file:

<pre>
    COPY FROM TEST.BP TO F.SAMPLE REC1 OVERWRITING
    &nbsp;
    1 records copied</pre>

See the result:

<pre>
    LIST F.SAMPLE
    &nbsp;
    F.SAMPLE......     ID..................   FIELD 1 HEADER
    &nbsp;
    REC1               REC1                   Field one - up
                                              dated</pre>

# System ("@") variables

## @AM (@FM), @VM, @SM, @TM

Attribute (field) mark (ASCII 254), value mark (ASCII 253), subvalue mark
(ASCII 252) and text mark (ASCII 251) respectively.

## @CALLSTACK

Intended to return current call stack information; isn't yet
implemented. SYSTEM(1029) could be used to obtain call stack information, e.g:

Main program (test.b):

       GOSUB SECTION1
       STOP
       *-------------
    SECTION1:
       GOSUB SECTION2
       RETURN
       *-------------
    SECTION2:
       CRT OCONV( SYSTEM(1029), 'MCP' )
       CALL TEST.SUB
       RETURN
    END

Subroutine:

       SUBROUTINE TEST.SUB
    *
       GOSUB SECTION3
       RETURN
       *-------------
    SECTION3:
       CRT OCONV( SYSTEM(1029), 'MCP' )
       RETURN
    END

Output:

<pre>
    1\2\6\test.b]1\1\1\test.b
    2\1\3\TEST.SUB]1\3\12\test.b]1\2\6\test.b]1\1\1\test.b</pre>

## @CODEPAGE

Returns current codepage setting:

       CRT @CODEPAGE      ;* e.g. utf8

## @DATA

Data statements used in conjunction with INPUT statements are
stored in data stack or input queue. This stack is accessible
in the @DATA variable:

       DATA 'QWE'
       DATA 'RTY'
       CRT SYSTEM(14)   ;* number of bytes in data stack (EOL characters included)
       CRT DQUOTE(@DATA)
       CRT SYSTEM(14)   ;* after output of @DATA there's nothing in a queue

Output of this program:

<pre>
    8
    "QWE
    RTY
    "
    0</pre>

## @DATE

Returns the internal date; on some systems, this
differs from the DATE() function in that the variable is set when
program execution starts, whereas the function reflects the current
date:

      CRT @DATE               ;* e.g. 16349
      CRT OCONV(@DATE, 'D')   ;* date represented by 16349 is 04 OCT 2012

## @DAY

Day of month from @DATE (no leading zero included):

       CRT @DAY         ;* 4 for the date used in the sample right above

## @EOF

End of File character from TTY characteristics:

       CRT OCONV(@EOF, 'MX')         ;*  04

## @FILENAME

Current file name (is to be assigned for such operations as [ITYPE](#ITYPE) function call).

## @FOOTER.BREAK

For B options in heading

## @HEADER.BREAK

For B options in heading

## @ID

Used to reference the record-id in a query language
statement:

<pre>
       SORT STOCK BY-DSND @ID
       LIST STOCK WITH @ID = "1000"
       LIST STOCK WITH @ID LIKE AB...</pre>

## @LEVEL

The nesting level of execution statements - non stacked

## @LOCALE

Returns current Locale as jbase_locale

## @LPTRHIGH

Number of lines on the device to which you are printing (that is,
terminal or printer.

## @MONTH

Current Month

## @PARASENTENCE

The last sentence or paragraph that invoked the current process.

## @PATH

Pathname of the current account

## @PID

Returns current process ID

## @RECORD

Entire current record

## @SELECTED

Number of elements from the last select list - Non stacked.

### EXAMPLE

       proc_fname = SYSTEM(1027)
       OPEN proc_fname TO proc_file ELSE STOP 201, "PROC"
       SELECT proc_file TO proc_list
       CRT @SELECTED                                 ;* 0 - this is BASIC select
       EXECUTE 'SELECT ' : proc_fname : ' TO 9'
       CRT @SELECTED                                 ;* 0 - that's not default list
       EXECUTE 'SELECT ' : proc_fname
       CRT @SELECTED                                 ;* number of active sessions

## @TERMTYPE

The Terminal type

## @TIME

Returns the internal time - on some systems, this differs from the
TIME function in that the variable is set when program execution
starts, whereas the function reflects the current time.

### EXAMPLE

       MSLEEP 3000
       CRT @TIME, TIME()     ;*  e.g. 26359   26362

## @TIMEZONE

As per jBASE Timezone

## @TTY

Returns the terminal port name.

## @UID

Returns information from ROOT.THREAD for port @user

## @USER.ROOT, @USER.THREAD and @USERSTATS

The use of the @USER.ROOT command allows a jBC program to store and
retrieve a string of up to 63 bytes that is unique to that user. The
intention is to really "publish" information that other programs can
find.

### For example:

       @USER.ROOT = "Temenos T24 Financials"
       .....
       PRINT "root user declaration is" : @USER.ROOT

See attribute &lt;28&gt;, USER_PROC_USER_ROOT, in the section
"Layout of user record"

The @USER.THREAD is similar except a value exists for each PERFORM
level. So one program can set/retrieve it but if the program does a
PERFORM of a second program then the second program gets a different
set of values.

See attribute &lt;52&gt;, USER_PROC_USER_THREAD, in the section "Layout of user
record"

The @USERSTATS allows a program to retrieve all sorts of miscellanous
information about itself. For example if a program wants to find out
how many database I/O's it performed it could do this:

    INCLUDE JBC.h
       info1 = @USERSTATS
       read1 = info1<USER_PROC_STATS_READ>
       EXECUTE 'COUNT fb1 WITH *A1 EQ "x"'
       info2 = @USERSTATS
       read2 = info2<USER_PROC_STATS_READ>
       PRINT "The COUNT command took " : (read2-read1) : " READs from the database"

So a program can set a user-definable string to whatever value it likes,
up to 63 bytes, and other programs can use various methods (see "User
Information Retrieval" below) to access this data.

### User Information Retrieval

There are 3 ways of finding information about one or more users on a
TAFC system:

1. Using the @USER.ROOT, @USER.THREAD and @USERSTATS variables in your jBC
   code you can find information about yourself. You cannot find
   information about other users.

2. The "WHERE (V" command can be used to display the @USER.ROOT and
   @USER.THREAD data for specified users.

3. Using some jBC code you can find out lots of information about each
   user on the system. This is exactly the mechanism that the WHERE
   command uses. For example to display all users logged on you could
   write this.

### Example:

    INCLUDE JBC.h
       * Open the special jEDI file to access the user information.
       OPEN SYSTEM(1027) TO PROC ELSE STOP 201,SYSTEM(1027)
       SELECT PROC
       * For each user logged on read in their user information
       LOOP WHILE READNEXT key DO
           READ rec FROM PROC, key THEN
              PRINT "Port " : rec<USER_PROC_PORT_NUMBER> :   \
                 " is logged on by user " : rec<USER_PROC_ACCOUNT>
          END
       REPEAT

### Layout of user record

The information retrieved by either the READ in the above example
or the  @USERSTATS is the same and is as follows.

The first 40 attributes are data attributes that correlate to the
entire   user. Attributes 41 onwards are multi-valued and have one
value per program being PERFORM'ed by that user

All the numbers below can be replaced by symbolic references in
JBC.h, look for those that begin from "USER\_PROC\_".

&lt;1&gt; The port number

&lt;2&gt; The number of programs running in this port.

&lt;3&gt; Time the user started in Universal Co-ordinated Time or UTC (not a
 dyslexic mistake). This is raw UNIX time. You can convert this to TAFC
 internal time format using the U0FF0 conversion or to internal date
 format using the U0FF1 conversion.

&lt;4&gt; The process ID

&lt;5&gt; Account name

&lt;6&gt; User name. Normally the operating system name.

&lt;7&gt; Terminal name in TAFC format

&lt;8&gt; Terminal name in Operating system format.

&lt;9&gt; Database name

&lt;10&gt; TTY device name

&lt;11&gt; Language name.

&lt;12&gt; Time in UTC the listening thread last found the thread alive.

&lt;13&gt; Amount of heap space memory in free space chain on a process wide
basis. Not real-time, only updated every 15 seconds.

&lt;14&gt; Amount of heap space memory in use on a process wide basis. Not
real-time , only updated every 15 seconds

&lt;15&gt; Thread type as an internal integer.

&lt;16&gt; Type of thread as a text string.

&lt;17&gt; License counters

&lt;18&gt; Number of OPENs performed.

&lt;19&gt; Number of READs performed.

&lt;20&gt; Number of WRITE's performed.

&lt;21> Number of DELETE's performed

&lt;22> Number of CLEARFILE's performed

&lt;23> Number of PERFORM/EXECUTE's performed.

&lt;24> Number of INPUT's performed.

&lt;25> Not used.

&lt;26> Number of jBASE files the application thinks it has open at the
moment.

&lt;27> Number of jBASE files actually opened by the operating system
at the moment.

&lt;28> Any data set by the application using @USER.ROOT

&lt;29> Process Identifier. A string created by the operating system to
identify the process. It is O/S specific. Currenly on IBM i-series
platform only.

&lt;30> to &lt;40> Reserved.

Attributes 41 onward are multi-valued, one value per perform level,
and there are &lt;2> perform levels active.

&lt;41,n> Program name and command line arguments.

&lt;42,n> The line number in jBC the program is currently executing.

&lt;43,n> The source name in jBC the program is currently executing.

&lt;44,n> Not used.

&lt;45,n> Not used.

&lt;46,n> Status of program execution as a readable text string.

&lt;47,n> Status of program execution as an internal integer.

&lt;48,n> User CPU time . Depending upon the hardware this will be either
for the entire process or just the single thread.

&lt;49,n> System CPU time. Depending upon the hardware this will be either
for the entire process or just the single thread.

&lt;50,n> User CPU time used by any external child processes it might have
spawned.

&lt;51,n> System CPU time used by any external child processes it might
have spawned.

&lt;52,n> Any data set by the application using @USER.THREAD

# jBC Functions and Statements (@ - E)

## @

<a name="@"/>

Use the @ function to position the cursor to a specific point on the
terminal screen

### COMMAND SYNTAX

    @ (col{,row})

### SYNTAX ELEMENTS

**col** and **row** can be any expression that evaluates to a numeric
value.

**col** specifies, to which column on the screen the cursor should be
moved.

**row** specifies which row (line) on the screen to position the
cursor.

Specifying col on its own will locate the cursor to the required
column on whichever row it currently occupies.

### NOTES

When specified values exceed either of the physical limits of the
current terminal, then unpredictable results will occur.

The terminal address starts at (0,0), that being the top left hand
corner of the screen.

Cursor addressing will not normally work when directed at a printer.
If you wish to build printer independence into your programs, achieve
this by accessing the terminfo database through the SYSTEM () function.

### EXAMPLE

       FOR I = 1 TO 5
          CRT @(5, I) : "*" :
       NEXT I
       Home = @(0,0) ;* Remember the cursor home position
       CRT Home: "Hi honey, I'm HOME!" :

### EXAMPLE 2

Here the screen will be drawn, parts of it redrawn and then cleared:

       size_x = SYSTEM(2) - 5 ; size_y = SYSTEM(3) - 5
       info_x = 1  ;  info_y = size_y + 1
       DIM the_screen(size_x, size_y)
       CRT @(-1)
       MAT the_screen = '*'
       left_offset = 1
       GOSUB DRAW.SCREEN
       MAT the_screen = '#'
       left_offset = INT(size_x / 2)
       GOSUB DRAW.SCREEN
       hole_x = 5  ;  hole_y = 5  ;  hole_len = 5
       GOSUB MAKE.HOLE
       hole_x = left_offset - 5  ;  hole_y = 10  ;  hole_len = 20
       GOSUB MAKE.HOLE
       CRT @(info_x, info_y) : "That's all folks!" : @(-3)
                      ;* -3 clears all to the end of line
       *
       STOP
       *
       DRAW.SCREEN:
          CRT @(info_x, info_y) : 'Drawing ' : the_screen(1, 1) : "'s..."
          FOR i = left_offset TO size_x
             FOR j = 1 TO size_y
                CRT @(i, j) : the_screen(i, j):
             NEXT j
          MSLEEP(100) ;* 0.1 sec
          NEXT i
          MSLEEP(2000)
          RETURN
       *
       MAKE.HOLE:
          CRT @(info_x, info_y) : 'Making a hole at ' : hole_x : '/' : hole_y
          CRT @(hole_x, hole_y) : STR(' ', hole_len)
          MSLEEP(2000)
          RETURN
       END

## @ (SCREENCODE)

Use @(SCREENCODE) to output control sequences according to the
capabilities of the terminal

### COMMAND SYNTAX

    @ (ScreenCode)

### SYNTAX ELEMENTS

Control sequences for special capabilities of the terminal are achieved
by passing a negative number as its argument. ScreenCode is therefore
any expression that evaluates to a negative argument.

### NOTES

The design of TAFC allows you to import code from many older systems.
As these systems have traditionally not co-ordinated the development of
this function they expect different functionality in many instances. In
the following table, you should note that different settings of the
JBCEMULATE environment variable would elicit different functionality
from this function.

| Emulation | Code  | Function                                       |
|-----------|-------|------------------------------------------------|
| all       |  -1   | clear the screen and home the cursor           |
| all       |  -2   | Home the cursor                                |
| all       |  -3   | clear screen from the cursor to the end of the |
|           |       | screen                                         |
| all       |  -4   | clear screen from cursor to the end of the     |
|           |       | current screen line                            |
| ros       |  -5   | turn on character blinking                     |
| ros       |  -6   | turn off character blinking                    |
| ros       |  -7   | turn on protected field mode                   |
| ros       |  -8   | turn off protected field mode                  |
| all       |  -9   | move the cursor one character to the left      |
| all       | -10   | move the cursor one row up the screen          |
| ros       | -11   | turn on the cursor (visible)                   |
| ros       | -11   | enable protect mode                            |
| ros       | -12   | turn off the cursor (invisible)                |
| ros       | -12   | disable protect mode                           |
| ros       | -13   | status line on                                 |
| ros       | -13   | turn on reverse video mode                     |
| ros       | -14   | status line off                                |
| ros       | -14   | turn off reverse video mode                    |
| ros       | -15   | move cursor forward one character              |
| ros       | -15   | turn on underline mode                         |
| ros       | -16   | move cursor one row down the screen            |
| ros       | -16   | turn off underline mode                        |
| all       | -17   | turn on the slave (printer) port               |
| all       | -18   | turn off the slave (printer) port              |
| ros       | -19   | dump the screen to the slave port              |
| ros       | -19   | move the cursor right one character            |
| ros       | -20   | move the cursor down one character             |
| ros       | -311  | turn on the cursor (visible)                   |
| ros       | -312  | turn off the cursor (invisible)                |
| ros       | -313  | turn on the status line                        |
| ros       | -314  | turn off the status line                       |

If a colour terminal is in use, -33 to -64 will control colours.

The codes from -128 to -191 control screen attributes. Where Bit 0 is
least significant, you may calculate the desired code by setting Bit
7 and Bits 0-5:

| Bit Values | Description                   |
|------------|-------------------------------|
| Bit 0      | dimmed mode when set to 1     |
| Bit 1      | flashing mode when set to 1   |
| Bit 2      | reverse mode when set to 1    |
| Bit 3      | blanked mode when set to 1    |
| Bit 4      | underline mode when set to 1  |
| Bit 5      | bold mode when set to 1       |
| Bit 7      | always set to 1               |

Thus, reverse and flashing mode is -134.

To turn off all effects use -128.

### EXAMPLE

       CRT @(-1):@(30):@(52):'jBASE Heading':@(-128):
       CRT @(5,5):@(-4):'Prompt: ': ; INPUT Answer

## ABORT

<a name="ABORT"/>

The ABORT statement terminates the current running program and the
program that called it.

### COMMAND SYNTAX

    ABORT {message.number {, expression ...}}

### SYNTAX ELEMENTS

The optional message.number provided with the statement must be a
numeric value, which corresponds to a record key in the TAFC error
message file.

A single expression or a list of expression(s) may follow the
message.number. Where more than one expression is listed, they must be
delimited by the use of the comma character. The expression(s)
correspond to the parameters that need passing to the error file
record to print it.

The optional message.number and expression(s) given with the command
are parameters or resultants provided as variables, literal strings,
expressions, or functions.

### NOTES

Use this statement to terminate the execution of a jBC program together
with any calling program. It will then optionally display a message,
and return to the shell prompt.

The error file holds the optional message displayed on terminating the
program. For successful printing of the message, parameters such as
linefeeds, clearscreen, date and literal strings may also be required.
Setting the Command Level Restart option can alter operation of this
command.

### EXAMPLE

    * Open a file with random name (just to make sure that it doesn't exist)
       V.FNAME = ''
       FOR V.J = 1 TO 8
          V.RND = RND(26) + 65
          V.FNAME := CHAR(V.RND)        ;* A...Z
       NEXT V.J
       OPEN V.FNAME TO F.RAND ELSE ABORT 201, V.FNAME

Sample program output:

<pre>
     &lowast;&lowast;&lowast; Error [ 201 ] &lowast;&lowast;
    Unable to open file XCICLJPH</pre>

## ABS

<a name="ABS"/>

ABS function returns the absolute value of a number or an expression that
evaluates to a number.

### COMMAND SYNTAX

    ABS(expression)

### SYNTAX ELEMENTS

**expression** can be of any form that should evaluate to a numeric.
The ABS function will then return the absolute value of this
expression.

### EXAMPLES

       CRT ABS(10 - 15)

Displays the value 5.

       PositiveVar = ABS(100 - 200)

Assigns the value 100 to the variable PositiveVar.

## ABSS

<a name="ABSS"/>

Use the ABSS function to return the absolute values of all the elements
in a dynamic array. If an element in the dynamic array is null, it
returns null for that element.

### COMMAND SYNTAX

    ABSS(dynamic.array)

### EXAMPLE

       V.BEFORE = 500: @VM: 400: @VM: 300 :@SM: 200 :@SM: 100
       V.AFTER = SUBS(V.BEFORE, REUSE(300))     ;* decrease each element by 300
       CRT OCONV( ABSS(V.AFTER), 'MCP' )        ;*  200]100]0\100\200

## ADDS

<a name="ADDS"/>

Use ADDS function to create a dynamic array of the element-by-element addition
of two dynamic arrays. Added to each element of array1 is the
corresponding element of array2, which returns the result in the
corresponding element of a new dynamic array. If an element of one
array has no corresponding element in the other array, it returns the
existing element. If an element of one array is the null value, it
returns null for the sum of the corresponding elements.

### COMMAND SYNTAX

    ADDS(array1, array2)

### EXAMPLE

       Array1 = 2 :@VM: 4 :@VM: 6 :@SM: 10
       Array2 = 1 :@VM: 2: @VM: 3 :@VM: 4
       PRINT OCONV( ADDS(Array1, Array2), 'MCP' )   ;*  3]6]9\10]4

## ALPHA

<a name="ALPHA"/>

The ALPHA function is used to check if the expression consists entirely of
alphabetic characters.

### COMMAND SYNTAX

    ALPHA(expression)

### SYNTAX ELEMENTS

Returns 1 if the expression consists entirely of alphabetic
characters, else returns 0.

### INTERNATIONAL MODE

When using the ALPHA function in International Mode it determines the
properties of each character in the expression according to the Unicode
Standard, which in turn describes whether the character is alphabetic
or not.

### EXAMPLE

       V.STRING = 'AWERC'
    * check if there are only alphabetic characters
       CRT ALPHA(V.STRING)        ;* 1
    * add number to the end
       V.STRING := 1   ; CRT V.STRING    ;* AWERC1
    * check again if there are only alphabetic characters
       CRT ALPHA(V.STRING)        ;* 0

## ANDS

<a name="ANDS"/>

Use the ANDS function to create a dynamic array of the logical AND of
corresponding elements of two dynamic arrays.

Each element of the new dynamic array is the logical AND of the
corresponding elements of array1 and array2. If an element of one
dynamic array has no corresponding element in the other dynamic array,
it returns a false (0) for that element.

If both corresponding elements of array1 and array2 are null, it returns
null for those elements. If one element is the null value and the other
is zero or an empty string, it returns false for those elements.

### COMMAND SYNTAX

    ANDS(array1, array2)

### EXAMPLE

        A = 1 :@SM: 4 :@VM: 4 :@SM: 1
        B = 1 :@SM: 1 - 1 :@VM: 2
        PRINT OCONV( ANDS(A, B), 'MCP' )    ;*  1\0]1\0

## ASCII

<a name="ASCII"/>

The ASCII function converts all the characters in the expression from
the EBCDIC character set to the ASCII character set.

### COMMAND SYNTAX

    ASCII(expression)

### SYNTAX ELEMENTS

The expression may return a data string of any form. The function will
then assume that the characters are all members of the EBCDIC character
set and translate them using a character map. The original expression
is unchanged while the returned result of the function is now the ASCII
equivalent.

### EXAMPLE

Create the file test.txt in hex editor containing the following characters (in hex):

<pre>
    C8 85 93 93 96 40 91 C2 C3</pre>

Run the following program:

       OSREAD the_line FROM 'test.txt' ELSE NULL
       CRT ASCII(the_line)

Output:

<pre>
    Hello jBC</pre>

## ASSIGNED

<a name="ASSIGNED"/>

The ASSIGNED function is used to determine whether a variable has an
assigned value or not.

### COMMAND SYNTAX

    ASSIGNED(variable)

### SYNTAX ELEMENTS

ASSIGNED returns 1 if the variable has an assigned value
before the execution of this statement. If the variable has no
assigned value then the function returns 0.

### NOTES

Provision of this function is due to its implementation in older
versions of the language. You are advised to program in such a way,
to avoid using this statement.

See also: [UNASSIGNED](#UNASSIGNED)

### EXAMPLE

       COMMON /MY.COMM/ V.VAR1
       CRT ASSIGNED(V.VAR1)   ;* always 1 if "named_common = zero"
                              ;* (e.g. for prime emulation)
       CRT V.VAR1             ;* 0 at the first run, YES at the second
       CRT ASSIGNED(V.VAR2)   ;* 0
       V.VAR1 = 'YES'
       V.VAR2 = 'NO'

## BITAND

<a name="BITAND"/>

Use the BITAND function to perform the bitwise AND comparison of two
integers specified by numeric expressions.

### SYNTAX

    BITAND(expression1, expression2)

### DESCRIPTION

The bitwise AND operation compares two integers bit by bit. It returns
a bit of 1 if both bits are 1; else, it returns a bit of 0.

If either expression1 or expression2 evaluates to the null value, null
is returned.

Non integer values are truncated before the operation is performed.

The BITAND operation is performed on a 32-bit twos-complement word.

### NOTE

Differences in hardware architecture can make the use of the high-order
bit non portable.

### EXAMPLE

        PRINT BITAND(6,12)
        * The binary value of 6 = 0110
        * The binary value of 12 = 1100

This results in 0100, and the following output is displayed:

<pre>
    4</pre>

## BITCHANGE

<a name="BITCHANGE"/>

BITCHANGE toggles the state of a specified bit in the local bit table,
and returns the original value of the bit.

### COMMAND SYNTAX

    BITCHANGE(table_no)

### SYNTAX ELEMENTS

table_no specifies the position in the table of the bit to be changed.

### NOTES

For each process, it maintains a unique table of 128 bits (numbered 1
to 128) and treats each bit in the table as a two-state flag - the
value returned will always be zero or one.

BITCHANGE returns the value of the bit before it was changed. You can
therefore check and set (or reset) a flag in one step.

BITCHANGE also provides some special functions if you use one of the
following table_no values:

|Code|  Description                                          |
|----|-------------------------------------------------------|
|-1  |  toggles (enables/disables) the BREAK key Inhibit bit.|
|-2  |  toggles (enables/disables) the Command Level Restart |
|    |  feature.                                             |
|-3  |  toggles (enables/disables) the Break/End Restart     |
|    |  feature.                                             |

### EXAMPLE

        OLD.VAL = BITCHANGE(100)
        CRT OLD.VAL

If bit 100 in the table is zero, it sets to one and displays zero;
the reverse will apply if set to one.

## BITCHECK

<a name="BITCHECK"/>

BITCHECK returns the current value of a specified bit from the local
bit table.

### COMMAND SYNTAX

    BITCHECK(table_no)

### SYNTAX ELEMENTS

table_no specifies the position in the table of the bit for checking.

### NOTES

For each process, it maintains a unique table of 128 bits (numbered 1
to 128) and treats each bit in the table as a two-state flag - the
value returned will always be zero or one.

## BITLOAD

<a name="BITLOAD"/>

BITLOAD assigns all values in the local bit table, or retrieves all the
values.

### COMMAND SYNTAX

    BITLOAD({ bitstring })

### SYNTAX ELEMENTS

bit-string is an ASCII string of characters, which represent a
hexadecimal value. It is interpreted as a bit pattern and used to
assign values to the table from left to right. Assignment stops
at the end of the string or when a non-hexadecimal character
is found.

If the string represents less than 128 bits, the remaining bits in the
table are reset to 0 (zero).

If bit-string is omitted or evaluates to null, an ASCII hex character
string is returned, which defines the value of the table. Trailing
zeroes in the string are truncated.

### NOTES

A unique table of 128 bits (numbered 1 to 128) is maintained for each
process. Each bit in the table is treated as a two-state flag - the
value will always be 0 (zero) or 1.

### EXAMPLE 1

    VALUE.NEW = "0123456789ABCDEF"
    VALUE.OLD = BITLOAD(X)

Loads the bit table with the value of ASCII hex string NEW.VALUE
After assignment, the contents of the bit table is:

<pre>
    0000 0001 0010 0011
    0100 0101 0110 0111
    1000 1001 1010 1011
    1100 1101 1110 1111
    0000 0000 0000 0000
    0000 0000 0000 0000
    0000 0000 0000 0000
    0000 0000 0000 0000</pre>

**NOTE:** that all values beyond the 64th bit have been reset to 0 (zero).

### EXAMPLE 2

    TABLE.VALUE = BITLOAD()

Loads variable TABLE.VALUE with the hexadecimal values of the bit table

## BITNOT

<a name="BITNOT"/>

Use the BITNOT function to return the bitwise negation of an integer
specified by any numeric expression.

### COMMAND SYNTAX

    BITNOT(expression)

### DESCRIPTION

If expression evaluates to the null value, null is returned.

Non integer values are truncated before the operation is performed.
The BITNOT operation is performed on a 32-bit twos-complement word.

**NOTE:** Differences in hardware architecture can make the use of the
high-order bit non portable.

### EXAMPLE

    CRT BITNOT(6)     ;*  4294967289

Explanation of this example:

<pre>
    6 (decimal) = 110 (binary)
    Invert every bit (32-bit representation): 11111111111111111111111111111001
    Convert to decimal: 4294967289</pre>

## BITOR

<a name="BITOR"/>

Use the BITOR function to perform the bitwise OR comparison of two
integers specified by numeric expressions.

### COMMAND SYNTAX

    BITOR(expression1, expression2)

### DESCRIPTION

The bitwise OR operation compares two integers bit by bit. It returns
the bit 1 if the bit in either or both numbers is 1; else, it returns
the bit 0.

If either expression1 or expression2 evaluates to the null value, null
is returned.

Non integer values are truncated before the operation is performed.

The BITOR operation is performed on a 32-bit twos-complement word.

**NOTE:** Differences in hardware architecture can make the use of the
high-order bit non portable.

### EXAMPLE

       PRINT BITOR(6,12)
    * Binary value of 6 = 0110
    * Binary value of 12 = 1100

This results in 1110, and the following output is displayed:

<pre>
    14</pre>

## BITRESET

<a name="BITRESET"/>

BITRESET resets the value of a specified bit in the local bit table to
zero and returns the previous value of the bit.

### COMMAND SYNTAX

    BITRESET(table_no)

### SYNTAX ELEMENTS

table_no specifies the position in the table of the bit for reset. If
table_no evaluates to zero, it resets all elements in the table to
zero and returns the value zero.

### NOTES

For each process, it maintains a unique table of 128 bits (numbered 1
to 128) and treats each bit in the table as a two-state flag - the
value returned will always be zero or one.

BITRESET returns the previous value of the bit - you can reset and
check a flag in one step.

BITRESET also provides some special functions if you use one of the
following table_no values:

|Code|  Description                             |
|----|------------------------------------------|
|-1  | resets the BREAK key Inhibit bit.        |
|-2  | resets the Command Level Restart feature.|
|-3  | resets the Break/End Restart feature.    |

See also: [BITSET](#BITSET)

### EXAMPLE

        OLD.VALUE = BITRESET(112)
        PRINT OLD.VALUE

If table entry 112 is one, it returns a value of one, resets bit 112
to 0, and prints one. If table entry 112 is zero, returns a value of
0, and prints 0.

## BITSET

<a name="BITSET"/>

BITSET sets the value of a specified bit in the bit table to one and
returns the value of the bit before it was changed.

### COMMAND SYNTAX

    BITSET(table_no)

### SYNTAX ELEMENTS

table_no specifies the bit to be SET. If table_no evaluates to zero,
it sets all elements in the table to one and the returned value is one.

### NOTES

For each purpose, it maintains a unique table of 128 bits (numbered 1
to 128) and treats each bit in the table as a two-state flag - the
value returned will always be zero or one.

BITSET returns the previous value of the bit - you can check and set a
flag in one step.

BITSET also provides some special functions if you use one of the
following table_no values:

|Code|  Description                             |
|----|------------------------------------------|
|-1  | sets the BREAK key Inhibit bit           |
|-2  | sets the Command Level Restart feature   |
|-3  | sets the Break/End Restart feature       |

See also: [BITRESET](#BITRESET)

### EXAMPLE

        OLD.VALUE = BITSET(112)
        PRINT OLD.VALUE

If table entry 112 is zero, returns a value of zero, sets bit 112 to
one, and prints zero. If table entry 112 is one, returns a value of
one, and prints one.

## BITTEST

<a name="BITTEST"/>

Use the BITTEST function to test the bit number of the integer
specified by expression.

### COMMAND SYNTAX

    BITTEST(expression, bit#)

### NOTE

This function is reserved for future use and hadn't yet been implemented.

## BITXOR

<a name="BITXOR"/>

Use the BITXOR function to perform the bitwise XOR comparison of two
integers specified by numeric expressions. The bitwise XOR operation
compares two integers bit by bit. It returns a bit 1 if only one of
the two bits is 1; else, it returns a bit 0.

### COMMAND SYNTAX

    BITXOR(expression1, expression2)

### DESCRIPTION

If either expression1 or expression2 evaluates to the null value,
null is returned.

Non integer values are truncated before the operation is performed.

The BITXOR operation is performed on a 32-bit twos-complement word.

**NOTE:** Differences in hardware architecture can make the use of
the high-order bit nonportable.

### EXAMPLE

       PRINT BITXOR(6,12)
    * Binary value of 6 = 0110
    * Binary value of 12 = 1100

This results in 1010, and the following output is displayed:

<pre>
    10</pre>

## BREAK

<a name="BREAK"/>

Terminate the currently
executing loop. The EXIT statement is functionally equivalent to
the BREAK statement.

### EXAMPLE

       V.ARRAY = ''
       FOR V.I = 1 TO 10
          IF V.I EQ 4 THEN BREAK
          V.ARRAY<-1> = V.I
       NEXT V.I
       CRT FMT(V.ARRAY, 'MCP') ;* 1^2^3

### NOTE

BREAK terminates the innermost loop; if it's used outside a loop construct
it's ignored. The compiler will issue warning
message 44, and ignore the statement.

### EXAMPLE

       V.ARRAY = ''  ; V.J = 0
       LOOP
          V.J ++
       WHILE V.J LT 3 DO
          FOR V.I = 1 TO 10
    	     IF V.I EQ 4 THEN BREAK
             V.ARRAY<-1> = V.I
          NEXT V.I
       REPEAT
       BREAK
       CRT FMT(V.ARRAY, 'MCP') ;* 1^2^3^1^2^3

Compiler output:

<pre>
    [warning	(44)] "test2.b", 9 (offset 7) :
    BREAK/EXIT is invalid outside a FOR or LOOP - Ignored
    test2.c</pre>

## BREAK ON/OFF

Enables or disables the BREAK key. In UNIX terms, the BREAK key is known more commonly as the interrupt
sequence intr defined by the stty command.

### COMMAND SYNTAX

    BREAK ON / BREAK OFF

### EXAMPLE

       BREAK OFF
       CRT "Next 5 seconds Ctrl-C makes no action"
       MSLEEP(5000)
       BREAK ON
       CRT "And next 5 seconds Ctrl-C invokes debugger"
       MSLEEP(5000)

Output (user is to try to press Ctrl-C at both prompts):

<pre>
    Next 5 seconds Ctrl-C makes no action
    And next 5 seconds Ctrl-C invokes debugger
    Interrupt signal
    Source changed to .\test2.b
    0009    MSLEEP(5000)
    jBASE debugger-></pre>

## BYTELEN

<a name="BYTELEN"/>

The BYTELEN function will return the length of the expression as the
number of bytes rather than the number of characters.

### COMMAND SYNTAX

    BYTELEN(expression)

### SYNTAX ELEMENTS

The expression is to be a string. The BYTELEN function
will then return the byte count of the expression.

### EXAMPLE

       V.UTF = 'ABCDEF' \
             : CHAR(353) : CHAR(352) : CHAR(269) : CHAR(268) : CHAR(263) \
             : CHAR(262) : CHAR(382) : CHAR(381) : CHAR(273) : CHAR(272)
       V.LEN = LEN(V.UTF)  ;  CRT V.LEN  ;* 16
       CRT BYTELEN(V.UTF)                ;* 26
    *
    * [] takes characters, not bytes, so output is:
    * 41 42 43 44 45 46 C5A1 C5A0 C48D C48C C487 C486 C5BE C5BD C491 C490
       FOR V.I = 1 TO V.LEN
          CRT FMT(V.UTF[V.I,1], 'MX') : ' ' :
       NEXT V.I

### NOTES

The BYTELEN function will always return the actual byte count for the
expression; irrespective of the International Mode in operation at
the time. This compares with the LEN function, which will return a
character count. The character count may differ from the byte count
when processing in International Mode.

## CacheBucketList

<a name="CacheBucketList"/>

The CacheBucketList function will return a list of all buckets in the
cache. The list is represented as a string containg the bucket names
joined together via a given delimiter.

### COMMAND SYNTAX

    CacheBucketList(delimiter)

### EXAMPLE

    INCLUDE JBC.h
    CachePut('bucket1', 'item1', 'value1')
    CachePut('bucket2', 'item1', 'value1')
    buckets = CacheBucketList(@AM)
    CRT "First bucket: " : buckets<1>
    CRT "Second bucket: " : buckets<2>

The output is:

<pre>
    First bucket: bucket1
    Second bucket: bucket2</pre>

### NOTES

This function does not affect the bucket statistics.

## CacheClear

<a name="CacheClear"/>

The CacheClear function will delete all items in a bucket of the cache.

### COMMAND SYNTAX

    CacheClear(bucketname)

### EXAMPLE

    INCLUDE JBC.h
    CachePut('ACCOUNT', 'username', 'customer1')
    CRT '[': CacheGet('ACCOUNT', 'username'):']'
    CacheClear('ACCOUNT')
    CRT '[': CacheGet('ACCOUNT', 'username'):']'

The output is:

<pre>
    [customer1]
    []</pre>

### NOTES

The CacheClear() function also resets the statistics of a bucket.

## CacheClearAll

<a name="CacheClearAll"/>

The CacheClearAll function will clean all buckets in the cache.

### COMMAND SYNTAX

    CacheClearAll()

### EXAMPLE

    INCLUDE JBC.h
    CachePut('ACCOUNT', 'username', 'customer1')
    CRT '[': CacheGet('ACCOUNT', 'username'):']'
    CacheClearAll()
    CRT '[': CacheGet('ACCOUNT', 'username'):']'

The output is:

<pre>
    [customer1]
    []</pre>

### NOTES

The CacheClearAll() function also resets the statistics of all buckets.

## CacheClearStats

<a name="CacheClearStats"/>

The CacheClearStats function will reset statistics of the specified
bucket in the cache.

### COMMAND SYNTAX

    CacheClearStats()

### EXAMPLE

    INCLUDE JBC.h
    CacheClearStats('bucket1')

### NOTES

This function does change items in the bucket.

## CacheDelete

<a name="CacheDelete"/>

The CacheBucketList function will delete an item from a bucket in
the cache.

### COMMAND SYNTAX

    CacheDelete(bucket, item)

### EXAMPLE

    INCLUDE JBC.h
    CacheDelete('bucket1', 'item1')
    CachePut('bucket2', 'item1', 'value1')
    buckets = CacheBucketList(@AM)
    CRT "First bucket: " : buckets<1>
    CRT "Second bucket: " : buckets<2>

The output is:

<pre>
    First bucket: bucket1
    Second bucket: bucket2</pre>

### NOTES

This function does not affect statistics of the bucket.

## CacheExists

<a name="CacheExists"/>

The CacheExists function will return "1" if a item exists in the
bucket or "0" otherwise.

### COMMAND SYNTAX

    CacheExists(bucket, item)

### EXAMPLE

    INCLUDE JBC.h
    CRT CacheExists('bucket1', 'item1')
    CachePut('bucket1', 'item1', 'value1')
    CRT CacheExists('bucket1', 'item1')
    CRT CacheExists('bucket2', 'item1')

The output is:

<pre>
    0
    1
    0</pre>

### NOTES

The CacheExists() function also returns "0" if the bucket itself
does not exist in the cache. Also this function does not affect
statistics of the bucket.

## CacheGet

<a name="CacheGet"/>

The CacheExists function will return a value of an item from the
specified bucket of the cache. If an item is not in existance it
returns an empty string.

### COMMAND SYNTAX

    CacheGet(bucket,  item)

### EXAMPLE

    INCLUDE JBC.h
    CRT '[': CacheGet('bucket1', 'item1'):']'
    CachePut('bucket1', 'item1', 'value1')
    CRT '[': CacheGet('bucket1', 'item1'):']'

The output is:

<pre>
    []
    [value1]</pre>

### NOTES

This function increments CACHE_GETS statistics counter of the bucket.
If an item exists in the bucket the function increments CACHE_HITS
counter of this bucket.

## CacheGetOption

<a name="CacheGetOption"/>

The CacheGetOption function will return an option of the bucket.

### COMMAND SYNTAX

    CacheGetOption(bucket,  option)

### EXAMPLE

    INCLUDE JBC.h
    CRT 'CACHE_MAX_SIZE: ': CacheGetOption('bucket1', CACHE_MAX_SIZE)
    CRT 'CACHE_PURGE_THRESHOLD: ': CacheGetOption('bucket1', CACHE_PURGE_THRESHOLD)
    CachePut('bucket1', 'item1', 'value1')
    CRT 'CACHE_MAX_SIZE: ': CacheGetOption('bucket1', CACHE_MAX_SIZE)
    CRT 'CACHE_PURGE_THRESHOLD: ': CacheGetOption('bucket1', CACHE_PURGE_THRESHOLD)

The output is:

<pre>
    CACHE_MAX_SIZE: 0
    CACHE_PURGE_THRESHOLD: 0
    CACHE_MAX_SIZE: 1048576
    CACHE_PURGE_THRESHOLD: 90</pre>

### NOTES

The bucket should exists otherwise this function returns zeros.

The "option" parameter may have following values:

**CACHE_MAX_SIZE**: Bucket maximum size in bytes. By default, the
bucket size is 1048576. If the size reaches this value, the most
outdated data will be purged from the bucket to reduce its size.

**CACHE_PURGE_THRESHOLD**: Percentage (from 1 to 100) of a bucket
size exceeding of which leads to the bucket purging. By default,
it's value is 90. When a bucket size exceeds the
(CACHE_MAX_SIZE * CACHE_PURGE_THRESHOLD / 100) value the most
outdated data will be purged from the bucket to reduce its size.

This function does not affect statistics of the bucket.

## CacheKeyList

<a name="CacheKeyList"/>

The CacheKeyList function will return a list of all item names in the
specified bucket in the cache. The list is represented as a string
containing the item names joined together via a given delimiter.

### COMMAND SYNTAX

    CacheKeyList(bucket, delimiter)

### EXAMPLE

    INCLUDE JBC.h
    CachePut('bucket1', 'item1', 'value1')
    CachePut('bucket1', 'item2', 'value1')
    keys = CacheKeyList('bucket1', @AM)
    CRT 'First name: ':keys<1>
    CRT 'Second name: ':keys<2>

The output is:

<pre>
    First name: item1
    Second name: item2</pre>

### NOTES

This function does not affect statistics of the bucket.

## CachePut

<a name="CachePut"/>

The CacheExists function will put an item to the specified bucket of
the cache.

### COMMAND SYNTAX

    CachePut(bucket, item, value)

### EXAMPLE

    INCLUDE JBC.h
    CachePut('bucket1', 'item1', 'value1')
    CRT '[': CacheGet('bucket1', 'item1'):']'

The output is:

<pre>
    [value1]</pre>

### NOTES

This function increments CACHE_PUTS statistics counter of the bucket.

## CacheSetOption

<a name="CacheSetOption"/>

The CacheSetOption function will set an option of the bucket.

### COMMAND SYNTAX

    CacheSetOption(bucket,  option, value)

### EXAMPLE

    INCLUDE JBC.h
    CacheSetOption('bucket1', CACHE_MAX_SIZE, 100000)
    CacheSetOption('bucket1', CACHE_PURGE_THRESHOLD, 60)

### NOTES

If the bucket does not exist an empty bucket is created and the option
is applied to it.

The "option" parameter may have following values:

**CACHE_MAX_SIZE**: Bucket maximum size in bytes. By default, the
bucket size is 1048576. If the size reaches this value, the most
outdated data will be purged from the bucket to reduce its size.

**CACHE_PURGE_THRESHOLD**: Percentage (from 1 to 100) of a bucket
size exceeding of which leads to the bucket purging. By default,
it's value is 90. When a bucket size exceeds the
(CACHE_MAX_SIZE * CACHE_PURGE_THRESHOLD / 100) value the most
outdated data will be purged from the bucket to reduce its size.

This function does not affect statistics of the bucket.

## CacheStats

<a name="CacheStats"/>

The CacheStats function will return a statistics counter of the
specified bucket in the cache.

### COMMAND SYNTAX

    CacheStats(bucket, counter_id)

### EXAMPLE

    INCLUDE JBC.h
    CachePut('bucket1', 'item1', 'value1')
    CachePut('bucket1', 'item2', 'value2')
    CacheGet('bucket1', 'item1')
    CacheGet('bucket1', 'item3')
    CRT "CACHE_HITS: " : CacheStats('bucket1', CACHE_HITS)
    CRT "CACHE_GETS: " : CacheStats('bucket1', CACHE_GETS)
    CRT "CACHE_PUTS: " : CacheStats('bucket1', CACHE_PUTS)
    CRT "CACHE_SIZE: " : CacheStats('bucket1', CACHE_SIZE)
    CRT "CACHE_NB_ITEMS: " : CacheStats('bucket1', CACHE_NB_ITEMS)

The output is:

<pre>
    CACHE_HITS: 1
    CACHE_GETS: 2
    CACHE_PUTS: 2
    CACHE_SIZE: 12
    CACHE_NB_ITEMS: 2</pre>

### NOTES

The "counter_id" parameter may have following values:

**CACHE_HITS**: Number of successful hits to the bucket.
This counter is incremented by CacheGet function if a requested
item exists in the bucket.

**CACHE_GETS**: Number of reads from the bucket.
This counter is incremented by CacheGet on every call.

**CACHE_PUTS**: Number of writes to the bucket.
This counter is incremented by CachePut on every call.

**CACHE_SIZE**: Total size of the bucket in bytes.
This parameter is calculated by adding the lengths of all items of
the bucket which have a String.

**CACHE_NB_ITEMS**: Number of items in the bucket.

This function does not affect statistics of the bucket.

## CALL

<a name="CALL"/>

The CALL statement transfers program execution to an external
subroutine.

### COMMAND SYNTAX

    CALL {@} subroutine.name {(argument{, argument ... })}

### SYNTAX ELEMENTS

The CALL statement transfers program execution to the subroutine
called subroutine.name, which can be any valid string either quoted
or unquoted.

The CALL @ variant of this statement assumes that subroutine.name
is a variable that contains the name of the subroutine to call.

The CALL statement may optionally pass a number of parameters to the
target subroutine. These parameters can consist of any valid
expression or variable name. If a variable name is used then the
called program may return a value to the variable by changing the
value of the equivalent variable in its own parameter list.

### NOTES

When using an expression to pass a parameter to the subroutine, you
cannot use the built-in functions of jBC (such as COUNT), within the
expression.

An unlimited number of parameters can be passed to an external
subroutine. The number of parameters in the CALL statement must match
exactly the number expected in the SUBROUTINE statement declaring the
external subroutine, otherwise runtime error is raised.

It is not required that the calling program and the external
subroutine be compiled with the same PRECISION. However, any changes
to precision in a subroutine will not persist when control returns
to the calling program.

Variables passed as parameters to the subroutine may not reside in
any COMMON areas declared in the program.

### EXAMPLE

A subroutine:

       SUBROUTINE NUM.INCR(P.NUMBER)
    * increase the parameter
       P.NUMBER ++
       RETURN
    END

A calling program:

       V.ARRAY = 1 :@FM: 2 :@FM: 3 :@FM: 4
       CRT FMT(V.ARRAY, 'MCP')   ;* 1^2^3^4
       V.ARRAY<2> += 1
       CRT FMT(V.ARRAY, 'MCP')  ;* 1^3^3^4 - array element can be processed directly
       CALL NUM.INCR(V.ARRAY<2>)
       CRT FMT(V.ARRAY, 'MCP')   ;* still 1^3^3^4 - passing to a subr doesn't work
       V.VAR = V.ARRAY<2>
       CALL NUM.INCR(V.VAR)
       V.ARRAY<2> = V.VAR
       CRT FMT(V.ARRAY, 'MCP')   ;* now 1^4^3^4 - should use a variable
       V.SUBR = 'NUM.INCR'
       CALL @V.SUBR(V.VAR)       ;* can call a subroutine this way
       CRT V.VAR                 ;* 5
    * Dimensioned array is ok as well
       DIM V.DIM.ARR(3)
       V.DIM.ARR(2) = 'NUM.INCR'
       V.I = 2
       CALL @V.DIM.ARR(V.I) (V.VAR)
       CRT V.VAR        ;* 6
    * Pass by value rather than by reference - variable keeps its value:
       CALL NUM.INCR((V.VAR))
       CRT V.VAR        ;* 6
    * Wrong CALL:
       CALL NUM.INCR(V.VAR, 1)

Output:

<pre>
    1^2^3^4
    1^3^3^4
    1^3^3^4
    1^4^3^4
    5
    6
    6
     &lowast;&lowast; Error [ SUBROUTINE_PARM_ERROR ] &lowast;&lowast;
    'SUBROUTINE NUM.INCR' called with incorrect arguments , Line 1 , Source test2.b
    Trap from an error message, error message name = SUBROUTINE_PARM_ERROR
    Source changed to .\test2.b
    jBASE debugger-></pre>


## CALLC

<a name="CALLC"/>

The CALLC command transfers program control to an external function
(c.sub.name). The second form of the syntax calls a function whose name
is stored in a jBC variable (@var). The program could pass back return
values in variables. CALLC arguments can be simple variables or complex
expressions, but not arrays. Use CALLC as a command or function.

### COMMAND SYNTAX

    CALLC c.sub.name [(argument1[,argument2]...)]

    CALLC @var [(argument1[,argument2]...)]

**Calling a C Program in TAFC**

You must link the C program to TAFC before calling it from a BASIC
program. Perform the following procedure to prepare TAFC for CALLC:

- Write and compile the C program.
- Define the C program call interface
- Build the runtime version of TAFC (containing the linked C program).
- Write, compile, and execute the Basic program

**Calling a Function in Windows NT**

The CALLC implementation in TAFC for Windows NT or Windows 2000 uses
the Microsoft Windows Dynamic Link Library (DLL) facility. This
facility allows separate pieces of code to call one another without
permanently binding together. Linking between the separate pieces
occurs at runtime (rather than compile time) through a DLL interface.

For CALLC, developers create a DLL and then call that DLL from TAFC.

### EXAMPLES

In the following example, the called subroutine draws a circle with
its center at the twelfth row and twelfth column and a radius of 3:

    RADIUS = 3
    CENTER = "12,12"
    CALLC DRAW.CIRCLE(RADIUS,CENTER)

In the next example, the subroutine name is stored in the variable
SUB.NAME, and is indirectly called:

    SUB.NAME = DRAW.CIRCLE
    CALLC @SUB.NAME(RADIUS,CENTER)

The next example uses, CALLC as a function, assigning the return
value of the subroutine PROG.STATUS in the variable RESULT:

    RESULT = CALLC PROG.STATUS

## CALLdotNET

<a name="CALLdotNET"/>

The CALLdotNET command allows BASIC to call any .NET assembly and is
useful when using third party applications.

### COMMAND SYNTAX

    CALLdotNET NameSpaceAndClassName, methodName, param SETTING ret \
               [ON ERROR errStatment]

In order to use CALLdotNET, you need:

- The .NET Framework
- The dotNETWrapper.dll installed somewhere to where your PATH points.

### NOTE

The dotNETWrapper is loaded dynamically at runtime; therefore, a
compiled basic application has no dependencies on the .NET Framework.
Loading the framework takes between 5 and 7 seconds. However, this only
occurs when calling the .NET method for the first time.

### SYNTAX ELEMENTS

NameSpaceAndClassName The "full" NameSpace (e.g., myNameSpace.myClass)

methodName The name of the .NET in this class (e.g., "myMethod")

Param Any parameter (eg DynArray)

### EXAMPLE

In C#:

<pre>
    using System;
    using System.Windows.Forms;
    namespace myNameSpace
    {
	    public class Class1
	    {
		    public string sayHello(string str)
		    {
			    return "Thank you, I received : " + str;
		    }
		    public Class1(){}
	    }
    }</pre>

In VB.NET:

<pre>
    Namespace myNameSpace
      Public Class Class1
          Public Function sayHello(ByVal str As String) As String
            Dim sAnswer As String
            sAnswer = InputBox(str)
            sayHello = sAnswer
          End Function
      End Class
    End Namespace</pre>

Note: Create the .NET project as a 'Class Library'.

If using the visual studio IDE, this option is on selected when
creating a new project:

![.Net Project Creation](data:image/png;base64,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)

If using .NET SDK (instead of the IDE) to compile class libraries
into a 'DLL' file, the  'csc' (C# Compiler) or 'vbc' (Visual Basic
.NET compiler) command can be used from the command line:

<pre>
    csc /out:myNameSpace.dll /target:library sourcefile.cs</pre>

The name of the '.DLL' created must be the same as the 'namespace'
as used in the class library t locate the 'dotNetWrapper.dll' library:

After creating the library, place it in the same private directory as
the application. (i.e. the same directory as the jBC executable that
will call the class) This is a requirement of the .NET paradigm and
not TAFC. The directory should also be in the PATH environment variable.

![DLL Creation](data:image/png;base64,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)

*To call these methods from Basic*:

    CALLdotNET 'myNameSpace.Class1', 'mymethod', p SETTING ret
    CRT ret

### ON ERROR

You can manage any errors, which occur during the call, at the BASIC
level by getting the SYSTEM(0) variable.

This variable can have the following values:

|Code| Description                          |
|----|--------------------------------------|
| 1  | Not a Windows platform               |
| 2  | Cannot load the dotNETWrapper        |
| 3  | Cannot get assembly                  |
| 4  | Cannot get Class                     |
| 5  | Cannot get Method                    |
| 6  | Cannot Create Instance               |
| 7  | Unhandled Error in the .NET library  |

### EXAMPLE

BASIC code using the ON ERROR would look like this:

    PROGRAM testCALLdotNET
        ns.className = ''
        methodName = ''
        param = ''
        CRT "Please enter NameSpace.ClassName : "
        INPUT ns.className
        CRT "Please enter a Method Name : "
        INPUT methodName
        CRT "Please enter a Parameter : "
        INPUT param
        CALLdotNET ns.className, methodName, param SETTING ret \
            ON ERROR GOSUB errHandler
        CRT "Received back from .NET : " : ret
        STOP
    *
    errHandler:
        err = SYSTEM(0)
        BEGIN CASE
        CASE err = 2
           CRT "Cannot find dotNETWrapper.dll"
        CASE err = 3
           CRT "Class " : className : "doesn't exist !"
        CASE err = 5
           CRT "Method " : methodName : "doesn't exist !"
        END CASE
        RETURN

## CALLJ

<a name="CALLJ"/>

The CALLJ command allows BASIC to call a Java method. CALLJ is useful
when using third party applications offering a Java API (for example,
publish and subscribe, messaging, etc.)

### COMMAND SYNTAX

    CALLJ packageAndClassName, [$]methodName, param SETTING ret  \
          [ON ERROR] errStatment

In order to use CALLJ, you need:

- A Java virtual machine
- CLASSPATH environment variable set to point on the class you want to
  invoke

### NOTES

The Java virtual machine is loaded dynamically at runtime, so a
compiled basic application has no dependencies on any Java virtual
machine. By default, the program will search for:

jvm.dll on Windows platforms

libjvm.sl on HP UNIX

libjvm.so for other platforms

Although it is not usually necessary, it is possible to specify a Java
library by setting the JBCJVMLIB environment variable:

Windows:
set JBCJVMLIB=jvm.dll
AIX:
export JBCJVMLIB=libjvm.so

### PERFORMANCE CONSIDERATIONS

The first call to CALLJ carries the overhead of loading the Java
Virtual Machine into memory. Subsequent calls do not have this overhead.
Many additional threads will be created and used by the JVM.

In addition, calls to non static methods carry the overhead of calling
the constructor for the class. Wherever possible, static methods should
be used.

### SYNTAX ELEMENTS

**packageAndClassName** The "full" class name
(e.g., com.jbase.util.utilClass)

**methodName** The name of the Java method in this class
(e.g., "myMethod")

NOTE: If the method is static, you must append a dollay symbol ( $ ) before the name.
It will be removed from the method name before calling it.

**Param** Any parameter (eg DynArray)

### EXAMPLE

In Java:

<pre>
    package mypackage;
//
    public class mytestclass {
        static int i = 0;
        private mytestclass() {
        }
//
        public String mymethod(String s) {
	        return ( "Java Received : " + s ) ;
        }
//
        public static String mystaticmethod(String s) {
  		    i++;
  		    return s + " "  + i;
        }
    }</pre>

To call these methods from jBC:

    CALLJ 'mypackage.mytestclass', 'mymethod', p SETTING ret
    CRT ret
    CALLJ 'mypackage/mytestclass', '$mystaticmethod', p SETTING ret
    CRT ret

### ON ERROR

Use the SYSTEM(0) variable to manage any errors at the BASIC level,
which occur during the call.

This variable can have the following values:

|Value |  Description                  |
|------|-------------------------------|
| 1    | Fatal error creating thread   |
| 2    | Cannot create JVM             |
| 3    | Cannot find class             |
| 4    | Unicode conversion error      |
| 5    | Cannot find method            |
| 6    | Cannot find object constructor|
| 7    | Cannot instantiate object     |

### EXAMPLE

jBC code using the ON ERROR will look like this:

    PROGRAM testcallj
         className = ''
         methodName = ''
         param = ''
         CRT "Please enter a Class Name " :  ;   INPUT className
         CRT "Please enter a Method Name " :  ;  INPUT methodName
         CRT "Please enter a Parameter : "  ; INPUT param
         CALLJ className,methodName, param SETTING ret ON ERROR GOTO errHandler
         CRT "Received batch from Java : " : ret
    RETURN
    *
    errHandler:
         err = SYSTEM(0)
         IF err = 2 THEN
              CRT "Cannot find the JVM.dll !"
              RETURN
         END
         IF err = 3 THEN
              CRT "Class " : className : "doesn't exist !"
              RETURN
         END
    *
         IF err = 5 THEN
      	      CRT "Method " : methodName : "doesn't exist !"
              RETURN
         END
    END

The CALLJ function provides access to a JavaVM from within the BASIC
environment. For it to be able to start a JavaVM (JVM) the
environment needs to know where the JVM is located. Specifically it
needs to know where certain libraries are located.

**WINDOWS**

Windows: looking for 'jvm.dll'

Add "c:\jdk1.6.0_33\jre\bin\server" to the PATH environment variable.

A generic format might be  %JDKDIR%\jre\bin\server.

UNIX

For UNIX it is possible to configure generic symbolic links to make
profiles portable.

Location of JDK	export JDKDIR=/opt/java6

Symbolic link for JRE libs			/opt/java6/jrelib

Symbolic link for JVM library		/opt/java6/jvmlib

Linux

	 /opt/java6/jrelib   -> /opt/java6/jre/lib/amd64

	 /opt/java6/jvmlib   -> /opt/java6/jre/lib/amd64/server

.profile:

Add "/opt/java6/jrelib:/opt/java6/jvmlib" to the LD_LIBRARY_PATH

HP-UX

	 /opt/java6/jrelib   -> /opt/java6/jre/lib/IA64W

	 /opt/java6/jvmlib   -> /opt/java6/jre/lib/IA64W/server

	 .profile:

Add "/opt/java6/jrelib:/opt/java6/jvmlib" to the SHLIB_PATH

AIX (IBM JDK)

	 /opt/java6/jrelib   -> /opt/java6/jre/bin

	 /opt/java6/jvmlib   -> /opt/java6/jre/bin/classic

	 .profile:

Add "/opt/java6/jrelib:/opt/java6/jvmlib" to the LIBPATH

Solaris SPARC

	 /opt/java6/jrelib   -> /opt/java6/jre/lib/sparc

	 /opt/java6/jvmlib   -> /opt/java6/jre/lib/sparc/server

	 .profile:

Add "opt/java6/jrelib:/opt/java6/jvmlib" to the LD_LIBRARY_PATH

Solaris AMD64

	 /opt/java6/jrelib   -> /opt/java6/jre/lib/amd64

	 /opt/java6/jvmlib   -> /opt/java6/jre/lib/amd64/server

	 .profile:

Add "opt/java6/jrelib:/opt/java6/jvmlib" to the LD_LIBRARY_PATH

### EXAMPLES using JVM WITHOUT symbolic links as above:

Linux: looking for 'libjvm.so'

<pre>
    Add 2 directories to LD_LIBRARY_PATH.
    /opt/java6/jre/lib/amd64/server:/opt/java6/jre/lib/amd64</pre>

Solaris: looking for 'libjvm.so'

<pre>
    Add 2 directories to LD_LIBRARY_PATH.
    /opt/java6/jre/lib/sparc/server:/opt/java6/jre/lib/sparc</pre>

HP-UX 11: looking for 'libjvm.sl'

<pre>
    Add 2 directories to SHLIB_PATH.
   /opt/java6/jre/lib/IA64W/server:/opt/java6/jre/lib/IA64W</pre>

### OPTIONS

**JBCJVMLIB**

If the search for the library appears incorrect for your platform, then
you can override it by setting the **JBCJVMLIB** environment variable.

e.g.  `export JBCJVMLIB=jvm.shared_lib`

and then CALLJ will try to locate the library 'jvm.shared_lib' at runtime.

**JBCJVMPOLICYFILE**

You can specify a policy file for the JMV. The policy for a Java
application environment (specifying which permissions are available for
code from various sources) is represented by a Policy object. More
specifically, it is represented by a Policy subclass providing an
implementation of the abstract methods in the Policy class (which is in
the java.security package). You can override it by setting the
JBCJVMPOLICYFILE environment variable.

The source location for the default policy information is:

**WINDOWS**

<pre>
    %TAFC_HOME%\config\policy.all</pre>

**UNIX**

<pre>
    $TAFC_HOME/config/policy.all</pre>

e.g.  "export JBCJVMPOLICYFILE=/usr/jbase/mypolicy.all"

**JBCJVMENCODING**

Internally, the Java virtual machine always operates with data in
Unicode. However, as data transfers to or from the Java virtual
machine, the Java virtual machine converts the data to other encodings.
If the you want to change the default encoding of the JVM on your
platform, then you can override it by setting the JBCJVMENCODING
environment variable.

e.g.  "export JBCJVMENCODING=Cp1257"

**JBCJVMNOOPTS**

Internally, CALLJ is optimized to start the JVM with options (see the
table below). If you do not want to pass these options for the JVM,
then you can override it by setting the **JBCJVMNOOPTS** environment
variable. In this case no more options will be passed to the JVM.

**JBCIBMJDK**

On Linux we assumed that the Sun Java JDK would be used and the JVM
options reflect this. But as they are not compatible with the IBM JDK
you can set the JBCIBMJDK option to allow the running of the IBM JDK
for Linux.

### DEFAULT OPTIONS###

|Platform       |   Parameter                         |
|---------------|-------------------------------------|
|Win32:         |   -Xrs                              |
|Solaris:       |   -XX:+AllowUserSignalHandlers      |
|Linux:         |   -Xrs -XX:+AllowUserSignalHandlers |
|AIX 64 bits:   |   -Xrs -d64                         |
|HPUX 64 bits:  |   -Xrs -XX:+AllowUserSignalHandlers |

**JBCJVMOPT[1..5]**

If the you want to pass some options for the JVM, then set the
JBCJVMOPT[1..5] environment variable

e.g.  "export JBCJVMOPT1=-Xrs"

**JBCJVMOPTS**

Allows many options to be set within one variable.
e.g. export JBCJVMOPTS="-Xrs -Xms256M -Xmx512M"

### KNOWN LIMITATIONS

**HP-UX**

There is a problem with HP-UX due to its dynamic loader. See man
dlopen(3C) for detail of the TLS limitation.

This means that the JVM library must be linked against the calling
program, there are no known problems caused by this.

'ldd progname' lists current external library references and we
need to add libjvm.

The symptom looks like this:

<pre>
    JVM: dl_error [Can't dlopen a library containing Thread Local Storage: libjvm.sl]</pre>

If the program is built with the required link as below then it works.

<pre>
    jbc -Jo callj.b -ljvm -L/opt/java6/jre/lib/IA64W/server</pre>

If the CALLJ statement is inside a subroutine, then the program that
calls the subroutine must be built as above.

## CALLJEE

<a name="CALLJEE"/>

The CALLJEE function will connect to the JRemote Inbound JCA (TOCF/EE)
if not already connected, send the request, and receive the response.
The first invocation of CALLJEE will attempt to open a connection to the
application server. The following environment variables are used during
the open connection phase of the first call:

<pre>
    SET JREMOTE_INBOUND_HOST=127.0.0.1
    SET JREMOTE_INBOUND_PORT=55006</pre>

Subsequent invocations of CALLJEE will use a connection previously opened
by CALLJEE.

### EXAMPLE

    INCLUDE JBC.h
    ACTIVATION = "PRICE"
    ADDINFO = "PART.NUMBER=MC3815-3"
    ERR.CODE = CALLJEE(ACTIVATION, ADDINFO)
    RESULT = ADDINFO

Error codes:

| Code | Description                                             |
|------|---------------------------------------------------------|
| 0    | Action completed successfully                           |
| 1    | Communication error, this connection is no longer valid |
| 2    | Transaction error, the transaction is no longer valid   |
| 101  | Connect error, host not valid                           |
| 102  | Connect error, port not valid                           |


## CALLONEXIT

<a name="CALLONEXIT"/>

The CALLONEXIT function call allows you to specify the name of a
SUBROUTINE to call when the program terminates.

### COMMAND SYNTAX

    rc = CALLONEXIT('ErrorExit')

The subroutine definition would look like this

    SUBROUTINE CALLONEXIT(parm1)

You can add parameters to the error subroutine by adding multi-values
to the parameter to CALLONEXIT, which are passed to the called
subroutine in the first parameter.

If you execute CALLONEXIT multiple times with the same subroutine name,
it discards other calls.

If you execute CALLONEXIT multiple times with a different subroutine
name, then upon exit multiple subroutines will be called in the order
that CALLONEXIT was called.

### EXAMPLES

For example, consider the simple programs below. The program enters the
debugger. If at this point the login session terminates for any reason
(the line drops, the program is killed, the user enters 'off' at the
debugger prompt) , the two specified subroutines (ErrorExit and
EndProgram) will still be called just as they would if the program
were allowed to terminate normally.

    PROGRAM PROG1
    rc = CALLONEXIT('ErrorExit')
    EXECUTE "PROG2"

    PROGRAM PROG2
    rc = CALLONEXIT('EndProgram')
    DEBUG

All efforts are made to call the subroutine under all circumstances.
However, if a SIGKILL (signal 9) terminates the program, which cannot
be trapped, it does not call the subroutine. This is a feature of
operating systems, not a limitation. In addition, if the program
terminates due to say a memory error, then calling the subroutines
depends upon how badly the memory error has corrupted the memory.

## CASE

<a name="CASE"/>

The CASE statement allows the programmer to execute a particular
sequence of instructions based upon the results of a series of test
expressions.

### COMMAND SYNTAX

        BEGIN CASE
        CASE expression statement(s)
        CASE expression
        *statement(s)
        *. . .
        END CASE

### SYNTAX ELEMENTS

The BEGIN CASE and END CASE statements bound the CASE structure. Within
this block, an arbitrary number of CASE expression statements may exist
followed by any number of jBC statements. The expression should
evaluate to a TRUE or FALSE result. The evaluation of each expression
at execution time is in order. If the expression returns a TRUE result,
it then executes the statements below. On completion of the associated
statements, execution will resume at the first statement following
the END CASE.

### NOTES:

A default action (to trap error conditions for instance)
may be introduced by using an expression that is always TRUE, such as
"CASE 1". This should always be the last expression in the CASE block.

### EXAMPLE

       V.STRING = 'B'
       GOSUB CHK.IT
       V.STRING = 'ABC'
       GOSUB CHK.IT
       STOP
    *
    CHK.IT:
    *
       BEGIN CASE
       CASE V.STRING EQ 'A'
          CRT 'an A'
       CASE  V.STRING EQ 'B'
          CRT 'a B'
       CASE V.STRING EQ 'C'
          CRT 'a C'
       CASE 1
          CRT 'neither A nor B nor C'
       END CASE
       RETURN
    END

Output:

<pre>
    a B
    neither A nor B nor C
     </pre>

## CATALOG Command

<a name="CATALOG"/>

**Cataloging and Running your Programs**

Use the CATALOG command to create UNIX executables and shared libraries
from the application source code. Once you have cataloged your programs,
you can run them like any other command on the system.

The RUN command which is sometimes used to execute compiled jBC
programs without cataloging them can still be used but is really only
maintained for compatibility. Whenever possible, you should catalog your
programs rather than RUN them.

The CATALOG command should be executed from the application directory
rather than using link names and the application id should be used.
The reasons for executing the CATALOG command from the application
directory and application id are that the .profile script will have set
up the required environment variables correctly and that the correct
file permission will be used when creating and deleting UNIX
executables and directories.

The format of the CATALOG command is as follows.

<pre>
    CATALOG SourceFilename Itemlist</pre>

When first invoked the CATALOG command will create a $HOME/bin directory
into which the UNIX executables will be placed. A $HOME/lib directory
will also be created into which any subroutines will be placed. The lib
directory contains a jLibDefinition file, which describes how to build
the subroutines into shared libraries. The entries in the
jLibDefinition file are described below:

|Entry         |  Description                                    |
|--------------|-------------------------------------------------|
| libname      |  naming convention for shared object files.     |
| exportname   |  export list of shared objects. Used as cross   |
|              |  reference to find subroutine functions.        |
| maxsize      |  maximum size of a shared object library before |
|              |  creating another.                              |

When the maximum size of a shared library object is reached then a new
shared library object will be created by the CATALOG command. The new
shared library objects are named according to the definition of libname
and are numbered sequentially. For example:

libname=lib%a%n.so

where

%a = account or directory name

%n = number in sequence.

If subroutines were cataloged in the user account name, fred then the
shared object libraries produced would be named, libfred0.so
libfred1.so libfred2.so and so on.

Note: To guard against libraries being cataloged incorrectly, perhaps
under the wrong user account name, the definition of libname should
be changed to libfred%n.so. This will ensure that any shared objects
are created using the proper user account name.

The shared library objects,.so files, contain the UNIX executables for
subroutine source code. The shared library objects are linked at
runtime by the TAFC call function, which utilises the dynamic linker
programming interface. The dynamic linker will link shared libraries
at the start of program execution time, or when requested by the TAFC
call function. For example, each executable created using the TAFC
compiler will be linked with the TAFC jEDI library functions, libjedi.so,
at compilation time. This shared library enables database record
retrieval and update and will be loaded into memory by the dynamic
linker when an application executable starts execution. However the
shared library containing any subroutines required by the executing
program will only be loaded into memory when initially requested by the
subroutine call. Only one copy of any shared library is required in
memory at any time, thus reducing program memory requirements.

The $HOME/lib directory also contains a directory where all the subroutine
objects, .o files, are held. These are required for making the shared
library, .so files.

The $HOME/lib directory also contains an export list, .el file, built by
the CATALOG command, which is used as a cross reference when dynamically
linking shared objects at run time.

The main application program executables are placed into the $HOME/bin
directory.

To enable the application executables to be found the $HOME/bin path
should be added to the PATH environment variable.

To enable the executing application to call the correct application
subroutines the JBCOBJECTLIST or LD_LIBRARY_PATH environment variable
should be assigned to the application shared library path, $HOME/lib.
If the main application program or any subroutine programs make calls
to subroutines in other directories then the path of the shared library
directories should also be added to the JBCOBJECTLIST or LD_LIBRARY_PATH
environment variable.

It is recommended that executables or subroutines of the same name are
not available from different directories. This can make application
execution very confusing and is reliant on assigning the lib or bin
directories to the environment variable in the correct sequence. The
assignment of the environment variables should be included and exported
in the .profile script file.

Executables and shared library objects can be removed from the bin and l
ib directories by using the DECATALOG command.

## CATS

<a name="CATS"/>

The CATS function concatenates the corresponding elements in two dynamic
arrays.

### COMMAND SYNTAX

    CATS(DynArr1, DynArr2)

### SYNTAX ELEMENTS

DynArr1 and DynArr2 represent dynamic arrays.

### NOTES

If one dynamic array supplied to the CATS function is null then the result
of the CATS function is the non-null dynamic array.

### EXAMPLES

    * Same array structure -------------
       an_array =   "a" : @VM : "b" : @VM : "c"
       another_array = 1 : @VM : 2 : @VM : 3
       GOSUB DO.PROCEED                                     ;*   a1]b2]c3
    * Different array structure -------------
       an_array =      "a" : @SM : "b" : @VM : "c" : @VM : "d"
       another_array = "x" : @VM : "y" : @SM : "z"
       GOSUB DO.PROCEED                                     ;*   ax\b]cy\z]d
       STOP
    *-------------
    DO.PROCEED:
       the_result = CATS(an_array, another_array)
       CRT OCONV(the_result, 'MCP')
       RETURN

## CHAIN

<a name="CHAIN"/>

The CHAIN statement exits the current program and transfers process
control to the program defined by the expression. Process control will
never return to the originating program.

### COMMAND SYNTAX

    CHAIN expression

### SYNTAX ELEMENTS

The expression should evaluate to a valid UNIX or Windows command (this
may be another jBC program). The command string may be suffixed with
the (I option, which will cause any COMMON variables in the current
program to be inherited by the new program (providing it is a jBC
program).

### NOTES

There are no restrictions to the CHAIN statement and you may CHAIN from
anywhere to anywhere. However, it is advisable that your program
follows a logical path easily seen by another programmer. If the
program, which contains the CHAIN command (the current program) was
called from a JCL program, and the program to be executed (the target
program) is another jBC program, control will return to the original JCL
program when the target program terminates. If the target program is a JCL
program, control will return to the command shell when the JCL program
terminates.

### EXAMPLES

        CHAIN "OFF" ;* exit via the OFF command

        ! Prog1
        COMMON A,B
        A = 50 ; B = 100
        CHAIN "NEWPROG (I"

        ! NEWPROG
        COMMON I,J
        ! I and J inherited
        CRT I,J

## CHANGE

<a name="CHANGE"/>

The CHANGE statement operates on a variable and replaces all
occurrences of one string with another.

### COMMAND SYNTAX

    CHANGE expression1 TO expression2 IN variable

### SYNTAX ELEMENTS

**expression1** - may evaluate to any result and is the string of
characters that will be replaced.

**expression2** - may also evaluate to any result and is the string
of characters that will replace

**expression1** - The variable may be any previously assigned variable
in the program.

### NOTES

There is no requirement that strings be of the same length. The jBC
language also supports the CHANGE function for compatibility with
older systems.

### EXAMPLE

       V.STRING = 'ABCDEFCDYZ'
       CHANGE 'C' TO 'Q' IN V.STRING
       CRT V.STRING                 ;* ABQDEFQDYZ
       CHANGE 'QD' TO 'nnn' IN V.STRING
       CRT V.STRING                 ;* ABnnnEFnnnYZ
    * Both types of arrays are OK as well (dynamic ones can be processed in one go)
       V.ARRAY = V.STRING
       V.ARRAY<2> = V.STRING
       CHANGE 'nnn' TO 'mmm' IN V.ARRAY
       CRT OCONV(V.ARRAY, 'MCP')    ;* ABmmmEFmmmYZ^ABmmmEFmmmYZ
       DIM V.DIM.ARR(3)
       MAT V.DIM.ARR = V.STRING
       CHANGE 'nnn' TO 'mmm' IN V.DIM.ARR(2)
       CRT V.DIM.ARR(2)             ;* ABmmmEFmmmYZ
    * Funny but numbers can also be processed
       V.NUM = 12345.67
       CHANGE 3 TO 9 IN V.NUM
       CRT V.NUM                    ;* 12945.67
    * Compatibility mode
       V.STRING = CHANGE(V.STRING, 'YZ', '+-')
       CRT V.STRING                 ;* ABnnnEFnnn+-

## CHANGETIMESTAMP

<a name="CHANGETIMESTAMP"/>

Use CHANGETIMESTAMP to adjust existing timestamp to return new
timestamp value.

### COMMAND SYNTAX

    CHANGETIMESTAMP(Timestamp, Array)

### SYNTAX ELEMENTS

The CHANGETIMESTAMP function generates a new timestamp by adjusting
an existing timestamp value using the elements specified in the
dynamic array.

The format of the adjustment array is as follows:

<pre>
    Years^Months^Weeks^Days^Hours^Minutes^Seconds^Milliseconds</pre>

### EXAMPLE

       curr_time = MAKETIMESTAMP(DATE(), TIME(), '')
       CRT curr_time                                    ;*   e.g. 1358247401.205
    * Years^Months^Weeks^Days^Hours^Minutes^Seconds^Milliseconds
    * Add 100 milliseconds
       adj_array = ''
       adj_array<8> = 100
       CRT CHANGETIMESTAMP(curr_time, adj_array) ;* 1358247401.305 for example above
       adj_array<8> = ''
       adj_array<1> = 100   ;* 100 years
       CRT CHANGETIMESTAMP(curr_time, adj_array)   ;* 4513921001.205

## CHAR

<a name="CHAR"/>

The CHAR function returns the ASCII character specified by the
expression.

### COMMAND SYNTAX

    CHAR(expression)

### SYNTAX ELEMENTS

The expression must evaluate to a numeric argument in the range 0-255,
which is the entire ASCII character set.

### INTERNATIONAL MODE

The CHAR function will return Unicode values encoded as UTF-8 byte
sequences as follows:

Expression values 0 - 127 return UTF-8 single byte characters
equivalent to ASCII.

Expression values 127 - 248 return UTF-8 double byte character
sequences.

Expression values 249 - 255 return system delimiters 0xf8 - 0xff

Expression values > 255 return UTF-8 multi byte character
sequences

When system delimiter values are not specifically required,
generate UTF-8 byte sequences using the UTF8 function.
i.e. X = UTF8(@AM) will generate a UTF-8 byte sequence in variable X
for the system delimiter equating to Unicode value 0x000000fe.

### NOTES

jBC variables can contain any of the ASCII characters 0-255, thus there
are no restrictions on this function.

See also: [CHARS](#CHARS)

### EXAMPLE

       EQUATE VM TO CHAR(253)         ;* value Mark
       FOR V.I = 1 TO 6
          CRT CHAR(64 + V.I):         ;* ABCDEF
       NEXT V.I
       CRT ''                         ;* starts a new line
       CRT OCONV( CHAR(353), 'MX' )   ;* C5A1
       CRT CHAR(7)                    ;* rings a bell

## CHARS

<a name="CHARS"/>

The CHARS function accepts a dynamic array of numeric expressions and
returns a dynamic array of the corresponding ASCII characters.

### COMMAND SYNTAX

    CHARS(DynArr)

### SYNTAX ELEMENTS

Each element of DynArr must evaluate to a numeric argument in the range
0-255 (can exceed 255 if UTF-8 is used).

### NOTES

If any of the dynamic array elements are non-numeric, a run-time error
will occur.

See also: [CHAR](#CHAR)

### EXAMPLE

       V.ARRAY = 59 :@FM: 45 :@FM: 41
       V.CHARS = CHARS(V.ARRAY)
       CRT CHANGE(V.CHARS, @FM, '')

This code displays: ;-)

## CHDIR

<a name="CHDIR"/>

The CHDIR function allows the current working directory, as seen by the
process environment, to be changed.

### COMMAND SYNTAX

    CHDIR(expression)

### SYNTAX ELEMENTS

The expression should evaluate to a valid path name within the file
system. The function returns a Boolean TRUE result if the CHDIR
succeeded and a Boolean FALSE result if it failed.

### EXAMPLE

    INCLUDE JBC.h
       IF GETENV('TAFC_HOME', tafc_home) THEN
          IF CHDIR(tafc_home : DIR_DELIM_CH : 'config') ELSE
             CRT "TAFC configuration cannot be found"
             ABORT
          END
       END ELSE CRT 'TAFC home can not be found'

## CHECKSUM

<a name="CHECKSUM"/>

The CHECKSUM function returns a simple numeric checksum of a character
string.

### COMMAND SYNTAX

    CHECKSUM(expression)

### SYNTAX ELEMENTS

The expression may evaluate to any result but will usually be a string.
The function then scans every character in the string and sums up
the multiplication of character position by its ASCII value.
This algorithm doesn't really supply reliable result - see the example below.

### EXAMPLE

       CRT CHECKSUM('A')                ;* 65
       CRT CHECKSUM('AA')               ;* 65*1 + 65*2 = 195
       CRT CHECKSUM('B')                ;* 66
       CRT CHECKSUM( CHAR(0): '!' )     ;* 0*1 + 33*2 = 66

## CLEAR

<a name="CLEAR"/>

The CLEAR statement will initialize all local variables to numeric 0.

### COMMAND SYNTAX

    CLEAR

### NOTES

Use CLEAR at any time during the execution of the program.

### EXAMPLE

       COMMON /MY.COMM/ global_var
       global_var = 1000
       var = 5            ;   CRT var           ;* 5
       var ++             ;   CRT var           ;* 6
       CLEAR
    * only regular variables will be cleared
       CRT var                                  ;* 0
       CRT global_var                           ;* 1000

## CLEARCOMMON

<a name="CLEARCOMMON"/>

The CLEARCOMMON statement initializes all unnamed common variables to
a value of zero.

### COMMAND SYNTAX

    CLEARCOMMON

### EXAMPLE

       COMMON /MY.COMM/ global_var
       COMMON gl_unnamed
       global_var = 1000
       gl_unnamed = 1001
       CLEARCOMMON
    * only unnamed common will be cleared
       CRT global_var                           ;* 1000
       CRT gl_unnamed                           ;* 0

## CLEARDATA

<a name="CLEARDATA"/>

The CLEARDATA statement clears data stacked by the DATA statement.

### COMMAND SYNTAX

    CLEARDATA

### SYNTAX ELEMENTS

None

### EXAMPLE

    * SYSTEM(14) returns the number of characters available in input buffer
       CRT SYSTEM(14)        ;*  0
       DATA '123'
       DATA '456'
       CRT SYSTEM(14)        ;*  8 (including 2 line end characters)
       CLEARDATA
       CRT SYSTEM(14)        ;*  0

## CLEARFILE

<a name="CLEARFILE"/>

Use the CLEARFILE statement to clear all the data from a file previously
opened with the OPEN statement.

### COMMAND SYNTAX

    CLEARFILE { variable } { SETTING setvar } { ON ERROR statements }

### SYNTAX ELEMENTS

The variable should be the subject of an OPEN statement before the
execution of CLEARFILE upon it. If the variable is omitted from the
CLEARFILE statement, it assumes the default file variable as per the
OPEN statement.

### NOTES

The CLEARFILE statement will remove every database record on the file
against which it is executed, therefore, use with caution.

If the variable argument does not describe a previously opened file,
the program will enter the debugger with an appropriate message.

If the SETTING clause is specified and the CLEARFILE fails, it sets
setvar to one of the following values:

### INCREMENTAL FILE ERRORS

|Code   |    Description                        |
|-------|---------------------------------------|
|128    |    No such file or directory          |
|4096   |    Network error                      |
|24576  |    Permission denied                  |
|32768  |    Physical I/O error or unknown error|

### EXAMPLE

       OPEN 'F.TEMP' TO F.TEMP THEN
          V.ERR = ''
          CLEARFILE F.TEMP SETTING V.ERR
          IF V.ERR NE '' THEN
             CRT 'ERROR ' : V.ERR
             STOP
          END
          CRT 'FILE CLEARED'
       END ELSE
          EXECUTE 'CREATE-FILE DATA F.TEMP 1 101 TYPE=J4'
          OPEN 'F.TEMP' TO F.TEMP ELSE ABORT 201, 'F.TEMP'
       END

## CLEARINPUT

<a name="CLEARINPUT"/>

The CLEARINPUT command clears the terminal type-ahead buffer to allow
the next INPUT statement to force a response from the user.

### COMMAND SYNTAX

    CLEARINPUT

### EXAMPLE

In the following example, the CLEARINPUT statement clears the terminal
type-ahead buffer to provoke a response from the user to the prompt:

    CLEARINPUT
    PRINT "DO YOU WANT TO DELETE THIS FILE?(Y OR N)" ; INPUT X,1

NOTE: The CLEARINPUT command is synonymous with INPUTCLEAR.

## CLEARSELECT

Use the CLEARSELECT statement to clear active select lists.

### COMMAND SYNTAX

    CLEARSELECT { ListName | ListNumber }

### SYNTAX ELEMENTS

ListName must evaluate to a jBC list variable. ListNumber is one of the
numbered lists in the range 0 to 11. If neither ListName nor ListNumber
are specified then it clears the default list (0).

### EXAMPLE

    A = "good" : @AM : "bad" : @AM : "ugly"
    B = "night" : @AM : "day"
    SELECT A TO 3
    SELECT B TO blist
    adone = 0 ; bdone = 0
    //
    LOOP
     READNEXT Ael FROM 3 ELSE adone = 1
       READNEXT Bel FROM blist ELSE bdone = 1
    UNTIL adone AND bdone DO
       CRT Ael, Bel
       CLEARSELECT 3
       CLEARSELECT blist
    REPEAT

This program displays:

<pre>
    good night</pre>

## CLOSE

<a name="CLOSE"/>

Use the CLOSE statement to CLOSE an opened file, which is no longer
required.

### COMMAND SYNTAX

    CLOSE variable {, variable ... }

### SYNTAX ELEMENTS

The variable list should contain a list of previously opened file
variables that are no longer needed. The variables will be cleared
and may be reused as ordinary variables.

### NOTES

You can open an unlimited amount of files within jBC;
however leaving them open consumes valuable system resources.

Use good practice to hold open only those file descriptors to
which you have constant access.

### EXAMPLE

       EXECUTE 'DELETE-FILE DATA F.TEMP'
       EXECUTE 'CREATE-FILE DATA F.TEMP 1 101 TYPE=J4'
       OPEN 'F.TEMP' TO F.TEMP ELSE ABORT 201, 'F.TEMP'
       CRT ASSIGNED(F.TEMP)        ;* 1
       V.REC.INIT = 'LINE 1' :@FM: 'LINE 2' :@FM: 'LINE 3'
       WRITE V.REC.INIT TO F.TEMP, 'REC1'
       CLOSE F.TEMP
       CRT ASSIGNED(F.TEMP)        ;* 0

## CLOSESEQ

<a name="CLOSESEQ"/>

CLOSESEQ closes the file previously opened for sequential access.

### COMMAND SYNTAX

    CLOSESEQ FileVar

### SYNTAX ELEMENTS

FileVar contains the file descriptor of the previously opened
sequential file.

## COL1 and COL2

Use these functions in conjunction with the FIELD function to determine
the character positions 1 position before and 1 position after the
location of the last field.

### COMMAND SYNTAX

    COL1() / COL2()

### NOTES

When a field has been located in a string, it is sometimes useful to
know its exact position within the string to manipulate either it, or
the rest of the string. COL1() will return the position of the
character immediately before the last field located. COL2() will return
the position of the character immediately after the end of the last
field located. Use them to manipulate the string.

### EXAMPLE

      V.STRING = 'ABC/DEF/QWE/XYZ'
    * One field
       CRT FIELD(V.STRING, '/', 2)         ;* DEF
       CRT COL1()                          ;* 4 - position right before "DEF"
       CRT COL2()                          ;* 8 - position right after it
    * Alternate way
       CRT V.STRING['/', 2, 1]   ;* DEF
    * More than one field
       CRT FIELD(V.STRING, '/', 2, 2)      ;* DEF/QWE
       CRT COL1()                          ;* 4
       CRT COL2()                          ;* 12

## COLLECTDATA

<a name="COLLECTDATA"/>

Use the COLLECTDATA statement to retrieve data passed from the
PASSDATA clause of an EXECUTE statement.

### COMMAND SYNTAX

    COLLECTDATA variable

### SYNTAX ELEMENTS

**variable** is the name of the variable, which is to store the
retrieved data.

### NOTES

Use the COLLECTDATA statement in any program, which is EXECUTEd
(or PERFORMed) by another program where the calling program uses a
PASSDATA clause. The EXECUTEd program uses a COLLECTDATA statement
to retrieve the passed data.

If a PASSDATA clause is not in effect, variable will be assigned a
value of null.

### EXAMPLE

Program test.b:

       EXECUTE './test2' PASSDATA SYSTEM(40)

Program test2.b:

       COLLECTDATA the_parent
       CRT 'Executed from ' : the_parent

Program test2 executed by itself outputs "Executed from "; execution of program test
will output "Executed from test".

### NOTE

Compile both programs without "-E" switch so shared libraries will be created,
otherwise the data wouldn't be passed between programs.

## COMMON

<a name="COMMON"/>

The COMMON statement declares a list of variables and matrices that
can be shared among various programs. There can be many common areas
including a default, unnamed common area.

### COMMAND SYNTAX

    COMMON { /CommonName/ } variable {, variable ... }

### SYNTAX ELEMENTS

The list of variables should not have been declared or referenced
previously in the program file. The compiler will detect any bad
declarations and display suitable warning or error messages. If the
common area declared with the statement is to be named then the first
entry in the list should be a string, delimited by the / character.

### NOTES

The compiler will not, by default, check that variables declared in
COMMON statements are initialized before they have been used as this
may be beyond the scope of this single source code check. The -JCi
option, when specified to the jBC compiler, will force this check to
be applied to common variables as well. The initialization of named
common is controlled in the Config_EMULATE file.

Variables declared without naming the common area may only be shared
between the program and its subroutines (unless CHAIN is used).
Variables declared in a named common area may be shared across program
boundaries.

Dimensioned arrays are declared and dimensioned within the COMMON
statement.

### EXAMPLE

       COMMON /MY.COMM/ V.VAR1
       CRT ASSIGNED(V.VAR1)   ;* depends on emulation (e.g. 1 for prime)
       CRT V.VAR1             ;* first run: again depends on emulation
                              ;* (e.g. 0 for prime), second run: YES
       CRT ASSIGNED(V.VAR2)   ;* 0
       V.VAR1 = 'YES'
       V.VAR2 = 'NO'

### NOTE

When a COMMON area is used in different programs or subroutines, it has to be
declared in each of them. Variable names can be different but their number has to be the same.

### EXAMPLE

Program test.b:

       COMMON /MY.AREA/ global_var, global_dyn_array
       global_var = 42
       EXECUTE 'test2'

Program test2.b:

       COMMON /MY.AREA/ my_var, my_dyn_array
       CRT my_var

Run program test:

<pre>
    42</pre>

### NOTE

It's a good idea to put COMMON areas declaration for particular task to an insert file and include it
into every relevant source file.

### EXAMPLE

File I_MYTASK.COMMON:

       COMMON /MY.AREA/ global_var, global_dyn_array

Program test.b:

       $INSERT I_MYTASK.COMMON
       &nbsp;
       global_var = 42
       EXECUTE 'test2'

Program test2.b:

       $INSERT I_MYTASK.COMMON
       &nbsp;
       CRT global_var
       CRT ASSIGNED(global_dyn_array)

Run program test (**prime** emulation):

<pre>
    42
    1</pre>

**r83** emulation:

<pre>
    42
    0</pre>

### NOTE

If number of variables in COMMON area changes, all relevant source files are to be recompiled.

## COMPARE

<a name="COMPARE"/>

The COMPARE function compares two strings and returns a value
indicating whether or not they are equal.

### COMMAND SYNTAX

    COMPARE(expression1, expression2 {, justification } )

### SYNTAX ELEMENTS

**expression1** is the first string for comparison

**expression2** is the second string for comparison

**justification** specifies how the strings are to be compared. "L"
indicates a left justified comparison. "R" indicates a right justified
comparison. The default is left justification.

The function returns one of the following values:

|Code|    Description                              |
|----|---------------------------------------------|
|-1  |  The first string is less than the second   |
| 0  |  The strings are equal                      |
| 1  |  The first string is greater than the second|

### EXAMPLE

    A = "XY999"
    B = "XY1000"
    R1 = COMPARE(A, B, 'L')
    R2 = COMPARE(A, B, 'R')
    CRT R1, R2

The code above displays 1 -1, which indicates that XY999 is greater than
XY1000 in a left justified comparison and XY999 is less than XY1000 in
a right justified comparison.

### INTERNATIONAL MODE

When using the COMPARE function in International Mode, the function will
use the currently configured locale to determine the rules by which each
string is considered less than or greater than the other will.

## CONTINUE

<a name="CONTINUE"/>

The CONTINUE statement is the complimentary statement to the BREAK statement
without arguments.

### COMMAND SYNTAX

    CONTINUE

Use the statement within a loop to skip the remaining code in the current
iteration and proceed directly on to the next iteration.

### NOTES

See also: [BREAK](#BREAK), [EXIT](#EXIT)
The compiler will issue a warning message and ignore the statement if it is
found outside an iterative loop such as FOR...NEXT, LOOP...REPEAT.

### EXAMPLE

       num_array = ''
       FOR i = 1 TO 10
          IF i EQ 3 THEN CONTINUE
          num_array<-1> = i
       NEXT i
       CRT FMT(num_array, 'MCP')    ;* 1^2^4^5^6^7^8^9^10

## CONVERT

<a name="CONVERT"/>

The CONVERT function is the function form of the CONVERT statement. It
performs exactly the same function but may also operate on an expression
rather than being restricted to variables.

### COMMAND SYNTAX

    CONVERT(expression1, expression2, expression3)

### SYNTAX ELEMENTS

**expression1** is the string to which the conversion will apply.

**expression2** is the list of all characters to translate in
expression1.

**expression3** is the list of characters that will be converted to.

*NOTE:* For Prime, Universe and Unidata emulations:

**expression1** is the list of all characters to translate in
expression1.

**expression2** is the list of characters that will be converted to.

**expression3** is the string to which the conversion will apply.

See also: [CONVERT (STATEMENT)](#CONVERT_(STATEMENT))

### EXAMPLE

    * compile this program under same emulation that you're testing
       IF NOT(GETENV('JBCEMULATE', jbc_emu)) THEN
          CRT 'Emulation setting not found'
          STOP
       END
       *
       the_string = 'ABCCCDEFCDYZ'
       IF jbc_emu = 'prime' THEN
          the_result = CONVERT('CEY', '+-*', the_string)
       END ELSE
          the_result = CONVERT(the_string, 'CEY', '+-*')
       END
       *
       CRT jbc_emu, the_result                ;* e.g. prime AB+++D-F+D*Z

## CONVERT (STATEMENT)

<a name="CONVERTSTATEMENT"/>

The CONVERT statement converts one or more characters in a string to
their corresponding replacement characters.

### COMMAND SYNTAX

    CONVERT expression1 TO expression2 IN expression3

### SYNTAX ELEMENTS

**expression1** is the list of all characters to translate in
expression3

**expression2** is the list of characters that will be converted to.

**expression3** is the string to which the conversion will apply.

### NOTES

There is a one to one correspondence between the characters in
expression1 and expression2. That is, conversion of character 1 in
expression1 to character 1 in expression2, etc.

See also: [CONVERT](#CONVERT)

### EXAMPLE

    Value = 'ABCDEFGHIJ'
    CRT 'Original:   ':Value
    CONVERT 'BJE' TO '^+!' IN Value
    CRT 'Converted: ':Value

Output:

<pre>
    Original:   ABCDEFGHIJ
    Converted: A^CD!FGHI+</pre>

## COS

The COS function calculates the cosine of any angle using floating
point arithmetic, then rounds to the precision implied by the jBC
program, which makes it very accurate.

### COMMAND SYNTAX

    COS(expression)

This function calculates the cosine of an expression.

### SYNTAX ELEMENTS

The expression must evaluate to a numeric result or a runtime error
will occur.

### NOTES

Assumes the value returned by expression is in degrees.

### EXAMPLES

       * print cos i for 1 to 360 degrees
       FOR I = 1 TO 360
          cos_i = COS(I)
          CRT cos_i
          IF ABS(cos_i) GT 1 THEN CRT "It's wartime"
       NEXT I

## COUNT

<a name="COUNT"/>

The COUNT function returns the number of times that one string occurs
in another.

### COMMAND SYNTAX

    COUNT(expression1, expression2)

### SYNTAX ELEMENTS

Both expression1 and expression2 may evaluate to any data type but
logically they will evaluate to character strings.

### NOTES

The count is made on overlapping occurrences as a pattern match from
each character in expression1. This means that the string jjj occurs
3 times in the string jjjjj.

See also: [DCOUNT](#DCOUNT)

### EXAMPLES

    Calc = "56 * 23 / 45 * 12"
    CRT "There are " : COUNT(Calc, '*') : " multiplications"

## COUNTS

Use the COUNTS function to count the number of times a substring is
repeated in each element of a dynamic array. The result is a new
dynamic array whose elements are the counts corresponding to the
elements in the dynamic array.

### COMMAND SYNTAX

    COUNTS(dynamic.array, substring)

**dynamic.array** specifies the dynamic array whose elements are to
be searched.

**substring** is an expression that evaluates to the substring to be
counted. substring can be a character string, a constant, or a variable.
Each character in an element is matched to substring only once.
Therefore, when substring is longer than one character and a match is
found, the search continues with the character following the matched
substring. No part of the matched element is recounted toward another
match. If substring does not appear in an element, a 0 value is
returned. If substring is an empty string, the number of characters
in the element is returned. If substring is null, the COUNTS function
fails and the program terminates with a run-time error message. If any
element in dynamic.array is null, null is returned.

### EXAMPLE

    ARRAY= "A" :@VM: "AA" :@SM: "AAAAA"
    PRINT COUNTS(ARRAY, 'A')
    PRINT COUNTS(ARRAY, 'AA')

The output of this program is:

<pre>
    1]2\5
    0]1\2</pre>

## CREATE

Use the CREATE statement after an [OPENSEQ](#OPENSEQ) statement to
create a record in a jBASE directory file or to create a UNIX or
DOS file. CREATE creates the record or file if the [OPENSEQ](#OPENSEQ)
statement fails.

An [OPENSEQ](#OPENSEQ) statement for the specified file.variable must
be executed before the CREATE statement to associate the pathname or
record ID of the file to be created with the file.variable. If
file.variable is null, the CREATE statement fails and the program
enters the debugger.

Use the CREATE statement when [OPENSEQ](#OPENSEQ) cannot find a record
or file to open and the next operation is to be a [READSEQ](#READSEQ)
or [READBLK](#READBLK). If the first file operation is a
[WRITESEQ](#WRITESEQ),it creates the record or file if it does not exist.

If the record or file is created, it executes the THEN statements;
if no record or file is created, it executes the ELSE statements.

### COMMAND SYNTAX

    CREATE file.variable { THEN statements [ ELSE statements ] | ELSE statements }

### EXAMPLE

In the following example, RECORD does not yet exist.
When [OPENSEQ](#OPENSEQ) fails to open RECORD to the file variable FILE,
the CREATE statement creates RECORD in the type 1 file DIRFILE and opens
it to the file variable FILE.

    INCLUDE JBC.h
       out_dir = '.'  ;  out_file = 'report.txt'
       OPENSEQ out_dir, out_file TO f_out THEN
          WEOFSEQ f_out
       END ELSE
          CREATE f_out ELSE CRT 'File create error'  ;  STOP
          CRT 'File created'
       END
       WRITESEQ 'ABCDEFabcdef' TO f_out ELSE
          CRT 'Write error'
          STOP
       END
       CLOSESEQ f_out
       OSREAD the_content FROM out_dir : DIR_DELIM_CH : out_file ELSE NULL
       CRT the_content        ;* ABCDEFabcdef

## CRT

<a name="CRT"/>

The CRT statement sends data directly to the terminal, even if a
PRINTER ON statement is currently active.

### COMMAND SYNTAX

    CRT expression {, expression..} {:}

### SYNTAX ELEMENTS

An expression can evaluate to any data type. The CRT statement will
convert the result to a string type for printing. Expressions
separated by commas will be sent to the screen separated by a
tab character.

The CRT statement will append a newline sequence to the final
expression unless it is terminated with a colon (":") character.

### NOTES

As the expression can be any valid expression, it may have output
formatting applied to it.

A jBC program is normally executed using buffered output mode. This
means that data is not flushed to the terminal screen unless a
newline sequence is printed or terminal input is requested. This
makes it very efficient. However you can force output to be flushed
to the terminal by printing a null character CHAR (0). This has the
same effect as a newline sequence but without affecting screen output.

For compatibility, use DISPLAY in place of CRT.

### EXAMPLES

       V.VAR = 5
       CRT V.VAR           ;* 5
       V.VAR ++
       CRT V.VAR           ;* 6 (on the next line)
       V.VAR ++
       CRT ''              ;* start a new line
       CRT V.VAR           ;* 7 (2 lines below "6")
       V.RESULT = 50
       CRT 'The result: ':
       CRT V.RESULT        ;* will output: "The result: 50" on the same line
       MSLEEP(3000)
       CRT @(-1)                    ;* clears the screen and homes the cursor
       CRT @(40, 12):'Hello'        ;* will start output at row 11, column 39
       CRT ''
       V.NUM = 39
       V.STRING = 'In the year of'
       CRT V.STRING : ' ' : V.NUM    ;* In the year of 39
       CRT V.STRING, V.NUM           ;* In the year of  39
       V.LINE = '39R'
       V.STRING = 'In the year of'
       CRT V.STRING V.LINE             ;* same as FMT(V.STRING, '39R')
       V.VAR = 5
       CRT V.VAR > 1           ;* Result of an expression (1 in this case)
       CRT @SYS.BELL           ;* rings the bell

## DATA

The DATA statement stacks the series of expressions on a terminal input
FIFO stack. Terminal input statements will then treat this data as
if entered at the keyboard.

### COMMAND SYNTAX

    DATA expression {, expression ...}

### SYNTAX ELEMENTS

The expression may evaluate to any data type; views each comma-separated
expression as one line of terminal input.

### NOTES

The data stacked for input will subsequently be treated as input by any
jBC program. Therefore use it before PERFORM/EXECUTE, CHAIN or any other
method of transferring program execution. Use also to stack input for
the currently executing program; do not use to stack input back to an
executing program.

When a jBC program detects stacked data, it is taken as keyboard input
until the stack is exhausted. The program will then revert to the
terminal device for subsequent terminal input.

Stacked data delimited by field marks (xFE) will be treated as a series
of separate terminal inputs.

See also: [CLEARDATA](#CLEARDATA)

### EXAMPLE

Program test.b:

       DATA '12345'
       DATA '67890'
       EXECUTE 'test2'

Program test2.b:

       INPUT V.DATA1
       INPUT V.DATA2
       CRT 'I got ' : V.DATA1 : ' and ' : V.DATA2

If test2 is run by itself, it asks for user input. If test is run, the
output is:

<pre>
    I got 12345 and 67890</pre>

## DATE

The DATE() function returns the date in internal system form. This
date is expressed as the number of days since December 31, 1967.

### COMMAND SYNTAX

    DATE()

### NOTES

The system and your own programs should manipulate date fields in
internal form. They can then be converted to a readable format of your
choice using the [OCONV](#OCONV) function and the date conversion
codes.

See also: [TIMEDATE](#TIMEDATE)

### EXAMPLES

       curr_date = DATE()
       CRT curr_date                  ;* number of days (e.g. 16454) since day 1...
       CRT OCONV(1, 'D')              ;*  ...which is:  01 JAN 1968
       CRT OCONV(curr_date, 'D4/')    ;* e.g. 01/17/2013

## DCOUNT

<a name="DCOUNT"/>

The DCOUNT() function counts the number of field elements in a string
that are separated by a specified delimiter.

### COMMAND SYNTAX

    DCOUNT(expression1, expression2)

### SYNTAX ELEMENTS

**expression1** evaluates to a string in which fields are to be
counted.

**expression2** evaluates to the delimiter string used to count the
fields.

### NOTES

The delimiter string may consist of more than one character.

If expression1 is a NULL string, the function returns a value of zero.

The delimiter string may consist of any character, including system
delimiters such as field marks or value marks.

See also: [COUNT](#COUNT)

### EXAMPLES

       search_string = "A:B:C:D"
       CRT DCOUNT(search_string, ':')             ;* 4
       CRT COUNT(search_string, ':')              ;* 3 - COUNT returned
                                                  ;* number of ":" symbols
       CHANGE ':' TO '->' IN search_string
       CRT search_string                          ;* A->B->C->D
       CRT DCOUNT(search_string, '->')            ;* 4

## DEBUG

The DEBUG statement causes the executing program to enter the jBC
debugger.

### COMMAND SYNTAX

    DEBUG

### NOTES

Describes the debugger here.

### EXAMPLES

    IF FatalError = TRUE THEN
        DEBUG ;*enter the debugger
    END

## DECATALOG and DELETE-CATALOG Commands##

The DECATALOG and DELETE-CATALOG commands are used to remove the
run-time versions of  cataloged jBC programs.

### COMMAND SYNTAX

    DECATALOG SourceFilename ProgramName

    DECATALOG ProgramName

## DECRYPT##

<a name="DECRYPT"/>

The DECRYPT function decrypts strings.

### COMMAND SYNTAX

    DECRYPT(string, key, method)

### SYNTAX ELEMENTS

**string** specifies the string to be decrypted.

**Key** is the value used to decrypt the string. Its use depends on
method.

**method** is a value, which indicates the encryption mechanism to
use (see below).

The [ENCRYPT](#ENCRYPT) and DECRYPT functions that are part of jBC
now support the following cipher methods (Defined in JBC.h)

| Value               |    Description                             |
|---------------------|--------------------------------------------|
| JBASE_CRYPT_GENERAL |    General-purpose encryption scheme       |
| JBASE_CRYPT_ROT13   |    Simple ROT13 algorithm. (Key not used)  |
| JBASE_CRYPT_XOR11   |    XOR MOD11 algorithm. Uses the first     |
|                     |    character of a key as a seed value      |
| JBASE_CRYPT_RC2     |    RC2 algorithm                           |
| JBASE_CRYPT_DES     |    DES algorithm                           |
| JBASE_CRYPT_3DES    |    Three Key, Triple DES algorithm         |
| JBASE_CRYPT_BLOWFISH|    Blowfish algorithm                      |
| JBASE_CRYPT_AES     |    AES algorithm                           |
| JBASE_CRYPT_BASE64  |    (See below)                             |

BASE64 is not really an encryption method, but more of an encoding. The
reason for this is that the output of an encryption often results in a
binary string. It allows binary data to be represented as a character
string. BASE64 operation is not required but is performed in addition
to the primary algorithm.  e.g. JBASE_CRYPT_RC2_BASE64

ENCRYPT with this method is the same as a DECRYPT with method
JBASE_CRYPT_RC2 followed by DECRYPT with method JBASE_CRYPT_BASE64.

DECRYPT with this method is the same as a DECRYPT with method
JBASE_CRYPT_BASE64 followed by DECRYPT with method JBASE_CRYPT_RC2.

| Value                       |    Description       |
|-----------------------------|----------------------|
|JBASE_CRYPT_RC2_BASE64       | RC2 algorithm        |
|JBASE_CRYPT_DES_BASE64       | DES algorithm        |
|JBASE_CRYPT_3DES_BASE64      | Triple DES algorithm |
|JBASE_CRYPT_BLOWFISH_BASE64  | Blowfish algorithm   |

### NOTES

See also: [ENCRYPT](#ENCRYPT)

### EXAMPLES

    INCLUDE JBC.h
    //
    IF DECRYPT('rknzcyr', '', JBASE_CRYPT_ROT13) = "example" THEN
      CRT "ROT13 ok"
    END
    //
    IF ENCRYPT('g{ehvkm', '9', JBASE_CRYPT_XOR11) = "example" THEN
      CRT "XOR.MOD11 ok"
    END
    //
    cipher = JBASE_CRYPT_BLOWFISH_BASE64
    key    = "Our Very Secret Key"
    str    = "String to encrypt"
    enc = ENCRYPT( str, key, cipher )
    CRT "Encrypted: " : enc
    dec = DECRYPT( enc, key, cipher )
    CRT "Decrypted: " : dec

Displays as output:

<pre>
    ROT13 ok
    XOR.MOD11 ok
    Encrypted: xuy6DXxUkD32spyfsKEvUtXrsjP7mC+R
    Decrypted: String to encrypt</pre>

## DEFC

<a name="DEFC"/>

Use the DEFC statement to declare an external C function to the jBC
compiler, define its arguments, and return types. The DEFC statement
assumes that the C functions will need to manipulate jBC variables
and hence will also require the thread data pointer. As such, all C
functions require recoding to include the data pointer as an argument
to the C function. The location of the data pointer argument depends
upon the function return type.

### COMMAND SYNTAX

    DEFC {FuncType} FuncName ({ArgType {, ArgType ...}})

### SYNTAX ELEMENTS

FuncType and ArgType are selected from one of INT, FLOAT or VAR.
FuncType specifies the type of result that the function will return.
Assumes INT if FuncType is omitted. The optional list of ArgTypes
specifies the argument types that the C function will expect. The
compiler must know this in advance, as it will automatically perform
type conversions on these arguments.

### EXAMPLE

<pre>
    #include &lt;jsystem.h&gt;
    #include &lt;assert.h&gt;
    //
    #ifdef DPSTRUCT_DEF
    #define JBASEDP		  DPSTRUCT &lowast;dp,
    #else
    #define JBASEDP
    #endif
    //
    VAR &lowast;MyString(VAR &lowast;Result, JBASEDP  VAR &lowast;VarPtr)
    {
        char &lowast;Ptr;
        assert(dp != NULL);
        Ptr = (char &lowast;) CONV_SFB(VarPtr);
        printf("MyString: %s - %d\n", Ptr, strlen(Ptr) );
        STORE_VBI(Result, strlen(Ptr) );
        return(Result);
    }
    //
    INT32 MyCalc(INT32 Value1, INT32 Value2)
    {
        INT32  Result;
        Result =  (Value1 / Value2);
        printf("MyCalc: %d\n", Result);
        return(Result);
    }</pre>

### NOTES

Compile a DEFC for each C function before making any reference to it
else the compiler will not recognize the function name.

The function is called in the same manner, as it would be in a C
program, which means it can be used as if it was an intrinsic function
it as a standalone function call causes the compiler to generate code
that ignores any returned values.

When passing jBC variables to a C function, you must utilize the
predefined macros to access the various data types it contains. C
functions are particularly useful for increasing the performance
of tight loops that perform specific functions. The jBC compiler
must cater for any eventuality within a loop (such as the controlling
variable changing from integer to floating point). A dedicated C
function can ignore such events, if they are guaranteed not to happen.

The jBC programmer may freely ignore the type of argument used when
invoking the C function, as the jBC compiler will automatically perform
type conversion.

## DEFCE

With TAFC the DEFCE statement should be used, rather than the
[DEFC](#DEFC) statement, for calling external C programs, which are
pure 'C' code and do not use the TAFC library macro's and functions.

### EXAMPLE 1

For C functions that do not require TAFC functions use the DEFCE
statement, however the passing arguments can only be of type INT,
FLOAT and STRING.

<pre>
    DEFCE INT MYFUNC3(INT)
    INT32 MYFUNC3(INT32 Count)
    {
      INT32 Result;
	    ...
	    return Result;
    }</pre>

### EXAMPLE 2

    DEFCE INT cfunc( INT, FLOAT, VAR )
    Var1 = cfunc( A, 45, B )
    cfunc( 34, C, J )

You can call standard UNIX functions directly by declaring them with
the DEFC statement according to their parameter requirements. You can
only call them directly providing they return one of the type int or
float/double or that the return type may be ignored.

### EXAMPLE 3

    DEFCE INT getpid()
    CRT "Process id =" : getpid()

## DEFFUN

Use the DEFFUN statement to declare an external jBC function to the jBC
compiler and optionally define its arguments. Use DEFFUN in the program
that calls the function.

### COMMAND SYNTAX

    DEFFUN FuncName ({ { MAT } Argument1, { MAT } Argument2...})

### SYNTAX ELEMENTS

**FuncName** is the name used to define the function. It must be the
same as the source file name.

**Argument** specifies a value passed to the function by the calling
program. To pass an array, the keyword you must use the MAT before the
argument name. These parameters are optional (as indicated in the
command syntax) but can be specified for clarity. Note that if the
arguments are not initialized somewhere in the program you will receive
a compiler warning.

### NOTES

The DEFFUN statement identifies a user-written function to the jBC
compiler, which must be present in each program that calls the
function, before the function is called. A hidden argument is passed
to the function so that a value can be returned to the calling program.
The return value is set in the function using the RETURN (value)
statement. If the RETURN statement specifies no value then the function
returns an empty string.

### EXAMPLE 1###

    DEFFUN Add()
    A = 10
    B = 20
    sum = Add(A, B)
    PRINT sum
    X = RND(42)
    Y = RND(24)
    PRINT Add(X, Y)

    FUNCTION Add(operand1, operand2)
    result = operand1 + operand2
    RETURN(result)

## DEL

Use the DEL statement to remove a specified element of a dynamic array.

### COMMAND SYNTAX

    DEL variable<expression1{, expression2{, expression3}}>

### SYNTAX ELEMENTS

The variable can be any previously assigned variable or matrix element.
The expressions must evaluate to a numeric value or a runtime error
will occur.

**expression1** specifies the field in the array to operate upon and
must be present.

**expression2** specifies the multivalue within the field to operate
upon and is an optional parameter.

**expression3** is optionally present when expression2 has been
included. It specifies which subvalue to delete within the
specified multivalue.

### NOTES

Truncates non-integer values for any of the expressions to integers

Ignores invalid numeric values for the expressions without warning

The command operates within the scope specified, i.e. if specifying
only a field then it deletes the entire field (including its
multivalues and subvalues). If specifying a subvalue, then it
deletes only the subvalue leaving its parent multivalue and field
intact.

### EXAMPLE

       Numbers = ''
       FOR I = 1 TO 20
          Numbers<I> = I   ;*generate numbers
       NEXT I
       FOR I = 19 TO 1 STEP -2
          DEL Numbers<I>   ;* remove odd numbers
       NEXT I
       CRT CHANGE(Numbers, @FM, '>')  ;* 2>4>6>8>10>12>14>16>18>20

## DELETE

<a name="DELETE"/>

Use the DELETE statement to delete a record from a jBASE file.

### COMMAND SYNTAX

    DELETE {variable,} expression { SETTING setvar } { ON ERROR statements }

### SYNTAX ELEMENTS

If specified, variable should have been the subject of a previous
OPEN statement. If variable is omitted then it assumes the default
file variable.

The expression should evaluate to the name of a record stored in
the open file.

If the SETTING clause is specified and the delete fails, it sets
 setvar to one of the following values:

### INCREMENTAL FILE ERRORS

| Code  |    Description                        |
|-------|---------------------------------------|
|128    |    No such file or directory          |
|4096   |    Network error                      |
|24576  |    Permission denied                  |
|32768  |    Physical I/O error or unknown error|

### NOTES

The statement will have no effect if the record name does not
exist within the file.

If the program against the file record was holding a lock, it
will release the lock.

### EXAMPLE

       EXECUTE 'DELETE-FILE DATA F.TEMP'
       EXECUTE 'CREATE-FILE DATA F.TEMP 1 101 TYPE=J4'
       OPEN 'F.TEMP' TO F.TEMP ELSE ABORT 201, 'F.TEMP'
       V.REC.INIT = 'LINE 1' :@FM: 'LINE 2' :@FM: 'LINE 3'
       WRITE V.REC.INIT TO F.TEMP, 'REC1'
       WRITE V.REC.INIT TO F.TEMP, 'REC2'
       WRITE V.REC.INIT TO F.TEMP, 'REC3'
       DELETE F.TEMP, 'REC2' ON ERROR
          CRT 'DELETE ERROR'
          STOP
       END
    * "ON ERROR" part isn't triggered if a record doesn't exist
       DELETE F.TEMP, 'REC5' SETTING V.RET.CODE ON ERROR
          CRT 'REC5 - DELETE ERROR'
       END
       CLOSE F.TEMP
       EXECUTE 'LIST ONLY F.TEMP'

Output:

<pre>
    REC1
    REC3
     2 Records Listed</pre>

## DELETELIST

<a name="DELETELIST"/>

The DELETELIST statement will delete the previously stored list
named by expression.

### COMMAND SYNTAX

    DELETELIST expression

### SYNTAX ELEMENTS

The expression should evaluate to the name of a list that has been
stored with either the WRITELIST statement or the SAVE-LIST
command from the shell.

### NOTES

If POINTER-FILE is accessible then it saves lists within else are
saved in the jBASE work file.

### EXAMPLE

       EXECUTE 'SELECT .' :@FM: 'SAVE-LIST FILES-LIST'
       EXECUTE 'LIST &SAVEDLISTS& LIKE FILES-...'    ;*  FILES-LIST is here
       DELETELIST 'FILES-LIST'
       EXECUTE 'LIST &SAVEDLISTS& LIKE FILES-...'    ;* and now it's not

## DELETESEQ

DELETESEQ deletes a sequential file.

### COMMAND SYNTAX

    DELETESEQ Expression, Filename { SETTING setvar } { ON ERROR statements } \
    { LOCKED statements } THEN | ELSE statements

### SYNTAX ELEMENTS

**Expression** specifies the location of sequential file.

**Filename** specifies the sequential file name.

**Statements** conditional jBC statements

### EXAMPLE

Has to be put into file *test.b*.

       EXECUTE 'COPY FROM . test.b,temp.txt OVERWRITING'
       *
       OPENSEQ '.', 'temp.txt' TO temp_file ELSE
          CRT 'Failed to open temporary file'
          STOP
       END
       *
       READSEQ first_line FROM temp_file ELSE
          CRT 'Failed to read temporary file'
          STOP
       END
       *
       CRT first_line        ;* EXECUTE 'COPY FROM . test.b,temp.txt OVERWRITING'
       CLOSESEQ temp_file
       CRT DIR('temp.txt')<1>           ;* e.g. 540 - size of file
       *
       DELETESEQ '.', 'temp.txt' ELSE NULL
       CRT '<' : DIR('temp.txt')<1> : '>'          ;* <>

## DELETEU

<a name="DELETEU"/>

Use the DELETEU statement to delete a record without releasing the
update record lock set by a previous [READU](#READU) statement

See also: [READ](#READ) statements.

Use the OPEN statement to open a file. If specifying a file variable in
the OPEN statement, use it in the DELETEU statement. You must place a
comma between the file variable and the record ID expression. If
specifying no file variable in the DELETEU statement, the statement
applies to the default file.

See also: [OPEN](#OPEN) statement for a description of the default file.

## DIMENSION

<a name="DIM"/>

Use the DIM statement to declare arrays to the compiler before
referencing.

### COMMAND SYNTAX

    DIM{ENSION} variable(number{, number... }){, variable(number {,number...}) ...}

### SYNTAX ELEMENTS

The **variable** may be any valid variable name neither declared nor
previously used. The numbers define the size of each dimension and must
be either constants or the subject of an EQUATE statement.
A single DIM statement may declare a number of arrays by separating
their declarations with a comma.

### NOTES

Declare the array before it is referenced in the program source
(compilation as opposed to execution). If using a variable as an
undeclared dimensioned array the compiler will display an error
message.

Do not use the array variable as a normal variable or dynamic array
before dimensioning, as the compiler will detect this as an error.

A dimension size may not be specified as one as this has no logical
meaning. The compiler will detect this as a warning.

When arrays are referenced directly as in A = Array(7), the compiler
will optimize the reference as if it was a single undimensioned
variable.

See also: [COMMON](#COMMON)

### EXAMPLES

       DIMENSION V.ARRAY(10)
       MAT V.ARRAY = '!'
       V.ARRAY(5) = '?'
       FOR V.I = 1 TO 10
          CRT V.ARRAY(V.I):          ;* !!!!?!!!!!
       NEXT V.I

       DIM V.DIM3(2, 3, 4)
       MAT V.DIM3 = 1
       V.DIM3(1,2,1) *= 2
       CRT ''
       CRT V.DIM3(1,2,1)             ;* 2
       CRT V.DIM3(1,2)               ;* still 2
       CRT V.DIM3(1,20,1)            ;* runtime error ARRAY_SUBS

## DIR

Use the DIR function to return information about a file.

### COMMAND SYNTAX

    DIR(filename)

The filename is a string argument representing the path and filename
of a file. This function returns a dynamic array with four attributes.

| Attribute |                 Description              |
|-----------|------------------------------------------|
|  1        |File size in bytes                        |
|  2        |last modified date (in internal format)   |
|  3        |last modified time (in internal format)   |
|  4        |D if the filename is a directory, blank if|
|           |the filename is a file.                   |

### EXAMPLE

       IF NOT( GETENV('TAFC_HOME', V.HOME) ) THEN
          CRT 'TAFC_HOME not defined'
          STOP
       END
       CRT OCONV( DIR(V.HOME), 'MCP' )                  ;* e.g. 0^16214^32712^D
       CRT OCONV( DIR(V.HOME : '/jbcmessages'), 'MCP' ) ;* e.g. 204800^15815^57980

## DIV

<a name="DIV"/>

Use the DIV function to calculate the value of the quotient after
division of the dividend by the divisor.

### COMMAND SYNTAX

    DIV(dividend, divisor)

The dividend and divisor expressions can evaluate to any numeric
value. The only exception is that the divisor cannot be zero. If
either dividend or divisor evaluates to null, it returns null.
DIV is PRECISION-dependent.

### EXAMPLE

       CRT DIV(400, 200)                     ;* 2
       CRT DIV(200, 400)                     ;* 0.5
       CRT DIV(200, -400)                    ;* -0.5
       PRECISION 9
       CRT DIV(1, 10000000000)               ;* 0
       PRECISION 17
       CRT DIV(1, 10000000000)               ;* 0.0000000001

## DIVS

<a name="DIVS"/>

Use the DIVS function to create a dynamic array containing the result
of the element-by-element division of two dynamic arrays.

### COMMAND SYNTAX

    DIVS(array1, array2)

The division of each element of array1 is by the corresponding element
of array2, which returns the result in the corresponding element of a
new dynamic array. If elements of array1 have no corresponding elements
in array2, it pads array2 with ones and returns the array1 elements. If
an element of array2 has no corresponding element in array1, it returns
zero. If an element of array2 is zero, it prints a run-time error message
and returns 0. If either element of a corresponding pair is null, it
returns null.

### EXAMPLE

    A=10:@VM:15:@VM:9:@SM:4
    B=2:@VM:5:@VM:9:@VM:2
    PRINT DIVS(A,B)

The output of this program is: 5]3]1\4]0.

## DOWNCASE

<a name="DOWNCASE"/>

DOWNCASE converts all uppercase characters in an expression to lowercase
characters.

UPCASE converts all lowercase characters in an expression to uppercase
characters.

### COMMAND SYNTAX

    DOWNCASE(expression) | LOWCASE(expression) / UPCASE(expression)

### INTERNATIONAL MODE

When using the DOWNCASE or UPCASE function in International Mode the
conversion from upper case to lower case or vice versa will be
determined for each character in the expression by the Unicode
standard, which describes the up or down case properties for the
character.

### SYNTAX ELEMENTS

**expression** in a string containing some alphabetic characters

### NOTES

It ignores Non-alphabetic characters.

## DROUND

<a name="DROUND"/>

The DROUND function performs double-precision rounding on a value.
Double-precision rounding uses two words to store a number,
accommodating a larger number than in single-precision rounding,
which stores each number in a single word.

### COMMAND SYNTAX

    DROUND(val.expr [,precision.expr])

NOTE: DROUND affects the internal representation of the numeric
value. It performs the rounding without conversion to and from
string variables. This increases the speed of calculation.

### SYNTAX ELEMENTS

**val.expr** specifies the value to round.

**precision.expr** specifies the precision for the rounding.
Default precision is four places.

### EXAMPLE

       V.PI = 3.14159265358979323846
       CRT 'Default:', DROUND(V.PI)
       FOR V.I = 0 TO 20
          CRT DROUND(V.PI, V.I)
       NEXT V.I

Output:

<pre>
    Default:	3.1416
    3
    3.1
    3.14
    3.142
    3.1416
    3.14159
    3.141593
    3.1415927
    3.14159265
    3.141592654
    3.1415926536
    3.14159265359
    3.14159265359
    3.1415926535898
    3.14159265358979
    3.141592653589793
    3.1415926535897932
    3.14159265358979324
    3.141592653589793238
    3.1415926535897932385
    3.14159265358979323846</pre>

## DTX

<a name="DTX"/>

The DTX function will return the hexadecimal representation of a numeric
expression.

### COMMAND SYNTAX

    DTX(expression)

### SYNTAX ELEMENTS

expression must evaluate to a decimal numeric value or a runtime error
will occur.

### NOTES

See also: [XTD](#XTD).

### EXAMPLES

    Decimal = 254
    CRT DTX(Decimal)

displays FE

## DYNTOXML

<a name="DYNTOXML"/>

### COMMAND SYNTAX

    DYNTOXML(array, xsl, result)

### SYNTAX ELEMENTS

Convert the array to XML using the optimal xsl to transform

    XML = DYNTOXML(array, '', result)

Takes the contents of the dynamic array held in an array, and returns a
generic XML representation of that array or an error

(result=0 OK; result<>0 Bad);

### EXAMPLE

    a = "Tom" : @AM : "Dick" : @AM : "Harry"
    xml = DYNTOXML(a, '', result)
    CRT xml

**SCREEN OUTPUT**

<pre>
    &lt;?xml version="1.0" encoding ="ISO-8859-1"?&gt;
    &lt;array&gt;
      &lt;data attribute="1" value="1" subvalue="1">Tom&lt;/data&gt;
      &lt;data attribute="2" value="1" subvalue="1">Dick&lt;/data&gt;
      &lt;data attribute="3" value="1" subvalue="1">Harry&lt;/data&gt;
    &lt;/array&gt;</pre>

If a style sheet is passed in the second parameter, it performs a
transform to give a different format of XML.

### EXAMPLE

    xml = DYNTOXML(a, xsl, result)
    CRT xml

**SCREEN OUTPUT**

<pre>
    &lt;mycustomer&gt;
      &lt;firstname&gt;Tom&lt;/firstname&gt;
      &lt;lastname&gt;Dick&lt;/lastname&gt;
      &lt;address&gt;Harry&lt;/address&gt;
    &lt;/mycustomer&gt;</pre>

**XSL CONTENTS**

<pre>
    &lt;xsl:template match="/"&gt;
    &lt;mycustomer&gt;
      &lt;xsl:for-each select="array/data"&gt;
        &lt;xsl:if test="@attribute=1"&gt;
          &lt;firstname&gt;
            &lt;xsl:value-of select="."/&gt;
          &lt;/firstname&gt;
        &lt;/xsl:if&gt;
        &lt;xsl:if test="@attribute=2"&gt;
          &lt;lastname&gt;
            &lt;xsl:value-of select="."/&gt;
          &lt;/lastname&gt;
        &lt;/xsl:if&gt;
        &lt;xsl:if test="@attribute=3"&gt;
          &lt;address&gt;
            &lt;xsl:value-of select="."/&gt;
          &lt;/address&gt;
        &lt;/xsl:if&gt;
        &lt;xsl:if test="@attribute=4"&gt;
          &lt;address2&gt;
            &lt;xsl:value-of select="."/&gt;
          &lt;/address2&gt;
       &lt;/xsl:if&gt;</pre>

## EBCDIC

The EBCDIC function converts all the characters in an expression
from the ASCII character set to the EBCDIC character set.

### COMMAND SYNTAX

    EBCDIC(expression)

### SYNTAX ELEMENTS

**expression** may contain a data string of any form. The function
will convert it to a character string, assume that the characters
are all members of the ASCII set and translate them using a character
map. The original expression is unchanged while the returned result
of the function is now the EBCDIC equivalent.

### EXAMPLE

    READT AsciiBlock ELSE CRT "Tape failed!" ; STOP
    EbcdicBlock = EBCDIC(AsciiBlock) ;* Convert to EBCDIC

## ECHO

The ECHO statement will turn on or off the echoing of characters
typed at the keyboard.

### COMMAND SYNTAX

    ECHO ON

    ECHO OFF

    ECHO expression

### SYNTAX ELEMENTS

Use the statement with the keywords ON and OFF to specify echoing or
not. If used with an expression, then the expression should evaluate
to a Boolean TRUE or FALSE result.

TRUE: echoing on

FALSE: echoing off.

### NOTES

Use the SYSTEM function to determine the current state of character
echoing. SYSTEM(24) returns Boolean TRUE if enabled and returns Boolean
FALSE if disabled.

### EXAMPLES

    ECHO OFF
    CRT "Enter your password " :
    INPUT Password
    ECHO ON
    .....

This will disable the character input echoing while typing in a password.

## ENCRYPT

<a name="ENCRYPT"/>

The ENCRYPT function encrypts strings.

### COMMAND SYNTAX

    ENCRYPT(string, key, method)

### SYNTAX ELEMENTS

**string** specifies the string for encryption.

**key** is the value used to encrypt the string. Its use depends on
method.

**method** is a value, which indicates the encryption mechanism to use
(See below):

The ENCRYPT and [DECRYPT](#DECRYPT) functions that are part of jBC now
support the following cipher methods (Defined in JBC.h)

| Value               |    Description                                      |
|---------------------|-----------------------------------------------------|
| JBASE_CRYPT_GENERAL |    General-purpose encryption scheme                |
| JBASE_CRYPT_ROT13   |    Simple ROT13 algorithm. (Key not used)           |
| JBASE_CRYPT_XOR11   |    XOR MOD11 algorithm. Uses the first character of |
|                     |     a key as a seed value.                          |
| JBASE_CRYPT_RC2     |    RC2 algorithm                                    |
| JBASE_CRYPT_DES     |    DES algorithm                                    |
| JBASE_CRYPT_3DES    |    Three Key, Triple DES algorithm                  |
| JBASE_CRYPT_BLOWFISH|    Blowfish algorithm                               |
| JBASE_CRYPT_AES     |    AES algorithm                                    |
| JBASE_CRYPT_BASE64  |    (See below)                                      |

BASE64 is more of an encoding method rather than an encryption method.
The reason for this is that the output of an encryption often results in
a binary string, which allows the representation of binary data as a
character string. Although not required the BASE64 operation is performed
in addition to the primary algorithm.  E.g. JBASE_CRYPT_RC2_BASE64

ENCRYPT with this method is the same as an ENCRYPT with method
JBASE_CRYPT_RC2 followed by ENCRYPT with method JBASE_CRYPT_BASE64.

DECRYPT with this method is the same as a DECRYPT with method
JBASE_CRYPT_BASE64 followed by DECRYPT with method JBASE_CRYPT_RC2.

| Value                       |    Description       |
|-----------------------------|----------------------|
|JBASE_CRYPT_RC2_BASE64       | RC2 algorithm        |
|JBASE_CRYPT_DES_BASE64       | DES algorithm        |
|JBASE_CRYPT_3DES_BASE64      | Triple DES algorithm |
|JBASE_CRYPT_BLOWFISH_BASE64  | Blowfish algorithm   |
|JBASE_CRYPT_AES_BASE64       | AES algorithm        |

### NOTES

See also: [DECRYPT](#DECRYPT).

### EXAMPLES

    INCLUDE JBC.h
    IF DECRYPT('rknzcyr', '', JBASE_CRYPT_ROT13) = "example" THEN
    CRT "ROT13 ok"
    END
    //
    IF ENCRYPT('g{ehvkm', '9', JBASE_CRYPT_XOR11) = "example" THEN
    CRT "XOR.MOD11 ok"
    END
    //
    cipher = JBASE_CRYPT_BLOWFISH_BASE64
    key    = "Our Very Secret Key"
    str    = "String to encrypt"
    enc = ENCRYPT( str, key, cipher )
    CRT "Encrypted: " : enc
    dec = DECRYPT( enc, key, cipher )
    CRT "Decrypted: " : dec

Displays as output:

<pre>
    ROT13 ok
    XOR.MOD11 ok
    Encrypted: xuy6DXxUkD32spyfsKEvUtXrsjP7mC+R
    Decrypted: String to encrypt</pre>

### Hashing

The ENCRYPT function now supports SHA-2 hashing algorithms.


|JBC.h define                     | Hashing algorithm                   |
|---------------------------------|-------------------------------------|
|JBASE_SECUREHASH_SHA256          | SHA-2 family hashing algorithm      |
|JBASE_SECUREHASH_SHA256_BASE64   | SHA256 with BASE64                  |

### Hashing Example

    INCLUDE JBC.h
    Key = "" ;* unused for hashing
    EncryptType = JBASE_SECUREHASH_SHA256_BASE64
    StrOut = ENCRYPT(StrIn, Key, EncryptType)


### NOTES

See also: [DECRYPT](#DECRYPT).

See also: <a href="http://en.wikipedia.org/wiki/SHA-2">Wiki</a>


## ENTER

The ENTER statement unconditionally passes control to another
executable program.

### COMMAND SYNTAX

    ENTER program_name

    ENTER @variable_name

### SYNTAX ELEMENTS

**program_name** is the name of the program for execution. The use of
single or double quotes to surround program_name is optional.

@ specifies that the program name is contained in a named variable.

**variable_name** is the name of the variable, which contains the
program
name.

### NOTES

The jBC COMMON data area can be passed to another jBC program by
specifying the option "I" after the program name. Pass the COMMON
data area only to another jBC program.

Use ENTER to execute any type of program.

If the program which contains the ENTER command (the current program)
was called from a JCL program, and the program for execution (the target
program) is another jBC program, control will return to the original JCL
program when the target program terminates. If the target program is a
JCL program, control will return to the command shell when the JCL
program terminates.

### EXAMPLES

    ENTER "menu"

    ProgName = "UPDATE"
    ENTER @ProgName

## EQS

Use the EQS function to test if elements of one dynamic array are equal
to the elements of another dynamic array.

### COMMAND SYNTAX

    EQS(array1, array2)

EQS compares each element of array1 with the corresponding element
of array2 and returns, a one if the two elements are equal in the
corresponding element of a dynamic array. It returns a zero if the two
elements are not equal. It returns zero if an element of one dynamic
array has no corresponding element in the other dynamic array. If either
element of a corresponding pair is null, it returns null for that
element.

### EXAMPLE

    A=1:@VM:45:@SM:3:@VM:'one'
    B=0:@VM:45:@VM:1
    PRINT EQS(A,B)

The output of this program is: 0]1\0]0

## EQUATE

Use EQUATE to declare a symbol equivalent to a literal, variable or
simple expression.

### COMMAND SYNTAX

    EQU{ATE} symbol TO expression

### SYNTAX ELEMENTS

**symbol** is the name of the symbol to use; can be any name that
would be valid for a variable.

**expression** can be a literal, a variable or a simple expression.

### NOTES

Sensible use of EQUATEd symbols can make your program easier to
maintain, easier to read, and more efficient.

Efficiency can be enhanced because the address of an EQUATEd value
is computed during compilation and is substituted for each occurrence
of the symbol name. Unlike the address of a variable, which must be
computed for each access during run time, the address of a symbol is
always known. This significantly reduces the processing overhead
involved in accessing a particular value. See also: the example for
a more detailed explanation of the other benefits.

Enhance Readability by referring to say, QTY rather than INV_LINE(4).
You would simply "EQUATE QTY TO INV_LINE(4)" at an early stage in the
program. This can also help with maintenance of the program,
particularly in situations where record layouts might change. For
example, if the quantity field moves to INV_LINE(6), you only have
to change one line in your program.

### EXAMPLE

       DIM NV_LINE(10)
       MAT NV_LINE = 100
       COMMON FLAG
       EQUATE NO_CHARGE TO FLAG
       EQUATE CR TO CHAR (13), TRUE TO 1, FALSE TO 0
       EQUATE PRICE TO NV_LINE(7), TAX TO 0.175
       EQUATE DASHES TO "-------"
       IF NO_CHARGE = TRUE THEN PRICE = 0
       CRT "Tax = ":PRICE * TAX:CR:DASHES

Output:

<pre>
    Tax = 17.5
    -------</pre>

## EREPLACE

Use the EREPLACE function to replace substring in an expression with
another substring. If you do not specify an occurrence, it replaces
each occurrence of a substring.

### COMMAND SYNTAX

    EREPLACE(expression, substring, replacement [,occurrence [,begin] ] )

### SYNTAX ELEMENTS

**occurrence** specifies the number of occurrences of substring to
replace. To replace all occurrences, specify occurrence as a number
less than 1. **begin** specifies the first occurrence to replace. If
begin is omitted or less than one, it defaults to one. If
**substring** is an empty string, replacement is prefixed to
expression. If replacement is an empty string, it removes all
occurrences of substring. If **expression** evaluates to null, it
returns null. If substring, replacement, occurrence, or begin evaluates
to null, the EREPLACE function fails and the program terminates with a
run-time error message. The EREPLACE function behaves like the CHANGE
function except when substring evaluates to an empty string.

### EXAMPLE

    A = "AAABBBCCCDDDBBB"
    PRINT EREPLACE(A,'BBB', 'ZZZ')
    PRINT EREPLACE(A, '', 'ZZZ')
    PRINT EREPLACE(A, 'BBB', '')

The output of this program is:

<pre>
    AAAZZZCCCDDDZZZ
    ZZZAAABBBCCCDDDBBB
    AAACCCDDD</pre>

## EXECUTE

<a name="EXECUTE"/>

The EXECUTE or [PERFORM](#PERFORM) statement allows the currently
executing program to pause and execute any other UNIX/NT program,
including another jBC program or a TAFC command.

### COMMAND SYNTAX

    EXECUTE | PERFORM expression { CAPTURING variable}  \
        { RETURNING | SETTING variable} { PASSLIST {expression}}  \
        { RTNLIST {variable}}{ PASSDATA variable} { RTNDATA variable}

Executes external programs or OS commands;
you can intercept screen output and error messages from any program.
Passes data, dynamic arrays and lists to executed jBC programs.

### SYNTAX ELEMENTS

The PERFORMed expression can be formed from any TAFC construct. The
system will not verify that the command exists before executing it.
Use a new Bourne Shell to execute a command (sh) by default. The shell
type can be changed by preceding the command with a CHAR(255)
concatenated with either "k", "c", or "s" to signify the Korn shell,
C shell or Bourne Shell.

Variables used to pass data to the executed program should have been
assigned to a value before using. You can use any variable name to
receive data.

*CAPTURING variable*

The capturing clause will capture any output that the executing program
would normally send to the terminal screen and place it in the variable
specified. A field mark in the variable replaces every newline normally
sent to the terminal.

*RETURNING variable or SETTING variable*

The returning and setting clauses are identical. Both clauses will
capture the output associated with any error messages the executing
program issues. The first field of the variable will be set to the exit
code of the program.

*PASSLIST variable*

The PASSLIST clause allows TAFC programs to exchange lists or dynamic
arrays between them. The variable should contain the list that the
program wishes to pass to the TAFC program it is executing. The program
to be executed should be able to process lists, otherwise the list will
just be ignored. If the variable name is not specified then the clause
will pass the default select list to the executing program.

*RTNLIST variable*

If the executed program sets up a list then use the RTNLIST clause to
place that list into a specified variable. It places the list in the
default list variable if omitted.

*PASSDATA variable*

Passes the data in the specified variable to another jBC program, the
executing jBC program should retrieve the data using the
[COLLECTDATA](#COLLECTDATA) statement.

*RTNDATA variable*

The RTNDATA statement returns any data passed from an executing jBC
program in the specified variable. The executing jBC program should
use the RTNDATA statement to pass data back to the calling program.

### NOTES

The clauses may be specified in any order within the statement but
only one of each clause may exist.

### EXAMPLE

       V.CMD = 'COUNT .'
       HUSH ON
       EXECUTE V.CMD RETURNING V.CNT
       HUSH OFF
       CRT V.CNT<1,2>     ;* e.g. 15

### EXAMPLE 2

       EXECUTE 'SELECT F.TEMP' :@FM: 'SAVE.LIST TEMP-LIST'

### EXAMPLE 3

       EXECUTE CHAR(255) : 'kecho $SHELL'   ;* /usr/bin/ksh

### EXAMPLE 4

       EXECUTE 'df -m' CAPTURING V.OUTPUT
       LOOP
          REMOVE V.LINE FROM V.OUTPUT SETTING V.STATUS
          CRT '[' : V.LINE : ']'
          IF V.STATUS EQ 0 THEN BREAK
       REPEAT

Sample output of the last example:

<pre>
    [Filesystem    MB blocks      Free %Used    Iused %Iused Mounted on]
    [/dev/hd4         512.00    276.03   47%    12020    16% /]
    [/dev/hd2        5120.00   1398.12   73%    67516    18% /usr]
    [/dev/hd9var      640.00     95.71   86%    13280    36% /var]
    [/dev/hd3         768.00    505.89   35%     8812     7% /tmp]
    [/dev/hd1         128.00    121.68    5%      185     1% /home]
    [/proc                 -         -    -         -     -  /proc]</pre>

## EXIT

<a name="EXIT"/>

The EXIT statement halts the execution of a program and returns a
numeric exit code to the parent process. For compatibility with older
versions of the language, use the EXIT statement without an expression.
In this case, it is synonymous with the [BREAK](#BREAK) statement.

### COMMAND SYNTAX

    EXIT(expression)

    EXIT

### SYNTAX ELEMENTS

Any expression provided must be parenthesized and evaluate to a numeric
result. The numeric result is used as the UNIX or Windows exit code,
which is returned to the parent process by the C function exit(). If the
expression does not evaluate to a numeric result the program will enter
the debugger and display a suitable error message.

### NOTES

The expression has been forced to be parenthesized to avoid confusion
with the EXIT statement without an expression as much as is possible.
The authors apologize for having to provide two different meanings for
the same keyword

See also: [BREAK](#BREAK)

### EXAMPLE

    READ Record FROM FileDesc, RecordKey ELSE
        CRT "Record " : RecordKey : " is missing"
        EXIT(1)
    END ELSE
        CRT "All required records are present"
        EXIT(0)
    END

### EXAMPLE 2

       V.ARRAY = ''
       FOR V.I = 1 TO 10
          IF V.I EQ 4 THEN EXIT
          V.ARRAY<-1> = V.I
       NEXT V.I
       CRT FMT(V.ARRAY, 'MCP') ;* 1^2^3

## EXP

The EXP function returns the mathematical constant to the specified
power.

### COMMAND SYNTAX

    EXP(expression)

### SYNTAX ELEMENTS

The expression may consist of any form of jBC expression but should
evaluate to a numeric argument or a runtime error occurs and the
program enters the debugger.

### NOTES

The function returns a value that is accurate to as many decimal
places specified by the [PRECISION](#PRECISION) of the program.

### EXAMPLE

    zE10 = EXP(10) ;* Get e^10

## EXTRACT

The EXTRACT function is an alternative method of accessing values in
a dynamic array other than using the <n,n,n> syntax described earlier.

### COMMAND SYNTAX

    EXTRACT(expression1, expression2 {, expression3 {, expression4}})

### SYNTAX ELEMENTS

**expression1** specifies the dynamic array to work with and will
normally be a previously assigned variable.

The expressions 2 through 4 should all return a numeric value or a
runtime error will occur and the program will enter the debugger.

**expression2** specifies the field to extract, **expression3** the
value to extract and **expression4** the sub-value to extract.

### EXAMPLES

    array = "0"    ;    array<2> = "1"    ;    array<3> = "2"    ;    array<2,2> = 'Text'
    CRT DQUOTE( OCONV( EXTRACT(array, 2), 'MCP' ) )    ;*    "1]Text"
    CRT DQUOTE( EXTRACT(array, 2, 2) )                 ;*    "Text"
    CRT DQUOTE( EXTRACT(array, -1) )                   ;*    ""

This finction is useful when you need to take a part of a dynamic array in EVAL clause of
jQL statement (angle brackets notation won't work), e.g.:

<pre>
    LIST . SAMPLE 1 EVAL "(-12:@FM:5:@FM:-7)<2>" ID.SUPP
    &nbsp;
    Error in Statement "LIST . SAMPLE 1 EVAL "(-12:@FM:5:@FM:-7)<2>""
    Error in attribute definition item (-12:@FM:5:@FM:-7)<2>
    Error in Itype: expecting EOF, found '>'
    &nbsp;
    LIST . SAMPLE 1 EVAL "EXTRACT(-12:@FM:5:@FM:-7, 2)" ID.SUPP
    &nbsp;
    5</pre>

# jBC Functions and Statements (F - J)

## FADD

<a name="FADD"/>

The FADD function performs floating point addition of two numeric
values.

### COMMAND SYNTAX

    FADD(expression1, expression2)

### SYNTAX ELEMENTS

Both expression1 and expression 2 must evaluate to non-null numeric
values.

### NOTES

If either of the arguments evaluates to null then a run time
"non-numeric" error will occur.

### EXAMPLES

    PRECISION 7
    CRT FADD(0.5044, 23.7290002)

displays 24.2334002

## FDIV

<a name="FDIV"/>

The FDIV function performs floating point division on two numeric
values. (Similarly, FMUL does the multiplication.)

### COMMAND SYNTAX

    FDIV(expression1, expression2)
    FMUL(expression1, expression2)

### SYNTAX ELEMENTS

Both expression1 and expression 2 must evaluate to non-null numeric
values.

### NOTES

If either of the arguments evaluates to null then a run time
"non-numeric" error will occur.

If the second argument evaluates to zero then a run time "divide by
zero" error will occur.

The calculation is not subject to the PRECISION setting.

### EXAMPLE

        CRT FDIV(1, 7)                   ;* 0.1428571429
        CRT FMUL(2.54, 5.703358)         ;* 14.48652932

## FIELD

The FIELD function returns a multi-character delimited field from
within a string.

### COMMAND SYNTAX

    FIELD(string, delimiter, occurrence{, extractCount})

### SYNTAX ELEMENTS

**string** specifies the string, from which the field(s) is to be
extracted.

**delimiter** specifies the character or characters that delimit
the fields within the dynamic array.

**occurrence** should evaluate to an integer of value 1 or higher.
It specifies the delimiter used as the starting point for the
extraction.

**extractCount** is an integer that specifies the number of fields
to extract. If omitted, assumes one.

### NOTES

If the emulation option, jbase_field, is set then the field delimiter
may consist of more than a single character, allowing fields to be
delimited by complex codes.

See also: [GROUP](#GROUP)

### EXAMPLES

       V.STRING = 'ABC/DEF/QWE/XYZ'
    * One field
       CRT FIELD(V.STRING, '/', 2)         ;* DEF
    * Alternate way
       CRT V.STRING['/', 2, 1]             ;* DEF
    * More than one field
       CRT FIELD(V.STRING, '/', 2, 2)      ;* DEF/QWE
       CRT V.STRING['/', 2, 3]             ;* DEF/QWE/XYZ
       CRT DQUOTE( FIELD(V.STRING, '/', 2, 99) )    ;* take "all the rest after 1st"

## FIELDS

The FIELDS function is an extension of the FIELD function. It returns a
dynamic array of multi-character delimited fields from a dynamic
array of strings.

### COMMAND SYNTAX

    FIELDS(DynArr, Delimiter, Occurrence{, ExtractCount})

### SYNTAX ELEMENTS

**DynArr** should evaluate to a dynamic array.

**Delimiter** specifies the character or characters that delimit the
fields within the dynamic array.

**Occurrence** should evaluate to an integer of value 1 or higher. It
specifies the delimiter used as the starting point for the extraction.

**ExtractCount** is an integer that specifies the number of fields to
extract. If omitted, assumes one.

### NOTES

If the emulation option, jbase_field, is set then the field delimiter
may consist of more than a single character, allowing fields to be
delimited by complex codes.

### EXAMPLES

The following program shows how each element of a dynamic array can be
changed with the FIELDS function.

    t = ""
    t<1> = "a:b:c:d:e:f"
    t<2> = "aa:bb:cc:dd:ee:ff" : @VM: "1:2:3:4" : @SM: ":W:X:Y:Z"
    t<3> = "aaa:bbb:ccc:ddd:eee:fff" :@VM:@SM
    t<4> = "aaaa:bbbb:cccc:dddd:eeee:ffff"
    r1 = FIELDS(t,':',2)
    r2 = FIELDS(t,':',2,3)
    r3 = FIELDS(t,'bb',1,1)

The above program creates three dynamic arrays.

V - represents a value mark.

s - represents a sub-value mark.

|Array| Contents                                         |
|-----|--------------------------------------------------|
| r1  | <1>b                                             |
|     | <2>bb v 2 s W                                    |
|     | <3>bbb                                           |
|     | <4>bbbb                                          |
|     |                                                  |
| r2  | <1>b:c:d                                         |
|     | <2>bb:cc:dd v 2:3:4 s W:X:Y<3>bbb:ccc:ddd v s    |
|     | <4>bbbb:cccc:dddd                                |
|     |                                                  |
| r3  | <1>a:b:c:d:e:f                                   |
|     | <2>aa: v 1:2:3:4 s W:X:Y:Z                       |
|     | <3>aaa: v s                                      |
|     | <4>aaaa:                                         |

## FILEINFO

<a name="FILEINFO"/>

Use the FILEINFO function to return information about the specified file
variable.

### COMMAND SYNTAX

    FILEINFO(file.variable, key)

If **key** is 0, this function returns 1 if file.variable is a valid file variable, zero otherwise.
If **key** is 1, this function returns file status information.

### EXAMPLES

       IF NOT( GETENV('JEDIFILENAME_SYSTEM', FN.SYSTEM) ) THEN ABORT
       OPEN FN.SYSTEM TO F.SYSTEM ELSE NULL
       OPEN 'SOMENONEXISTENTFILE' TO F.SOMEFILE ELSE NULL
       CRT FILEINFO(F.SYSTEM, 0)        ;* 1
       CRT FILEINFO(F.SOMEFILE, 0)      ;* 0

       IF NOT( GETENV('TAFC_HOME', tafc_home) ) THEN
          CRT 'TAFC_HOME not defined'
          STOP
       END
       //
       log_dir = tafc_home : '/tmp'
       log_file = 'jbase_error_trace'
       //
       OPENSEQ log_dir, log_file READONLY TO f_log THEN
          CRT FMT( FILEINFO(f_log, 1), 'MCP' )
       END ELSE
          CRT 'jbase_error_trace not found'
       END

Sample output from the second example:

<pre>
    0^0^0^0^100666^107817^1^0^0^70770^24915^24915^34405^16705^25887^16643
    ^39761^16220^0^C:\home\kzm\v-t24\r11\tafc/tmp\jbase_error_trace^SEQ^0
    ^0^0^0^0^C:\home\kzm\v-t24\r11\tafc/tmp\jbase_error_trace^0^0^unknown</pre>

## FILELOCK

Use the FILELOCK statement to acquire a lock on an entire file. This
prevents other users from updating the file until the program releases
it. A FILELOCK statement that does not specify lock.type is equivalent
to obtaining an update record lock on every record of the file. An open
file is specified by file.variable. If no file.variable is specified, the
default file is assumed; if the file is neither accessible nor open, the
program enters the debugger.

### COMMAND SYNTAX

    FILELOCK filevar { LOCKED statements } { ON ERROR statements }

    FILEUNLOCK filevar { ON ERROR statements }

### DESCRIPTION

When the FILELOCK statement is executed, it will attempt to take an
exclusive lock on the entire file. If there are any locks currently
outstanding on the file, then the statement will block until there are
no more locks on the file. The use of the LOCKED clause allows the
application to perform an unblocked operation.

When the FILELOCK statement is blocked waiting for a lock, other
processes may continue to perform database operations on that file,
including the removal of record locks and the taking of record locks.
Once the FILELOCK is taken, it will block ALL database accesses to the
file whether or not the access involves record locks. i.e. a READ will
block once it has been executed, as will, CLEARFILE etc,. The lock
continues until the file is closed, the program terminates, or a
FILEUNLOCK statement is executed.

NOTE: The FILELOCK statement might differ to those found on other vendors
systems. You should also not that the use of these statements for other
than administration work, for example, within batch jobs, is not
recommended.
The replacement of such with more judicious use of item locks is
advised.

**IMPLEMENTATION NOTES**

The FILELOCK command is implemented using the native locking mechanism
of the operating system and is entirely at its mercy. Because of this,
you may see some slight implementation differences between operating
systems. These comments on native locking do not apply to the NT
platform as TAFC uses the NT locking mechanism.

The uses of the native (UNIX) locking mechanism means the file in
question MUST NOT use the jBASE locking mechanism. You can set a
file to use the native locking mechanism by using the jchmod
command:

jchmod +N filename {filename ...}

Alternatively, like this when the file is originally created:

<pre>
    CREATE-FILE filename 1,1 23,1 NETWORK=TRUE</pre>

If the file continues to use the jBASE record locking, then the ON
ERROR clause will be taken and the SYSTEM(0) and [STATUS](#STATUS)
functions will set to 22 to indicate the error.

### EXAMPLES

    OPEN '','SLIPPERS' TO FILEVAR ELSE STOP "CAN'T OPEN FILE"
    FILELOCK FILEVAR LOCKED STOP 'FILE IS ALREADY LOCKED'
    FILEUNLOCK DATA
    OPEN '','SLIPPERS' ELSE STOP "CAN'T OPEN FILE"
    FILELOCK LOCKED STOP 'FILE IS ALREADY LOCKED'
    PRINT "The file is locked."
    FILEUNLOCK

## FILEUNLOCK

Use the FILEUNLOCK statement to release a file lock set by the
FILELOCK statement.

### COMMAND SYNTAX

    FILEUNLOCK [file.variable] [ ON ERROR statements ]

**file.variable** specifies a file previously locked with a
FILELOCK statement. If file.variable is not specified, the default
file with the FILELOCK statement is assumed .If file.variable is
not a valid file variable then the FILEUNLOCK statement will enter
the debugger.

*The ON ERROR Clause*

The ON ERROR clause is optional in the FILELOCK statement. The ON
ERROR clause lets you specify an alternative for program termination
when encountering a fatal error during processing of the FILELOCK
statement. If a fatal error occurs, with no ON ERROR clause specified,
the program enters the debugger.

If the ON ERROR clause is used, the value returned by the STATUS
function is the error number.

### EXAMPLE

In the following example, the first FILEUNLOCK statement unlocks
the default file. The second FILEUNLOCK statement unlocks the file
variable FILE.

    OPEN '', 'SLIPPERS' ELSE STOP "CAN'T OPEN SLIPPERS"
    FILELOCK
    FILEUNLOCK
    OPEN 'PIPE' TO FILEVAR ELSE STOP
    FILELOCK FILEVAR
    FILEUNLOCK FILEVAR

## FIND

<a name="FIND"/>

The FIND statement determines if a specified string fully matches to an
element in a dynamic array.

### COMMAND SYNTAX

    FIND expression1 IN Var1 {, expression2} SETTING Var2 {, Var3 {, Var4}} \
         THEN | ELSE statement(s)

### SYNTAX ELEMENTS

**expression1** evaluates to the string with which to compare every
element of the dynamic array. Var1 is the dynamic array that will be
searched. The FIND command will normally find the first occurrence of
expression1 unless **expression2** is specified. If specified then
expression2 will cause a specific occurrence of expression1 to be
located. The three variables **Var2, Var3, Var4** are used to record the
Field, Value and Sub-Value positions in which expression1 was found.

If expression1 is found in any element of Var1 then Vars 2, 3 and 4 are
set to the position in which it was found and any THEN clause of the
statement is executed. If expression1 is not found within any element
of the dynamic array then Vars 2, 3 and 4 are undefined and the ELSE
clause of the statement is executed.

### NOTES

The statement may omit either the THEN clause or the ELSE clause but
may not omit both. It is valid for the statement to contain both
clauses if required.

See also: [LOCATE](#LOCATE), [FINDSTR](#FINDSTR)

### EXAMPLE

       V.ARRAY = 'ABC'   \
           :@FM: 'DEF' :@VM: '123' :@VM: 'XYZ' :@VM: '456' \
           :@FM: '789' \
           :@FM: '---' : @SM: 'XYZ'
       GOSUB RESET.IT
       FIND 'XYZ' IN V.ARRAY SETTING V.FLD, V.VAL ELSE NULL
       CRT V.FLD, V.VAL            ;*   2       3
       GOSUB RESET.IT
       FIND 'XYYYZ' IN V.ARRAY SETTING V.FLD, V.VAL ELSE NULL
       CRT V.FLD, V.VAL            ;*   0       0
       GOSUB RESET.IT
       FIND 'XYZ' IN V.ARRAY, 2 SETTING V.FLD, V.VAL, V.SVAL ELSE NULL
       CRT V.FLD, V.VAL, V.SVAL    ;*   4       1       2
       GOSUB RESET.IT
    * Full match is required
       FIND 'XY' IN V.ARRAY SETTING V.FLD, V.VAL ELSE NULL
       CRT V.FLD, V.VAL            ;*   0       0
       GOSUB RESET.IT
       STOP
    RESET.IT:
       V.FLD = 0  ; V.VAL = 0  ;  V.SVAL = 0
       RETURN

## FINDSTR

<a name="FINDSTR"/>

The FINDSTR statement locates a string as a substring of a dynamic
array element. It is similar in operation to the FIND statement, except that
the full match isn't required.

### COMMAND SYNTAX

    FINDSTR expression1 IN Var1 {, expression2} SETTING Var2 {,Var3 {, Var4}} \
            THEN | ELSE statement(s)

### SYNTAX ELEMENTS

**expression1** evaluates to the string with which to search every
element of the dynamic array. **Var1** is the actual dynamic array
that will be searched. FINDSTR will normally locate the first
occurrence of **expression1** unless **expression2** is specified. If
specified then expression2 will cause a specific occurrence of
expression1 to be located. The three variables **Var2, Var3, Var4** are
used to record the Field, Value and Sub-Value positions in which
expression1 was found.

If expression1 is found as a substring of any element of Var1 then
Vars 2, 3 and 4 are set to the position in which it was found and
the THEN clause of the statement is executed if it is present. If
expression1 is not found within any element of the dynamic array
then Vars 2,3 and 4 are undefined and the ELSE clause of the
statement is executed.

### NOTES

The statement may omit either the THEN clause or the ELSE clause but
may not omit both. It is valid for the statement to contain both
clauses if required.

### EXAMPLE

       V.ARRAY = 'ABC'   \
             :@FM: 'DEF' :@VM: '123' :@VM: 'XYZ' :@VM: '456' \
             :@FM: '789' \
             :@FM: '---' : @SM: 'XYZ'
       V.FLD = 0  ; V.VAL = 0  ;  V.SVAL = 0
       FINDSTR 'XY' IN V.ARRAY SETTING V.FLD, V.VAL ELSE NULL
       CRT V.FLD, V.VAL            ;*   2       3

## FORMLIST

<a name="FORMLIST"/>

The FORMLIST statement creates an active select list from a
dynamic array.

### COMMAND SYNTAX

    FORMLIST dyn.array { TO listname | listnum }

### SYNTAX ELEMENTS

**dyn.array** specifies the dynamic array from which the active
select list is to be created

If **listname** is specified then the newly created list will be
placed in the variable. Alternatively, a select list number in the
range 0 to 10 can be specified with listnum. If neither listname
nor listnum is specified then the default list variable will be
assumed.

### NOTES

See also: [DELETELIST](#DELETELIST), [READLIST](#READLIST), [WRITELIST](#WRITELIST)

### EXAMPLE

    MyList = "key1":@AM:"key2":@AM:"key3"
    FORMLIST MyList TO ListVar
    //
    LOOP
       READNEXT Key FROM ListVar ELSE EXIT
       READ Item FROM Key THEN
       * Do whatever processing is necessary on Item
       END
    REPEAT

## FLUSH

Writes all the buffers for a sequential I/O file immediately. Normally,
sequential I/O uses buffering for input/output operations, and writes
are not immediately flushed.

### COMMAND SYNTAX

    FLUSH file.variable { THEN statements [ ELSE statements ] | ELSE statements }

**file.variable** specifies a file previously opened for sequential
processing. If file.variable evaluates to null, the FLUSH statement
fails and the program enters the debugger. After the buffer is written
to the file, it executes the THEN statements, ignoring the ELSE
statements.

If none of the above can be completed, it executes the ELSE
statements.

### EXAMPLE

       dir_name = '.'
       file_name = 'report.txt'
       DELETESEQ dir_name, file_name ELSE NULL
       *
       OPENSEQ dir_name, file_name TO f_report ELSE NULL
       WRITESEQ 'New data' TO f_report ELSE NULL
       *
       FLUSH f_report ELSE NULL
       CRT '<' : DIR(file_name)<1> : '>'     ;* 9

### NOTE

For **prime** emulation FLUSH in this example will fail if there were still no
WRITESEQs since file isn't created immediately on OPENSEQ:

       dir_name = '.'
       file_name = 'report.txt'
       DELETESEQ dir_name, file_name ELSE NULL
       *
       OPENSEQ dir_name, file_name TO f_report ELSE NULL
       *
       FLUSH f_report ELSE NULL
       CRT '<' : DIR(file_name)<1> : '>'     ;* 0

This program will crash with the following message:

<pre>
    &lowast;&lowast; Error [ NOT_FILE_VAR ] &lowast;&lowast;
    Variable is not an opened file descriptor , Line     7 , Source test.b
    Trap from an error message, error message name = NOT_FILE_VAR</pre>

Under **seq** emulation program will not crash.

## FMT

<a name="FMT"/>

Format data according to mask definition.

### INTERNATIONAL MODE

When using the FMT function in International Mode the "Width" fields
refer to character display widths, such that a character may take up
more than a single display position. This is typical of the Japanese,
Chinese, and characters whereby the character display requires
possibly two display positions.

Additional date formatting codes have been provided for use in
Internationalized programs.

See also: [OCONV](#OCONV) for date/time/numeric masks and [FMTS](#FMTS).

|Mask Code|	                             Description                       |
|---------|----------------------------------------------------------------|
|j        | Justification                                                  |
|         |                                                                |
|         |   R:  Right Justified                                          |
|         |   L:  Left Justified                                           |
|         |   U:  Left Justified, Break on space. Note: This justification |
|         |        will format the output into blocks of data in the       |
|         |        variable and it is up to the programmer to actually     |
|         |        separate the blocks.	                                   |
|         |   D:  Date (OCONV)                                             |
|         |   M:  Time (OCONV)                                             |
|         |                                                                |
|n        | Decimal Precision: A number from 0 to 9 that defines the       |
|         | decimal precision. It specifies the number of digits for       |
|         | output following the decimal point. The processor inserts      |
|         | trailing zeros if necessary. If n is omitted or is 0, a decimal|
|         | point will not be output.                                      |
|         |                                                                |
|m        | Scaling Factor: A number that defines the scaling factor. The  |
|         | source value is descaled (divided) by that power of 10. For    |
|         | example, if m=1, the value is divided by 10; if m=2, the value |
|         | is divided by 100, and so on. If m is omitted, it is assumed   |
|         | equal to n (the decimal precision).                            |
|         |                                                                |
|Z        | Suppress leading zeros. NOTE: fractional values, which have no |
|         | integer, will have a zero before the decimal point. If the     |
|         | value is zero, a null will be output.                          |
|         |                                                                |
|,        | The thousands separator symbol. It specifies insertion of      |
|         | thousands separators every three digits to the left of the     |
|         | decimal point. You can change the display separator symbol by  |
|         | invoking the SET-THOU command. Use the SET-DEC command to      |
|         | specify the decimal separator.                                 |
|         |                                                                |
|c        | Credit Indicator. NOTE: If a value is negative and you have not|
|         | specified one of these indicators, the value will be displayed |
|         | with a leading minus sign. If you specify a credit indicator,  |
|         | the data will be output with either the credit characters or an|
|         | equivalent number of spaces, depending on its value.           |
|         |                                                                |
|         |  C:     Prints the literal CR after negative values.           |
|         |  D:     Prints the literal DB after positive values.           |
|         |  E:     Encloses negative values in angle brackets < >         |
|         |  M:     Prints a minus sign after negative values.             |
|         |  N:     Suppresses embedded minus sign.                        |
|         |                                                                |
|$        |  Appends a Dollar sign to value.                               |
|         |                                                                |
|         |  Fill Character and Length                                     |
|         |                                                                |
|         |  #n:   Spaces. Repeat space n times. Output value is overlaid  |
|         |        on the spaces created.                                  |
|         |   n:   Asterisk. Repeat asterisk n times. Output value is      |
|         |        overlaid on the asterisks created.                      |
|         |  %n:   Zero. Repeat zeros n times. Output value is overlaid on |
|         |        the zeros created.                                      |
|         |  &x:   Format. x can be any of the above format codes, a       |
|         |        currency symbol, a space, or literal text. The first    |
|         |        character following & is used as the default fill       |
|         |        character to replace #n fields without data. Format     |
|         |        strings are enclosed in parentheses "()".               |

### EXAMPLES

       X = 1234.56
       CRT DQUOTE( FMT(X, 'R2#10') )           ;*  "   1234.56"
       CRT FMT(X, 'L2%10')                     ;*  1234.56000
       CRT FMT(X, 'R2%10')                     ;*  0001234.56
       CRT FMT(X, 'L2*10')                     ;*  1234.56***
       CRT FMT(X, 'R2*10')                     ;*  ***1234.56
       X = 123456.78
       CRT DQUOTE( FMT(X, 'R2,$#15') )         ;*  "    $123,456.78"
       CRT DQUOTE( FMT(X, 'R2,&$#15') )        ;*  "     123,456.78"
       CRT DQUOTE( FMT(X, 'R2,& $#15') )       ;*  "    $123,456.78"
       X = -123456.78
       CRT DQUOTE( FMT(X, 'R2,C&*$#15') )      ;*  "  $123,456.78CR"
       X = 1234567890
       CRT FMT(X, 'R((###) ###-###)')          ;*  (234) 567-890
       CRT FMT(X, 'R((#3) #2-#4)')             ;*  (234) 56-7890
       X = 16376
       CRT FMT(X, 'D4/')                       ;*  10/31/2012
       CRT FMT(X, 'DY')                        ;*  2012
       CRT FMT(X, 'DY2')                       ;*  12
       CRT FMT(X, 'D2')                        ;*  31 OCT 12
       CRT FMT(X, 'DQ')                        ;*  4 (quarter)
       CRT FMT(X, 'DD')                        ;*  31
       CRT FMT(X, 'DM')                        ;*  10
       CRT FMT(X, 'DMA')                       ;*  OCTOBER
       CRT FMT(X, 'DJ')                        ;* 305 - number of a day in the year
       CRT FMT(X, 'DW')                        ;* 3 - number of a day in the week
       CRT FMT(X, 'DWA')                       ;* WEDNESDAY
       CRT FMT(TIME(), 'MT')                   ;* e.g. 21:25
       CRT FMT(TIME(), 'MTS')                  ;* e.g. 21:25:30
       X = 'A LONG STRING TO BE SPLIT'
       CRT FMT(X, '10L')                       ;* A LONG STR.ING TO BE .SPLIT
       X = 'ABCDEF'
       CRT FMT(X, 'MX')                        ;* 414243444546
       CRT FMT(@FM, 'MX')                      ;* FE

## FMTS

<a name="FMTS"/>

Use the FMTS function to format elements of dynamic array for output.
Each element of the array is independently acted upon and returned as
an element in a new dynamic array.

### COMMAND SYNTAX

    FMTS(dynamic.array, format)

### SYNTAX ELEMENTS

**format** is an expression that evaluates to a string of formatting
codes. The Syntax of the format expression is:

[width] [background] justification [edit] [mask]

The format expression specifies the width of the output field, the
placement of background or fill characters, line justification,
editing specifications, and format masking.

For complete syntax details, See also: [FMT](#FMT) function.

If dynamic.array evaluates to null, it returns null. If format
evaluates to null, the FMTS function fails and the program enters
the debugger.

### EXAMPLE

       X = 1234.56 :@FM: 123456.78 :@FM: -123456.78 :@FM: 1234567890
       CRT OCONV( FMTS(X, 'R2*12'), 'MCP' )

Output:

<pre>
    &lowast;&lowast;&lowast;&lowast;&lowast;1234.56^&lowast;&lowast;&lowast;123456.78^&lowast;&lowast;-123456.78^234567890.00</pre>

## FOLD

<a name="FOLD"/>

The FOLD function re-delimits a string by replacing spaces with
attribute marks at positions defined by a length parameter.

### COMMAND SYNTAX

    FOLD(expression1, expression2)

### SYNTAX ELEMENTS

**expression1** evaluates a string to be re-delimited.

**expression2** evaluates to a positive integer that represents
the maximum number of characters between delimiters in the
resultant string.

### NOTES

The FOLD function creates a number of sub-strings such that the
length of each sub-string does not exceed the length value in
expression2. It converts spaces to attribute marks except when
enclosed in sub-strings and removes extraneous spaces.

### EXAMPLES

The following examples show how the FOLD function delimits
text based on the length parameter. The underscores represent
attribute marks.

    q = "Smoking is one of the leading causes of statistics"
    CRT OCONV( FOLD(q, 7), 'MCP' )

Output:
<pre>
    Smoking^is one^of the^leading^causes^of^statist^ics</pre>

    q = "Hello world"
    CRT OCONV( FOLD(q, 5), 'MCP' )

Output:
<pre>
    Hello^world</pre>

    q = "Let this be a reminder to you all" \
        : " that this organization will not tolerate failure."
    CRT OCONV( FOLD(q, 30), 'MCP')

Output:

<pre>
Let this be a reminder to you^all that this organization^will not tolerate failure.</pre>

    q = "the end"
    CRT OCONV( FOLD(q, 0), 'MCP' )

Output:
<pre>
    t^h^e^e^n^d</pre>

## FOOTING

<a name="FOOTING"/>

The FOOTING statement halts all subsequent output to the terminal at
the end of each output page. The statement allows the evaluation and
display of an expression at the foot of each page. Output, which is
current, and being sent to the terminal, the output is paused until
the entry of a carriage return at the terminal (unless the N option
is specified either in the current HEADING or in this FOOTING).

### COMMAND SYNTAX

    FOOTING expression

### SYNTAX ELEMENTS

The expression should evaluate to a string, which is printed at the
bottom of every page of output. The string could contain a number of
interpreted special characters, replaced in the string before printing.

The following characters have special meaning within the string:

| Value     |    Description                                         |
|-----------|--------------------------------------------------------|
|"C{n}"     |  Center the line. If n is specified the output line is |
|           |  assumed to be n characters long.                      |
|"D" or \\  |  Replace with the current date.                        |
|"L" or ]   |  Replace with the newline sequence.                    |
|"N"        |  Terminal output does not pause at the end of each     |
|           |  page.                                                 |
|"P" or ^   |  Replace with the current page number.                 |
|"PP" or ^^ |  Replace with the current page number in a field of 4  |
|           |  characters. The field is right justified.             |
|"T" or \   |  Replace with the current time and date.               |
|"          |  Replace with a single " character.                    |

### NOTES

If the output is to the printer a PRINTER ON statement is in force;
output sent to the terminal with the CRT statement is not paged; if
output is to the terminal then all output is paged.

### EXAMPLE

    FOOTING 'Programming staff by weight Page "P"'

## FOR

<a name="FOR"/>

The FOR statement allows the construction of looping constructs within
the program, which is controlled by a counting variable; this can be
terminated early by expressions tested after every iteration.

### COMMAND SYNTAX

    FOR var=expression1 TO expression2 { STEP expression3 }  \
       { WHILE | UNTIL expression4 }
    ...
    NEXT {var}

### SYNTAX ELEMENTS

**var** is the counting variable used to control the loop. The first
time the loop is entered var is assigned the value of expression1,
which must evaluate to a numeric value. After each iteration of the
loop, var is automatically incremented by one.

**expression2** must also evaluate to a numeric value as it causes the
loop to terminate when the value of var is greater than the value of
this expression. expression2 is evaluated at the start of every
iteration of the loop and compared with the value of expression1.

If the STEP expression3 clause is included within the statement, var
will automatically be incremented by the value of expression3 after
each iteration of the loop. expression3 is evaluated at the start of
each iteration.

**expression3** may be negative, in which case the loop will terminate
when var is less than expression2.
The statement may optionally include either an evaluated WHILE or UNTIL
clause (not both), before each iteration of the loop. When the WHILE
clause is specified the loop will only continue with the next iteration
if expression4 evaluates to Boolean TRUE. When the UNTIL clause is
specified the loop will only continue with the next iteration if
expression4 evaluates to Boolean FALSE.

### NOTES

Because expression2 and expression3 must be evaluated upon each
iteration of the loop, you should only code complex expressions here
if they may change within each iteration. If the values they yield will
not change then you should assign the value of these expressions to a
variable before coding the loop statement. You can replace expressions
3 and 4 with these variables. This can offer large performance increases
where complex expressions are in use.

See also: [BREAK](#BREAK), [CONTINUE](#CONTINUE).

### EXAMPLE

       V.ARRAY = ''
       FOR V.I = 1 TO 10
          V.ARRAY<-1> = 'Element #' : V.I
       NEXT V.I
       CRT V.ARRAY<6>                          ;* Element #6
       //
       FOR V.I = 10 TO 1 STEP -2 WHILE V.I GT 3
          DEL V.ARRAY<V.I>
       NEXT V.I
       CRT V.ARRAY<6>                          ;* Element #9
       CRT V.ARRAY<3>                          ;* Element #3

## FSUB

<a name="FSUB"/>

The FSUB function performs floating-point subtraction on two numeric
values.

### COMMAND SYNTAX

    FSUB(expression1, expression2)

### SYNTAX ELEMENTS

Both expression1 and expression 2 must evaluate to non-null numeric
values.

### NOTES

If either of the arguments evaluates to null then a run time "non-numeric"
error will occur.

### EXAMPLES

    PRECISION 7
    CRT FSUB(2.54, 5.703358)

displays -3.163358

## FUNCTION

Identifies a user-defined function, which can be invoked by other jBC
programs, arguments to the function can optionally be declared.

### COMMAND SYNTAX

    FUNCTION name({ MAT } variable, { MAT } variable...)

### SYNTAX ELEMENTS

Name is the name by which the function is invoked.

Variable is an expression used to pass values between the calling
program and the function.

### NOTES

Use the FUNCTION statement to identify user-written source code
functions. Each function must be coded in separate records and the
record Id must match that of the Function Name, which in turn should
match the reference in the calling program.

The optional comma separated variable list can be a number of
expressions that pass values between the calling programs and the
function. To pass an array the variable name must be preceded by the
MAT keyword. When a user-written function is called, the calling program
must specify the same number of variables that are specified in the
FUNCTION statement.

An extra 'hidden' variable is used to return a value from the
user-written function. The value to be returned can be specified
within the Function by the RETURN (value) statement. If using the
RETURN statement without a value then by default it returns an empty
string.

The calling program must specify a DEFFUN or DEFB statement to describe
the function to be called and the function source must be cataloged and
locatable similar to subroutines.

### EXAMPLE

The function:

        FUNCTION ADD.FUNC(operand1, operand2)
        result = operand1 + operand2
        RETURN(result)
    END


The calling program:

       DEFFUN ADD.FUNC()
       CRT ADD.FUNC(1, 2)           ;* 3
       CRT ADD.FUNC(100, 200)       ;* 300

## GES

Use the GES function to test if elements of one dynamic array are
greater than or equal to corresponding elements of another dynamic
array.

### COMMAND SYNTAX

    GES(array1, array2)

### SYNTAX ELEMENTS

Compares each element of array1 with the corresponding element of
array2, if the element from array1 is greater than or equal to the
element from array2, it returns a one in the corresponding element
of a new dynamic array. If the element from array1 is less than the
element from array2, it returns a zero (0). If an element of one
dynamic array has no corresponding element in the other dynamic array,
it evaluates the undefined element as empty, and the comparison
continues.

If either element of a corresponding pair is null, it returns null for
that element.

## GET

<a name="GET"/>

The GET statement reads a block of data directly from a device.

### COMMAND SYNTAX

    GET Var {,length} { SETTING Count } FROM Device { UNTIL TermChars } \
        { RETURNING TermChar }  { WAITING Timeout } THEN | ELSE statements

### SYNTAX ELEMENTS

**Var** is the variable in which to place the input (from the previously
open Device).

If length is specified, it limits the number of characters read from the
input device.

If the optional Count option is used, it returns the number of characters
actually read from the device.

Device is the file variable associated with the result from a successful
OPENSEQ or OPENSER command.

**TermChars** specifies one or more characters that will terminate input.

**TermChar** The actual character that terminated input

**Timeout** is the number of seconds to wait for input.  If no input is
present when the timeout period expires, the ELSE clause (if specified)
is executed.

### NOTES

The GET statement does no pre-or post-processing of the input data stream -
nor does it handle any terminal echo characteristics. If this is desired,
the application - or device drive - will handle it.
If there are no specified length and timeout expressions, the default input
length is one (1) character. If no length is specified, but TermChars are,
there is no limit to the number of characters input.
The GET syntax requires a specified THEN or ELSE clause, or both. The THEN
clause executes when the data received is error free; the ELSE clause
executes when the data is unreceiveable (or a timeout occurs).

See: [GETX](#GETX)

## GETCWD

The GETCWD function allows a jBC program to determine the current working
directory of the program, which is normally be the directory in which
execution of the program occurred but possibly changed using the CHDIR()
function.

### COMMAND SYNTAX

    GETCWD(Var)

### SYNTAX ELEMENTS

When executed the Var will be set to the name of the current working
directory; the function itself returns a Boolean TRUE or FALSE value to
indicate whether the command was successful or not.

### NOTES

Refer to your UNIX or Windows documentation for more information on the
concept of the current working directory.

### EXAMPLES

    IF GETCWD(Cwd) THEN
       CRT "Current Working Directory = " : Cwd
    END ELSE
       CRT "Could not determine CWD!"
    END

## GETENV

<a name="GETENV"/>

All processes have an environment associated with them that contains a
number of variables indicating the state of various parameters. The
GETENV function allows a jBC program to determine the value of any of
the environment variables associated with it.

### COMMAND SYNTAX

    GETENV(expression, variable)

### SYNTAX ELEMENTS

The expression should evaluate to the name of the environment variable
whose value is to be returned. The function will then assign the value
of the environment variable to variable. The function itself returns a
Boolean TRUE or FALSE value indicating the success or failure of the
function.

See: [PUTENV](#PUTENV)

### EXAMPLE

    IF GETENV('PATH', ExecPath) THEN
        CRT "Execution path is " : ExecPath
    END ELSE
        CRT "Execution path is not set up"
    END

## GETLIST

<a name="GETLIST"/>

GETLIST allows the program to retrieve a previously stored list
(perhaps created with the SAVE-LIST command), into a jBC
variable.

### COMMAND SYNTAX

    GETLIST expression TO variable1 { SETTING variable2 } THEN | ELSE statements

### SYNTAX ELEMENTS

**variable1** is the variable into which the list will be read.
expression should evaluate to the name of a previously stored list
to retrieve, or null. If **expression** evaluates to null, the current
default external select list (generated by a previous
[SELECT](#SELECT) command for example) will be retrieved. If
specified, **variable2** will be set to the number of elements in
the list.

If the statement succeeds in retrieving the list, then the statements
associated with any THEN clause will be executed. If the statement
fails to find the list, then the statements associated with any ELSE
clause will be executed.

### NOTES

The GETLIST statement is identical in function to the
[READLIST](#READLIST) statement.
See also: [DELETELIST](#DELETELIST), [WRITELIST](#WRITELIST)

### EXAMPLE

       EXECUTE 'SELECT . SAMPLE 5' :@FM: 'SAVE-LIST FILES-LIST'
       GETLIST 'FILES-LIST' TO V.FILES.L ELSE
          CRT 'GETLIST error'
          STOP
       END
       LOOP
          REMOVE V.FILE FROM V.FILES.L SETTING V.STATUS
          CRT '[' : V.FILE : ']'
          IF V.STATUS EQ 0 THEN BREAK
       REPEAT

Output of this program looks like:

<pre>
    5 record(s) saved to list 'FILES-LIST'
    [&COMO&]
    [&COMO&]D]
    [&ED&]
    [&ED&]D]
    [&PH&]</pre>

## GETUSERGROUP

If the statement succeeds in retrieving the list, then the statements
the user ID specified by @uid. For Windows NT or Windows 2000, it
returns zero.

### COMMAND SYNTAX

    GETUSERGROUP(uid)

### EXAMPLES

In the following example, the program statement assigns the user group
to variable X:

    X = GETUSERGROUP(@UID)

In the next example, the program statement assigns the user group for
1023 to variable X:

    X = GETUSERGROUP(1023)

## GETX

<a name="GETX"/>

The GETX statement reads a block of data (in ASCII hexadecimal format)
directly from a device.

### COMMAND SYNTAX

    GETX Var {,length} { SETTING Count } FROM Device { UNTIL TermChars } \
         { RETURNING TermChar } { WAITING Timeout } THEN | ELSE statements

### SYNTAX ELEMENTS

**Var** is the variable in which to place the input (from the
previously open Device).

If specifying a length it limits the number of characters read
from the input device.

If the optional Count option is used, it returns the number of
characters actually read from the device.

Device is the file variable associated with the result from a
successful [OPENSEQ](#OPENSEQ) or [OPENSER](#OPENSER) command.

**TermChars** specifies one or more characters that will terminate
input.

**TermChar** The actual character that terminated input

**Timeout** is the number of seconds to wait for input.  If no input
is present when the timeout period expires, the ELSE clause
(if specified) is executed.

### NOTES

The GETX statement does no pre-or post-processing of the input data
stream nor does it handle any terminal echo characteristics. It is
assumed that if this is desired the application - or device drive -
will handle it.

If there are no specified length and timeout expressions, the default
input length is one (1) character. If there is no length specified,
but TermChars are, there is no limit to the number of characters input.
The GETX syntax requires a specified THEN or ELSE clause, or both.
The THEN clause executes when the data received is error free; the
ELSE clause executes when the data is unreceiveable (or a timeout
occurs).

GETX will convert all input into ASCII hexadecimal format after input.

See also: [GET](#GET)

## GOSUB

<a name="GOSUB"/>

The GOSUB statement causes execution of a local subroutine, after which
execution will continue with the next line of code.

### COMMAND SYNTAX

    GOSUB label

### SYNTAX ELEMENTS

The label should refer to an existent label within the current source
code, which identifies the start of a local subroutine.

### EXAMPLE

       var_1 = 1  ; var_2 = 2  ; var_3 = 3
       GOSUB MAKE.ARRAY
       GOSUB OUTPUT                               ;* -1^-2^-3
       var_1 = -1  ; var_2 = -2 ; var_3 = -3
       GOSUB MAKE.ARRAY
       GOSUB OUTPUT                               ;* 1^2^3
       var_1 = 1  ; var_2 = -2 ; var_3 = 3
       GOSUB MAKE.ARRAY
       GOSUB OUTPUT                               ;* -1^2^-3
       STOP
    *------------------------Subroutines------------------------------------
    MAKE.ARRAY:
       dyn_array = NEGS(var_1 :@FM: var_2 :@FM: var_3)
       RETURN
    *------------
    OUTPUT:
       CRT FMT(dyn_array, 'MCP')
       RETURN

If you, for example, forget a RETURN in MAKE.ARRAY section the execution will
continue till the next RETURN, i.e. section OUTPUT will be executed 6 times
instead of 3.

## GOTO

The GOTO statement causes program execution to jump to the code at a
specified label.

### COMMAND SYNTAX

    GO{TO} Label

### SYNTAX ELEMENTS

The label should refer to an existing label within the current source
code.

### NOTES

Warning: using the GOTO command obscures the readability of the code
and is a hindrance to maintainability. All programs written using the
GOTO construct can be written using structured statements such as
LOOP and FOR. There are various opinions on this issue but the
consensus is, avoid GOTO.

One possibly acceptable use of the GOTO statement is to transfer
execution to an error handler upon detection of a fatal error that
will cause the program to terminate.

### EXAMPLE

    GOTO Exception ;* jump to the exception handler
    .....
    * exception handler
    Exception:
    ....
    STOP

## GROUP

<a name="GROUP"/>

The GROUP function is equivalent to the FIELD function.

### COMMAND SYNTAX

    GROUP(Expression1, Expression2, Expression3, Expression4)

### SYNTAX ELEMENTS

**Expression1** evaluates to the string containing fields to be
extracted.

**Expression2** evaluates to the character(s) delimiting each field
within Expression1.

**Expression3** should evaluate to a numeric value specifying the
number of the first field to extract from Expression1.

**Expression4** evaluates to a numeric value specifying the number
of fields to extract as a group.

### NOTES

Expression2 may evaluate to more than a single character allowing
fields to be delimited with complex expressions.

### EXAMPLES

    A = "123:-456:-789:-987:-"
    CRT GROUP(A, ':-', 2, 2)

This example displays the following on the terminal (being the second and
third fields and their delimiter within variable A):

<pre>
    456:-789</pre>

## GROUPSTORE

Insert the variable contents into dynamic array (or replace an element in it).

### COMMAND SYNTAX

    GROUPSTORE from.var IN to.var USING start, replace, delimiter

### EXAMPLE

        to.var = 'QQQ' :@FM: 'WWW' :@FM: 'EEE'
        from.var = 'rtz'
        GROUPSTORE from.var IN to.var USING 2, 0, @FM   ;* start,replace,delim
        CRT FMT(to.var, 'MCP')                          ;* QQQ^rtz^WWW^EEE
        GROUPSTORE from.var IN to.var USING 4, 1
        CRT FMT(to.var, 'MCP')                          ;* QQQ^rtz^WWW^rtz
        GROUPSTORE from.var IN to.var USING 2, 0, @VM
        CRT FMT(to.var, 'MCP')                          ;* QQQ^rtz^WWW^rtz]rtz

## HEADING

Heading halts all subsequent output to the terminal at the end of each
page. The statement evaluates and displays an expression at the top of
each page. Current output sent to the terminal, is paused until entry
of a carriage return at the terminal - unless the N option is
specified.

### COMMAND SYNTAX

    HEADING expression

### SYNTAX ELEMENTS

The expression should evaluate to a string printed at the top of every
page of output. The string may contain a number of interpreted special
characters, replaced in the string before printing. The following
characters have special meaning within the string:

| Value     |    Description                                         |
|-----------|--------------------------------------------------------|
|"C{n}"     |  Center the line. If n is specified the output line is |
|           |  assumed to be n characters long.                      |
|"D" or \\  |  Replace with the current date.                        |
|"L" or ]   |  Replace with the newline sequence.                    |
|"N"        |  Terminal output does not pause at the end of each     |
|           |  page.                                                 |
|"P" or ^   |  Replace with the current page number.                 |
|"PP" or ^^ |  Replace with the current page number in a field of 4  |
|           |  characters. The field is right justified.             |
|"T" or \   |  Replace with the current time and date.               |
|"          |  Replace with a single " character.                    |

### NOTES

If output is to the printer, a PRINTER ON statement is in use, and does
not page output sent to the terminal with the CRT statement. Unless you
specify the "N" option, all output sent to the terminal is paged.

### EXAMPLES

    HEADING 'Programming staff by size of waist Page "P"'

## HEADINGE and HEADINGN##

The HEADINGE statement is the same as the HEADING statement, which
causes a page eject with the HEADING statement.

The HEADINGN statement is the same as the HEADING statement, and
suppresses the page eject.

## HUSH

Use the HUSH statement to suppress the display of all output normally
sent to a terminal during processing. HUSH also suppresses output to a
COMO file.

HUSH acts as a toggle. If it is used without a qualifier, it changes
the current state. Do not use this statement to shut off output
display unless you are sure the display is unnecessary. When you use
HUSH ON, all output is suppressed including error messages and requests
for information.

### COMMAND SYNTAX

    HUSH { ON | OFF | expression }

### EXAMPLE

       CRT 'PASSWORD:':
       HUSH ON
       INPUT V.PASSWORD
       HUSH OFF

## ICONV

The ICONV function converts data in external form such as dates to
their internal form.

### COMMAND SYNTAX

    ICONV(expression1, expression2)

### SYNTAX ELEMENTS

**expression1** evaluates to the data upon which the conversion is
to be performed.

**expression2** should evaluate to the conversion code that is to be
performed against the data.

### NOTES

If the conversion code used assumes a numeric value and a non-numeric
value is passed then the original value in expression1 is returned
unless the emulation option iconv_nonnumeric_return_null is set.

### EXAMPLES

    * see internal date representation
       CRT ICONV('20121231', 'D')                            ;* 16437
    * calculate difference between dates
       CRT ICONV('20121231', 'D') - ICONV('20111231', 'D')   ;* 366
    * check if a year is a leap one
       CRT OCONV( ICONV('20111231', 'D4'), 'DJ' )    ;*  365
       CRT OCONV( ICONV('20121231', 'D4'), 'DJ' )    ;*  366

       CRT ICONV('00:01:02', 'MTS')        ;* 62
       CRT ICONV('4020412042', 'MX')       ;* @ A B

## ICONVS

<a name="ICONVS"/>

Use ICONVS to convert each element of dynamic.array to a specified
internal storage format.

### COMMAND SYNTAX

    ICONVS(dynamic.array, conversion)

### SYNTAX ELEMENTS

**conversion** is an expression that evaluates to one or more valid
conversion codes, separated by value marks (ASCII 253).

Each element of **dynamic.array** is converted to the internal format
specified by conversion and is returned in a dynamic array. If multiple
codes are used, they are applied from left to right. The first
conversion code converts the value of each element of dynamic.array.
The second conversion code converts the value of each element of the
output of the first conversion, and so on. If dynamic.array evaluates
to null, it returns null. If an element of dynamic.array is null, null
it returns null for that element. If conversion evaluates to null, the
ICONV function fails and the program terminates with a run-time error
message.

The STATUS function reflects the result of the conversion:

|Code|     Description                                                   |
|----|-------------------------------------------------------------------|
| 0  |The conversion is successful.                                      |
| 1  |An element of dynamic.array is invalid. It returns an empty string,|
|    |unless dynamic.array is null, in which case it returns null.       |
| 2  |Conversion is invalid.                                             |
| 3  |Successful conversion of possibly invalid data.                    |

See also: [OCONVS](#OCONVS) function.

## IF (statement)

Allows other statements to be conditionally executed

### COMMAND SYNTAX

    IF expression THEN | ELSE statements

### SYNTAX ELEMENTS

It evaluates the expression to a value of Boolean TRUE or FALSE. If the
expression is TRUE executes then the statements defined by the THEN
clause (if present). If the expression is FALSE executes the statements
defined by the ELSE clause.

The THEN and ELSE clauses may take two different forms being single
and multiple line statements.

The simplest form of either clause is of the form:

    IF A THEN CRT A

Or

    IF A ELSE CRT A

However, expand the clauses to enclose multiple lines of code using the
END keyword as so:

    IF A THEN
        A = A*6
        CRT A
    END ELSE
        A = 76
        CRT A
    END

You can combine the single and multi-line versions of either clause to
make complex combinations of the command. For reasons of readability
it is suggested that where both clauses are present for an IF statement
that the same form of each clause is coded.

### NOTES

IF statements can be nested within either clause to any number of
levels.

### EXAMPLE

    CRT "Are you sure (Y/N) " :
    INPUT Answer, 1_
    IF OCONV (Answer, 'MCU') = "Y" THEN
        GOSUB DeleteFiles
        CRT "Files have been deleted"
    END ELSE
        CRT "File delete was ignored"
    END

## IFS

Use the IFS function to return a dynamic array whose elements are
chosen individually from one of two dynamic arrays based on the
contents of a third dynamic array.

### COMMAND SYNTAX

    IFS(dynamic.array, true.array, false.array)

IFS evaluate each element of the **dynamic.array**. If the element
evaluates to true, it returns the corresponding element from
**true.array** to the same element of a new dynamic array. If the
element evaluates to false, it returns the corresponding element
from **false.array**. If there is no corresponding element in the
correct response array, it returns an empty string for that
element. If an element is null, that element evaluates to false.

## IN

<a name="IN"/>

The IN statement allows the program to receive raw data from the
input device, which is normally the terminal keyboard, one character
at a time.

### COMMAND SYNTAX

    IN Var { FOR expression THEN | ELSE statements }

### SYNTAX ELEMENTS

**Var** will be assigned the numeric value (0 - 255 decimal) of the
next character received from the input device. The statement will
normally wait indefinitely (block) for a character from the keyboard.

Specifying the FOR clause to the IN statement allows the statement
to stop waiting for keyboard after a specified amount of time. The
expression should evaluate to a numeric value, which will be taken
as the number of deci-seconds (tenths of a second) to wait before
abandoning the input.

The **FOR** clause must have either or both of the THEN or ELSE
clauses If a character is received from the input device before the
time-out period then Var is assigned its numeric value and the THEN
clause is executed (if present). If the input statement times out
before a character is received then Var is unaltered and the ELSE
clause is executed (if present).

### NOTES

See also: [INPUT](#INPUT), [INPUTNULL](#INPUTNULL).

### EXAMPLE

       LOOP
          IN in_key
          IF in_key EQ 27 THEN ;* ESC seen
             IN in_key_2 FOR 2 THEN ;* Function Key?
                IN in_key_3 FOR 2 THEN
                   CRT ''
                   BEGIN CASE
                   CASE in_key_2 EQ 79 AND in_key_3 EQ 80
                      CRT 'F1 detected'
                   CASE in_key_2 EQ 79 AND in_key_3 EQ 81
                      CRT 'F2 detected'
                   END CASE
                END
             END ELSE
                CRT ''
                CRT 'ESC pressed, exiting'
                STOP
             END
          END
       REPEAT

## INDEX

The INDEX function will return the position of a character or
characters within another string.

### COMMAND SYNTAX

    INDEX(expression1, expression2, expression3)

### SYNTAX ELEMENTS

**expression1** evaluates to the string to be searched.

**expression2** evaluates to the string or character that will
be searched for within expression1.

**expression3** should evaluate to a numeric value and specify
which occurrence of expression2 should be searched for within
expression1.

### NOTES

If the specified occurrence of expression2 is not found in
expression1 then it returns Zero (0).

### EXAMPLE

    ABet = "abcdefghijklmnopqrstuvwxyzabc"
    CRT INDEX(ABet, 'a', 1)
    CRT INDEX(ABet, 'a', 2)
    CRT INDEX(ABet, 'jkl', 1)

The above code will display:

<pre>
    1
    27
    10</pre>

## INMAT

The INMAT() function returns the number of dimensioned array elements.

### COMMAND SYNTAX

    INMAT( {array} )

DESCRIPTION

Using the INMAT() function, without the 'array' argument, returns the
number of dimensioned array elements from the most recent
[MATREAD](#MATREAD), [MATREADU](#MATREADU), [MATREADL](#MATREADL) or
[MATPARSE](#MATPARSE) statement. If the number of array elements exceeds
the number of elements specified in the corresponding [DIMENSION](#DIMENSION)
statement, the INMAT() function will return zero.

Using the INMAT(), function with the 'array' argument, returns the
current number of elements to the dimensioned 'array'.

### NOTES

In some dialects the INMAT() function is also used to return the modulo
of a file after the execution of an OPEN statement, which is
inconsistent with its primary purpose and not implemented in jBASE. To
achieve this functionality use the [IOCTL](#IOCTL) function with the
JIOCTL_COMMAND_FILESTATUS command.

### EXAMPLES

       DIM cust_rec(99)
       MAT cust_rec = ''
       CRT INMAT(cust_rec)                  ;* 99
       DIM cust_rec(299)
       cust_rec(150) = 'Y'
       CRT INMAT(cust_rec)                  ;* 299
       CRT INMAT()                          ;* 0
       *
       EXECUTE 'DELETE-FILE DATA F.TEMP'
       EXECUTE 'CREATE-FILE DATA F.TEMP 1 101 TYPE=J4'
       OPEN 'F.TEMP' TO f_temp ELSE ABORT 201, 'F.TEMP'
       new_rec = 'LINE 1' :@FM: 'LINE 2' :@FM: 'LINE 3'
       WRITE new_rec TO f_temp, 'REC1'
       *
       MAT cust_rec = ''
       MATREAD cust_rec FROM f_temp, 'REC1' ELSE
          CRT 'Read error'
          STOP
       END
       CRT INMAT(cust_rec)                  ;* 299 - current size
       CRT INMAT()                          ;* 3
       *
       dyn_array = 1 :@FM: 2 :@VM: 3 :@SM: 4: @FM: 5 :@FM: 6
       MATPARSE cust_rec FROM dyn_array
       CRT INMAT()                          ;* 4 (only FMs count)
       CRT FMT(cust_rec(2), 'MCP')          ;* 2]3\4
       DIM cust_rec(100,2)
       CRT FMT( INMAT(cust_rec), 'MCP' )      ;* 100]2

## INPUT

<a name="INPUT"/>

The INPUT statement allows the program to collect data from the current
input device, which will normally be the terminal keyboard but may be
stacked input from the same or separate program.

### COMMAND SYNTAX

    INPUT {@ (expression1 {, expression2 )}{:} Var{{, expression3}, expression4} \
          {:}{_} { WITH expression5 } { FOR expression6 THEN | ELSE statements }

### SYNTAX ELEMENTS

**@(expression1, expression2)** allows the screen cursor to be
positioned to the specified column and row before the input prompt is
sent to the screen. The syntax for this is the same as the @( )
function described earlier.

**Var** is the variable in which the input data is to be stored.

**expression3**, when specified, should evaluate to a numeric value.
This will cause input to be terminated with an automatic newline
sequence after exactly this number of characters has been input.
If the _ option is specified with expression4 then the automatic
newline sequence is not specified but any subsequent input characters
are belled to the terminal and thrown away.

**expression4** when specified, should evaluate to a sequence of 1
to 3 characters. The first character will be printed expression3
times to define the field on the terminal screen. At the end of the
input if less than expression3 characters were input then the rest
of the field is padded with the second character if it was supplied.
If the third character is supplied then the cursor will be
positioned after the last character input rather than at the end
of the input field.

The : option, when specified, suppress the echoing of the newline
sequence to the terminal. This will leave the cursor positioned
after the last input character on the terminal screen.

WITH expression5 allows the default input delimiter (the newline
sequence) to be changed. When specified, expression5, should
evaluate to a string of up to 256 characters, each of which may
delimit the input field. If this clause is used then the newline
sequence is removed as a delimiter and must be specified
explicitly within expression5 as CHAR(10).

The "FOR" clause allows the "INPUT" statement to time out after a
specified waiting period instead of blocking as normal Expression6
should evaluate to a numeric value, which will be taken as the
number of deci-seconds (tenths of a second) to wait before timing
out. The time-out value is used as the time between each keystroke
and should a time-out occur, Var would hold the characters that
were input until the time-out.

The FOR clause requires either the THEN and ELSE clauses or both;
if no time-out occurs the THEN clause is taken. If a time-out does
occur, the ELSE clause is taken.

### NOTES

The INPUT statement will always examine the data input stack before
requesting data from the input device. If data is present on the
stack then it is used to satisfy INPUT statements one field at a
time until the stack is exhausted. Once exhausted, the INPUT statement
will revert to the input device for further input. There is no way
(by default) to input a null field to the INPUT@ statement. If the
INPUT@ statement receives the newline sequence only as input, then
the Var will be unchanged. Use the INPUTNULL statement to define a
character that indicates a NULL input.

Use the CONTROL-CHARS command to control whether or not control
characters (i.e. those outside the range x'1F' - x'7F') are
accepted by INPUT.

See also: [IN](#IN), [INPUTNULL](#INPUTNULL).

### EXAMPLE

Ask user for an input; time limit is 60 seconds; every 3 seconds the
remaining time is updated on user screen.

       V.TIMEOUT = 60
       GOSUB UPD.CNT
       V.ANS = ''
       LOOP
       WHILE V.ANS EQ '' DO
          INPUT V.ANS, 1 : FOR 30 ELSE
             V.TIMEOUT -= 3
             IF V.TIMEOUT LE 0 THEN BREAK
             GOSUB UPD.CNT
          END
       REPEAT
       IF V.ANS NE '' THEN CRT 'The choice was', DQUOTE(V.ANS)
       ELSE CRT "The choice wasn't done"
       STOP
    UPD.CNT:
       CRT @(0):'Seconds left: ': FMT(V.TIMEOUT, '2R') : '. Your choice':
       RETURN


### EXAMPLE 2

Pad the input field.

Code:

       CRT @(-1)
       INPUT @(17,2):the_input,50,'_..':_

User screen:

                        ? _________________________________________________


See also: [PROMPT](#PROMPT).

## INPUTCLEAR

The INPUTCLEAR statement clears the type-ahead buffer.

### COMMAND SYNTAX

    INPUTCLEAR

### SYNTAX ELEMENTS

None

### NOTES

INPUTCLEAR only clears the type-ahead buffer. It does not clear data
stacked with the DATA statement.

The INPUTCLEAR statement is synonymous with [CLEARINPUT](#CLEARINPUT).

### EXAMPLE

    CRT "Start year end processing (Yes/No) :"
    INPUTCLEAR
    INPUT ans
    IF ans # "Yes" THEN
    CRT "year end processing not started"
    END

## INPUTNULL

<a name="INPUTNULL"/>

The INPUTNULL statement allows the definition of a character that
will allow a null input to be seen by the INPUT@ statement.

### COMMAND SYNTAX

    INPUTNULL expression

### SYNTAX ELEMENTS

The **expression** should evaluate to a single character.
Subsequently, any INPUT@ statement that sees only this character
input before the new-line sequence will NULL the variable in
which input is being stored.

If expression evaluates to the NULL string " then the default
character of _ is used to define a NULL input sequence.

### NOTES

The INPUT statement does not default to accepting the _ character
as a NULL input, the programmer must explicitly allow this with
the statement: INPUTNULL ''. In the example below an ampersand can be used
to input the empty value.

### EXAMPLE

    INPUTNULL "&"
    INPUT @(10,10):Answer,1
    IF Answer = '' THEN
       CRT "A NULL input was received"
    END

## INS

<a name="INS"/>

The INS statement allows the insertion of elements into a dynamic
array.

### COMMAND SYNTAX

    INS expression BEFORE Var<expression1{, expression2{, expression3}}>

### SYNTAX ELEMENTS

**expression** evaluates to the element to be inserted in the dynamic
array.

**expression1** expression2 and expression3 should all evaluate to
numeric values and specify the Field, Value and Sub-Value before
which the new element is to be inserted.

### NOTES

Specifying a negative value to any of the expressions 1 through 3
will cause the element to append as the last Field, Value or
Sub-Value rather than at a specific position. Only one expression
may be negative otherwise only the first negative value is used
correctly while the others are treated as the value 1.

The statement will insert NULL Fields, Values or Sub-Values
accordingly if any of the specified insertion points exceeds the
number currently existing.

### EXAMPLE

       Values = ''
       FOR I = 1 TO 50
          INS I BEFORE Values<-1>
       NEXT I
       FOR I = 2 TO 12
          INS I*7 BEFORE Values<7,I>
       NEXT I
       CRT FMT(Values, 'MCP')

The output is (one line):

<pre>
    1^2^3^4^5^6^7]14]21]28]35]42]49]56]63]70]77]84^8^9^10^11^12^13^14^15^16^
    17^18^19^20^21^22^23^24^25^26^27^28^29^30^31^32^33^34^35^36^37^38^39^40^
    41^42^43^44^45^46^47^48^49^50</pre>

## INSERT

<a name="INSERT"/>

INSERT is the function form of the INS statement, with preference
given to the use of INS.

### COMMAND SYNTAX

    INSERT(expression1, expression2{, expression3 {, expression4 }}; expression5)

### SYNTAX ELEMENTS

**expression1** evaluates to a dynamic array in which to insert a
new element and will normally be a variable.

**expression2**, **expression3** and **expression4** should evaluate to numeric
values and specify the Field, Value and Sub-Value before which the new
element will be inserted.

**expression5** evaluates to the new element to be inserted in
expression1.

### EXAMPLES

        B = 'Field 1' :@VM: 2 :@VM: 3 :@VM: 5 :@FM: 'Field 2'
        A = INSERT(B, 1, 4; 'Field1Value4')
        CRT OCONV(A, 'MCP')          ;* Field 1]2]3]Field1Value4]5^Field 2

## INT

<a name="INT"/>

The INT function truncates a numeric value into its nearest integer
form.

### COMMAND SYNTAX

    INT(expression)

### SYNTAX ELEMENTS

expression should evaluate to a numeric value. The function will then
return the integer portion of the value.

### NOTES

The function works by truncating the fractional part of the numeric
value rather than by standard mathematical rounding techniques.
Therefore, INT(9.001) and INT(9.999) will both return the value 9.

### EXAMPLES

    CRT INT(22 / 7)

Displays the value 3

## IOCTL

<a name="IOCTL"/>

The jBC language provides an intrinsic function called IOCTL that
behaves in a similar manner to the C function ioctl(). Its purpose
is to allow commands to be sent to the database driver for a
particular file, and then to receive a reply from the database
driver.

As with the C function ioctl, the use of IOCTL is highly dependent
upon the database driver it is talking to. Each database driver may
choose to provide certain common functionality, or may add its own
commands and so on. This is especially true of user-written database
drivers.

First, an example of a source program that opens a file and finds
the type of file:

    INCLUDE JBC.h
    OPEN "MD" TO DSCB ELSE STOP 201, "MD"
    status = ""
    IF IOCTL(DSCB, JIOCTL_COMMAND_FILESTATUS, status) THEN
       PRINT "Type of file = " : DQUOTE(status<1>)
    END ELSE
       PRINT "IOCTL FAILED !! unknown file type"
    END

If the ELSE clause is taken, it does not necessarily mean there is
an error, it only means that the database driver for file "MD"
does not support the command that was requested from it. The file
JBC.h is supplied with jBASE in the directory TAFC_HOME sub
directory include. If the source is compiled with the jbc or BASIC
command, this directory is automatically included in the search path
and no special action is needed by the programmer for the "INCLUDE
JBC.h" statement.

The format of the IOCTL function is:

    IOCTL(Filevar, Command, Parameter)

Where:

**filevar** Is a variable that has had a file opened against it
using the OPEN statement. However, if you want to use the default
file variable, use -1 in this position.

For example:

    OPEN "MD" ELSE STOP
    filevar = -1
    IF IOCTL(filevar, JIOCTL_COMMAND_xxx, status)
    ...

**command** can be any numeric value (or variable containing a
numeric). However, it is up to the database driver to support that
particular command number. The remainder of this chapter describes
the common IOCTL command numbers supported by the jBASE database
drivers provided.

Status Pass here a jBC variable. The use of this variable depends
upon the command parameter, and will be described later for each
command supported.

The return value is 0 for failure, or 1 for success. A value of
"-1" generally shows the command has not been recognized.

The remainder of this section will deal with the IOCTL commands
that are supported by the provided jBASE database drivers, and the
JBC_COMMAND_GETFILENAME command that is supported for all database
drivers.

*JBC_COMMAND_GETFILENAME COMMAND*
Using this command to the IOCTL function, you can determine the exact
file name that was used to open the file. This is helpful because
jEDI uses Q pointers, F pointers and the JEDIFILEPATH environment
variable to actually open the file, and the application can never be
totally sure where the resultant file was really opened. Normally of
course, this is of no concern to the application.

### EXAMPLE

Open the file CUSTOMERS and find out the exact path that was used to
open the file.

    INCLUDE JBC.h
    OPEN "CUSTOMERS" TO DSCB ELSE STOP 201, "CUSTOMERS"
    filename = ""
    IF IOCTL(DSCB, JBC_COMMAND_GETFILENAME, filename) ELSE
       CRT "IOCTL failed !!" ; EXIT(2)
    END
    PRINT "Full file path = " : DQUOTE(filename)

This command is executed by the jBC library code rather than the jEDI
library code or the database drivers, so it can be run against a file
descriptor for any file type.

*JIOCTL_COMMAND_CONVERT COMMAND*

Some of the jBC database drivers will perform an automatic conversion
of the input and output record when performing reads and writes.

An example of this is when writing to a directory. In this case, the
attribute marks will be converted to new-line characters and a
trailing new-line character added. Similarly for reading from a
directory the new-line characters will be replaced with attribute
marks, and the trailing new-line character will be deleted.

The above example is what happens for the database driver for
directories. It assumes by default that the record being read or
written is a text file and that the conversion is necessary. It tries
to apply some intelligence to reading files, as text files always have
a trailing new-line character. Therefore, if a file is read without a
trailing new-line character, the database driver assumes the file must
be a binary file rather than a text file, and no conversion takes
place.

This conversion of data works in most cases and usually requires no
special intervention from the programmer.

There are cases however, when this conversion needs to be controlled
and interrogated, and the IOCTL function call with the
JIOCTL_COMMAND_CONVERT command provides the jBASE database drivers
that support this conversion with commands to control it.

The call to IOCTL, if successful, will only affect file operations
that use the same file descriptor. Consider the following code:

    INCLUDE JBC.h
    OPEN "MD" TO FILEVAR1 ELSE ...
    OPEN "MD" TO FILEVAR2 ELSE ...
    IF IOCTL(FILEVAR1, JIOCTL_COMMAND_CONVERT, 'RB')

In the above example, any future file operations using variable
FILEVAR1 will be controlled by the change forced in the IOCTL
request. Any file operations using variable FILEVAR2 will not be
affected and will use the default file operation.

Input to the IOCTL is a string of controls delimited by a comma
that tell the database driver what to do. The output from the IOCTL
can optionally be a string to show the last conversion that the
driver performed on the file.

The descriptions of the available controls that can be passed as
input to this IOCTL function are:

|Code  |                    Description                                 |
|------|----------------------------------------------------------------|
| RB   | All future reads to be in binary (no conversion)               |
| RT   | All future reads to be in text format (always do a             |
|      | conversion)                                                    |
| RS   | Return to caller the status of the last read("B" = binary,     |
|      | "T" = text)                                                    |
| WB   | All future writes to be in binary (no conversion)              |
| WT   | All future writes to be in text format (always do a            |
|      | conversion)                                                    |
| WI   | All future writes to decide themselves whether binary or text  |
| WS   | Return to caller the status of the last write ("B" = binary,   |
|      | "T" = text )                                                   |
| KB   | All future reads/writes have the record key unaltered          |
| KT   | All future reads/writes have the record key modified           |
| KI   | All future reads/writes to decide if to do a conversion        |
| KS   | Return to caller the status of the last record key             |
|      | ("B" = binary, "T" = text )                                    |

### EXAMPLE 1

The application wants to open a file, and to ensure that all reads and writes to that file are in binary, and that no translation such as new-lines to attribute marks is performed.

    INCLUDE JBC.h
    OPEN "FILE" TO DSCB ELSE STOP 201, "FILE"
    IF IOCTL(DSCB,JIOCTL_COMMAND_CONVERT, 'RB,WB') ELSE
       CRT "UNABLE TO IOCTL FILE 'FILE'" ; EXIT(2)
    END

### EXAMPLE 2

Read a record from a file, and find out if the last record read was in text format (were new-lines converted to attribute marks and the trailing new-line deleted), or in binary format (with no conversion at all).

    INCLUDE JBC.h
    OPEN "." TO DSCB ELSE STOP 201, "."
    READ rec FROM DSCB, "prog.o" ELSE STOP 202, "prog.o"
    status = "RS"
    IF IOCTL(DSCB, JIOCTL_COMMAND_CONVERT, status) THEN
       IF status EQ "T" THEN CRT "TEXT" ELSE CRT "BINARY"
    END ELSE
       CRT "The IOCTL failed !!"
    END

<a name="JIOCTL_COMMAND_FILESTATUS"/>

*JIOCTL_COMMAND_FILESTATUS COMMAND*

The JIOCTL_COMMAND_FILESTATUS command will return an attribute delimited list of the status of the file to the caller.

| Attribute |                 Description                                |
|-----------|------------------------------------------------------------|
| <1>       |File type, as a string                                      |
| <2>       |File type, as a string                                      |
| <2>       |FileFlags, as decimal number, show LOG, BACKUP and TRANS    |
| <3>       |BucketQty, as decimal number, number of buckets in the file |
| <4>       |BucketSize, as decimal number, size of each bucket in bytes |
| <5>       |SecSize, as decimal number, size of secondary data space    |
| <6>       |Restore Spec, a string showing any restore re-size          |
|           |specification                                               |
| <7>       |Locking identifiers, separated by multi-values              |
| <8>       |FileFlags showing LOG, BACKUP and TRANSACTION permissions   |
| <8,1>     |Set to non-zero to suppress logging on this file            |
| <8,2>     |Set to non-zero to suppress transaction boundaries on this  |
|           |file                                                        |
| <8,3>     |Set to no-zero to suppress backup of the file using jbackup |
| <9>       |Hashing algorithm used                                      |

### EXAMPLE 1

Open a file and see if the file type is a directory.

    INCLUDE JBC.h
    OPEN ".." TO DSCB ELSE STOP 201, ".."
    status = ""
    IF IOCTL(DSCB, JIOCTL_COMMAND_FILESTATUS, status) ELSE
       CRT "IOCTL failed !!" ; EXIT(2)
    END
    IF status<1> EQ "UD" THEN
       PRINT "File is a directory"
    END ELSE
       PRINT "File type is " : DQUOTE(status<1>)
       PRINT "This is not expected for .."
    END

### EXAMPLE 2

Open a file ready to perform file operations in a transaction against
it. Make sure the file has not been removed as a transaction type
file by a previous invocation of the command "jchmod -T CUSTOMERS".

    INCLUDE JBC.h
    OPEN "CUSTOMERS" TO DSCB ELSE STOP 201, "CUSTOMERS"
    IF IOCTL(DSCB, JIOCTL_COMMAND_FILESTATUS, status) ELSE
       CRT "IOCTL failed !!" ; EXIT(2)
    END
    IF status<8,2> THEN
       CRT "Error ! File CUSTOMERS is not"
       CRT "part of transaction boundaries !!"
       CRT 'Use "jchmod +T CUSTOMERS" !!'
       EXIT(2)
    END

*JIOCTL_COMMAND_FINDRECORD COMMAND*

This command will find out if a record exists on a file without the
need to actually read in the record. This can provide large performance
gains in certain circumstances.

### EXAMPLE

Before writing out a control record, make sure it doesn't already exist.
As the control record is quite large, it will provide performance gains
to simply test if the output record already exists, rather than reading
it in using the READ statement to see if it exists.

    INCLUDE JBC.h
    OPEN "outputfile" TO DSCB ELSE STOP 201, "outputfile"
    * Make up the output record to write out in "output"
    key = "output.out"
    rc = IOCTL(DSCB, JIOCTL_COMMAND_FINDRECORD, key)
    BEGIN CASE
       CASE rc EQ 0
          WRITE output ON DSCB,key
          CRT "Data written to key " : key
       CASE rc GT 0
          CRT "No further action, record already exists"
       CASE 1
          CRT "IOCTL not supported for file type"
    END CASE

**JIOCTL_COMMAND_FINDRECORD_EXTENDED COMMAND**

This command to the IOCTL function returns the record size and the time
and date the record was last updated. If the record does not exist,
null is returned. The time/date stamp is returned in UTC format.

### EXAMPLE

Print the time and data of last update for each record in filename.

    INCLUDE JBC.h
    OPEN "filename" TO DSCB ELSE STOP 201, "filename"
    *
    * Select each record in the newly opened file
    *
    SELECT DSCB
    LOOP WHILE READNEXT record.key DO
    *
    * Get the details on the record and look for errors.
    *
       record.info = record.key
       IF IOCTL(DSCB, JIOCTL_COMMAND_FINDRECORD_EXTENDED, record.info) ELSE
          CRT "Error! File driver does not support this"
          STOP
       END
    *
    * Extract and convert the returned data
    *
       record.size = record.info<1>
       record.utc = record.info<2>
       record.time = OCONV(record.utc, 'U0ff0')
       record.date = OCONV(record.utc, 'U0ff1')
    *
    * Print the information.
    *
       PRINT "Record key " :record.key: " last updated at " :
       PRINT OCONV(record.time, 'MTS'): " " :
       PRINT OCONV(record.date, 'D4')
    REPEAT

**JIOCTL_COMMAND_HASH_RECORD COMMAND**

For jBASE hashed files such as j3 and j4 each record is pseudo-randomly
written to one of the buckets (or groups) of the hashed file. The actual
bucket it is written to depends upon two factors:

The actual record key (or item-id)

The number of buckets in the file (or modulo)

This IOCTL command shows which bucket number the record would be found
in, given the input record key. The bucket number is in the range 0 to
(b-1) where b is the number of buckets in the file specified when the
file was created (probably using CREATE-FILE).

The command only returns the expected bucket number, as is no indication
that the record actually exists in the file.

Two attributes are returned by this command. The first is the hash
value that the record key has hashed to, and the second attribute is
the bucket number.

### EXAMPLE

Open a file, and find out what bucket number the record "PIPE&SLIPPER"
would be found in.

    INCLUDE JBC.h
    OPEN "WEDDING-PRESENTS" TO DSCB ELSE STOP
    key = "PIPE&SLIPPER"
    parm = key
    IF IOCTL(DSCB, JIOCTL_COMMAND_HASH_RECORD, parm) THEN
      PRINT "key " :key: " would be in bucket " :parm<2>
    END ELSE
       CRT "IOCTL failed, command not supported"
    END

**JIOCTL_COMMAND_HASH_LOCK COMMAND**

The jEDI locking mechanism for records in jEDI provided database
drivers is not strictly a 100% record locking mechanism. Instead, it
uses the hashed value of the record key to give a value from 0 to
230-1 to describe the record key. The IOCTL command can be used to
determine how a record key would be converted into a hashed value for
use by the locking mechanism.

### EXAMPLE

Lock a record in a file and find out what the lock id of the record
key is. The example then calls the jRLA locking demon and the display
of locks taken should include the lock taken by this program.

    INCLUDE JBC.h
    DEFC getpid()
    OPEN "WEDDING-PRESENTS" TO DSCB ELSE STOP
    key = "PIPE&SLIPPER"
    parm = key
    IF IOCTL(DSCB, JIOCTL_COMMAND_HASH_LOCK, parm) ELSE
       CRT "IOCTL failed, command not supported"
       EXIT(2)
    END
    PRINT "The lock ID for the key is " : parm
    PRINT "Our process id is " : getpid()

## ISALPHA

The ISALPHA function will check that the expression consists of entirely
alphabetic characters.

### COMMAND SYNTAX

    ISALPHA(expression)

Same as [ALPHA](#ALPHA).

## ISALNUM##

The ISALNUM function will check that the expression consists of
entirely alphanumeric characters.

### COMMAND SYNTAX

    ISALNUM(expression)

### SYNTAX ELEMENTS

The expression can return a result of any type. The ISALNUM function
will then return TRUE (1) if the expression consists of entirely
alphanumeric characters. The function will return FALSE (0) if the
expression contains any characters, which are not alphanumeric.

### INTERNATIONAL MODE

When the ISALNUM function is used in International Mode the properties
of each character is determined according to the Unicode Standard.

### EXAMPLE

Extending the example for [ALPHA](#ALPHA):

       V.STRING = 'AWERC'
    * check if there are only alphabetic characters
       CRT ISALPHA(V.STRING)             ;* 1
    * add number to the end
       V.STRING := 1   ; CRT V.STRING    ;* AWERC1
    * check again if there are only alphabetic characters
       CRT ISALPHA(V.STRING)             ;* 0
    * check if there are only alphanumeric characters
       CRT ISALNUM(V.STRING)             ;* 1

## ISCNTRL

The ISCNTRL function will check that the expression consists entirely of
control characters.

### COMMAND SYNTAX

    ISCNTRL(expression)

### SYNTAX ELEMENTS

The expression can return a result of any type. The ISCNTRL function will
then return TRUE (1) if the expression consists of entirely control
characters. The function will return FALSE (0) if the expression contains
any characters, which are not control characters.

### INTERNATIONAL MODE

When the ISCNTRL function is used in International Mode the properties
of each character is determined according to the Unicode Standard.

### EXAMPLE

       V.STRING = CHAR(13) : CHAR(10)
       CRT ISCNTRL(V.STRING)        ;* 1
       V.STRING = @FM : V.STRING
       CRT ISCNTRL(V.STRING)        ;* 1

## ISDIGIT

The ISDIGIT function will check that the expression consists of entirely
numeric characters.

### COMMAND SYNTAX

    ISDIGIT(expression)

### SYNTAX ELEMENTS

The expression can return a result of any type. The ISDIGIT function
will then return TRUE (1) if the expression consists of entirely
numeric characters. The function will return FALSE (0) if the
expression contains any characters, which are not numeric.

### INTERNATIONAL MODE

When the ISDIGIT function is used in International Mode the properties
of each character is determined according to the Unicode Standard.

### EXAMPLE

       V.VAR = 5
       CRT ISDIGIT(V.VAR)                 ;* 1
       V.VAR = -1
       CRT ISDIGIT(V.VAR)                 ;* 0 (we have minus now)

## ISLOWER

The ISLOWER function will check that the expression consists of entirely
lower case characters.

### COMMAND SYNTAX

    ISLOWER(expression)

### SYNTAX ELEMENTS

The expression can return a result of any type. The ISLOWER function will
then return TRUE (1) if the expression consists of entirely lower case
characters. The function will return FALSE (0) if the expression contains
any characters, which are not lower case characters.

### INTERNATIONAL MODE

When the ISLOWER function is used in International Mode the properties of
each character is determined according to the Unicode Standard

## ISPRINT##

The ISPRINT function will check that the expression consists of entirely
printable characters.

### COMMAND SYNTAX

    ISPRINT(expression)

### SYNTAX ELEMENTS

The expression can return a result of any type. The ISPRINT function will
then return TRUE (1) if the expression consists of entirely printable
characters. The function will return FALSE (0) if the expression contains
any characters, which are not printable.

### INTERNATIONAL MODE

When the ISPRINT function is used in International Mode the properties of
each character is determined according to the Unicode Standard.

## ISSPACE

The ISSPACE function will check that the expression consists of entirely
space type characters.

### COMMAND SYNTAX

    ISSPACE(expression)

### SYNTAX ELEMENTS

The expression can return a result of any type. The ISSPACE function will
then return TRUE (1) if the expression consists of entirely spacing type
characters. The function will return FALSE (0) if the expression contains
any characters, which are not space characters.

### INTERNATIONAL MODE

When the ISSPACE function is used in International Mode the properties of
each character is determined according to the Unicode Standard.

### EXAMPLE

       a_string = ''             ;  GOSUB CHK.IT    ;*  0
       a_string := ' '           ;  GOSUB CHK.IT    ;*  1
       a_string := CHAR(9)       ;  GOSUB CHK.IT    ;*  1 (TAB)
       a_string := CHAR(10)      ;  GOSUB CHK.IT    ;*  1 (CR)
       a_string := CHAR(11)      ;  GOSUB CHK.IT    ;*  1 (Vertical Tab)
       a_string := CHAR(12)      ;  GOSUB CHK.IT    ;*  1 (Form feed)
       a_string := CHAR(13)      ;  GOSUB CHK.IT    ;*  1 (LF)
    *
       STOP
    *
    CHK.IT:
       CRT ISSPACE(a_string)
       RETURN
    END

## ISUPPER

The ISUPPER function will check that the expression consists of entirely
upper case characters.

### COMMAND SYNTAX

    ISUPPER(expression)

### SYNTAX ELEMENTS

The expression can return a result of any type. The ISUPPER function
will then return TRUE (1) if the expression consists of entirely lower
case characters. The function will return FALSE (0) if the expression
contains any characters, which are not upper case characters.

### INTERNATIONAL MODE

When the ISUPPER function is used in International Mode the properties
of each character is determined according to the Unicode Standard.

## ITYPE

<a name="ITYPE"/>

ITYPE function is used to return the value resulting from the
evaluation of an I-type expression in a jBASE file dictionary.

### COMMAND SYNTAX

    ITYPE(i.type)

**I.type** is an expression evaluating to the contents of the compiled
I-descriptor. You must compile the I-descriptor before the ITYPE
function uses it; otherwise, you get a run-time error message.

Using several methods set the I.type to the evaluated I-descriptor in
several ways. One way is to read the I-descriptor from a file
dictionary into a variable, then use the variable as the argument to
the ITYPE function. If the I-descriptor references a record ID, the
current value of the system variable **@ID** is used. If the
I-descriptor, references field values in a data record, the data is
taken from the current value of the system variable @RECORD.

To assign field values to @RECORD, read a record from the data file
into @RECORD before invoking the ITYPE function.

If i.type evaluates to null, the ITYPE function fails and the program
terminates with a run-time error message.

NOTE: Set the @FILENAME to the name of the file before ITYPE execution.

### EXAMPLE

    * Data preparation
    *
       V.FILE = 'F.TEMP'
       EXECUTE 'DELETE-FILE ' : V.FILE
       EXECUTE 'CREATE-FILE ' : V.FILE : ' 1 101 TYPE=J4'
       OPEN V.FILE TO F.TEMP ELSE ABORT 201, 'F.TEMP'
       OPEN 'DICT', V.FILE TO F.TEMP.DICT ELSE ABORT 201, 'F.TEMP]D'
    * Field 1 dictionary entry
       R.DICT.D1 = ''
       R.DICT.D1<1> = 'D'
       R.DICT.D1<2> = '1'
       R.DICT.D1<5> = '25L'
       R.DICT.D1<6> = 'S'
       WRITE R.DICT.D1 TO F.TEMP.DICT, 'FOOTWEAR'
    *
    * I-descriptor
       V.DESCR = 'SIZE'
       R.DICT.I = ''
       R.DICT.I<1> = 'I'
       R.DICT.I<2> = 'FOOTWEAR[":", 2, 1]'
       R.DICT.I<4> = V.DESCR
       R.DICT.I<5> = '3R'
       R.DICT.I<6> = 'S'
       WRITE R.DICT.I TO F.TEMP.DICT, V.DESCR
    *
    * Data records
       R.DATA = ''
       R.DATA<1> = 'SLIPPERS:8'
       WRITE R.DATA TO F.TEMP, 'JIM'
       R.DATA = ''
       R.DATA<1> = 'BOOTS:10'
       WRITE R.DATA TO F.TEMP, 'GREG'
       R.DATA = ''
       R.DATA<1> = 'SLIPPERS:5'
       WRITE R.DATA TO F.TEMP, 'ALAN'
    *
    * Data is prepared; now proceed it
    *
       @FILENAME = V.FILE
       READ V.ITYPE FROM F.TEMP.DICT, V.DESCR ELSE ABORT
    *
       SSELECT F.TEMP TO V.PEOPLE.L
       LOOP
          READNEXT V.ID FROM V.PEOPLE.L ELSE BREAK
          @ID = V.ID
          READ @RECORD FROM F.TEMP, @ID ELSE ABORT
          V.RET = ITYPE(V.ITYPE)
          CRT @ID : "'S FOOTWEAR HAS SIZE " : V.RET
       REPEAT

The output of this program is:

<pre>
    ALAN'S FOOTWEAR HAS SIZE 5
    GREG'S FOOTWEAR HAS SIZE 10
    JIM'S FOOTWEAR HAS SIZE 8</pre>

## JBASECOREDUMP

JBASECOREDUMP is used as a diagnostic tool for applications. It allows
a snapshot of the application to be dumped to an external file for later
analysis.

- The JBASECOREDUMP function will stop the execution of a jbc program or subroutine.
- The applications snapshot is also saved in the logs.
- The filename for the external file will always be unique.
- If called via jAgent an exception will be thrown.

### COMMAND SYNTAX

    JBASECOREDUMP(expression1, expression2)

### SYNTAX ELEMENTS

**expression1** should evaluate to a string:

If assigned a value, expression1 will be used as the extension for the external
text file created to hold execution snapshot.

    rc = JBASECOREDUMP('SERVICE', 0)

This will create the file with name structured as:

"JBASECOREDUMP.&lt;&lt;UUID&gt;&gt;.&lt;&lt;expression1&gt;&gt;",
e.g.:

<pre>
    JBASECOREDUMP.a57d07cc-6539-470f-9959-24ed7c715f4f.SERVICE.</pre>

If a null string is used:

    rc = JBASECOREDUMP('', 0)

This will create the file with name structured as:

"JBASECOREDUMP.&lt;&lt;UUID&gt;&gt;,
e.g.:

<pre>
    JBASECOREDUMP.a57d07cc-6539-470f-9959-24ed7c715f4f</pre>

**expression2** should evaluate to a numeric integer:

<pre>
    0: Add all varables to the external text file.
    1: Suppess any UNASSIGNED varables saved to the external file.</pre>

### NOTES

jBC functionality will be affected in the following areas:

- Calling from a jbc subroutine.
- Running a program in a jsh.
- External text filenames are now unique for coredump files.
- Calling process started via EXECUTE/PERFORM from within a jbc program.
- When called via jAgent, using a jbc subroutine.

*Calling from a jbc subroutine.*

When the JBASECOREDUMP function is called from a jbc program it will stop execution.
The call stack is saved to a file, and also saved to the logs.
Each core dump now is assigned a unique ID.

*Running a program in a jsh.*

If called from a program while in a jSH, a message is now displayed along
with the UUID for the core dump, you can use this to locate the stack trace
in the logs.

<pre>
    &lowast;&lowast; Error [ JBASECOREDUMP ] &lowast;&lowast; Program Aborted, Coredump UUID: &lt;&lt;UUID&gt;&gt;</pre>

*Calling process started via EXECUTE/PERFORM from within a jbc program.*

If JBASECOREDUMP is called from a process started via EXECUTE/PERFORM from a
jbc program, use RETURNING/SETTING to capture the output associated with any
error messages the executing program issues.

    EXECUTE "MYPROGRAM" CAPTURING junk SETTING rc
         * rc<1,1> holds the error code "JBASECOREDUMP".
         * rc<1,2> holds the UUID for the core dump.

Because all JBASECOREDUMP's are logged you can use this UUID to check the log files.

*When called via jAgent, using a jbc subroutine.*

A new exception type has been created to return the UUID to the client
application. (JSubroutineCoreDumpException)

The following is a simple example of how to check for core dumps.

<pre>
    try {
      _connection.call("CALLCOREDUMP_WITH_FILENAME", null);
    }
    catch (const JSubroutineCoreDumpException &e) {
      const std::string uuid = e.getMessage()->c_str();
      // handle exception
    }</pre>

Use this UUID to check on the server for what went wrong.
The Java and C# clients have also been updated to handle this new exception
type.

### EXAMPLE

example.b:

    001 rc = JBASECOREDUMP('ERRORFILE', '')

Compile:

<pre>
    jcompile example.b</pre>

run:

<pre>
    &lowast;&lowast; Error [ JBASECOREDUMP ] &lowast;&lowast; Program Aborted,
    Coredump UUID: 4d5a252a-c009-4aec-9e1f-73d3251c6b81</pre>

<pre>
     dir JBASECOREDUMP&lowast;
    JBASECOREDUMP.4d5a252a-c009-4aec-9e1f-73d3251c6b81.ERRORFILE</pre>

<pre>
    ct . JBASECOREDUMP.4d5a252a-c009-4aec-9e1f-73d3251c6b81.ERRORFILE
    JBASECOREDUMP.4d5a252a-c009-4aec-9e1f-73d3251c6b81.ERRORFILE
    001 jBASE Core dump created at Fri Feb 24 11:21:10 2012
    002 UUID: 4d5a252a-c009-4aec-9e1f-73d3251c6b81
    003 Program example , port 87 , process id 3488
    004
    005 CALL/GOSUB stack
    006
    007 Backtrace:
    008 #0: jmainfunction.b:1
    009 #1: example.b:1 -> Line 1 , Source jmainfunction.b
    010
    011 Backtrace log:
    012 Program jmainfunction.b, Line 1, Stack level 0
    013 Line 0 , Source jmainfunction.b , Level 0
    014 >>> Program example.b, Line 1, Stack level 1
    015 Line 1 , Source jmainfunction.b
    016
    017 All the defined VAR's in the program
    018
    019 SUBROUTINE main()
    020 00000000006BEE90 : rc : (V) String : 0 bytes at address 0000000055740A58 :</pre>

Locating entry in the logs using the UUID.

<pre>
    find "4d5a252a-c009-4aec-9e1f-73d3251c6b81" %TAFC_HOME%\log\default</pre>

The following lines may appear in the log file:

<pre>
    ---- C:\R12\LOG\DEFAULT\EXAMPLE.HML0001.JBCUSER.LOG.ERROR.20120224-112110.3488
    E0224 11:21:10.737900 5832 tafc_logger_c_api.cpp:33]
    Coredump file: JBASECOREDUMP.4d5a252a-c009-4aec-9e1f-73d3251c6b81.ERRORFILE
    E0224 11:21:10.739899 5832 tafc_logger_c_api.cpp:33]
    UUID: 4d5a252a-c009-4aec-9e1f-73d3251c6b81</pre>

Type the following command to display the log file:

<pre>
    CT %TAFC_HOME%\LOG\DEFAULT\EXAMPLE.HML0001.JBCUSER.LOG.ERROR.20120224-
       112110.3488</pre>

The below log file will appear "example.HML0001.JBCUSER.LOG.ERROR.20120224-112110.3488":

<pre>
    001 Log file created at: 2012/02/24 11:21:10
    002 Running on machine: HML0001
    003 Log line format: [IWEF]mmdd hh:mm:ss.uuuuuu threadid file:line] msg
    004 E0224 11:21:10.737900 5832 tafc_logger_c_api.cpp:33] Coredump file:
        JBASECOREDUMP.4d5a252a-c009-4aec-9e1f-73d3251c6b81.ERRORFILE
    005 E0224 11:21:10.739899 5832 tafc_logger_c_api.cpp:33] jBASE Core dump created
        at Fri Feb 24 11:21:10 2012
    006 E0224 11:21:10.739899 5832 tafc_logger_c_api.cpp:33] UUID:
        4d5a252a-c009-4aec-9e1f-73d3251c6b81
    007 E0224 11:21:10.739899 5832 tafc_logger_c_api.cpp:33] Program example , port
        87, process id 3488
    008 E0224 11:21:10.739899 5832 tafc_logger_c_api.cpp:33]
    009 E0224 11:21:10.739899 5832 tafc_logger_c_api.cpp:33] CALL/GOSUB stack
    010 E0224 11:21:10.739899 5832 tafc_logger_c_api.cpp:33]
    011 E0224 11:21:10.739899 5832 tafc_logger_c_api.cpp:33] Backtrace:
    012 E0224 11:21:10.739899 5832 tafc_logger_c_api.cpp:33] #0: jmainfunction.b:1219
    013 E0224 11:21:10.739899 5832 tafc_logger_c_api.cpp:33] #1: example.b:1->Line 1,
        Source jmainfunction.b
    014 E0224 11:21:10.739899 5832 tafc_logger_c_api.cpp:33]
    015 E0224 11:21:10.739899 5832 tafc_logger_c_api.cpp:33] Backtrace log:
    016 E0224 11:21:10.739899 5832 tafc_logger_c_api.cpp:33] Program jmainfunction.b,
        Line 1, Stack level 0
    017 E0224 11:21:10.739899 5832 tafc_logger_c_api.cpp:33] Line 0 ,
        Source jmainfunction.b , Level 0
    018 E0224 11:21:10.739899 5832 tafc_logger_c_api.cpp:33] >>> Program example.b,
        Line 1, Stack level 1
    019 E0224 11:21:10.739899 5832 tafc_logger_c_api.cpp:33] Line 1 ,
        Source jmainfunction.b
    020 E0224 11:21:10.739899 5832 tafc_logger_c_api.cpp:33]
    021 E0224 11:21:10.739899 5832 tafc_logger_c_api.cpp:33] All the defined VAR's
        in the program
    022 E0224 11:21:10.739899 5832 tafc_logger_c_api.cpp:33]
    023 E0224 11:21:10.739899 5832 tafc_logger_c_api.cpp:33] SUBROUTINE main()
    024 E0224 11:21:10.739899 5832 tafc_logger_c_api.cpp:33] 00000000006BEE90 :
        rc : (V) String : 0 bytes at address 0000000055740A58 :</pre>

## JBASESubroutineExist

Check if a subroutine exists in current environment:

### COMMAND SYNTAX

    CALLC JBASESubroutineExist(SubName, SubInfo)

where **SubName** is subroutine name; returns 1 or 0.
**SubInfo** is reserved for future use.

### EXAMPLE

       SubName = 'CDD'
       Result = CALLC JBASESubroutineExist(SubName, SubInfo)
       CRT Result            ;* 1 in T24 environment
       SubName = 'QWERTY'
       Result = CALLC JBASESubroutineExist(SubName, SubInfo)
       CRT Result            ;* 0

## JBASETHREADCreate

JBASETHREADCreate command is used to start a new thread.

### COMMAND SYNTAX

    JBASETHREADCreate(ProgramName, Arguments, User, Handle)

### SYNTAX ELEMENTS

**ProgramName** specifies the name of the program to execute.

**Arguments** specifies the command line arguments.

**User** specifies the name of the user in format
"user{,account{,password}}" or "" to configure as calling user id.

## JBASETHREADStatus

JBASETHREADStatus command shows the status of all running threads.

### COMMAND SYNTAX

    JBASETHREADStatus(ThreadList)

### SYNTAX ELEMENTS

**ThreadList** is a list of the threads active in this process,
with one attribute per thread.

The layout of the multi-values in each attribute is as follows:

| Value   |    Description                                |
|---------|-----------------------------------------------|
|< n,1 >  |  port number                                  |
|< n,2 >  |  thread handle returned from JBASETHREADCreate|

## JQLCOMPILE

JQLCOMPILE compiles a jQL statement.

### COMMAND SYNTAX

    JQLCOMPILE(Statement, Command, Options, Messages)

### SYNTAX ELEMENTS

**Statement** is the variable, which receives the compiled statement.
Majority of functions use the compiled statement to execute and work
on the result set etc.

**Command** is the actual jQL query that you want to compile (such as
SELECT or something similar). Use RETRIEVE to obtain data records as
the verb rather than an existing jQL verb. This will ensure that the
right options are set internally. In addition, use any word that is
not a jQL reserved word as the verb and it will work in the same way
as RETRIEVE: implement a PLOT command that passes the entire command
line into JQLCOMPILE and the results will be the same as if the first
word was replaced with RETRIEVE.

**Option:** You must specify JQLOPT_USE_SELECT to supply a select list
to the JQLEXECUTE function; the compile builds a different execution
plan if using select lists.

**Messages:** If the statement fails to compile, this dynamic array
is in the STOP format, therefore STOP messages can be programmed and
printed. Provides a history of compilation for troubleshooting
purposes; Returns -1 if there is a problem found in the statement
and 0 for no problem.

## JQLEXECUTE

JQLEXECUTE starts executing a compiled jQL statement.

### COMMAND SYNTAX

    JQLEXECUTE(Statement, SelectVar)

### SYNTAX ELEMENTS

**Statement** is the valid result of a call to a
JQLCOMPILE (Statement, ...)

**SelectVar** is a valid select list used to limit the statement to a
predefined set of items. For example - how it's used in jQL (note the "&gt;") prompt:

<pre>
    SELECT PROGRAMMERS WITH IQ_IN_PTS > 250
    &nbsp;
    1 Item Selected
    &nbsp;
    > LIST PROGRAMMERS NAME
    &nbsp;
    PROGRAMMERS...    NAME
    &nbsp;
    0123              COOPER, F B</pre>

This function returns -1 in the event of a problem, such as an
incorrect statement variable. It will cause the statement to run
against the database and produce a result set for use with JQLFETCH().

## JQLFETCH

JQLFETCH is used to fetch the next result in a compiled jQL statement.

### COMMAND SYNTAX

    JQLFETCH(Statement, ControlVar, DataVar)

### SYNTAX ELEMENTS

**Statement** is the result of a valid call to JQLCOMPILE(), followed
by a valid call to JQLEXECUTE().

**ControlVar** will receive the 'control break' elements of any query.
For example, if there are BREAK values in the statement, described here
is the the format of ControlVar is:

<pre>
    Attr 1  Level: 0 means detail line 1 - 25 for the control breaks, the same as the
            A correlative NB.
    Attr 2  Item ID
    Attr 3  Break control Value is 1 if a blank line should be output first.
    Attr 4  Pre-break value for 'B' option in header
    Attr 5  Post-break value for 'B' option in header</pre>

**DataVar** will receive the actual screen data on a LIST statement for
instance. The format is one attribute per column.

Applies Attribute 7 Conversions (or attribute 3 in Prime-style DICTS) to
the data.

If the property STMT_PROPERTY_FORMAT is set then each attribute is also
formatted according to the width and justification of the attribute
definition and any override caused by the use of FMT, of DISPLAY. LIKE
on the command line.

### NOTES

Column headers may also affect the formatting for that column.
This function is called until there is no more output (multiple).

## JQLGETPROPERTY

JQLGETPROPERTY is used to get the property of a compiled jQL statement

### COMMAND SYNTAX

    JQLGETPROPERTY(PropertyValue, Statement, Column, PropertyName)

### SYNTAX ELEMENTS

**PropertyValue** receives the requested property value from the system
or "" if the property is not set.

**Statement** is the result of a valid JQLCOMPILE(Statement).

**Column** specifies the column number for which the property value was
requested (otherwise 0 for the whole statement).

**PropertyName** are EQUATED values defined by INCLUDEing the file
JQLINTERFACE.h.

This function returns -1 if there is a problem with the parameters or
the programmer. These properties answer questions such as "Was LPTR
mode asked for" and "How many columns are there?"

### NOTES

Properties are valid after the compile; this is the main reason for
separating the compile and execute into two functions. After
compiling, it is possible to examine the properties and to set the
properties before executing.

## JQLPUTPROPERTY

JQLPUTPROPERTY sets a property in a compiled jQL statement.

### COMMAND SYNTAX

    JQLPUTPROPERTY(PropertyValue, Statement, Column, PropertyName)

### SYNTAX ELEMENTS

**PropertyValue** specifies the value to be set for the specified
property, such as one or "BLAH".

**Statement** is the result of a valid JQLCOMPILE() function.

**Column** holds 0 for a general property of the statement, or a
column number if the property is set for a specific column.

**PropertyName** are EQUATED values defined by INCLUDEing the file
JQLINTERFACE.h. There are lots of these and someone is going to have
to document each one.

This function returns -1 if it locates a problem in the statement
and 0 for no problem.

### NOTES

Some properties may require JQLEXECUTE()first.

Properties are valid after the compile; this is the main reason for
separating the compile and execute into two functions. After compiling,
it is possible to examine the properties and set properties before
executing.

## Sample program illustrating the usage of compiled jQL statement:

    INCLUDE jQLProperties.h
       //
       IF NOT( GETENV('TAFC_HOME', V.HOME) ) THEN
          CRT 'TAFC_HOME not defined'
          STOP
       END
       //
       V.QUERY = 'LIST ONLY ' : V.HOME : '/jbcmessages'
       V.STMT = ''
       //
       V.DUMMY = JQLCOMPILE(V.STMT, V.QUERY, 0, V.MSG)
       //
       V.SEL.VAR = ''
       V.RET = JQLEXECUTE(V.STMT, V.SEL.VAR)
       IF V.RET NE 0 THEN CRT 'JQLEXECUTE RETURNED', V.RET  ; STOP
       //
       LOOP
          GOSUB FETCH.NEXT
       UNTIL V.FETCH NE 1
       REPEAT
       //
       STOP
       //
    FETCH.NEXT:
       //
       V.FETCH = JQLFETCH(V.STMT, V.CTRL, V.DATA)
       IF V.FETCH NE 1 THEN RETURN
       V.RET = JQLGETPROPERTY(PropertyValue, V.STMT, 0, \
    	 STMT_PROPERTY_EXECUTE_COUNT)
       CRT 'ID #' : PropertyValue : ':' , V.DATA<1>
       //
       RETURN
    END

Output:

<pre>
    @ID #1:	INV_FILE_TYPE
    @ID #2:	DEVICE_QUIT
    @ID #3:	RTN_NOGOSUB
    @ID #4:	ARRAY_ILLEGAL_SIZE
    @ID #5:	DIFF_COMMON
    @ID #6:	QLNOVERB
    @ID #7:	QLPARAMERR
    ...
    @ID #487:	417
    @ID #488:	80044228
    @ID #489:	80044233
    @ID #490:	80045024</pre>

# jBC Functions and Statements (K - O)

## KEYIN

KEYIN function is used to read a single character from the input buffer
and return it.

### COMMAND SYNTAX

    KEYIN()

KEYIN uses raw keyboard input, therefore all special character handling
(for example, backspace) is disabled. System special character handling
(for example, processing of interrupts) is unchanged.

### EXAMPLE

Output current time and date in the current line on the terminal until user
presses q or Q key.

       V.HOME = @(0)   ;* remember cursor position at the start of the current line
       LOOP
          LOOP
             V.BUFF = SYSTEM(14)    ;* check if there's anything in keyboard buffer
             IF V.BUFF NE 0 THEN BREAK
             CRT V.HOME:TIMEDATE():     ;* e.g. 22:27:08 24 OCT 2012
             MSLEEP 3000
          REPEAT
          V.KEY = UPCASE( KEYIN() )
          IF V.KEY EQ 'Q' THEN BREAK    ;* exit if q or Q was pressed
       REPEAT

## LATIN1

<a name="LATIN1"/>

LATIN1 function converts a UTF-8 byte sequence into the binary or latin1
equivalent.

### COMMAND SYNTAX

    LATIN1(expression)

### SYNTAX ELEMENTS

The expression is to be a UTF-8 encoded byte sequence, which is the
default format when executing in International Mode.

### EXAMPLE

       utf_line = CHAR( XTD('C3') )   \
             : CHAR( XTD('9F') )      \    ;* c3 9f: LATIN SMALL LETTER SHARP S
             : CHAR( XTD('C3') )      \
             : CHAR( XTD('9D') )    ;* c3 9d: LATIN CAPITAL LETTER Y WITH ACUTE
       lat_line = LATIN1(utf_line)
       CRT lat_line, SEQ(lat_line[1,1]), SEQ(lat_line[2,1])

The output of this program is:

<pre>
    &#223;&#221;    223     221</pre>

### NOTE

To run this example the following environment variables are to be set:

<pre>
    JBASE_I18N=1
    JBASE_CODEPAGE=utf8</pre>

## LEFT

<a name="LEFT"/>

The LEFT function extracts a sub-string of a specified length from the
beginning of a string.

### COMMAND SYNTAX

    LEFT(expression, length)

### SYNTAX ELEMENTS

**expression** evaluates to the string from which the sub string is
extracted.

**length** specifies the number of the extracted characters. If the
length is less than 1, then LEFT() returns null.

### NOTES

The LEFT() function is equivalent to sub-string extraction starting
from the first character position, i.e. expression[1,length]

See also: [RIGHT](#RIGHT)

### EXAMPLES

    S = "The world is my lobster"
    CRT DQUOTE( LEFT(S,9) )
    CRT DQUOTE( LEFT(S,999) )
    CRT DQUOTE( LEFT(S,0) )

This code displays:

<pre>
    "The world"
    "The world is my lobster"
    ""</pre>

## LEN

LEN function returns the character length of the supplied expression.

### COMMAND SYNTAX

    LEN(expression)

### SYNTAX ELEMENTS

**expression** can evaluate to any type and the function will convert
it to a string automatically.

### INTERNATIONAL MODE

The LEN function will return the number of characters in the specified
expression rather than the number of bytes, in International Mode. If
the expression consists of entirely of UTF-8 characters in the ASCII
range 0 - 127 then the character length of the expression will equate
to the byte length. However, when the expression contains characters
outside the ASCII range 0 - 127 then byte length and character length
will differ. If the byte is specifically required then use the
[BYTELEN](#BYTELEN) function in place of the LEN function.

### NOTES

Do not use programs manipulating byte counts in International Mode.

### EXAMPLE

    * Centered string output
       V.STRING = 'I AM IN THE VERY CENTER'   ; V.WIDTH = 50
       V.LEN = LEN(V.STRING)
       V.OFF.L = INT((V.WIDTH - V.LEN) / 2)    ;* left offset
       V.OFF.R = V.WIDTH - V.LEN - V.OFF.L     ;* right offset
       CRT SQUOTE( STR(' ', V.OFF.L) : V.STRING : STR(' ', V.OFF.R) )

Output is:

<pre>
    '             I AM IN THE VERY CENTER              '</pre>

## LENDP

LENDP function returns the display length of an expression

### COMMAND SYNTAX

    LENDP(expression)

### SYNTAX ELEMENTS

The **expression** can evaluate to any type. The LENDP function
evaluates each character in the expression and returns the calculated
display length.

INTERNATIONAL MODE

The LENDP function will return the display length for the characters
in the specified expression rather than the number of bytes, in
International Mode.

### NOTES

Some characters, usually Japanese, Chinese, etc will return a display
length of greater than one for some characters. Some characters, for
instance control characters or null (char 0), will return a display
length of 0.

## LENS

LENS function is used to return a dynamic array of the number of bytes
in each element of the dynamic.array.

### COMMAND SYNTAX

    LENS(dynamic.array)

Each element of dynamic.array must be a string value. The characters
in each element of dynamic.array are counted, with the counts returned.

The LENS function includes all blank spaces, including trailing blanks,
in the calculation.

If dynamic.array evaluates to a null string, it returns zero (0). If
any element of dynamic.array is null, returns zero (0) for that element.

### INTERNATIONAL MODE

The LENS function will return the number of characters in the specified
expression rather than the number of bytes, in International Mode. If
the expression consists of entirely of UTF-8 characters in the ASCII
range 0 - 127 then the character length of the expression will equate
to the byte length. However, when the expression contains characters
outside the ASCII range 0 - 127 then byte length and character length
will differ. See
[BYTELEN](#BYTELEN) function for more information.

### NOTES

Do not use programs to manipulate byte counts in International Mode.

## LES

LES function is used to determine whether elements of one dynamic
array are less than or equal to the elements of another dynamic
array.

### COMMAND SYNTAX

    LES(array1, array2)

It compares each element of array1 with the corresponding element
of array2. If the element from array1 is less than or equal to the
element from array2,  1 is returned in the corresponding element of
a new dynamic array. If the element from array1 is greater than the
element from array2, it returns zero (0). If an element of one dynamic
array has no corresponding element in the other dynamic array, it
evaluates the undefined element as empty, and the comparison continues.

If either of a corresponding pair of elements is null, it returns null
for that element. If you use the subroutine syntax, it returns the
resulting dynamic array as return.array.

## LN

LN function returns the value of the natural logarithm of the supplied
value.

### COMMAND SYNTAX

    LN(expression)

### SYNTAX ELEMENTS

**expression** should evaluate to a numeric value. The function will
then return the natural logarithm of that value.

### NOTES

The calculation of the natural logarithm is by using the mathematical
constant 'e' as a number base.

### EXAMPLE

    A = LN(22 / 7)

## LOCALDATE

LOCALDATE returns an internal date using the specified Timestamp and
TimeZone combination.

### COMMAND SYNTAX

    LOCALDATE(Timestamp, TimeZone)

### SYNTAX ELEMENTS

The LOCALDATE function uses the specified timestamp and adjusts the
value by the specified time zone to return the date value in internal
date format.

### EXAMPLE

    start_time = MAKETIMESTAMP(DATE(), TIME(), '')
    time_shift = 100  ;  time_shift<8> = ''    ;* add 100 years to current date
    end_time = CHANGETIMESTAMP(start_time, time_shift)
    CRT OCONV(LOCALDATE(end_time, ''), 'D')               ;* e.g. 20 JUN 2113

## LOCALTIME

LOCALTIME returns an internal time using the specified Timestamp and
TimeZone combination.

### COMMAND SYNTAX

    LOCALTIME(Timestamp, TimeZone)

### SYNTAX ELEMENTS

The LOCALTIME function uses the specified timestamp and adjusts the
value by the specified time zone to return the time value in internal
time format.

## LOCATE

<a name="LOCATE"/>

LOCATE statement finds the position of an element within a specified
dimension of a dynamic array.

### COMMAND SYNTAX

    LOCATE expression1 IN expression2{<expression3{,expression4}>},{, expression5} \
           { BY expression6 } SETTING Var THEN | ELSE statement(s)

### SYNTAX ELEMENTS

**expression1** evaluates to the string that will be searched in
expression2.

**expression2** evaluates to the dynamic array within which
expression1 will search for the string.

**expression3** and **expression4** cause a value or subvalue
search respectively, when specified.

**expression5** indicates the field, value or subvalue from which the
search will begin.

**expression6** causes different searches to arrange the elements in
different order, which can considerably improve the performance of
some searches. The available string values for expression6 are:

|String|    Description                                      |
|------|-----------------------------------------------------|
|  AL  |Values are in ascending alphanumeric order           |
|  AR  |Values are in right justified, then ascending order  |
|  AN  |Values are in ascending numeric order                |
|  DL  |Values are in descending alphanumeric order          |
|  DR  |Values are in right justified, then descending order |
|  DN  |Values are in descending numeric order               |

Var will be set to the position of the Field, Value or Sub-Value in
which expression1 was found if indeed. If it was not found and
expression6 was not specified then Var will be set to one position
past the end of the searched dimension. If expression6 did specify
the order of the elements then Var will be set to the position before
which the element should be inserted to retain the specified order.

The statement must include one or both of the THEN and ELSE clauses.
If expression1 is found in an element of the dynamic array, then it
executes the statements defined by the THEN clause. If expression1
is not found in an element of the dynamic array, then it executes
the statements defined by the ELSE clause.

### INTERNATIONAL MODE

When the LOCATE statement is used in International Mode, the statement
will use the currently configured locale to determine the rules by
which each string is considered less than or greater than the other
will.

### NOTES

See also: [FIND](#FIND), [FINDSTR](#FINDSTR)

### EXAMPLE

Using LOCATE to sort an array.

       V.ARR = ''
       FOR V.I = 1 TO 1000
          V.ARR<V.I> = RND(1000)
       NEXT V.I
       V.SORTED = ''
        FOR V.I = 1 TO 1000
          V.IN = V.ARR<V.I>
          LOCATE V.IN IN V.SORTED<1> BY 'AN' SETTING V.INS.POSN ELSE NULL
          INS V.IN BEFORE V.SORTED<V.INS.POSN>
       NEXT V.I
       CRT MINIMUM(V.ARR), MAXIMUM(V.ARR)  ;* e.g. "0       998"
       CRT V.SORTED<1>, V.SORTED<1000>     ;* numbers should be the same as above

## LOCK

<a name="LOCK"/>

LOCK statement is used to set an execution lock thus preventing any
other jBC program to wait until this program has released it.

### COMMAND SYNTAX

    LOCK expression { THEN | ELSE statements}

### SYNTAX ELEMENTS

The expression should evaluate to a numeric value between 0 and 255
(63 in R83 import mode).

The statement will execute the THEN clause (if defined) providing
the lock could be taken. If another program holds the LOCK and an
ELSE clause is provided then the statements defined by the ELSE
clause are executed. If no ELSE clause was provided with the
statement then it will block (hang) until the other program has
released the lock.

### NOTES

See also: [UNLOCK](#UNLOCK)

If you use the environment variable JBCEMULATE set to r83, to compile
the program the number of execution locks is limited to 64. If an
execution lock greater than this number is specified, then the actual
lock taken is the specified number modulo 64.

### EXAMPLES

    LOCK 32 ELSE
        CRT "This program is already executing!"
    STOP
    END

## Logger

The logger function allows you to log your message in a file or display to
screen.

### COMMAND SYNTAX

    Logger(Category, Severity, Message)

### SYNTAX ELEMENTS

**Category** is any user defined category. Any meaningful name can be
provided.

**Severity**: You can use predefined severity level for your logging
information.

TAFC_LOG_INFO

TAFC_LOG_WARNING

TAFC_LOG_ERROR

TAFC_LOG_FATAL

**Message** is any user defined meaningful message for logging.

### NOTES

You can control logging information from tafc.ini, please refer to the user
guide for more details.

### EXAMPLE

    INCLUDE JBC.h
    Logger('ACC', TAFC_LOG_INFO, 'Message for ACC category at INFO level')
    Logger('ACC', TAFC_LOG_WARNING, 'Message for ACC category at WARNING level')
    Logger('ACC', TAFC_LOG_ERROR, 'Message for ACC category at ERROR level')

## LOOP

<a name="LOOP"/>

LOOP allows the programmer to specify loops with multiple exit
conditions.

### COMMAND SYNTAX

    LOOP statements1 WHILE | UNTIL expression DO statements2 REPEAT

### SYNTAX ELEMENTS

**statements1** and **statements2** consist of any number of standard
statements include the LOOP statement itself, thus allowing nested loops.

**statements1** will always be executed at least once, after which the
WHILE or UNTIL clause is evaluated.

**expression** is tested for Boolean TRUE/FALSE by either the WHILE
clause or the UNTIL clause. When tested by the WHILE clause statements2
will only be executed if expression is Boolean TRUE. When tested by the
UNTIL clause, statements2 will only be executed if the expression
evaluates to Boolean FALSE.

**REPEAT** causes the loop to start again with the first statement
following the LOOP statement.

### NOTES

See also: [BREAK](#BREAK), [CONTINUE](#CONTINUE)

### EXAMPLE

      IF NOT( GETENV('TAFC_HOME', V.HOME) ) THEN
          CRT 'TAFC_HOME not defined'
          STOP
       END
      EXECUTE 'SELECT ' : V.HOME : '/jbcmessages SAMPLE 10' RTNLIST V.MSG.L
    * Retrieve @IDs one by one
       LOOP
          REMOVE V.ID FROM V.MSG.L SETTING V.STATUS
          CRT V.ID
          IF V.STATUS EQ 0 THEN BREAK   ;* end of list reached
       REPEAT

Output looks like:

<pre>
    INV_FILE_TYPE
    DEVICE_QUIT
    RTN_NOGOSUB
    ARRAY_ILLEGAL_SIZE
    DIFF_COMMON
    QLNOVERB
    QLPARAMERR
    SP-HoldCount
    603
    1134</pre>

The loop used in this example can also be defined this way:

       LOOP
          REMOVE V.ID FROM V.MSG.L SETTING V.STATUS
          CRT V.ID
       UNTIL V.STATUS EQ 0
       REPEAT


## LOWER

<a name="LOWER"/>

This function lowers system delimiters in a string to the next lowest
delimiter.

### COMMAND SYNTAX

    LOWER(expression)

### SYNTAX ELEMENTS

**expression** is a string containing one or more delimiters, lowered as
follows:

| ASCII character  | Lowered to      |
|------------------|-----------------|
| 255              | 254             |
| 254              | 253             |
| 253              | 252             |
| 252              | 251             |
| 251              | 250             |
| 250              | 249             |
| 249              | 248             |

### EXAMPLE

       V.ARRAY = 1 :@FM: 2 :@FM: 3 :@FM: 4
       CRT OCONV(V.ARRAY, 'MCP')                      ;*  1^2^3^4
       CRT OCONV( LOWER(V.ARRAY), 'MCP' )             ;*  1]2]3]4

## MAKETIMESTAMP

<a name="MAKETIMESTAMP"/>

MAKETIMESTAMP generates a timestamp using combination of internal date,
time and timezone.

### COMMAND SYNTAX

    MAKETIMESTAMP(InternalDate, InternalTime, TimeZone)

### SYNTAX ELEMENTS

The internal date and internal time values are combined together with the
time zone specification to return a UTC timestamp in decimal seconds.

### EXAMPLE

       CRT MAKETIMESTAMP( DATE(), TIME(), 'Europe/London')   ;* e.g. 1352113823.755
       CRT MAKETIMESTAMP( DATE(), TIME(), 'Europe/Belgrade') ;* e.g. 1352110223.755

## MAT

<a name="MAT"/>

This command is used to assign a single value for every element in a
specified array or to assign the entire contents of one array to another.

### COMMAND SYNTAX

    MAT Array = expression

    MAT Array1 = MAT Array2

### SYNTAX ELEMENTS

**Array**, **Array1** and **Array2** are all pre-dimensioned arrays
declared with the DIM statement. **expression** can evaluate to any
data type.

### NOTES

If any element of the array Array2 has not been assigned a value then a
runtime error message will occur. This can be avoided by coding the
statement MAT Array2 = " after the DIM statement.

### EXAMPLE

       DIM A(45), G(45)
       MAT G = "Array value"
       MAT A = MAT G
       CRT DQUOTE(A(45))                    ;* "Array value"

## MATBUILD

<a name="MATBUILD"/>

This statement is used to create a dynamic array out of a dimensioned
array.

### COMMAND SYNTAX

    MATBUILD variable FROM array{, expression1{, expression2}} { USING expression3}

### SYNTAX ELEMENTS

**variable** is the jBC variable into which the created dynamic array
will be stored. Array is a previously dimensioned and assigned matrix
from which the dynamic array will be created.

**expression1** and **expression2** should evaluate to numeric integers.
expression1 specifies the array element from which the extraction
starts; expression2 specifies the array element on which the extraction
ends (inclusive).

By default, each array element is separated in the dynamic array by a
field mark. By specifying **expression3**, the separator character can
be changed. If expression3 evaluates to more than a single character,
only the first character of the string is used.

### NOTES

When specifying extraction starting and ending positions with
multi-dimensional arrays, it is necessary to expand the matrix into its
total number of variables for calculating the correct element number.
See the information about dimensioned arrays earlier in this chapter for
detailed instructions on calculating element numbers.

### EXAMPLE

       DIM A(40)
       MAT A = 'VALUE '
       FOR V.I = 1 TO 40
           A(V.I) := V.I
       NEXT V.I
       MATBUILD Dynamic FROM A, 3, 7 USING ":"
       CRT Dynamic               ;* VALUE 3:VALUE 4:VALUE 5:VALUE 6:VALUE 7

 Builds a 5 element string separated by ":" character.
 "MATBUILD Dynamic FROM A" builds a field mark separated dynamic array
from   every element contained in the matrix A.

## MATCHES

<a name="MATCHES"/>

MATCH or MATCHES clause applies pattern matching to an expression.

### COMMAND SYNTAX

    expression1 MATCHES expression2

### SYNTAX ELEMENTS

**expression1** may evaluate to any type. **expression2** should
evaluate to a valid pattern matching string as described below.

**expression1** is then matched to the pattern supplied and a value of
Boolean TRUE is returned if the pattern is matched. A value of Boolean
FALSE is returned if the pattern is not matched.

**expression2** can contain any number of patterns to match those
separated by value marks. The value mark implies a logical OR of the
specified patterns and the match will evaluate to Boolean TRUE if
expression1 matches any of the specified patterns.

### INTERNATIONAL MODE

When using the MATCHES statement in International Mode, the statement
will use the currently configured locale to determine the properties
according to the Unicode Standard for each character in the expression.
i.e., is the character alpha or numeric?

### NOTES

The rule table shown below shows construction of pattern matching
strings (n refers to any integer number).

| Pattern          | Explanation                                   |
|------------------|-----------------------------------------------|
| nN               | Matches a sequence of n digits                |
| nA               | Matches a sequence of n alpha characters      |
| nC               | Matches a sequence of n alpha characters      |
|                  | or digits                                     |
| nX               | Matches a sequence of any characters          |
| "string"         | Matches the character sequence string exactly |


Applies the pattern to all characters in expression1 and it must match
all characters in the expression to evaluate as Boolean TRUE.

Specify the integer value 'n' as '0'. This will cause the pattern to
match any number of characters of the specified type.

### EXAMPLES

    * T24 IDs matching
       transfer_id = 'FT130172HQJ4'
       CRT transfer_id MATCHES "'FT'5N5X"           ;*  1
       hist_id = 'FT130172HQJ4;1'
       CRT hist_id MATCHES "'FT'5N5X"               ;*  0
       CRT hist_id MATCHES "'FT'5N5X;1N"            ;*  1
    * date
       start_date = '2011-10-25'
       CRT start_date MATCHES "4N'-'2N'-'2N"        ;*  1
    * emulations compatibility
       cust_name = 'JOHN DORY'
       CRT cust_name MATCH "JOHN..."            ;*  1 under prime, 0 under jbase
       CRT cust_name MATCH "'JOHN'..."          ;*  1 under prime, 0 under jbase
       CRT cust_name MATCH "'JOHN'0X"           ;*  1 under both
       CRT cust_name MATCH "'John'..."          ;*  0 under both
    * "C" - alphanumeric - isn't supported at all under prime
       CRT '2HQJ4' MATCHES "5C"                 ;* 1 under jbase emulation
    * numbers
       CRT 9.99 MATCHES "0N'.'2N"               ;* 1
       CRT '.99' MATCHES "0N'.'2N"              ;* 1
    * avoid messing up data with patterns (example for prime):
       cust_address = '3RD FLOOR, 17A ELM STREET'
       CRT cust_address MATCH "...17A..."   ;* 0 - 17A means 17 alpha characters
       CRT cust_address MATCH "...'17A'..." ;* 1 - here '17A' is a string to search

## MATCHFIELD

<a name="MATCHFIELD"/>

This function is used to check a string against a match pattern.

### COMMAND SYNTAX

    MATCHFIELD(string, pattern, field)

### SYNTAX ELEMENTS

**field** is an expression that evaluates to the portion of the
match string to be returned.

If string matches pattern, the MATCHFIELD function returns the
portion of string that matches the specified field in pattern.
If string does not match pattern, or if string or pattern evaluates
to the null value, the MATCHFIELD function returns an empty string.
If field evaluates to the null value, the MATCHFIELD function fails
and the program terminates with a run-time error.

**pattern** must contain specifiers to cover all characters contained
in string. For example, the following statement returns an empty
string because not all parts of string are specified in the pattern:

    MATCHFIELD('XYZ123AB', '3X3N', 1)

To achieve a positive pattern match on the string above, use the
following statement:

    MATCHFIELD('XYZ123AB', '3X3N0X', 1)

This statement returns a value of "XYZ".

### NOTES

See also: [MATCHES](#MATCHES) operator for information about pattern
matching.

### EXAMPLES

        Q = MATCHFIELD('AA123BBB9', '2A0N3A0N', 3)
        PRINT 'Q=', Q                               ;*  Q=     BBB
        ADDR = '20 GREEN ST. NATICK, MA.,01234'
        ZIP = MATCHFIELD(ADDR, '0N0X5N', 3)
        PRINT 'ZIP=' , ZIP                          ;*  ZIP=   01234
        UNV = 'PART12345 BLUE AU'
        COL = MATCHFIELD(UNV, '10X4A3X', 2)
        PRINT 'COL= ', COL                          ;*  COL=   BLUE
        XYZ = MATCHFIELD('ABCDE1234', '2N3A4N', 1)
        PRINT 'XYZ= ', XYZ                          ;*  XYZ=
        ABC = MATCHFIELD('1234AB', '4N1A', 2)
        PRINT 'ABC= ', ABC                          ;*  ABC=

## MATPARSE

<a name="MATPARSE"/>

MATPARSE statement is used to assign the elements of a matrix from the
elements of a dynamic array.

### COMMAND SYNTAX

    MATPARSE array{, expression1{, expression2}} FROM variable1  \
            { USING expression3} SETTING variable2

### SYNTAX ELEMENTS

**array** is a previously dimensioned matrix, which will be assigned
from each element of the dynamic array. variable1 is the jBC variable
from which the matrix array will be stored.

**expression1** and **expression2** should evaluate to numeric
integers. **expression1** specifies which element of the array the
assignment will start with; **expression2** specifies which element of
the array the assignment will end with (inclusive).

By default, the dynamic array assumes the use of a field mark to
separate each array element. By specifying **expression3**, the
separator character can be changed. If **expression3** evaluates to
more than a single character, only
the first character of the string is used.

As assignment will stop when the contents of the dynamic array
have been exhausted, it can be useful to determine the number of
matrix elements that were actually assigned to. If the SETTING
clause is specified then **variable2** will be set to the number of
elements of the array that were assigned to.

### NOTES

When specifying starting and ending positions with
multi-dimensional arrays, it is necessary to expand the matrix
into its total number of variables to calculate the correct
element number.

See the information about dimensioned arrays earlier in this
section for detailed instructions on calculating element numbers.

### EXAMPLES

       DIM dim_array(100)
       dyn_array = ''   ;     delim_array = ''
       FOR i = 1 TO 100
          dyn_array<-1> = i
          delim_array := i*2 : '-'
       NEXT i
    * Full copy
       MATPARSE dim_array FROM dyn_array
       CRT dim_array(1)                 ;* 1
       CRT dim_array(100)               ;* 100
    * Using different array delimiter
       MAT dim_array = 'Default'
       MATPARSE dim_array FROM delim_array USING '-'
       CRT dim_array(1)                 ;* 2
       CRT dim_array(100)               ;* 200
    * Partial copy
       MAT dim_array = 'Default'
       MATPARSE dim_array, 3, 7 FROM dyn_array
       CRT dim_array(1)                 ;* Default
       CRT dim_array(3)                 ;* 1
       CRT dim_array(5)                 ;* 3
       CRT dim_array(100)               ;* Default
    * "Over-copy"
       FOR i = 101 TO 103               ;* add 3 elements to dynamic array
          dyn_array<-1> = i
       NEXT i
       MAT dim_array = 'Default'
       MATPARSE dim_array FROM dyn_array
       CRT dim_array(1)                 ;* 1
       CRT dim_array(100)               ;* 100
       the_extra = dim_array(0)           ;* all excess elements are here
       CHANGE @FM TO '>>>' IN the_extra
       CRT the_extra                        ;* 101>>>102>>>103
    * 2-dimensioned array population: "left-to-right":
       DIM two_dim_array(100,2)
       MATPARSE two_dim_array FROM dyn_array
       CRT two_dim_array(1,1)                 ;* 1
       CRT two_dim_array(1,2)                 ;* 2
       CRT two_dim_array(2,1)                 ;* 3
       CRT two_dim_array(2,2)                 ;* 4
       CRT two_dim_array(50,2)                ;* 100
       CRT DQUOTE(two_dim_array(100,1))       ;* ""

## MATREAD

<a name="MATREAD"/>

The MATREAD statement allows a record stored in a jBASE file to
be read and mapped directly into a dimensioned array.

### COMMAND SYNTAX

    MATREAD array FROM {variable1,} expression { SETTING setvar } \
            { ON ERROR statements } \
            { LOCKED statements} { THEN | ELSE statements}

### SYNTAX ELEMENTS

**array** should be a previously dimensioned array, which will be used
to store the record to be read. If specified,

**variable1** should be a jBC variable that has previously been
opened to a file using the OPEN statement. If variable1 is not
specified then the default file is assumed. The expression should
evaluate to a valid record key for the file.

If no record is found and the record could be read from the file
then it is mapped into the array and executes the THEN statements
(if any). If the record cannot be read from the file then array is
unchanged and executes the ELSE statements (if any).

If the record could not be read because another process already
had a lock on the record then any one of the two actions is taken.
If the LOCKED clause was specified in the statement then the
statements dependent on it are executed. If no LOCKED clause was
specified then the statement blocks (hangs) until the other process
releases the lock. If a LOCKED clause is used and the read is
successful, a lock will be set.

If the SETTING clause is specified, setvar will be set to the number
of fields in the record on a successful read. If the read fails,
setvar will be set to one of the following values:

### INCREMENTAL FILE ERRORS

|Code   |    Description                        |
|-------|---------------------------------------|
|128    |    No such file or directory          |
|4096   |    Network error                      |
|24576  |    Permission denied                  |
|32768  |    Physical I/O error or unknown error|

If ON ERROR is specified, it executes the statements following the ON
ERROR clause for any of the above Incremental File Errors except error
128.

### NOTES

The record is mapped into the array using a predefined algorithm. The
record is expected to consist of a number of field separated records,
which are then assigned one at a time to each successive element of
the matrix.

See the NOTES on matrix organization earlier in this section for
details of multi dimensional arrays.

If there are more fields in the record than elements in the array,
then the final element of the array will be assigned all remaining
fields. If there were fewer fields in the record than elements in the
array then the remaining array elements will be assigned a null value.

If multi-values are read into an array element they will then be
referenced individually as:

      Array(n)<1,m>

not

      Array(n)<m>

### EXAMPLES

    MATREAD Xref FROM CFile, "XREF" ELSE MAT Xref = ''

    MATREAD Ind FROM IFile, "INDEX" ELSE MAT Ind = 0

    MATREAD record FROM filevar, id SETTING val ON ERROR
    PRINT "Error number " :val: " occurred which prevented record from being read."
       STOP
    END THEN
       PRINT 'Record read successfully'
    END ELSE
       PRINT 'Record not on file'
    END
    PRINT "Number of attributes in record = " : val

## MATREADU

<a name="MATREADU"/>

MATREADU statement allows a record stored in a jBASE file to be read
and mapped directly into a dimensioned array. The record will also be
locked for update by the program.

### COMMAND SYNTAX

    MATREADU array FROM {variable1,} expression { SETTING setvar } \
            { ON ERROR statements } \
            { LOCKED statements } { THEN | ELSE statements }

### SYNTAX ELEMENTS

**array** should be a previously dimensioned array, which will be used
to store the record to be read. If specified, **variable1** should be a
jBC variable that has previously been opened to a file using the
[OPEN](#OPEN) statement. If **variable1** is not specified then the
default file is assumed. The expression should evaluate to a valid
record key for the file.

If found, the record could be read from the file then it is mapped into
array and executes the THEN statements (if any). If the record cannot be
read from the file for some reason then array is unchanged and executes
the ELSE statements (if any).

If the record could not be read because another process already had a
lock on the record then one of two actions is taken. If the LOCKED clause
was specified in the statement then the statements dependent on it are
executed. If no LOCKED clause was specified then the statement blocks
(hangs) until the other process releases the lock.

If the SETTING clause is specified, setvar will be set to the number of
fields in the record on a successful read. If the read fails, setvar
will be set to one of the following values:

### INCREMENTAL FILE ERRORS

|Code   |    Description                        |
|-------|---------------------------------------|
|128    |    No such file or directory          |
|4096   |    Network error                      |
|24576  |    Permission denied                  |
|32768  |    Physical I/O error or unknown error|

If ON ERROR is specified, the statements following the ON ERROR clause
will be executed for any of the above Incremental File Errors except
error 128.

### NOTES

The record is mapped into the array using a predefined algorithm. The
record is expected to consist of a number of Field separated records,
which are then assigned one at a time to each successive element of the
matrix. See the NOTES on matrix organization earlier in this
section for details of the layout of multi dimensional arrays.

If there were more fields in the record than elements in the array,
then the final element of the array will be assigned all remaining
fields. If there were fewer fields in the record than elements in
the array then remaining array elements will be assigned a null
value.

If multi-values are read into an array element then they will be
referenced individually as:

    Array(n)<1,m>

not

    Array(n)<m>

### EXAMPLES

    MATREADU Xref FROM CFile, "XREF" ELSE MAT Xref = ''
    MATREADU Ind FROM IFile, "INDEX" LOCKED
       GOSUB InformUserLock ;* Say it is locked
    END THEN
       GOSUB InformUserOk ;* Say we got it
    END ELSE
       MAT Ind = 0 ;* It was not there
    END

    MATREADU record FROM filevar, id SETTING val ON ERROR
       PRINT "Error number " :val: " occurred which prevented record from being read"
       STOP
    END LOCKED
       PRINT "Record is locked"
    END THEN
       PRINT 'Record read successfully'
    END ELSE
       PRINT 'Record not on file'
    END
    PRINT "Number of attributes in record = " : val

## MATWRITE

<a name="MATWRITE"/>

The MATWRITE statement transfers the entire contents of a dimensioned
array to a specified record on disc.

### COMMAND SYNTAX

    MATWRITE array TO | ON {variable,} expression { SETTING setvar }  \
           { ON ERROR statements }

### SYNTAX ELEMENTS

**array** should be a previously dimensioned and initialized array. If
specified, **variable** should be a previously opened file variable
(i.e. the subject of an OPEN statement). If variable is not specified
the default file variable is used. **expression** should evaluate to the
name of the record in the file.

If the **SETTING** clause is specified and the write succeeds, setvar
will be set to the number of attributes read into the array.

If the **SETTING** clause is specified and the write fails, setvar will
be set to one of the following values:

### INCREMENTAL FILE ERRORS

|Code   |    Description                        |
|-------|---------------------------------------|
|128    |    No such file or directory          |
|4096   |    Network error                      |
|24576  |    Permission denied                  |
|32768  |    Physical I/O error or unknown error|


If ON ERROR is specified, the statements following the ON ERROR clause
will be executed for any of the above Incremental File Errors except
error 128.

### NOTES

The compiler will check that the variable specified is a dimensioned
array before its use in the statement.

### EXAMPLES

    DIM A(8)
    MAT A = 99
    ....
    MATWRITE A ON "NewArray" SETTING ErrorCode ON ERROR
       CRT "Error: " :ErrorCode: " Record could not be written."
    END
    ...
    MATWRITE A ON RecFile, "OldArray"

## MATWRITEU

<a name="MATWRITEU"/>

MATWRITEU statement transfers the entire contents of a dimensioned
array to a specified record on file, in the same manner as the
MATWRITE statement. An existing record lock will be preserved.

### COMMAND SYNTAX

    MATWRITEU array TO | ON {variable,} expression { SETTING setvar }  \
            { ON ERROR statements }

### SYNTAX ELEMENTS

**array** should be a previously dimensioned and initialized
array. If specified, variable should be a previously opened file
variable (i.e. the subject of an OPEN statement). If variable is
not specified the default file variable is used.

**expression** should evaluate to the name of the record in the file.

If the SETTING clause is specified and the write succeeds, setvar
will be set to the number of attributes read into array.

If the SETTING clause is specified and the write fails, setvar
will be set to one of the following values:

### INCREMENTAL FILE ERRORS

|Code   |    Description                        |
|-------|---------------------------------------|
|128    |    No such file or directory          |
|4096   |    Network error                      |
|24576  |    Permission denied                  |
|32768  |    Physical I/O error or unknown error|

If ON ERROR is specified, the statements following the ON ERROR
clause will be executed for any of the above Incremental File
Errors except error 128.

### NOTES

The compiler will check that the variable specified is indeed a
dimensioned array before its use in the statement.

### EXAMPLES

    DIM A(8)
    MAT A = 99
    ....
    MATWRITEU A ON "NewArray"

## MAXIMUM

<a name="MAXIMUM"/>

MAXIMUM function is used to return the element of a dynamic array with
the highest numerical value.

### COMMAND SYNTAX

    MAXIMUM(DynArr)

### SYNTAX ELEMENTS

**DynArr** should evaluate to a dynamic array.

### NOTES

Null dynamic array elements are treat as zero.

Non-numeric dynamic array elements are ignored.

See also: [MINIMUM](#MINIMUM)

### EXAMPLES

       PRECISION 5
       dyn_array = 4.29442 :@AM: -3.60441 :@VM :4.29445 :@AM: 2.00042   \
             :@SM: -33.90228
       CRT MAXIMUM(dyn_array)           ;* 4.29445
    * non-numeric elements are ignored
       dyn_array<2,1> = '9000,00'
       CRT MAXIMUM(dyn_array)           ;* still 4.29445
    * PRECISION matters
       PRECISION 2
       CRT MAXIMUM(dyn_array)           ;* now 4.29442

## MINIMUM

<a name="MINIMUM"/>

MINIMUM function is used to return the element of a dynamic array
with the lowest numerical value.

### COMMAND SYNTAX

    MINIMUM(DynArr)

### SYNTAX ELEMENTS

**DynArr** should evaluate to a dynamic array.

### NOTES

Null dynamic array elements are treat as zero.

Non-numeric dynamic array elements are ignored.

See also: [MAXIMUM](#MAXIMUM).

### EXAMPLES

If EResults is a variable containing the dynamic array:

    1.45032:@AM:-3.60851:@VM:4.29445:@AM:2.07042:@SM:-3.90258

the code:

    PRECISION 3
    CRT MINIMUM(EResults)

displays -3.903

## MOD

<a name="MOD"/>

MOD function returns the arithmetic modulo of two numeric expressions.

### COMMAND SYNTAX

    MOD(expression1, expression2)

### SYNTAX ELEMENTS

Both **expression1** and **expression2** should evaluate to numeric
expressions or else runtime error will occur.

### NOTES

The remainder of expression1 divided by expression2 calculates the
modulo. If expression2 evaluates to 0, then the value of
expression1 is returned.

### EXAMPLES

    FOR I = 1 TO 10000
       IF MOD(I, 1000) = 0 THEN CRT "+" :
    NEXT I

displays a "+" on the screen every 1000 iterations.

## MODS

MODS function is used to create a dynamic array of the remainder
after the integer division of corresponding elements of two dynamic
arrays.

### COMMAND SYNTAX

    MODS(array1, array2)

The MODS function calculates each element according to the following
formula:

<pre>
    XY.element = X ?? (INT(X / Y) * Y)</pre>

X is an element of array1 and Y is the corresponding element of array2.
The resulting element is returned in the corresponding element of a new
dynamic array. If an element of one dynamic array has no corresponding
element in the other dynamic array, 0 is returned. If an element of
array2 is 0, 0 is returned. If either of a corresponding pair of
elements is null, null is returned for that element.

### EXAMPLES

       A = 3 :@VM: 7
       B = 2: @SM: 7 :@VM: 4
       PRINT OCONV( MODS(A, B), 'MCP' )       ;*  1\0]3

## MSLEEP

<a name="MSLEEP"/>

MSLEEP allows the program to pause execution for a specified number of
milliseconds.

### COMMAND SYNTAX

    MSLEEP {milliseconds}

### SYNTAX ELEMENTS

**milliseconds** must be an integer, which, specifies the number of
milliseconds to sleep.

When there are no parameters assumes a default time of 1 millisecond.

### NOTES

If a debugger is invoked and execution is continued while a program is
sleeping, then the user will be prompted:

Continue with SLEEP (Y/N) ?

If "N" is the response, the program will continue at the next statement
after the MSLEEP.

See also: [SLEEP](#SLEEP) to sleep for a specified number of seconds or
until a specified time.

### EXAMPLES

       CRT MAKETIMESTAMP( DATE(), TIME(), '' )           ;*  e.g. 1353068005.934
       MSLEEP(100)      ;* 0.1 sec
       CRT MAKETIMESTAMP( DATE(), TIME(), '' )           ;*  e.g. 1353068006.044
       MSLEEP(3000)      ;* 3 sec
       CRT MAKETIMESTAMP( DATE(), TIME(), '' )           ;*  e.g. 1353068009.039
       MSLEEP 3000       ;* this syntax also works
       CRT MAKETIMESTAMP( DATE(), TIME(), '' )           ;*  e.g. 1353068012.035
    * Sleep until the beginning of the next hour
       time = OCONV( TIME(), 'MT' )
       sleep_until = time[1, 2] + 1
       IF sleep_until EQ 24 THEN sleep_until = '00'
       sleep_until := ':00'
       CRT "I'll be back at " : sleep_until   ;*  e.g. I'll be back at 13:00
       SLEEP sleep_until
       CRT OCONV( TIME(), 'MTS' ), ',', "I'm back as promised"

## MULS##

MULS function is used to create a dynamic array of the element-by-element
multiplication of two dynamic arrays.

### COMMAND SYNTAX

    MULS(array1, array2)

Each element of **array1** is multiplied by the corresponding element
of **array2** with the result being returned in the corresponding element
of a new dynamic array. If an element of one dynamic array has no
corresponding element in the other dynamic array, 0 is returned. If
either of a corresponding pair of elements is null, null is returned
for that element.

### EXAMPLE

       A = 1 :@VM: 2 :@VM: 3 :@SM: 4
       B = 4 :@VM: 5 :@VM: 6 :@VM: 9
       PRINT OCONV( MULS(A, B), 'MCP' )       ;*  4]10]18\0]0

## NEGS

NEGS function returns the negative values for all the elements in a
dynamic array. NEG() function returns the negative value for a variable
or an expression.

### COMMAND SYNTAX

    NEGS(dynamic.array)

If the value of an element is negative, the returned value is positive.
If dynamic.array evaluates to null, null is returned. If any element
is null, null is returned for that element.

### EXAMPLE

       dyn_array = 1 :@FM: 2 :@VM :3
       GOSUB PROC.IT                              ;* -1^-2]-3
       dyn_array = 1 :@FM: '' :@VM :3
       GOSUB PROC.IT                              ;* -1^0]-3
       dyn_array = -1 :@FM: -2 :@VM: -3
       GOSUB PROC.IT                              ;*  1^2]3
       dyn_array = 1 :@SM: -2 :@FM: 3
       GOSUB PROC.IT                              ;*  -1\2^-3
       dyn_array<-1> = 'A text'
       GOSUB PROC.IT                            ;* Non-numeric value -- ZERO USED
                                                ;* -1\2^-3^0
       CRT NEG(0)                               ;* 0
       CRT NEG(100)                             ;* -100
       CRT NEG(dyn_array<1> LT dyn_array<2>)    ;* -1 (negative of "true")
       CRT NEG(-1000)                           ;* 1000
       CRT NEG('qwert')                         ;* Non-numeric value -- ZERO USED
                                                ;* 0
       STOP
       &nbsp;
    PROC.IT:
       CRT FMT( NEGS(dyn_array), 'MCP' )
       RETURN
    END

## NES

NES function is used to determine whether elements of one dynamic
array are equal to the elements of another dynamic array.

### COMMAND SYNTAX

    NES(array1, array2)

Each element of **array1** is compared with the corresponding element
of **array2**. If the two elements are equal, 0 is returned in the
corresponding element of a new dynamic array. If the two elements are
not equal, 1 is returned. If an element of one dynamic array has no
corresponding element in the other dynamic array, a 1 is returned. If
either of a corresponding pair of elements is null, null is returned
for that element.

## NEXT

Terminator statement for [FOR](#FOR) loop.

## NOBUF

NOBUF statement turns off buffering for a file previously opened for
sequential processing.

### COMMAND SYNTAX

    NOBUF file.variable { THEN statements [ ELSE statements ] | ELSE statements }

### DESCRIPTION

jBASE can buffer for sequential input and output operations. The NOBUF
statement turns off this behavior and causes all writes to the file to
be performed immediately. The NOBUF statement should be used in
conjunction with a successful OPENSEQ statement and before any input
or output is performed on the record.

If the NOBUF operation is successful, it executes the THEN statements
otherwise, executes the ELSE statements. If file.variable is not a
valid file descriptor then NOBUF statement fails and the program
enters the debugger.

### EXAMPLE

In the following example, if RECORD in DIRFILE can be opened,
output buffering is turned off:

    OPENSEQ 'DIRFILE', 'RECORD' TO FILE THEN NOBUF FILE
    ELSE ABORT

## NOT

NOT function is used to invert the Boolean value of an expression.
It is useful for explicitly testing for a false condition.

### COMMAND SYNTAX

    NOT(expression)

### SYNTAX ELEMENTS

**expression** may evaluate to any Boolean result.

### NOTES

The NOT function will return Boolean TRUE if the expression returns
a Boolean FALSE. It will return Boolean FALSE if the expression
returns a Boolean TRUE.

The NOT function is useful for explicitly testing for the false
condition of some test and can clarify the logic of such a test.

### EXAMPLE

    EQU Sunday TO NOT( MOD( DATE(), 7))
    IF Sunday THEN
       CRT "It is Sunday!"
    END

In this example, the expression MOD (DATE(),7) will return 0 (FALSE)
if the day is Sunday and 1 to 6 (TRUE) for the other days. To
explicitly test for the day Sunday we need to invert the result of
the expression. By using the NOT function we return 1 (TRUE) if the
day is Sunday and 0 (FALSE) for all other values of the expression.

## NOTS

NOTS function is used to return a dynamic array of the logical
complements of each element of dynamic.array.

### COMMAND SYNTAX

    NOTS(dynamic.array)

If the value of the element is true, the NOTS function returns a
false value (0) in the corresponding element of the returned array.
If the value of the element is false, the NOTS function returns a
true value (1) in the corresponding element of the returned array.

A numeric expression that evaluates to 0 has a logical value of false.
A numeric expression that evaluates to anything else, other than the
null value, is a logical true.

An empty string is logically false. All other string expressions,
including strings, which consist of an empty string, spaces, or the
number 0 and spaces, are logically true.

If any element in dynamic.array is null, it returns null for that
element.

### EXAMPLE

       X = 5  ; Y = 5
       PRINT OCONV( NOTS(X-Y :@VM: X+Y), 'MCP' )     ;*  1]0

## NULL

NULL statement performs no function but can be useful in clarifying
syntax and where the language requires a statement but the programmer
does not wish to perform any actions.

### COMMAND SYNTAX

    NULL

### SYNTAX ELEMENTS

None

### EXAMPLES

    LOCATE A IN B SETTING C ELSE NULL

## NUM

NUM function is used to test arguments for numeric values.

### COMMAND SYNTAX

    NUM(expression)

### SYNTAX ELEMENTS

**expression** may evaluate to any data type.

### NOTES

Not exactly it checks that every character in expression is a numeric -
rather if an expression can be considered as a number.

To execute user code migration from older systems correctly, the
NUM function will accept both a null string and the single
characters ".", "+", and "-" as being numeric.

If running jBC in ros emulation the "." , "+" and "-" characters
would not be considered numeric.

### EXAMPLES (prime emulation)

       CRT NUM('')                     ;* 1
       CRT NUM('123334440.12')         ;* 1
       CRT NUM('1233344.40.12')        ;* 0
       CRT NUM('1,233,344.40')         ;* 0 - thousand delimiters don't do
       CRT NUM('1 233 344.40')         ;* 0 - neither do spaces
       CRT NUM('00012')                ;* 1 - leading zeroes are ok
       CRT NUM('-123334440.12')        ;* 1 - minus is ok...
       CRT NUM('123334440.12-')        ;* 0 - ...but not everywhere
       CRT NUM('+123334440.12')        ;* 1
       CRT NUM('6.02e23')              ;* 0 - E notation doesn't work
       CRT NUM('1233Q34440.12')        ;* 0 - of course it's not
       CRT NUM('2+2')                  ;* 0 - expression isn't evaluated
       CRT NUM('.00')                  ;* 1

## NUMS

NUMS function is used to determine whether the elements of a
dynamic array are numeric or nonnumeric strings.

### COMMAND SYNTAX

    NUMS(dynamic.array)

If an element is numeric, a numeric string, or an empty string,
it evaluates to true, and returns a value of 1 to the corresponding
element in a new dynamic array. If the element is a non-numeric
string, it evaluates to false, and returns a value of 0.

The NUMS of a numeric element with a decimal point ( . ) evaluates to
true; the NUMS of a numeric element with a comma ( , ) or dollar sign
( $ ) evaluates to false.

If dynamic.array evaluates to null, it returns null. If an element of
dynamic.array is null, it returns null for that element.

### INTERNATIONAL MODE

When using the NUMS function in International Mode, the statement will
use the Unicode Standard to determine whether an expression is numeric.

## OBJEXCALLBACK

jBASE OBjEX provides the facility to call a subroutine from a front-end
program written in a tool that supports OLE, such as Delphi or Visual
Basic. The OBJEXCALLBACK statement allows communication between the
subroutine and the calling OBjEX program.

### COMMAND SYNTAX

    OBJEXCALLBACK expression1, expression2 THEN | ELSE statements

### SYNTAX ELEMENTS

**expression1** and **expression2** can contain any data. They are
returned to the OBjEX program where they are defined as variants.

If the subroutine containing the OBJEXCALLBACK statement is not called
from an OBjEX program (using the Call Method) then the ELSE clause will
be taken.

### NOTES

The OBJEXCALLBACK statement is designed to allow jBC subroutines to
temporarily return to the calling environment to handle exception
conditions or prompt for additional information. After servicing this
event, the code should return control to the jBC program to ensure that
the proper clean up operations are eventually made. The two parameters can
be used to pass data between the jBC and OBjEX environments in both
directions. They are defined as Variants in the OBjEX environment and as
normal variables in the jBC environment.

See the OBjEX documentation for more information.

### EXAMPLE

    param1 = "SomeActionCode"
    param2 = ProblemItem
    OBJEXCALLBACK param1, param2 THEN
    * this routine was called from ObjEX
    END ELSE
    * this routine was not called from ObjEX
    END

## OCONV

<a name="OCONV"/>

OCONV statement converts internal representations of data to their
external form.

### COMMAND SYNTAX

    OCONV(expression1, expression2)

### SYNTAX ELEMENTS

**expression1** may evaluate to any data type but must be relevant to
the conversion code.

**expression2** should evaluate to a conversion code from the list
below. Alternatively, expression2 may evaluate to a user exit known
to the jBC language or supplied by the user.

### INTERNATIONAL MODE

Description of date, time, number and currency conversions when
used in ICONV and International Mode

### NOTES

OCONV will return the result of the conversion of expression1 by
expression2. Shown below are valid conversion codes:

|Conversion   |     Action                                               |
|-------------|----------------------------------------------------------|
|D{n{c}}      |   Converts an internal date to an external date format.  |
|             |   The numeric argument n specifies the field width       |
|             |   allowed for the year and can be 0 to 4 (default 4).    |
|             |   The character 'c' causes the date to be return in the  |
|             |   form ddcmmcyyyy. If it is not specified then the month |
|             |   name is returned in abbreviated form.                  |
|DI           |   Allows the conversion of an external date to the       |
|             |   internal format even though an output conversion       |
|             |   is expected.                                           |
|DD           |   Returns the day in the current month.                  |
|DM           |   Returns the number of the month in the year.           |
|DMA          |   Returns the name of the current month.                 |
|DJ           |   Returns the number of the day in the year (0-366).     |
|DQ           |   Returns the quarter of the year as a number 1 to 4.    |
|DW           |   Returns the day of the week as a number 1 to 7         |
|             |   (Monday is 1).                                         |
|DWA          |   Returns the name of the day of the week.               |
|DY{n}        |   Returns the year in a field of n characters.           |
|F            |   Given a prospective filename for a command such as     |
|             |   CREATE-FILE this conversion will return a filename     |
|             |   that is acceptable to the version of UNIX TAFC is      |
|             |    running on.                                           |
|MCA          |   Removes all but alphabetic characters from the input   |
|             |   string.                                                |
|MC/A         |   Removes all but the NON-alphabetic characters in the   |
|             |   input string.                                          |
|MCN          |   Removes all but numeric characters in the input string.|
|MC/N         |   Removes all but NON numeric characters in the input    |
|             |   string.                                                |
|MCB          |   Returns just the alphabetic and numeric characters from|
|             |   the input string.                                      |
|MC/B         |   Removes the alphabetic and numeric characters from     |
|             |   their input string.                                    |
|MCC;s1;s2    |   Replaces all occurrences of string s1 with string s2.  |
|MCL          |   Converts all upper case characters in the string to    |
|             |   lower case characters.                                 |
|MCU          |   Converts all lower case characters in the string to    |
|             |   upper case characters.                                 |
|MCT          |   Capitalizes each word in the input string; e.g. JIM    |
|             |   converts to Jim.                                       |
|MCP{c}       |   Converts all non-printable characters to a period      |
|             |   character "." in the input string. When supplied use   |
|             |   the character                                          |
|             |   "c" in place of the period.                            |
|MCPN{n}      |   In the same manner as the MCP conversion, it replaces  |
|             |   all non-printable characters. The ASCII hexadecimal    |
|             |   value                                                  |
|             |   follows the replacing character.                       |
|MCNP{n}      |   Performs the opposite conversion to MCPN. The ASCII    |
|             |   hexadecimal value following the tilde character        |
|             |   converts to its                                        |
|             |   original binary character value.                       |
|MCDX         |   Converts the decimal value in the input string to its  |
|             |   hexadecimal equivalent.                                |
|MCXD         |   Converts the hexadecimal value in the input string to  |
|             |   its decimal equivalent.                                |
|Gncx         |   Extracts x groups separated by character c skipping n  |
|             |   groups, from the input string.                         |
|MT{HS}       |   Performs time conversions.                             |
|MD           |   Converts the supplied integer value to a decimal value.|
|MP           |   Converts a packed decimal number to an integer value.  |
|MX           |   Converts ASCII input to hexadecimal characters.        |
|T            |   Performs file translations given a cross-reference     |
|             |   table in a record in a file.                           |

### EXAMPLES

Date and time:

       CRT OCONV(1, 'D')         ;* 01 JAN 1968
       CRT OCONV( DATE(), 'D' )    ;* here and below output for 30 MAY 2013
       CRT OCONV( DATE(), 'D2' )   ;* 30 MAY 13
       CRT OCONV( DATE(), 'D4/' )  ;* 05/30/2013
       CRT OCONV( DATE(), 'DY' )   ;* 2013
       CRT OCONV( DATE(), 'DY2' )  ;* 13
       CRT OCONV( DATE(), 'DQ' )   ;* 2 (quarter)
       CRT OCONV( DATE(), 'DM' )   ;* 5 (month number)
       CRT OCONV( DATE(), 'DMA' )  ;* MAY
       CRT OCONV( DATE(), 'DD' )   ;* 30
       CRT OCONV( DATE(), 'DJ' )   ;* 150 (number of a day in the year)
       CRT OCONV( DATE(), 'DW' )   ;* 4 (day number in a week, starting from Monday)
       CRT OCONV( DATE(), 'DWA' )  ;* THURSDAY
       CRT OCONV( TIME(), 'MT' )   ;* 20:04
       CRT OCONV( TIME(), 'MTS' )  ;* 20:04:08
       CRT OCONV(1, 'MTS')       ;* 00:00:01
    * difference of 2 dates (in days)
       CRT ICONV('20121231', 'D') - ICONV('20111231', 'D')   ;* 366
    * Check if a year is a leap one
       CRT OCONV( ICONV('20131231', 'D4'), 'DJ' )    ;*  365
       CRT OCONV( ICONV('20161231', 'D4'), 'DJ' )    ;*  366

Strings:

    * split a string
       the_string = 'LONG STRING TO BE SPLIT'
       the_split = FMT(the_string, '10L')
       CRT OCONV(the_split, 'MCP')         ;* LONG STRIN.G TO BE SP.LIT
    * hexadecimal output
       CRT OCONV(the_split, 'MX')
    * Output:
    * 4C4F4E4720535452494EFB4720544F204245205350FB4C495420202020202020
    *
    * Remove non-alphabetic symbols:
       CRT OCONV(the_split, 'MCA')     ;* LONGSTRINGTOBESPLIT
    * Remove all alphabetic symbols:
       CRT OCONV( OCONV(the_split, 'MC/A'), 'MX' )  ;* 20FB202020FB20202020202020
    * Note FB symbols in the output above.. see what's that
       CRT OCONV('FB', 'MCXD')    ;* 251 a.k.a. @TM
       CHANGE @TM TO '->' IN the_split ; CRT the_split ;* LONG STRIN->G TO BE SP->LIT
    * Remove non-numeric symbols:
       CRT OCONV('another 1 bites the dust', 'MCN')    ;* 1
    * Remove all numeric symbols:
       CRT OCONV('another 1 bites the dust', 'MC/N')   ;* another  bites the dust
    * formatting
       CRT SQUOTE( FMT(the_string, '30L') )    ;* 'LONG STRING TO BE SPLIT       '
       CRT SQUOTE( FMT(the_string, '30R') )    ;* '       LONG STRING TO BE SPLIT'
    * replace some data
       CRT OCONV(the_string, 'MCC;STRING;DATA')  ;* LONG DATA TO BE SPLIT
    * change case
       CRT OCONV(the_string, 'MCL')  ;* long string to be split
       CRT OCONV('do it', 'MCU')     ;* DO IT
       CRT OCONV(the_string, 'MCT')  ;* Long String To Be Split
    * extract delimited fields: skip 1 space-delimited word, take 3 from that point
       CRT OCONV(the_string, 'G1 3')  ;* STRING TO BE

Numbers:

    * amounts
       amount_fcy = 1234
       CRT FMT(amount_fcy, 'R%7')   ;*       0001234
       amount_fcy += 0.56
       CRT FMT(amount_fcy, 'R2*19')              ;*  ************1234.56
       CRT SQUOTE( FMT(amount_fcy, 'L2,#19') )     ;*  '1,234.56           '
       CRT FMT(-amount_fcy, 'R2,C&*$#15')        ;*           $1,234.56CR
       CRT FMT(amount_fcy,'L0')                  ;* 1235
    * phone numbers
       CRT FMT(1234567890, 'R((###) ###-###)')       ;* (234) 567-890
       CRT FMT(74952223355, 'R(+# (#3) #3-#2-#2)')   ;* +7 (495) 222-33-55
    * FMT() and OCONV() are often interchangeable;
    * though it's not the case for next 2 lines...
       CRT DQUOTE( FMT(123456.78, 'R2,$#15') )           ;*  "    $123,456.78"
       CRT DQUOTE( OCONV(123456.78, 'R2,$#15') )         ;*  Error in Range Test

User exits:

       CRT OCONV("", "U50BB")        ;* port number and user name
       HUSH ON
       EXECUTE 'SELECT .'
       HUSH OFF
       CRT OCONV("", "U30E0")        ;* number of items in active SELECT list
    * sleep
       start_time = TIME()  ;  dummy = OCONV(3, "U307A")
       CRT TIME() - start_time        ;* 3
    * reverse a string
       CRT OCONV('desrever saw gnirtS', "U51AA")
    * remove duplicate consecutive characters
       CRT OCONV('hhahhahh', "U31AC")        ;* haha


See also: [FMT](#FMT) function.


## OCONVS

<a name="OCONVS"/>

OCONVS function converts the elements of dynamic.array to a specified
format for external output.

### COMMAND SYNTAX

    OCONVS(dynamic.array, conversion)

Converts the elements to the external output format specified by
conversion and returns it in a dynamic array.

**conversion** must evaluate to one or more conversion codes separated
by value marks (ASCII 253).

If multiple codes are used, they are applied from left to right as
follows: the left-most conversion code is applied to the element, the next
conversion code to the right is then applied to the result of the first
conversion, and so on.

If dynamic.array evaluates to null, it returns null. If any element of
dynamic.array is null, it returns null for that element. If conversion
evaluates to null, the OCONVS function fails and the program terminates
with a run-time error message.

The STATUS function reflects the result of the conversion:

|Code|   Status                                                  |
|----|-----------------------------------------------------------|
| 0  |   The conversion is successful.                           |
| 1  |   Passes an invalid element to the OCONVS function; the   |
|    |   original element                                        |
|    |   is returned. If the invalid element is null, it returns |
|    |   null for that element.                                  |
|    |   unless dynamic.array is null, in which case it returns  |
|    |   null.                                                   |
| 2  |   The conversion code is invalid.                         |


### NOTES

For information about converting elements in a dynamic array to an
internal format, see also: [ICONVS](#ICONVS) function.

### INTERNATIONAL MODE

Description of date, time, number and currency conversions when used
in ICONV and International Mode.

## ONGOTO

The ON...GOSUB and ON...GOTO statements are used to transfer program
execution to a label based upon a calculation.

### COMMAND SYNTAX

    ON expression GOTO label{, label...}

    ON expression GOSUB label{, label...}

### SYNTAX ELEMENTS

**expression** should evaluate to an integer numeric value. Labels
should be defined somewhere in the current source file.

**ON GOTO** will transfer execution to the labeled source code line
in the program.

**ON GOSUB** will transfer execution to the labeled subroutine within
the source code.

### NOTES

Use the value of expression as an index to the list of labels
supplied. If the expression evaluates to 1 then the first label
will jump to 2 then the second label will be used and so on.

If the program was compiled when the emulation included the setting
generic_pick = true, then no validations are performed on the index
to see if it is valid. Therefore, if the index is out of range this
instruction will take no action and report no error.

If the program was compiled for other emulations then the index will
be range checked. If found that the index is less than 1, it is
assumed to be 1 and a warning message is issued. If the index is found
to be too big, then the last label in the list will be used to transfer
execution and a warning message will be issued.

### EXAMPLE

       cntrl_var = 1
    *
       ON cntrl_var GOSUB BIGGER
       ON cntrl_var GOSUB EXCEPT, SMALLER
       ON cntrl_var GOSUB SMALLER
    *
       STOP
    *
    BIGGER:
       cntrl_var ++
       CRT cntrl_var
       RETURN
    *
    SMALLER:
       cntrl_var --
       CRT cntrl_var
       RETURN
    *
    EXCEPT:
       CRT 'Error occured'
       RETURN
    *
    END

Output of this program:

<pre>
    2
    1
    0</pre>

## OPEN

<a name="OPEN"/>

OPEN statement is used to open a file or device to a descriptor
variable within jBC.

### COMMAND SYNTAX

    OPEN {expression1,}expression2 TO {variable} { SETTING setvar } \
         THEN | ELSE statements

### SYNTAX ELEMENTS

The combination of **expression1** and **expression2** should evaluate
to a valid file name of a file type that already installed on the
jBASE system. If the file has a dictionary section to be opened by the
statement then specify by the literal string "DICT" being specified in
expression1. If specified, the variable will be used to hold the
descriptor for the file. It should then be to access the file using
READ and WRITE. If no file descriptor variable is supplied, then the
file will be opened to the default file descriptor.

Specific data sections of a multi level file may be specified by
separating the section name from the file name by a "," char in
expression2.

If the OPEN statement fails, it will execute any statements associated
with an ELSE clause. If the OPEN is successful, it will execute any
statements associated with a THEN clause. Note that the syntax requires
either one or both of the THEN and ELSE clauses.

If specifying the SETTING clause and the open fails, setvar will be set
to one of the following values:

### INCREMENTAL FILE ERRORS

|Code   |    Description                        |
|-------|---------------------------------------|
|128    |    No such file or directory          |
|4096   |    Network error                      |
|24576  |    Permission denied                  |
|32768  |    Physical I/O error or unknown error|

### NOTES

The OPEN statement uses the environment variable JEDIFILEPATH to search
for the named file. If there is no defined named file, it will search
the current working directory followed by the home directory of the
current process.
The file that is the subject of the OPEN statement can be of any type
known to the jBASE system. Its type will be determined and correctly
opened transparently to the application, which need not be aware of
the file type.

A jBC program can open an unlimited amount of files (up the limit set by
OS settings).

### EXAMPLE

       EXECUTE 'DELETE-FILE DATA F.TEMP'
       EXECUTE 'CREATE-FILE DATA F.TEMP 1 101 TYPE=J4'
       OPEN 'F.TEMP' TO F.TEMP ELSE ABORT 201, 'F.TEMP'
       V.REC.INIT = 'LINE 1' :@FM: 'LINE 2' :@FM: 'LINE 3'
       WRITE V.REC.INIT TO F.TEMP, 'REC1'
       CLOSE F.TEMP

### EXAMPLE 2

Get list of current processes and output port number and PID for each:

       OPEN SYSTEM(1027) TO PROC ELSE STOP 201, "PROC"
       SELECT PROC TO SEL
       LOOP
       WHILE READNEXT key FROM SEL DO
          READ PROCESSRECORD FROM PROC, key ELSE CRT "Read Error"  ;  STOP
          V.PORTNO = PROCESSRECORD<1>
          V.PID = PROCESSRECORD<4>
          PRINT FMT(V.PORTNO, '2R') : '|' : FMT(V.PID, '8R')
       REPEAT

## OPENDEV

OPENDEV statement is used to open a device (or file) for sequential
writing and/or reading.

### COMMAND SYNTAX

    OPENDEV Device TO FileVar { LOCKED statements } THEN | ELSE statements

### SYNTAX ELEMENTS

**Device** specifies the target device or file.

**FileVar** contains the file descriptor of the file when the open
was successful.

**Statements** are conditional jBC statements.

### NOTES

If the device does not exist or cannot be opened it executes the ELSE
clause. Once open it takes a lock on the device. If the lock cannot be
taken then the LOCKED clause is executed if it exists otherwise the
ELSE clause is executed. The specified device can be a regular file,
pipe or special device file. Regular file types only take locks. Once
open the file pointer is set to the first line of sequential data.

### EXAMPLE

    OPENDEV "\\.\TAPE0" TO tape.drive ELSE STOP

Opens the Windows default tape drive and prepares it for sequential
processing.

For more information on sequential processing, see [READSEQ](#READSEQ),
[WRITESEQ](#WRITESEQ) the sequential processing example.

## OPENINDEX

OPENINDEX statement is used to open a particular index definition for
a particular file. This index file variable can later be used with
the SELECT statement.

### COMMAND SYNTAX

    OPENINDEX filename,indexname TO indexvar { SETTING setvar } THEN  \
      | ELSE statements

### SYNTAX ELEMENTS

**filename** should correspond to a valid file which has at least one
index.

**indexname** should correspond to an index created for the filename.

**indexvar** is the variable that holds the descriptor for the index.

If the **OPEN** statement fails then it will execute any statements
associated with an ELSE clause. If the **OPEN** is successful then it
will execute any statements associated with a THEN clause. Note that the
syntax requires either one or both of the THEN and ELSE clauses.

If the **SETTING** clause is specified and the OPEN fails, setvar will be
set to one of the following values:

### INCREMENTAL FILE ERRORS

|Code   |    Description                        |
|-------|---------------------------------------|
|128    |    No such file or directory          |
|4096   |    Network error                      |
|24576  |    Permission denied                  |
|32768  |    Physical I/O error or unknown error|

### EXAMPLES

    OPENINDEX "CUSTOMER","IXLASTNAME" TO custlastname.ix SETTING errval ELSE
      CRT "OPENINDEX failed for file CUSTOMER, index IXLASTNAME"
      ABORT
    END

## OPENPATH

<a name="OPENPATH"/>

OPENPATH statement is used to open a file (given an absolute or
relative path) to a descriptor variable within jBC.
See also: [OPEN](#OPEN) statement.

### COMMAND SYNTAX

    OPENPATH expression1 TO {variable} { SETTING setvar } THEN | ELSE statements

### SYNTAX ELEMENTS

**expression1** should be an absolute or relative path to the file
including the name of the file to be opened. If specified, variable
will be used to hold the descriptor for the file. It should then be
to access the file using READ and WRITE. If no file descriptor
variable is supplied, then the file will be opened to the default
file descriptor.

If the **OPENPATH** statement fails it will execute any statements
associated with an ELSE clause. If successful, the OPENPATH will
execute any statements associated with a THEN clause. Note that
the syntax requires either one or both of the THEN and ELSE
clauses.

If the **SETTING** clause is specified and the open fails, setvar
will be set to one of the following values:

### INCREMENTAL FILE ERRORS

|Code   |    Description                        |
|-------|---------------------------------------|
|128    |    No such file or directory          |
|4096   |    Network error                      |
|24576  |    Permission denied                  |
|32768  |    Physical I/O error or unknown error|

### NOTES

The path specified may be either a relative or an absolute path
and must include the name of the jBASE file being opened.

The file that is the subject of the OPENPATH statement can be of
any type known to the jBASE system. Its type will be determined
and correctly opened transparently to the application, which need
not be aware of the file type.

A jBC program can open an unlimited amount of files.

### EXAMPLES

    OPENPATH "C:\Home\CUSTOMERS" TO F.Customers ELSE
       ABORT 201, "CUSTOMERS"
    END

Opens the file CUSTOMERS (located in C:\Home) to its own file
descriptor F.Customers

    OPEN "F:\Users\data\CUSTOMERS" ELSE ABORT 201, "CUSTOMERS"

Opens the CUSTOMERS file (located in F:\Users\data) to the default
file variable.

## OPENSEQ

<a name="OPENSEQ"/>

OPENSEQ is used to open a file for sequential writing and/or
reading.

### COMMAND SYNTAX

    OPENSEQ Path{,File} {READONLY} TO FileVar { LOCKED statements }  \
            THEN | ELSE statements

### SYNTAX ELEMENTS

**Path** specifies the relative or absolute path of the target
directory or file.

**File** specifies additional path information of the target
file.

**FileVar** contains the file descriptor of the file when the
open was successful.

**Statements** are conditional jBC statements.

### NOTES

If the file does not exist or cannot be opened it then executes
the ELSE clause. However, if JBASICEMULATE is set for Sequoia
(use value "seq") emulation then OPENSEQ will create the file if it
does not exist. This behavior can also be achieved by specifying
"openseq_creates = true" in Config_EMULATE for the emulation being
used. Once open a lock is taken on the file. If the lock cannot be
taken then the LOCKED clause is executed if it exists otherwise the
ELSE clause is executed. If specified the READONLY process takes a
read lock on the file, otherwise it takes a write lock. The specified
file can be a regular, pipe or special device file. Locks are only
taken on regular file types. Once open the file pointer is set to the
first line of sequential data.

### EXAMPLE 1

Create a flat file and write to it. If file already exists - append data to it:

       V.DIR.OUT = '.'
       V.FILE.OUT = 'report.txt'
       OPENSEQ V.DIR.OUT, V.FILE.OUT TO F.FILE.OUT THEN
          SEEK F.FILE.OUT, 0, 2 ELSE  ;* go to the end
             CRT 'Seek error'
             STOP
          END
          WRITESEQ 'One more line' TO F.FILE.OUT ELSE
             CRT 'Write error'
             STOP
          END
       END ELSE
          WRITESEQ 'Line 1' TO F.FILE.OUT ELSE
             CRT 'Write error'
             STOP
          END
       END


### EXAMPLE 2

Run the previous example several times, then - this one
(flat file will be read and proceeded line-by-line):

       V.DIR.IN = '.'
       V.FILE.IN = 'report.txt'
       OPENSEQ V.DIR.IN, V.FILE.IN TO F.FILE.IN ELSE
          CRT 'Failed to open', V.FILE.IN
          STOP
       END
       V.LINE.NO = 0
       LOOP
          READSEQ V.LINE FROM F.FILE.IN ELSE BREAK
          V.LINE.NO ++
          CRT '[' : V.LINE.NO : ']' : V.LINE
       REPEAT

Output will look like:

<pre>
    [1]Line 1
    [2]One more line
    [3]One more line
    ...</pre>

## OPENSER

<a name="OPENSER"/>

OPENSER statement is used to handle the Serial IO.

Serial IO to the COM ports on NT and to device files, achieves this
on UNIX by using the sequential file statements. In addition, you
can perform certain control operations using the [IOCTL](#IOCTL)
function.

### COMMAND SYNTAX

    OPENSER Path,DevInfo | PIPE TO FileVar THEN | ELSE Statements

### SYNTAX ELEMENTS

**Path** is the pathname of the required device.

**DevInfo** consists of the following:

| Baud  |     | baud rate required                       |
|-------|-----|------------------------------------------|
| Flow  |  y  | X-ON X-OFF flow control (default)        |
|       |  n  | no flow control                          |
|       |  i  | input flow control                       |
|       |  o  | output flow control                      |
|       |     |                                          |
|Parity |  y  | X-ON X-OFF flow control (default)        |
|       |  n  | no flow control                          |
|       |  i  | input flow control                       |
|       |  o  | output flow control                      |

**PIPE** specifies the file is to be opened to a PIPE for reading.

### NOTES

The PIPE functionality allows a process to open a PIPE, once
opened then the process can execute a command via the
[WRITESEQ](#WRITESEQ)/[SEND](#SEND) statement and then received
the result back via the [GET](#GET)/[READSEQ](#READSEQ) statements.

### EXAMPLES

       FileName = "/dev/pts/1"
       OPENSER FileName TO File ELSE STOP 201, FileName
       WRITESEQ "ls -l" TO File ELSE NULL
       LOOP
          Terminator = CHAR(10)
          WaitTime = 4
          GET Input SETTING Count FROM File UNTIL Terminator RETURNING TermChar \
                WAITING WaitTime THEN
             CRT "Get Ok, Input " :Input: " Count " :Count: "TermChar" :TermChar
          END ELSE
             CRT "Get Timed out Input " :Input: " Count " : Count: " TermChar" \
                :TermChar
          END
       WHILE Input NE "" DO
       REPEAT

## ORS

ORS function is used to create a dynamic array of the logical OR of
corresponding elements of two dynamic arrays.

### COMMAND SYNTAX

    ORS(array1, array2)

Each element of the new dynamic array is the logical OR of the
corresponding elements of **array1** and **array2**. If an element
of one dynamic array has no corresponding element in the other
dynamic array, it assumes a false for the missing element.

If both corresponding elements of array1 and array2 are null, it
returns null for those elements. If one element is the null value
and the other is 0 or an empty string, it returns null. If one
element is the null value and the other is any value other than 0
or an empty string, it returns true.

### EXAMPLE

       A = "A" :@SM: 0 :@VM: 4 :@SM: 1
       B = 0 :@SM: 1-1 :@VM :2
       PRINT OCONV( ORS(A, B), 'MCP')         ;*   1\0]1\1

## OSBREAD

<a name="OSBREAD"/>

OSBREAD command reads data from a file starting at a specified byte
location for a certain length of bytes, and assigns the data to a
variable.

### COMMAND SYNTAX

    OSBREAD var FROM file.var [ AT byte.expr ] LENGTH length.expr  \
            [ ON ERROR statements ]

OSBREAD performs an operating system block read on a UNIX or
Windows file.

### SYNTAX ELEMENTS

**var** specifies a variable to which the data read is assigned.

**FROM file.var** specifies a file from which the data is read.

**AT byte.expr** specifies a location inside the file from where
the data reading operation is to start. If byte.expr is 0, the
read begins at the beginning of the file.

**LENGTH length.expr** specifies length of data to be read from the
file, starting at byte.expr. length.expr cannot be longer than the
maximum string length determined by your system configuration.

**ON ERROR statements** are statements executed if a fatal error
occurs (if the file is not open, or if the file is a read-only
file). If you do not specify the ON ERROR clause, the program will
terminate under such fatal error conditions.

*STATUS Function Return Values*
After you execute OSBREAD, the STATUS function returns either 0 or
a failure code.

### NOTE

Before you use OSBREAD, you must open the file by using the
[OSOPEN](#OSOPEN) or [OPENSEQ](#OPENSEQ) command.

jBASE uses the ASCII 0 character [CHAR (0)] as a string-end delimiter.
Therefore, ASCII 0 cannot be used in any string variable within jBASE.
OSBREAD converts CHAR(0) to CHAR(128) when reading a block of data.

### EXAMPLE

In the following example, the program test.b reads itself and outputs its
contents to the screen:

       OSOPEN 'test.b' TO MYFILE ELSE STOP
       OSBREAD Data FROM MYFILE AT 0 LENGTH 10000
       CRT Data

## OSBWRITE

<a name="OSBWRITE"/>

OSBWRITE command writes an expression to a sequential file starting at a
specified byte location.

### COMMAND SYNTAX

    OSBWRITE expr { ON | TO } file.var [ AT byte.expr ] [ NODELAY ]  \
             [ ON ERROR statements ]

OSBWRITE immediately writes a file segment out to the UNIX, Windows
NT, or Windows 2000 file. There is no necessity to specify a length
expression because the number of bytes in expr is already written to
the file.

OSBWRITE converts CHAR (128) back to CHAR(0) when writing a block of
characters.

### SYNTAX ELEMENTS

**expr** specifies the expression to be written in the file.

**ON | TO file.var** specifies the file on which the expression is to
be written.

**AT byte.expr** specifies the byte number from where the expression
is to be written. For example, if byte.expr is 0, then the expression
is written in the beginning of the file.

**NODELAY** forces an immediate write.

**ON ERROR statements** are the statements executed if the OSBWRITE
statement fails with fatal error, I/O error, or jBASE cannot find the
file. If you do not specify the ON ERROR clause and a fatal error
occurs, the program will terminate.

*STATUS Function Return Values*

After you execute OSBWRITE, the STATUS function returns either 0 or
a failure code.

| Code | Description               |
|------|---------------------------|
|0     | The write was successful. |
|1     | The write failed.         |

### NOTES

Before you use OSBWRITE, you must open the file by using the OSOPEN or
OPENSEQ command.

jBASE uses the ASCII 0 character [CHAR (0)] as a string-end delimiter.
Therefore, ASCII 0 cannot be used in any string variable within jBASE.
If jBASE reads a string that contains CHAR(0) characters by using
OSBREAD, those characters are converted to CHAR(128).

### EXAMPLE

In the following example, the program statement writes the data in MYPIPE
to the opened file starting from the beginning of the file:

    OSBWRITE Data ON MYPIPE AT 0

## OSCLOSE

<a name="OSCLOSE"/>

OSCLOSE command closes a sequential file that you have opened with the
OSOPEN or OPENSEQ command.

### COMMAND SYNTAX

    OSCLOSE file.var [ ON ERROR statements ]

### SYNTAX ELEMENTS

**file.var** specifies the file to close.

**ON ERROR statements** specifies statements executed when the OSCLOSE
statement fails with fatal error, I/O error, or JBASE cannot find the
file.

If you do not specify the ON ERROR clause and a fatal error occurs, the
program will enter the debugger.

*STATUS Function Return Values*

After you execute OSCLOSE, the STATUS function returns either 0 or a
failure code.

| Code | Description                   |
|------|-------------------------------|
|0     | Closes the file successfully. |
|1     | Fails to write the file.      |

### EXAMPLE

In the following example, the program statement closes the file opened
to MYPIPE file variable.

    OSCLOSE MYPIPE

## OSDELETE

<a name="OSDELETE"/>

OSDELETE command deletes a NT or UNIX file.

### COMMAND SYNTAX

    OSDELETE filename [ ON ERROR statements ]

### SYNTAX ELEMENTS

**filename** specifies the file to be deleted. Filename must include the
file path. If you do not specify a path, jBASE searches the current
directory.

**ON ERROR statements** specifies the statements to execute if the
OSDELETE statement fails with fatal error, I/O error, or jBASE cannot
find the file.

If you do not specify the ON ERROR clause and a fatal error occurs,
the program will terminate.

*STATUS Function Return Values*

After you execute OSDELETE, the STATUS function returns either 0 or
a failure code.

| Code | Description                     |
|------|---------------------------------|
|0     |  Deletes the file successfully. |
|1     |  Fails to delete the file.      |

### EXAMPLES

In the following example, the program statement deletes the file
'MYPIPE' in the current directory:

    OSDELETE "MYPIPE"

## OSOPEN

<a name="OSOPEN"/>

OSOPEN command opens a sequential file that does not use CHAR (10) as
the line delimiter.

### COMMAND SYNTAX

    OSOPEN filename TO file.var [ ON ERROR statements ] { THEN | ELSE } statements

Read/write access mode is the default. Override this access mode by
using READONLY and WRITEONLY.

### SYNTAX ELEMENTS

**filename** specifies the file to be opened. Filename must include
the entire path name unless the file resides in the current directory.

**TO file.var** specifies a variable to contain a pointer to the file.

**ON ERROR** statements are statements executed when the OSOPEN
statement fails with fatal error, I/O error, or JBASE cannot find
the file. If you do not specify the ON ERROR clause and a fatal
error occurs, the program will enter the debugger.

**THEN** statements executes if the read is successful.

**ELSE** statements executes if the read is not successful or the
record (or ID) does not exist.

### NOTES

After opening a sequential file with [OSOPEN](#OSOPEN), use
[OSBREAD](#OSBREAD) to read a block of data from the file, or
[OSBWRITE](#OSBWRITE) to write a block of data to the file. You also
can use [READSEQ](#READSEQ) to read a record from the file, or
[WRITESEQ](#WRITESEQ) or [WRITESEQF](#WRITESEQF) to write a record to
the file, if the file is not a named pipe. ([READSEQ](#READSEQ),
[WRITESEQ](#WRITESEQ), [WRITESEQF](#WRITESEQF) are line-oriented
commands that use CHAR (10) as the line delimiter.)

### EXAMPLE

In the following example, the program statement opens the file
'MYSLIPPERS' as SLIPPERS.

    OSOPEN 'MYSLIPPERS' TO SLIPPERS ELSE STOP

## OSREAD

<a name="OSREAD"/>

OSREAD reads an OS file.

### COMMAND SYNTAX

    OSREAD Variable FROM expression { ON ERROR Statements }  \
          { THEN | ELSE } Statements

### SYNTAX ELEMENTS

**Variable** specifies the variable which is to be assigned to the
read data.

**Expression** specifies the full file path.  If the file resides in
the JEDIFILEPATH then just the file name is required.

**ON ERROR** Statements are conditional jBC statements to be executed
when the OSREAD statement fails with fatal error (because the file is
not open), I/O error, or jBASE cannot find the file. If you do not
specify the ON ERROR clause and a fatal error occurs, the program will
terminate.

THEN | ELSE:  If the OSREAD statement fails, it will execute any
statements associated with an ELSE clause. If the OSREAD is successful,
it will execute any statements associated with a THEN clause. Note that
the syntax requires either one or both of the THEN and ELSE clauses.

### WARNING

Do not use OSREAD on large files. The jBC OSREAD command reads an
entire sequential file and assigns the contents of the file to a
variable. If the file is too large for the program memory, the
program aborts and generates a runtime error message. On large files,
use [OSBREAD](#OSBREAD) or [READSEQ](#READSEQ).
jBASE uses the ASCII 0 character (CHAR (0)) as a string-end delimiter.
ASCII 0 is not useable within string variable in jBC. This command
converts CHAR(0) to CHAR(128) when reading a block of data.

### NOTE

OSREAD doesn't include the LF character after the last line in the file
to the resulting variable:

### EXAMPLE

       V.DIR.OUT = '.'  ;   V.FILE.OUT = 'report.txt'
       OPENSEQ V.DIR.OUT, V.FILE.OUT TO F.FILE.OUT THEN
          WEOFSEQ F.FILE.OUT
       END ELSE
          CREATE F.FILE.OUT ELSE CRT 'File create error'  ;  STOP
       END
       V.BUFFER = STR('.', 999)
       LOOP
          WRITESEQ V.BUFFER TO F.FILE.OUT ELSE CRT 'Write error'  ;  STOP
          V.FILE.SIZE = DIR(V.FILE.OUT)<1>
          CRT V.FILE.SIZE
       UNTIL V.FILE.SIZE GE 10000
       REPEAT
       CLOSESEQ F.FILE.OUT
       OSREAD V.ALL FROM V.FILE.OUT ELSE CRT 'Read error'  ;  STOP
       CRT LEN(V.ALL)
       CRT DQUOTE( RIGHT(V.ALL, 20) )

Output:

<pre>
    1000
    2000
    3000
    4000
    5000
    6000
    7000
    8000
    9000
    10000
    9999
    "...................."</pre>

## OSWRITE

<a name="OSWRITE"/>

The OSWRITE command writes the contents of an expression to a
sequential file.

### COMMAND SYNTAX

    OSWRITE expr { ON | TO } filename [ ON ERROR statements ]

### SYNTAX ELEMENTS

**expr** specifies the expression to be written into a file.

**ON | TO filename** specifies the name of a sequential file to
which the expression is to be written.

**ON ERROR** statements are statements to be executed when the
OSWRITE statement fails with fatal error (because the file is
not open), I/O error, or jBASE cannot find the file. If you do not
specify the ON ERROR clause and if a fatal error occurs, the program
will enter the debugger.

### NOTE

JBASE uses the ASCII 0 character [CHAR(0)] as a string-end delimiter.
For this reason, you cannot use ASCII 0 in any string variable in
jBASE. If jBASE reads a string with a CHAR(0) character, and then the
character is converted to CHAR(128), OSWRITE converts CHAR(128) to
CHAR(0) when writing a block of characters.

### EXAMPLE

In the following example, the program segment writes the contents of
FOOTWEAR variable to the file called "PINK" in the
directory '/usr/local/myslippers'.

    OSWRITE FOOTWEAR ON "/usr/local/myslippers/PINK"

## OUT

OUT statement is used to send raw characters to the current output
device (normally the terminal).

### COMMAND SYNTAX

    OUT expression

### SYNTAX ELEMENTS

**expression** should evaluate to a numeric integer in the range 0
to 255, being the entire range of ASCII characters.

### NOTES

The numeric expression is first converted to the raw ASCII character
specified and then sent directly to the output advice.

### EXAMPLES

    EQUATE BELL TO OUT 7
    BELL ;* Sound terminal bell
    FOR I = 32 TO 127 ; OUT I ; NEXT I ;* Printable chars
    BELL

# jBC Functions and Statements (P - T)

## PAGE

PAGE command is used to print any FOOTING statement, throw a PAGE and
print any heading statement on the current output device.

### COMMAND SYNTAX

    PAGE {expression}

### SYNTAX ELEMENTS

If **expression** is specified it should evaluate to a numeric integer,
which will cause the page number after the page throw to be set to this
value.

### EXAMPLES

    HEADING '10 PAGE REPORT'
    FOR I = 1 TO 10
    	    PAGE
    	    GOSUB PrintPage
    NEXT I

## PAUSE

PAUSE statement allows processing to be suspended until an external
event triggered by a [WAKE](#WAKE) statement from another process or
a timeout occurs.

### COMMAND SYNTAX

    PAUSE {expression}

### SYNTAX ELEMENTS

**expression** may evaluate to a timeout value, which is the maximum
number of seconds to suspend the process. If the expression is omitted
then the PAUSE statement will cause the process to suspend until woken
by the [WAKE](#WAKE) statement.

If a timeout value is specified and the suspended process is not woken
by the [WAKE](#WAKE) statement then the process will continue once the
timeout period has expired.

If a [WAKE](#WAKE) statement is executed before a PAUSE statement, then
the PAUSE will be ignored and processing will continue until a subsequent
PAUSE statement.

### EXAMPLE

Pausing program:

       @USER.ROOT = 'Sleeping beauty'
       start_time = TIME()
       CRT 'Pausing...'
       PAUSE 20
       IF TIME() - start_time LT 20 THEN CRT "Who's there?"
       ELSE CRT 'Resuming...'

Waking program:

    INCLUDE JBC.h
       OPEN SYSTEM(1027) TO PROC ELSE STOP 201, SYSTEM(1027)
       SELECT PROC
       *
       LOOP WHILE READNEXT key DO
          READ rec FROM PROC, key THEN
             IF rec<USER_PROC_USER_ROOT> EQ 'Sleeping beauty' THEN
                CRT 'Found...' :
                WAKE rec<USER_PROC_PORT_NUMBER>
                CRT 'and awoken'
                STOP
             END
          END
       REPEAT
       CRT 'Nobody sleeps'

## PERFORM

<a name="PERFORM"/>

PERFORM is synonymous with [EXECUTE](#EXECUTE)

## PRECISION##

<a name="PRECISION"/>

PRECISION statement informs the number of digits of precision used after
the decimal point.

### COMMAND SYNTAX

    PRECISION integer

### NOTES

A PRECISION statement can be specified any number of times in a source file.
Only the most recently defined precision will be active at any one time.

Calling programs and external subroutines do not have to be compiled at the
same degree of precision, however, any changes to precision in a subroutine
will not persist when control returns to the calling program.

jBASE uses the maximum degree of precision allowed on the host machine in all
mathematical calculations to ensure maximum accuracy. It then uses the defined
precision to format the number.

### EXAMPLE

        PRECISION 6
        CRT 2 / 3

will print the value 0.666666 (note: truncation not rounding!).

### EXAMPLE 2

       var_1 = '0.123456789012345678901234567890123456789012345678901234567890'
       var_2 = '0.1234567890123456789012345678901234567890123456789012345678901'
       PRECISION 13
       GOSUB TEST                ;* 1
       PRECISION 17
       GOSUB TEST                ;* 0
       STOP
    TEST:
       var_3 = (var_1 = var_2)
       CRT var_3
       RETURN
    END


## PRINT

PRINT statement sends data directly to the current output device like terminal
or printer.

### COMMAND SYNTAX

    PRINT expression {, expression...} {:}

### SYNTAX ELEMENTS

An **expression** can evaluate to any data type. The PRINT statement will
convert the result to a string type for printing. Expressions separated by
commas will be sent to the output device separated by a tab character.

The PRINT statement will append a newline sequence to the final expression
unless it is terminated with a colon ":" character.

### NOTES

As the expression can be any valid expression, it may have output formatting
applied to it.

If a PRINTER ON statement is currently active then output will be sent to the
currently assigned printer form queue.

See also: SP-ASSIGN command and [CRT](#CRT).

### EXAMPLES

       A = 3
       PRINT DQUOTE(A 'R#5')            ;*  "    3"
       PRINT @(8,20) : "Patrick" :

## PRINTER

PRINTER statement controls the destination of output from the PRINT
statement.

### COMMAND SYNTAX

    PRINTER ON | OFF | CLOSE

### NOTES

**PRINTER ON** redirects all subsequent output from the PRINT statement
to the print spooler.

**PRINTER OFF** redirects all subsequent output from the PRINT statement
to the terminal device.

**PRINTER CLOSE** will act as PRINTER OFF but in addition closes the
currently active spool job created by the active PRINTER ON statement.

### EXAMPLES

        PRINTER ON             ;* Open a spool job
        FOR I = 1 TO 60
           PRINT "Line " : I   ;* Send to printer
           PRINTER OFF
           PRINT "+" :         ;* Send to terminal
           PRINTER ON          ;* Back to printer
        NEXT I
        PRINTER CLOSE          ;* Allow spooler to print it

## PRINTERR

PRINTERR statement is used to print standard jBASE error messages.

### COMMAND SYNTAX

    PRINTERR expression

### SYNTAX ELEMENTS

Field 1 of the **expression** should evaluate to the numeric or string
name of a valid error message in the jBASE error message file. If the
error message requires parameters then these can be passed to the message
as subsequent fields of the expression.

### INTERNATIONAL MODE

When the PRINTERR statement is used in International Mode, the error
message file to be used, i.e. the default "jBASICmessages" or other as
configured via the error message environment variable, will be suffixed
with the current locale. For example, if the currently configured
locale is "fr_FR" then the statement will attempt to find the specified
error message record id in the "jBASICmessages_fr_FR" error message
file. If the file cannot be found then the country code will be discarded
and just the language code used. i.e. the file "jBASICmessages_fr" will
be used. If this file is also not found then the error message file
"jBASICmessages" will be used.

### NOTES

The PRINTERR statement is most useful for user-defined messages that
have been added to the standard set.

You should be very careful when typing this statement it is very
similar to the PRINTER statement. Although this is not ideal, the
PRINTERR statement must be supported for compatibility with older
systems.

### EXAMPLE

       PRINTERR 201 : CHAR(254) : "CUSTOMERS"

Output:

<pre>
     &lowast;&lowast; Error [ 201 ] &lowast;&lowast;
    Unable to open file CUSTOMERS</pre>

## PROCREAD

<a name="PROCREAD"/>

PROCREAD statement is used to retrieve data passed to programs from a
jCL program.

### COMMAND SYNTAX

    PROCREAD variable THEN | ELSE statements

### SYNTAX ELEMENTS

**variable** is a valid jBC identifier, which will be used to store
the contents of the primary input buffer of the last jCL program
called.

If a jCL program does not initiate the program the PROCREAD will fail
and execute any statements associated with an ELSE clause. If the
program was initiated by a jCL program then the PROCREAD will succeed,
the jCL primary input buffer will be assigned to variable and any
statements associated with a THEN clause will be executed.

### NOTES

It is recommended that the use of jCL and therefore the PROCREAD
statement should be not be expanded within your application and
gradually replaced with more sophisticated methods such as UNIX
scripts or jBC programs.

### EXAMPLE

    PROCREAD Primary ELSE
      CRT "Unable to read the jCL buffer"
      STOP
    END

## PROCWRITE

PROCWRITE statement is used to pass data back to the primary input
buffer of a calling jCL program.

### COMMAND SYNTAX

    PROCWRITE expression

### SYNTAX ELEMENTS

**expression** may evaluate to any valid data type.

### NOTES

See also: [PROCREAD](#PROCREAD)

### EXAMPLE

    PROCWRITE "Success" : CHAR(254) : "0"

## PROGRAM

PROGRAM statement performs no function other than to document the
source code.

### COMMAND SYNTAX

    PROGRAM progname

### SYNTAX ELEMENTS

Progname can be any string of characters.

### EXAMPLE

    PROGRAM HelpUser
    !
    ! Start of program

## PROMPT

PROMPT statement is used to change the PROMPT character used by terminal
input commands.

### COMMAND SYNTAX

    PROMPT expression

### SYNTAX ELEMENTS

**expression** can evaluate to any printable string.

### NOTES

The entire string is used as the prompt.

The default prompt character is the question mark "?" character.

### EXAMPLE

    PROMPT "Next answer : "
    INPUT Answer

## PUTENV

<a name="PUTENV"/>

PUTENV is used to set environment variables for the current process.

### COMMAND SYNTAX

    PUTENV(expression)

### SYNTAX ELEMENTS

**expression** should evaluate to a string of the form:

EnvVarName=value

where

EnvVarName is the name of a valid environment variable and value is
any string that makes sense to the variable being set.

If PUTENV function succeeds it returns a Boolean TRUE value, if it
fails it will return a Boolean FALSE value.

### NOTES

PUTENV only sets environment variables for the current process and
processes spawned (say by EXECUTE) by this process. These variables
are known as export only variables.

See also: [GETENV](#GETENV)

### EXAMPLE

       V.ENV = 'JBASE_ERRMSG_ZERO_USED'
       IF NOT( PUTENV(V.ENV : '=35') ) THEN
          CRT 'PUTENV failed'
          STOP
       END
       CRT 'See the impact of JBASE_ERRMSG_ZERO_USED'
       CRT '=35'
       CRT V.VAR     ;* variable not assigned; nothing is being output
       IF NOT( PUTENV(V.ENV : '=0') ) THEN
          CRT 'PUTENV failed'
          STOP
       END
       CRT '=0'
       CRT V.VAR     ;* Invalid or uninitialised variable --  NULL USED ,
                     ;* Var (UNKNOWN) , Line    17 , Source test.b

## PWR

PWR function raises a number to the n'th power.

### COMMAND SYNTAX

    PWR(expression1, expression2)

or

    expression1 ^ expression2

### SYNTAX ELEMENTS

Both **expression1** and **expression2** should evaluate to numeric
arguments. The function will return the value of expression1 raised
to the value of expression2.

### NOTE

If expression1 is negative and expression2 is not an integer then a
maths library error is displayed and the function returns the value
0. The resulting output is "0.0nan".

All calculations are performed at the maximum precision supported on
the host machine and truncated to the compiled precision on completion.

### EXAMPLE

          A = 2
          B = 31
          CRT "2 GB is " : A ^ B                   ;* 2 GB is 2147483648
          CRT "2 GB is definitely " : PWR(A, B)    ;* 2 GB is definitely 2147483648
          CRT "-2 GB is " : NEG(A)^B               ;* -2 GB is -2147483648
          CRT "2 to the power of 31.5 is " : PWR(A, B+0.5)
                                       ;* 2 to the power of 31.5 is 3037000499.9761
          CRT "-2 to the power of 31.5 is " : PWR( NEG(A), B+0.5)
                                       ;* -2 to the power of 31.5 is 0.0nan

## QUOTE / DQUOTE / SQUOTE

These three functions will enclose a single or double quotation mark
at the beginning and end of a string.

### COMMAND SYNTAX

    QUOTE(expression)

    DQUOTE(expression)

    SQUOTE(expression)

### SYNTAX ELEMENTS

**expression** may be any expression that is valid in the JBC language.

### NOTES

The QUOTE and DQUOTE functions will enclose the value in double
quotation marks. The SQUOTE function will enclose the value in
single quotation marks.

### EXAMPLES

See ["String variables"](#String_variables).

## RAISE

RAISE function raises system delimiters in a string to the next
highest delimiter.

### COMMAND SYNTAX

    RAISE(expression)

### SYNTAX ELEMENTS

The **expression** is a string containing one or more delimiters,
which are raised as follows:

| ASCII character  | Raised to       |
|------------------|-----------------|
| 248              | 249             |
| 249              | 250             |
| 250              | 251             |
| 251              | 252             |
| 252              | 253             |
| 253              | 254             |
| 254              | 255             |

### EXAMPLE

       V.ARRAY = 1 :@TM: 2 :@SM: 3 :@VM: 4
       CRT OCONV( V.ARRAY, 'MCP' )                      ;*  1.2\3]4
       CRT OCONV( RAISE(V.ARRAY), 'MCP' )               ;*  1\2]3^4

## READ

<a name="READ"/>

READ statement allows a program to read a record from a previously
opened file into a variable.

### COMMAND SYNTAX

    READ variable1 FROM {variable2,} expression { SETTING setvar }  \
         { ON ERROR statements } THEN | ELSE statements

### SYNTAX ELEMENTS

**variable1** is the identifier into which the record will be read.

**variable2**, if specified, should be a jBC variable that has
previously been opened to a file using the OPEN statement. If
variable2 is not specified then the default file is assumed.

The expression should evaluate to a valid record key for the file.

If the SETTING clause is specified and the reading process fails,
setvar will be set to one of the following values:

### INCREMENTAL FILE ERRORS

| Code  | Description                           |
|-------|---------------------------------------|
|128    |    No such file or directory          |
|4096   |    Network error                      |
|24576  |    Permission denied                  |
|32768  |    Physical I/O error or unknown error|

If ON ERROR is specified, the statements following the ON ERROR
clause will be executed for any of the above Incremental File
Errors except error 128.

### NOTES

If you wish to set a lock on a record, you should do so explicitly
with the [READU](#READU) statement.

### EXAMPLE

       IF NOT( GETENV('TAFC_HOME', V.HOME) ) THEN
          CRT 'TAFC_HOME not defined'
          STOP
       END
       OPEN V.HOME : '/jbcmessages' TO F.MSG ELSE ABORT 201, 'jbcmessages'
       READ R.MSG FROM F.MSG, 'ARRAY_ILLEGAL_SIZE' ELSE
          CRT 'ERROR READING THE FILE, ID=ARRAY_ILLEGAL_SIZE'
          STOP
       END
       CRT R.MSG

Program output:

<pre>
    &lowast;&lowast; Error [ ARRAY_ILLEGAL_SIZE ] &lowast;&lowast; ^NEWLINE^^DEBUGQUIT^Attempt to DIMension
    a variable with 0 or fewer elements , Line ^LINENO^ , Source ^SOURCENAME^</pre>

## READBLK

<a name="READBLK"/>

READBLK statement is used to read a block of data of a specified
length from a file opened for sequential processing and assign
it to a variable.

### COMMAND SYNTAX

    READBLK variable FROM file.variable, blocksize { THEN statements \
            [ ELSE statements ] | ELSE statements }

The READBLK statement reads a block of data beginning at the
current position in the file and continuing for blocksize bytes
and assigns it to variable. The current position is reset to just
beyond the last readable byte.

**file.variable** specifies a file previously opened for
sequential processing.

If the data can be read from the file, the THEN statements
are executed; any ELSE statements are ignored. If the file
is not readable or if the end of file is encountered, the ELSE
statements are executed and the THEN statements are ignored. If
the ELSE statements are executed, variable is set to an empty
string. If either file.variable or blocksize evaluates to null,
the READBLK statement fails and the program enters the debugger.

### INTERNATIONAL MODE

When using the READBLK statement in International Mode, care must
be taken to ensure that the input variable is handled properly
subsequent to the READBLK statement. The READBLK statement requires
that a "bytecount" be specified, however when manipulating variables
in International Mode character length rather than byte lengths are
usually used and hence possible confusion or program malfunction can
occur.

If requiring character data convert the input variable from
'binary/latin1' to UTF-8 byte sequence via the [UTF8](#UTF8)
function.

It is recommended that the [READBLK](#READBLK)/[WRITEBLK](#WRITEBLK)
statements not be used when executing in International Mode. Similar
functionality can be obtained via the
[READSEQ](#READSEQ)/[WRITESEQ](#WRITESEQ) statement, which can be
used to read/writecharacters a line at a time from a file.

### NOTE

A new line in UNIX files is one byte long, whereas in Windows NT it is
two bytes long. This means that for a file with newlines, the same
READBLK statement may return a different set of data depending on the
operating system the file is stored under.

The difference between the [READSEQ](#READSEQ) statement and the
READBLK statement is that the READBLK statement reads a block of
data of a specified length, whereas the READSEQ statement reads a
single line of data.

### EXAMPLE

       IF NOT( GETENV('TAFC_HOME', V.HOME) ) THEN
          CRT 'TAFC_HOME not defined'
          STOP
       END
       V.FILE.IN = 'RELEASE'
       V.FILE.INFO = DIR(V.HOME : '/' : V.FILE.IN)
       V.SIZE = V.FILE.INFO<1>
       OPENSEQ V.HOME, V.FILE.IN TO F.FILE.IN ELSE
          CRT 'Failed to open', V.FILE.IN
          STOP
       END
       V.BLK.SIZE = MINIMUM(V.SIZE :@FM: 512)
       READBLK V.TEXT FROM F.FILE.IN, V.BLK.SIZE ELSE
          CRT 'Failed to read', V.FILE.IN
          STOP
       END
       CRT V.TEXT[1, INDEX(V.TEXT, CHAR(10), 1)]   ;* 1st line, e.g.:
                                                   ;* jBase Release : R11.0.0.0

## READL

<a name="READL"/>

READL statement allows a process to read a record from a previously
opened file into a variable and takes a read-only shared lock on the
record. It respects all records locked with the [READU](#READU)
statement but allows other processes using READL to share the same
lock.

### COMMAND SYNTAX

    READL variable1 FROM {variable2,} expression { SETTING setvar }  \
          { ON ERROR statements } \
          { LOCKED statements } THEN | ELSE statements

### SYNTAX ELEMENTS

**variable1** is the identifier into which the record will be
read.

**variable2**, if specified, should be a jBC variable that has
previously been opened to a file using the OPEN statement if
variable2 is not specified then the default file is assumed.

The expression should evaluate to a valid record key for the file.

If the SETTING clause is specified and the read fails, setvar
will be set to one of the following values:

### INCREMENTAL FILE ERRORS

| Code  | Description                           |
|-------|---------------------------------------|
|128    |    No such file or directory          |
|4096   |    Network error                      |
|24576  |    Permission denied                  |
|32768  |    Physical I/O error or unknown error|


If ON ERROR is specified, the statements following the ON ERROR
clause will be executed for any of the above Incremental File
Errors except error 128.

### NOTES

READL takes a read-only shared record lock whereas [READU](#READU)
takes an exclusive lock. This means that any record, which is read
using READL, can also be read by another process using a READL.
In other words, the lock on the record is 'shared' in that no
[READU](#READU) lock against the same record can be taken.

Similarly, if [READU](#READU) takes a lock then READL will respect
that lock. By comparison, [READU](#READU) takes an exclusive lock
in that the one process retains control over the record.

The usage of READU is already well documented and understood. The
usage of READL allows for an application to present a record to one
or more users such that its integrity is ensured, i.e. the user(s)
viewing the record can be assured that wysiwyg and that no updates
to that record have been made whilst viewing the record.

While it is permissible to [WRITE](#WRITE) a record that has a READL
lock, the intent of READL is to permit a 'read-only' shared lock and
the act of WRITEing this record would not be considered good
programming practice.

READ takes no lock at all and does not respect any lock taken with
[READU](#READU) or READL. In other words, a READ can be performed at
any time and on any record regardless of any existing locks.

Due to limitations on Windows platforms, the READL statement behaves
the same as the READU statement, in other words they both take
exclusive locks.

If the record could not be read because another process already had a
[READU](#READU) lock on the record then one of two actions is taken.
If the LOCKED clause was specified in the statement then the
statements dependent on it are executed.

If no LOCKED clause was specified then the statement blocks (hangs)
until the other process releases the lock. The SYSTEM (43) function
can be used to determine which port has the lock.

If the statement fails to read the record then any statements
associated with the ELSE clause will be executed. If the statement
successfully reads the record then the statements associated with
any THEN clause are executed.

Either or both of THEN and ELSE clauses must be specified with the
statement.

The lock taken by the READL statement will be released by any of the
following events however, be aware that the record will not be fully
released until all shared locks have been released:

The same program with [WRITE](#WRITE), [WRITEV](#WRITEV) or
[MATWRITE](#MAXWRITE) statements writes to the record.

The same program with the DELETE statement deletes the record.

The record lock is released explicitly using the [RELEASE](#RELEASE)
statement.

The program stops normally or abnormally.

When a file is OPENed to a local file variable in a subroutine then
the file is closed when the subroutine RETURNS so all locks taken on
that file are released, including locks taken in a calling program.
Files that are opened to [COMMON](#COMMON) variables are not closed
so the locks remain intact.

### EXAMPLE

       OPEN 'F.TEMP' TO f_temp ELSE
          EXECUTE 'CREATE-FILE DATA F.TEMP 1 101 TYPE=J4'
          OPEN 'F.TEMP' TO f_temp ELSE
             CRT 'OPEN FAILED'
             STOP
          END
       END
       rec_id = 'REC1'
       READL record FROM f_temp, rec_id LOCKED
          CRT 'Lock failure'
          STOP
       END ELSE NULL
       CRT RECORDLOCKED(f_temp, rec_id)  ;* 2 under Windows, 1 under Unix


See also: [WRITE](#WRITE), [WRITEU](#WRITEU), [MATWRITE](#MATWRITE),
[MATWRITEU](#MATWRITEU), [RELEASE](#RELEASE), and [DELETE](#DELETE)

## READLIST

<a name="READLIST"/>

READLIST allows the program to retrieve a previously stored list
(perhaps created with the SAVE-LIST command), into a jBC variable.

### COMMAND SYNTAX

    READLIST variable1 FROM expression { SETTING variable2 } THEN | ELSE statements

### SYNTAX ELEMENTS

**variable1** is the variable into which the list will be read.

**expression** should evaluate to the name of a previously stored
list to retrieve. If specified, **variable2** will be set to the
number of elements in the list.

If the statement succeeds in retrieving the list, then the
statements associated with any THEN clause will be executed.
If the statement fails to find the list, then the statements
associated with any ELSE clause will be executed.

### NOTES

READLIST statement is identical in function to the
[GETLIST](#GETLIST) statement.

See also: [DELETELIST](#DELETELIST), [FORMLIST](#FORMLIST),
[WRITELIST](#WRITELIST)

### EXAMPLES

Find the list first

    READLIST MyList FROM "MyList" ELSE STOP
    LOOP
    * Loop until there are no more elements
    WHILE READNEXT Key FROM MyList DO
    ......
    REPEAT

## READNEXT

<a name="READNEXT"/>

READNEXT retrieves the next element in a list variable.

### COMMAND SYNTAX

    READNEXT variable1, variable2 { FROM variable3 } { SETTING setvar }  \
             { THEN | ELSE statements }

### SYNTAX ELEMENTS

**variable1** is the variable into which the next element of the
list will be read.

**variable2** is used when the list has been retrieved externally
from a [SSELECT](#SSELECT) or similar TAFC command that has used an
exploding sort directive. When specified, this variable will be set
to the multi-value reference of the current element. For example,
if the SSELECT used a BY-EXP directive on field 3 of the records in
a file, the list will contain each record key in the file as many
times as there are multi-values in the field. Each READNEXT instance
will set variable2 to the multi-value in field 3 to which the element
refers. This allows the multi-values in field 3 to be retrieved in
sorted order.

If variable3 is specified with the FROM clause, the READNEXT operates
on the list contained in variable3. If variable3 is not specified, the
default select list variable will be assumed.

If the SETTING clause is specified and the read (to build the next
portion of the list) fails, setvar will be set to one of the following
values:

### INCREMENTAL FILE ERRORS

| Code  | Description                           |
|-------|---------------------------------------|
|128    |    No such file or directory          |
|4096   |    Network error                      |
|24576  |    Permission denied                  |
|32768  |    Physical I/O error or unknown error|

### NOTES

READNEXT can be used as an expression returning a Boolean TRUE or
FALSE value. If an element is successfully read from the list, TRUE
is returned. If the list was empty, FALSE is returned.

See also: [SELECT](#SELECT), extensions for secondary indexes.

### EXAMPLE

       EXECUTE 'DELETE-FILE DATA F.TEMP'
       EXECUTE 'CREATE-FILE DATA F.TEMP 1 101 TYPE=J4'
       OPEN 'F.TEMP' TO F.TEMP ELSE ABORT 201, 'F.TEMP'
       V.REC.INIT = 'LINE 1' :@FM: 'LINE 2' :@FM: 'LINE 3'
       WRITE V.REC.INIT TO F.TEMP, 'REC1'
       WRITE V.REC.INIT TO F.TEMP, 'REC2'
       WRITE V.REC.INIT TO F.TEMP, 'REC3'
       CLOSE F.TEMP
       V.SEL = 'SSELECT F.TEMP TO 9'
       EXECUTE V.SEL
       READNEXT V.ID FROM 9 ELSE CRT 'READNEXT 1 FAILED'
       CRT 'NEXT:' : V.ID                                   ;* NEXT:REC1
       READNEXT V.ID FROM 9 ELSE CRT 'READNEXT 2 FAILED'
       CRT 'NEXT:' : V.ID                                   ;* NEXT:REC2

## READPREV

<a name="READPREV"/>

This statement is syntactically similar to the [READNEXT](#READNEXT)
but it works in reverse order. There are some considerations when
the direction is changed from forward search to backward search or
vice-versa.

When [SELECT](#SELECT) statement is first executed forward direction
is assumed. Therefore if [SELECT](#SELECT) is immediately followed by
READPREV, then a change of direction is assumed.

During the [READNEXT](#READNEXT) or READPREV sequence a next-key pointer
is kept up to date. This is the record or index key to be used, should
a [READNEXT](#READNEXT) be executed.

During a change of direction from forward [READNEXT](#READNEXT) to
backward [READPREV](#READPREV) then the next record key or index key
read in by the READPREV will be the one preceding the next-key pointer.

When the select list is exhausted it will either point one before the
start of the select list (if READPREVs have been executed) or one past
the end of the select list (if READNEXTs have been executed). Thus in
the event of a change of direction the very first or very last index
key or record key will be used.

Behaviour of READNEXT/READPREV depends on emulation. The following example is
for *jbase* emulation:

### EXAMPLE

Consider the following jBC code

        list = "DAVE" :@FM: "GREG" :@FM: "JIM"
        SELECT list

The following table shows what happens if you do [READNEXT](#READNEXT)s
and [READPREV](#READPREV)s on the above code and the reasons for it.

|Statements executed | Result of operation | Comments                   |
|--------------------|---------------------|----------------------------|
|READNEXT key ELSE   | key becomes "DAVE"  | key becomes "DAVE"         |
|READNEXT key ELSE   | key becomes "GREG"  | Second key in list         |
|READPREV key ELSE   | key becomes "DAVE"  | Reversed so take preceding |
|                    |                     | key                        |
|READPREV key ELSE   | Take ELSE clause    | The next key ptr exhausted |
|                    |                     | at start.                  |
|READNEXT key ELSE   | key becomes "DAVE"  | First key in list          |
|READNEXT key ELSE   | key becomes "GREG"  | Second key in list         |
|READNEXT key ELSE   | key becomes "JIM"   | Final key. Next key ptr    |
|                    |                     | exhausted.                 |
|READPREV key ELSE   | key becomes "JIM"   | Reversed but list          |
|                    |                     | exhausted.                 |
|READPREV key ELSE   | key becomes "GREG"  | Second key in list         |
|READPREV key ELSE   | key becomes "DAVE"  | First key in list          |

### EXAMPLE 2

This code shows the behaviour of READNEXT/READPREV under *prime* emulation.
The difference to the example above starts with the first READPREV:

       list = "DAVE" :@FM: "GREG" :@FM: "JIM"
       SELECT list
       READNEXT V.ID ELSE CRT 'READNEXT 1 FAILED'
       CRT 'NEXT:' : V.ID                              ;*  NEXT:DAVE
       READNEXT V.ID ELSE CRT 'READNEXT 2 FAILED'
       CRT 'NEXT:' : V.ID                              ;*  NEXT:GREG
       READPREV V.ID ELSE CRT 'READPREV 1 FAILED'
       CRT 'PREVIOUS:' : V.ID                          ;*  PREVIOUS:JIM
       READPREV V.ID ELSE CRT 'READPREV 2 FAILED'      ;*  READPREV 2 FAILED
       CRT 'PREVIOUS:' : V.ID                          ;*  PREVIOUS:
       READNEXT V.ID ELSE CRT 'READNEXT 3 FAILED'      ;*  READNEXT 3 FAILED
       CRT 'NEXT:' : V.ID                              ;*  NEXT:


## READSELECT##

See also: [READLIST](#READLIST)

## READSEQ

<a name="READSEQ"/>

READSEQ reads data from a file opened for sequential access.

### COMMAND SYNTAX

    READSEQ Variable FROM FileVar THEN | ELSE statements

### SYNTAX ELEMENTS

**Variable** specifies the variable to contain next record from sequential
file.

**FileVar** specifies the file descriptor of the file opened for sequential
access.

**Statements** are Conditional jBC statements.

### NOTES

Each READSEQ reads a line of data from the sequentially opened file. After
each READSEQ, the file pointer moves forward to the next line of data. The
variable contains the line of data less the new line character from the
sequential file.

The default buffer size for a READSEQ is 1024 bytes. This can be changed
using the IOCTL () function with the JIOCTL_COMMAND_SEQ_CHANGE_RECORDSIZE
Sequential File Extensions.

### EXAMPLE

### Step 1. Create a text file with long lines (1100 bytes each):

       OPENSEQ '.', 'test.txt' TO F.OUT.FILE THEN
          WEOFSEQ F.OUT.FILE
       END ELSE
          CREATE F.OUT.FILE ELSE
             CRT 'FILE CREATION ERROR'
             STOP
          END
       END
    * Create a ruler-like output
       V.LINE = ''
       FOR V.I = 1 TO 1100 STEP 10
          V.J = V.I + 9
          V.LINE := STR('-', 10 - LEN(V.J)) : V.J
       NEXT V.I
    * Now write it
       FOR V.I = 1 TO 10
          WRITESEQ V.LINE TO F.OUT.FILE ELSE
             CRT 'FILE WRITE ERROR'
             STOP
          END
       NEXT V.I

Line ends in this file are shown here (JED, Ctrl-E to go to line end):

<pre>
    0001 ------1050------1060------1070------1080------1090------1100
    0002 ------1050------1060------1070------1080------1090------1100
    0003 ------1050------1060------1070------1080------1090------1100
    0004 ------1050------1060------1070------1080------1090------1100
    0005 ------1050------1060------1070------1080------1090------1100
    0006 ------1050------1060------1070------1080------1090------1100
    0007 ------1050------1060------1070------1080------1090------1100
    0008 ------1050------1060------1070------1080------1090------1100
    0009 ------1050------1060------1070------1080------1090------1100
    0010 ------1050------1060------1070------1080------1090------1100
    -------------------------------- End Of Record --------------------------------</pre>

### Step 2. Read a line from this text file using plain READSEQ:

       OPENSEQ '.', 'test.txt' TO F.IN.FILE THEN
          NULL
       END ELSE
          CRT 'ERROR OPENING FILE'
          STOP
       END
       READSEQ V.LINE FROM F.IN.FILE ELSE
          CRT 'ERROR READING FILE'
          STOP
       END
       CRT LEN(V.LINE)                      ;*  1024
       CRT V.LINE[-20,20]                   ;*  --1010------1020----

### Step 3. Read a line from this text file using IOCTL() first:

    INCLUDE JBC.h
       OPENSEQ '.', 'test.txt' TO F.IN.FILE THEN
          NULL
       END ELSE
          CRT 'ERROR OPENING FILE'
          STOP
       END
       IF IOCTL(F.IN.FILE, JIOCTL_COMMAND_SEQ_CHANGE_RECORDSIZE, 2048) THEN
          NULL
       END ELSE
          CRT 'IOCTL FAILED !!!'
          STOP
       END
       READSEQ V.LINE FROM F.IN.FILE ELSE
          CRT 'ERROR READING FILE'
          STOP
       END
       CRT LEN(V.LINE)                      ;*  1100
       CRT V.LINE[-20,20]                   ;*  ------1090------1100

### Step 3 (alternate). Use subsequent READSEQs to read that file:

       OPENSEQ '.', 'test.txt' TO F.IN.FILE THEN
          NULL
       END ELSE
          CRT 'ERROR OPENING FILE'
          STOP
       END
       V.EOF = ''
       LOOP
          V.LINE = ''
          LOOP
             READSEQ V.CHUNK FROM F.IN.FILE ELSE
                V.EOF = 1
                BREAK
             END
             V.LEN = BYTELEN(V.CHUNK)
             V.LINE := V.CHUNK
             IF V.LEN LT 1024 THEN BREAK
          REPEAT
    * Line processing goes here
          IF V.EOF THEN BREAK
          CRT LEN(V.LINE)                      ;*  1100
          CRT V.LINE[-20,20]                   ;*  ------1090------1100
       REPEAT

## READT

<a name="READT"/>

READT statement is used to read a range of tape devices 0-9.

### COMMAND SYNTAX

    READT variable { FROM expression } THEN | ELSE statements

### SYNTAX ELEMENTS

**variable** is the variable that will receive any data read from the
tape device.

**expression** should evaluate to an integer value in the range 0-9 and
specifies from which tape channel to read data. If the FROM clause is
not specified the READT will assume channel 0.

If the READT fails then the statements associated with any ELSE clause
will be executed. SYSTEM (0) will return the reason for the failure as
follows:

| Code | Description                                |
|------|--------------------------------------------|
|1     | There is no media attached to the channel. |
|2     | An end of file mark was found.             |

### NOTES

A "tape" does not only refer to magnetic tape devices, but also any
device that has been described to TAFC. Writing device descriptors for
jBASE is beyond the scope of this manual.

If no tape device has been assigned to the specified channel the TAFC
debugger is entered with an appropriate message.

Each instance of the READT statement will read the next record
available on the device. The record size is not limited to a single
tape block and the entire record will be returned whatever block size
has been allocated by the T-ATT command.

### EXAMPLE

    LOOP
    	  READT TapeRec FROM 5 ELSE
        	  Reason = SYSTEM(0)
        	  IF Reason = 2 THEN BREAK ;* done
        	  CRT "ERROR"  ;  STOP
    	  END
    REPEAT

## READU

<a name="READU"/>

READU statement allows a program to read a record from previously
opened file into variable. It respects record locking and locks the
specified record for update.

### COMMAND SYNTAX

    READU variable1 FROM {variable2,} expression { SETTING setvar }  \
          { WAIT timeout } { ON ERROR statements } { LOCKED statements }  \
          THEN | ELSE statements

### SYNTAX ELEMENTS

**variable1** is the identifier into which the record will be read.

**variable2** if specified, should be a jBC variable that has
previously been opened to a file using the OPEN statement. If
variable2 is not specified then the default file is assumed.

The **expression** should evaluate to a valid record key for the
file.

If the **SETTING** clause is specified and the read fails, setvar
will be set to one of the following values:

### INCREMENTAL FILE ERRORS

| Code  | Description                           |
|-------|---------------------------------------|
|128    |    No such file or directory          |
|4096   |    Network error                      |
|24576  |    Permission denied                  |
|32768  |    Physical I/O error or unknown error|

If WAIT clause is specified and the record stated in Variable1 is
already locked, READU waits 'timeout' milliseconds before executing
LOCKED statement. If LOCKED clause is not specified WAIT clause does
not effect to the READU behaviour. Without LOCKED clause READU is
blocked until the lock is released regardless to the WAIT clause
parameter.

If ON ERROR is specified, the statements following the ON ERROR
clause will be executed for any of the above Incremental File Errors
except error 128.

### NOTES

If the record could not be read because another process already had a
lock on the record then one of two actions is taken. If the LOCKED
clause was specified in the statement then the statements dependent
on it are executed. If no LOCKED clause was specified then the
statement
blocks (hangs) until the other process releases the lock. Use the
SYSTEM (43) function to determine which port has the lock.

If the statement fails to read the record then any statements associated
with the ELSE clause will be executed. If the statement successfully
reads the record then the statements associated with any THEN clause are
executed. Either or both of THEN and ELSE clauses must be specified with
the statement.

The lock taken by the READU statement will be released by any of the
following events:

The same program with [WRITE](#WRITE), [WRITEV](#WRITEV) or
[MATWRITE](#MATWRITE) statements writes to the record.

The same program with the DELETE statement deletes the record.

The record lock is released explicitly using the [RELEASE](#RELEASE)
statement.

The program stops normally or abnormally.

When a file is OPENed to a local file variable in a subroutine then the
file is closed when the subroutine RETURNS so all locks taken on that
file are released, including locks taken in a calling program. Files that
are opened to [COMMON](#COMMON) variables are not closed so the locks
remain intact.

See also: [WRITE](#WRITE), [WRITEU](#WRITEU), [MATWRITE](#MATWRITE),
[MATWRITEU](#MATWRITEU), [RELEASE](#RELEASE), and [DELETE](#DELETE)

### EXAMPLE

       OPEN 'F.TEMP' TO F.TEMP ELSE
          EXECUTE 'CREATE-FILE DATA F.TEMP 1 101 TYPE=J4'
          OPEN 'F.TEMP' TO F.TEMP ELSE
             CRT 'OPEN FAILED'
             STOP
          END
       END
       READU V.REC FROM F.TEMP, 'REC1' LOCKED
          CRT 'Lock failure'
          STOP
       END ELSE NULL
       V.REC<-1> = 'A field'
       WRITE V.REC TO F.TEMP, 'REC1'

## READV

<a name="READV"/>

READV statement allows a program to read a specific field from a
record in a previously opened file into a variable.

### COMMAND SYNTAX

    READV variable1 FROM { variable2,} expression1, expression2 { SETTING setvar }  \
         { ON ERROR statements } THEN | ELSE statements

### SYNTAX ELEMENTS

**variable1** is the identifier into which the record will be read.

**variable2** if specified, should be a jBC variable that has
previously been opened to a file using the OPEN statement. If
variable2 is not specified, the default file is assumed.

**expression1** should evaluate to a valid record key for the
file.

**expression2** should evaluate to a positive integer. If the
number is invalid or greater than the number of fields in the
record, a NULL string will be assigned to variable1. If the
number is 0, then the readv0 emulation setting controls the
value returned in variable1. If a non-numeric argument is
evaluated, a run time error will occur.

If the SETTING clause is specified and the read fails, setvar
will be set to one of the following values:

### INCREMENTAL FILE ERRORS

| Code  | Description                           |
|-------|---------------------------------------|
|128    |    No such file or directory          |
|4096   |    Network error                      |
|24576  |    Permission denied                  |
|32768  |    Physical I/O error or unknown error|

If ON ERROR is specified, the statements following the ON ERROR
clause will be executed for any of the above Incremental File
Errors except error 128.

### NOTES

If you wish to set a lock on a record, do so explicitly with the
[READU](#READU) or [READVU](#READVU) statement. To read a field
from a previously opened file into a variable and take a read-only
shared lock on the field, use [READVL](#READVL).

### EXAMPLE

       OPEN 'F.TEMP' TO f_temp THEN
          ret_error = ''
          CLEARFILE f_temp SETTING ret_error
          IF ret_error NE '' THEN
             CRT 'ERROR ' : ret_error
             STOP
          END
       END ELSE
          EXECUTE 'CREATE-FILE DATA F.TEMP 1 101 TYPE=J4'
          OPEN 'F.TEMP' TO f_temp ELSE ABORT 201, 'F.TEMP'
       END
       *
       out_record = 'Field 1' :@FM: 'Field 2' :@FM: 'Field 3'
       WRITE out_record TO f_temp, 'REC1'
       *
       READV second_field FROM f_temp, 'REC1', 2 ELSE
          CRT 'Read error'
          STOP
       END
       *
       CRT second_field           ;*  Field 2

## READVL

<a name="READVL"/>

READVL statement is used to acquire a shared record lock and then
read a field from the record.

The READVL statement conforms to all the specifications of the
[READL](#READL) and [READV](#READV) statements.

## READVU

<a name="READVU"/>

READVU statement allows a program to read a specific field in a
record in a previously opened file into a variable. It also respects
record locking and locks the specified record for update.

### COMMAND SYNTAX

    READVU variable1 FROM {variable2,} expression1, expression2 { SETTING setvar }  \
           { ON ERROR statements } { LOCKED statements } THEN | ELSE statements

### SYNTAX ELEMENTS

**variable1** is the identifier into which the record will be
read.

**variable2** if specified, should be a jBC variable that has
previously been opened to a file using the OPEN statement. If
variable2 is not specified then the default file is assumed.

**expression1** should evaluate to a valid record key for the file.

**expression2** should evaluate to a positive integer number. If
the number is invalid or greater than the number of fields in the
record, then a NULL string will be assigned to variable1. If the
number is 0, then the readv0 emulation setting controls the value
returned in variable1. If a non-numeric argument is evaluated a run
time error will occur.

If the SETTING clause is specified and the read fails, setvar will
be set to one of the following values:

### INCREMENTAL FILE ERRORS

| Code  | Description                           |
|-------|---------------------------------------|
|128    |    No such file or directory          |
|4096   |    Network error                      |
|24576  |    Permission denied                  |
|32768  |    Physical I/O error or unknown error|

If ON ERROR is specified, the statements following the ON ERROR clause
will be executed for any of the above Incremental File Errors except
error 128.

### NOTES

If the record could not be read because another process already had a
lock on the record then one of two actions is taken. If the LOCKED clause
was specified in the statement then the statements dependent on it are
executed. If no LOCKED clause was specified then the statement blocks
(hangs) until the other process releases the lock.

If the statement fails to read the record then any statements associated
with the ELSE clause are executed. If the statement successfully reads the
record then the statements associated with any THEN clause are executed.
Either or both of the THEN and ELSE clauses must be specified with the
statement.

The lock taken by the [READVU](#READVU) statement will be released by any
of the following events:

The same program with [WRITE](#WRITE), [WRITEV](#WRITEV),
[MATWRITE](#MATWRITE) or [DELETE](#DELETE) statements writes to the
record.

The record lock is released explicitly using the [RELEASE](#RELEASE)
statement.

The program stops normally or abnormally.

When a file is OPENed to a local file variable in a subroutine then the
file is closed when the subroutine RETURNS so all locks taken on that
file are released, including locks taken in a calling program. Files
that are opened to [COMMON](#COMMON) variables are not closed so the
locks remain intact.

See also: [WRITE](#WRITE), [WRITEU](#WRITEU), [MATWRITE](#MATWRITE),
[MATWRITEU](#MATWRITEU), [RELEASE](#RELEASE), and [DELETE](#DELETE)

### EXAMPLE

    OPEN "Customers" ELSE ABORT 201, "Customers"
    OPEN "DICT Customers" TO DCusts ELSE
    	    ABORT 201, "DICT Customers"
    END
    LOOP
    	    READVU Rec FROM DCusts, "Xref",7 LOCKED
        	  CRT "Locked - retrying"
        	  SLEEP 1; CONTINUE ;* Restart LOOP
    	    END THEN
            READ DataRec FROM Rec ELSE
                ABORT 202, Rec
           END
           BREAK ;*leave the LOOP
       END ELSE
           ABORT 202, "Xref"
       END
    REPEAT

## READXML

<a name="READXML"/>

READXML rec FROM file, id ELSE STOP 202,id

Reads a record from a file using the style sheet held in
DICT->@READXML to transform the data into xml format

### EXAMPLE

       READ rec FROM file,id THEN
          CRT rec
       END
       READXML xml FROM file,id THEN
          CRT xml
       END

Screen output:

<pre>
    CLIVE^PIPENSLIPPERS^999 LETSBE AVENUE
    ...
    &lt;?xml version="1.0" encoding="UTF-8"?&gt;
    &lt;mycustomer&gt;
    &lt;firstname&gt;CLIVE&lt;/firstname&gt;
    &lt;lastname&gt;PIPENSLIPPERS&lt;/lastname&gt;
    &lt;address&gt;999 LETSBE AVENUE&lt;/address&gt;</pre>

## RECORDLOCKED

<a name="RECORDLOCKED"/>

RECORDLOCKED function is called to ascertain the status of a record
lock.

### COMMAND SYNTAX

    RECORDLOCKED(filevar, recordkey)

### SYNTAX ELEMENTS

**filevar** is a file variable from a previously executed OPEN
statement.

**recordkey** is an expression for the record id that will be
checked.

### NOTES

RECORDLOCKED returns an integer value to indicate the record lock
status of the specified record id.

| Code | Description                               |
|------|-------------------------------------------|
|3     |  Locked by this process by a FILELOCK     |
|2     |  Locked by this process by a READU        |
|1     |  Locked by this process by a READL        |
|0     |  Not locked                               |
|-1    |  Locked by another process by a READL     |
|-2    |  Locked by another process by a READU     |
|-3    |  Locked by another process by a FILELOCK  |

If the return value is negative, then the SYSTEM(43) and STATUS function
calls can be used to determine the port number of the program that holds
the lock. If -1 is returned, more than 1 port could hold the lock and so
the port number returned will be the first port number found.

### EXAMPLE

Run this program from one session, wait for "RECORD LOCKED. PRESS ANY KEY TO WRITE"
message, then run it in another session:

       OPEN 'F.TEMP' TO F.TEMP ELSE
          EXECUTE 'CREATE-FILE DATA F.TEMP 1 101 TYPE=J4'
          OPEN 'F.TEMP' TO F.TEMP ELSE
             CRT 'OPEN FAILED'
             STOP
          END
       END
       READU V.REC FROM F.TEMP, 'REC1' LOCKED
          CRT 'Lock failure (' : RECORDLOCKED(F.TEMP, 'REC1') : ')'
          STOP
       END ELSE NULL
       PROMPT 'RECORD LOCKED. PRESS ANY KEY TO WRITE'
       INPUT DUMMY
       V.REC<-1> = 'A field'
       WRITE V.REC TO F.TEMP, 'REC1'

## REGEXP

<a name="REGEXP"/>

REGEXP function is a powerful function that allows pattern matching
using UNIX regular expressions. REGEXP is not supported on Windows.

### COMMAND SYNTAX

    REGEXP(variable, expression)

### SYNTAX ELEMENTS

**variable** can be any type of jBC variable and is the variable upon
which pattern matching will be performed.

**expression** should evaluate to a standard UNIX regular expression
as defined in the UNIX documentation.

### NOTES

The function returns a numeric integer value being the first character
in variable that matches the specified regular expression. If
a match is not found then the function returns 0. If the regular expression
was invalid then the function returns -1.

### EXAMPLES

       String = "jBASE Software Inc."    ;* 4 (position of matching pattern -
       CRT REGEXP(String, 'S[^t]*')      ;*   "S" followed by "t" later on)
    * find an exact value in a list
       CRT REGEXP('051', '^(050|5001|051|053|265|4007|5007|037|060|098)$')   ;* 1
       CRT REGEXP('05123', '^(050|5001|051|053|265|4007|5007|037|060|098)$') ;* 0
    * everything in range "000" - "999" except "037"
       CRT REGEXP('036', '(0[0-24-9][0-9]|0[0-9][0-68-9]|[1-9][0-9][0-9])')  ;* 1
       CRT REGEXP('037', '(0[0-24-9][0-9]|0[0-9][0-68-9]|[1-9][0-9][0-9])')  ;* 0
       CRT REGEXP('137', '(0[0-24-9][0-9]|0[0-9][0-68-9]|[1-9][0-9][0-9])')  ;* 1
    * everything in range "000" - "999" except "037" and "057"
       CRT REGEXP('036', '(0[0-246-9][0-9]|0[0-9][0-68-9]|[1-9][0-9][0-9])') ;* 1
       CRT REGEXP('037', '(0[0-246-9][0-9]|0[0-9][0-68-9]|[1-9][0-9][0-9])') ;* 0
       CRT REGEXP('057', '(0[0-246-9][0-9]|0[0-9][0-68-9]|[1-9][0-9][0-9])') ;* 0
       CRT REGEXP('957', '(0[0-246-9][0-9]|0[0-9][0-68-9]|[1-9][0-9][0-9])') ;* 1
    * all 2-character country codes except "RS"
       CRT REGEXP('RS', '([A-QS-Z][A-Z]|[R][A-RT-Z])')                       ;* 0
       CRT REGEXP('AE', '([A-QS-Z][A-Z]|[R][A-RT-Z])')                       ;* 1
       CRT REGEXP('RU', '([A-QS-Z][A-Z]|[R][A-RT-Z])')                       ;* 1
    * negative lookahead assertion isn't supported ("all not containing 'bar'")
       CRT REGEXP('bar', '"^(?!.*?bar).*"')                                 ;* -1

## RELEASE

<a name="RELEASE"/>

RELEASE statement enables a program to explicitly release record locks
without updating the records using [WRITE](#WRITE).

### COMMAND SYNTAX

    RELEASE {{variable,} expression}

### SYNTAX ELEMENTS

If variable is specified it should be a valid file descriptor variable
(i.e. It should have been the subject of an [OPEN](#OPEN) statement)

If an expression is supplied it should evaluate to the record key of a
record whose lock the program wishes to free. If variable was specified
the record lock in the file described by it is released. If variable was
not specified the record lock in it releases the file described by the
default file variable

If RELEASE is issued without arguments then all record locks in all files
that were set by the current program will be released.

### NOTES

Where possible the program should avoid the use of RELEASE without
arguments; this is less efficient and can be dangerous - especially
in subroutines.

### EXAMPLE

This program optionally creates file F.TEMP and writes to it a record REC1, on the following
runs it updates that record - puts a new field in it, but only if theres less than 7 fields:

       OPEN 'F.TEMP' TO F.TEMP ELSE
          EXECUTE 'CREATE-FILE DATA F.TEMP 1 101 TYPE=J4'
          OPEN 'F.TEMP' TO F.TEMP ELSE
             CRT 'OPEN FAILED'
             STOP
          END
       END
       READU V.REC FROM F.TEMP, 'REC1' LOCKED
          CRT 'Record locked (' : RECORDLOCKED(F.TEMP, 'REC1') : ')'
          STOP
       END ELSE NULL
       IF DCOUNT(V.REC, @FM) GT 5 THEN RELEASE F.TEMP, 'REC1'
       ELSE
          V.REC<-1> = 'A field'
          WRITE V.REC TO F.TEMP, 'REC1'
       END

## REMOVE##

REMOVE will successively extract delimited strings from a dynamic
array.

### COMMAND SYNTAX

    REMOVE variable FROM array SETTING setvar

### SYNTAX ELEMENTS

**variable** is the variable, which is to receive the extracted string.

**array** is the dynamic array from which the string is to be extracted.

**setvar** is set by the system during the extraction to indicate the
type of delimiter found:

|Code|  Description       | Notes           |
|----|--------------------|-----------------|
|0   |  end of the array  |                 |
|1   |  xFF ASCII 255     |                 |
|2   |  xFE ASCII 254     | Field marker    |
|3   |  xFD ASCII 253     | Value marker    |
|4   |  xFC ASCII 252     | Subvalue marker |
|5   |  xFB ASCII 251     |                 |
|6   |  xFA ASCII 250     |                 |

### NOTES

The first time the REMOVE statement is used with a particular array,
it will extract the first delimited string it and set the special
"remove pointer" to the start of the next string (if any). The next
time REMOVE is used on the same array, the pointer will be used to
retrieve the next string and so on. The array is not altered.

The variable named in the SETTING clause is used to record the type of
delimiter that was found - so that you can tell whether the REMOVE
statement
 extracted a field, a value or a subvalue for example. Delimiters are
defined as characters between xF9 and xFF only. Once the end of the
array has been reached, the string variable will not be updated and
the SETTING clause will always return 0. You can reset the "remove
pointer" by assigning the variable to itself - for example REC = REC.

### EXAMPLE

       REC = "Field 1" :@FM: "Field 2" :@SM: " Sub-value" :@VM: "Value"
       REMOVE EXSTRING FROM REC SETTING V.STATUS  ; CRT V.STATUS         ;*  2
       REMOVE EXSTRING FROM REC SETTING V.STATUS  ; CRT V.STATUS         ;*  4
       REMOVE EXSTRING FROM REC SETTING V.STATUS  ; CRT V.STATUS         ;*  3
       REMOVE EXSTRING FROM REC SETTING V.STATUS  ; CRT V.STATUS         ;*  0
       REC = REC                   ;* reset "remove pointer"
       REMOVE EXSTRING FROM REC SETTING V.STATUS  ; CRT V.STATUS         ;*  2

## REPLACE

REPLACE is an obsolete way to assign to dynamic arrays via a function.

### COMMAND SYNTAX

    REPLACE(var, expression1{, expression2{, expression3}}; expression4)

### SYNTAX ELEMENTS

**var** is the dynamic array that the REPLACE function will use to assign
new values; remains unchanged.

**expression1** specifies into which field assignment will be made and
should evaluate to a numeric.

**expression2** specifies into which value assignment is to be
done and should evaluate to a numeric.

**expression3** specifies into which sub-value assignment is to be
done and should evaluate to a numeric.

**expression4** can evaluate to any data type and is the actual data
that will be assigned to the array.

### NOTES

The function returns a copy of var with the specified replacement
carried out. This value may be assigned to the original var in which
case the jBC compiler will optimize the assignment.

### EXAMPLE

       X = "jBASE" :@VM: "is" :@VM: "great" :@FM: '!'
       Y = REPLACE(X, 1, 2; 'is really')
       CRT FMT(X, 'MCP')                    ;*  jBASE]is]great^!
       CRT FMT(Y, 'MCP')                    ;*  jBASE]is really]great^!

## RETURN

<a name="RETURN"/>

RETURN statement transfers program execution to the caller of a
subroutine/function or to a specific label in the program.

### COMMAND SYNTAX

    RETURN {TO label}

or

    RETURN(expression)

### SYNTAX ELEMENTS

**label** must reference an existing label within the source of the
program.

**expression** evaluates to the value that is returned by a
user-written function.

### NOTES

The RETURN statement will transfer program execution to the statement
after the [GOSUB](#GOSUB) that called the current internal subroutine.

If the [RETURN](#RETURN) statement is executed in an external SUBROUTINE
and there are no outstanding GOSUBs, then the program will transfer
execution back to the program that called it via CALL.

The program will enter the debugger with an appropriate message should a
RETURN be executed with no GOSUB or [CALL](#CALL) outstanding.

The second form of the RETURN statement is used to return a value from a
user-written function. This form can only be used in a user-written
function.

## REWIND

<a name="REWIND"/>

REWIND statement issueS a rewind command to the device attached to the
specified channel.

### COMMAND SYNTAX

    REWIND { ON expression } THEN | ELSE statements

### SYNTAX ELEMENTS

**expression**, if specified, should evaluate to an integer in the range
0 to 9. Default is 0.

### NOTES

If the statement fails to issue the rewind then any statements
associated with the ELSE clause are executed. If the statement
successfully issues the rewind command then the statements associated
with any THEN clause are executed. Either or both of the THEN and ELSE
clauses must be specified with the statement.

If the statement fails then the reason for failure can be determined
via the value of SYSTEM(0) as follows:

| Code | Description                               |
|------|-------------------------------------------|
|1     | There is no media attached to the channel |
|2     | There is an end for file mark             |

## RIGHT

<a name="RIGHT"/>

RIGHT function returns a sub-string composed of the last n characters
of a specified string.

### COMMAND SYNTAX

    RIGHT(expression, length)

### SYNTAX ELEMENTS

**expression** evaluates to the string from, which the sub string is
extracted.

**length** is the number of characters that are extracted. If length is
less than 1, RIGHT () returns null.

### NOTES

The RIGHT () function is equivalent to sub-string extraction for the
last n characters, i.e. expression[n]

See also: [LEFT](#LEFT)

### EXAMPLE

    S = "The world is my lobster"

    CRT DQUOTE( RIGHT(S,7))
    CRT DQUOTE( RIGHT(S,99) )
    CRT DQUOTE( RIGHT(S,0) )

This code displays:

<pre>
    "lobster"
    "The world is my lobster"
    ""</pre>

## RND

RND function allows the generation of random numbers by a program.

### COMMAND SYNTAX

    RND(expression)

### SYNTAX ELEMENTS

**expression** should evaluate to a numeric integer value or a runtime
error will occur. The absolute value of expression is used by the
function. The highest number expression can be on Windows is
PWR(2,15) - 1. The highest number on UNIX is PWR(2,31) - 1.

### NOTES

The function will return a random integer number between 0 and the value
of expression-1.

See also: [ABS](#ABS)

### EXAMPLE

    FOR I=1 TO 20
       CRT RND(100) : ", " :
    NEXT I

prints 20 random numbers in the inclusive range 0 to 99.

## RQM

RQM is synonymous with [SLEEP](#SLEEP).

## RTNDATA

RTNDATA statement allows a jBC program to return specific data to the
RTNDATA clause of another program's [EXECUTE](#EXECUTE) statement.

### COMMAND SYNTAX

    RTNDATA expression

### SYNTAX ELEMENTS

**expression** may evaluate to any data type.

### NOTES

When a jBC program executes another jBC program using the EXECUTE
statement it may specify a variable to pick up data in using the
RTNDATA clause. The data picked up will be that specified by the
executed program using the RTNDATA statement.

The data will be discarded if the program is not executed by an
[EXECUTE](#EXECUTE) statement in another program.

## SADD

SADD function performs string addition of two base 10-string numbers.

### COMMAND SYNTAX

    SADD(expr1, expr2)

### SYNTAX ELEMENTS

**expr1** and **expr2** are strings consisting of numeric characters,
optionally including a decimal part.

### NOTES

The SADD function can be used with numbers that may exceed a valid
range with standard arithmetic operators.
The [PRECISION](#PRECISION) declaration has no effect on the value
returned by SADD.

### EXAMPLE

    A = 4000000000000000000000000000000
    B = 7
    CRT SADD(A,B)

Displays 4000000000000000000000000000007 to the screen

    CRT SADD(4.33333333333333333,1.8)

Displays 6.13333333333333333 to the screen

## SDIV

SDIV function performs a string division of two base 10-string numbers
and rounds the result to 14 decimal places.

### COMMAND SYNTAX

    SDIV(expr1, expr2)

### SYNTAX ELEMENTS

**expr1** and **expr2** are strings consisting of numeric characters,
with either optionally including a decimal part.

### NOTES

Use the SDIV function with numbers that may exceed a valid range with
standard arithmetic operators.

The [PRECISION](#PRECISION) declaration has no effect on the value
returned by SDIV.

### EXAMPLE

    A = 2
    B = 3
    CRT SDIV(A,B)

Displays 0.66666666666666 to the screen

    CRT SDIV(355,113)

Displays 3.14159292035398 to the screen

## SEEK

SEEK statement is used to move the file pointer by an offset specified
in bytes, relative to the current position, the beginning of the file,
or the end of the file.

### COMMAND SYNTAX

    SEEK file.variable [ , offset [ , relto] ] { THEN statements  \
       [ ELSE statements ] | ELSE statements }

### SYNTAX ELEMENTS

**file.variable** specifies a file previously opened for sequential
access.

**offset** is the number of bytes before or after the reference
position. A negative offset results in the pointer being moved
before the position specified by relto. If offset is not
specified, 0 is assumed.

The permissible values of relto and their meanings follow:

| Value | Description                           |
|-------|---------------------------------------|
|0      | Relative to the beginning of the file |
|1      | Relative to the current position      |
|2      | Relative to the end of the file       |

If relto is not specified, 0 is assumed.

If the pointer is moved, the THEN statements are executed and the
ELSE statements are ignored. If the THEN statements are not
specified, program execution continues with the next statement.

If the file cannot be accessed or does not exist the ELSE
statements are executed; any THEN statements are ignored.

If file.variable, offset, or relto evaluates to null, the SEEK
statement fails and the program terminates with a run-time error
message.

### NOTES

In Windows-based systems, line endings in files are denoted by the
character sequence RETURN + LINEFEED rather than the single
LINEFEED used in UNIX files. The value of offset should take into
account this extra byte on each line in Windows NT file systems.

If you use the [OPENDEV](#OPENDEV) statement to open a
tape device for sequential processing, you
can move the file pointer only to the beginning or the end of the
data.

Seeking beyond the end of the file and then writing creates a gap,
or hole, in the file. This hole occupies no physical space, and
reads from this part of the file return as ASCII CHAR 0 (neither
the number nor the character 0).

For more information about sequential file processing, See also:
[OPENSEQ](#OPENSEQ), [READSEQ](#READSEQ), and
[WRITESEQ](#WRITESEQ) statements.

### EXAMPLE

       V.DIR.OUT = '.'  ;   V.FILE.OUT = 'report.txt'
       OPENSEQ V.DIR.OUT, V.FILE.OUT TO F.FILE.OUT THEN
          WEOFSEQ F.FILE.OUT
       END ELSE
          CREATE F.FILE.OUT ELSE CRT 'File create error'  ;  STOP
       END
       WRITESEQ '1234567890ABCDEF' TO F.FILE.OUT ELSE
          CRT 'Write error'
          STOP
       END
    * go right after position 5 from the beginning
       SEEK F.FILE.OUT, 5, 0 ELSE CRT 'Seek error'  ;  STOP
       READSEQ V.STRING FROM F.FILE.OUT ELSE CRT 'Read error'  ;  STOP
       CRT V.STRING                 ;* 67890ABCDEF
    * go beyond end of file and write something there
       SEEK F.FILE.OUT, 3, 2 ELSE CRT 'Seek error'  ;  STOP
       WRITESEQ 'VWXYZ' TO F.FILE.OUT ELSE CRT 'Write error'  ;  STOP
       CLOSESEQ F.FILE.OUT
    * read full file contents
       OSREAD V.ALL FROM V.FILE.OUT ELSE CRT 'Read error'  ;  STOP
       CRT FMT( FMT( OCONV(V.ALL, 'MX'), '2L'), 'MCP ')
    * 31 32 33 34 35 36 37 38 39 30 41 42 43 44 45 46 FE 00 00 00 56 57 58 59 5A

## SELECT

<a name="SELECT"/>

SELECT statement creates a select list of elements in a specified
variable.

### COMMAND SYNTAX

    SELECT {variable1} { TO variable2 | listnum } { SETTING setvar }

### SYNTAX ELEMENTS

**variable1** can be an OPENed file descriptor, in which case the
record keys in the specified file will be selected, or an ordinary
variable in which case each field in the variable will become a list
element. variable1 may also be an existing list in which case the
elements in the list will be selected.

If **variable1** is not specified in the statement then it assumes
the default file variable.

If **variable2** is specified then the newly created list will be
placed in the variable. Alternatively, specify a select list number
in the range 0 to 10 with listnum. If neither variable2 nor listnum
is specified then it assumes the default list variable.

If specifying the SETTING clause and the select fails, it sets setvar
to one of the following values:

| Code  | Description                           |
|-------|---------------------------------------|
|128    |    No such file or directory          |
|4096   |    Network error                      |
|24576  |    Permission denied                  |
|32768  |    Physical I/O error or unknown error|

### NOTES

When constructing a list from record keys in a file, it does so by
extracting only the first few keys, which when removed from the list
obtains the next few keys and so on. Therefore, the creation of the
list is not immediate. This means that the list could contain records,
written to the file after starting the SELECT command.

Consider the situation where you open a file, SELECT it and then,
because of the keys obtained, write new records to the same file. It
would be easy to assume that these new keys would not show up in the
list because you created the list before the new records existed. This
is not the case. Any records written beyond the current position in
the file will eventually show up in the list. In situations where this
might cause a problem, or to ensure that you obtain a complete,
qualified list of keys, you should use a slower external command like
jQL SELECT or [SSELECT](#SSELECT) and then [READNEXT](#READNEXT)
to parse the file.

If using a variable to hold the select list, then it should be
unassigned or null before the SELECT. If it contains a number in the
range 0 to 10 then it will use the corresponding select list number
to hold the list, although you can still reference the list with the
variable name. This "feature" is for compatibility with older
platforms. See also example 3.

Lists can be selected as many times as required.

See also: the extensions for secondary indexes.

### EXAMPLE 1

    OPEN "Customers" ELSE ABORT 201, "Customers"
    SELECT TO CustList1
    SELECT TO CustList2

### EXAMPLE 2

    OPEN "Customers" TO CustFvar ELSE ABORT 201, "Customers"
    SELECT CustFvar TO 2
    Done = 0
    LOOP
       READNEXT CustId FROM 2 ELSE Done = 1
    UNTIL Done DO
       GOSUB ProcessCust
    REPEAT

### EXAMPLE 3

    CLEAR
    OPEN "Customers" TO CustFvar ELSE ABORT 201, "Customers"
    OPEN "Products" TO ProdFvar ELSE ABORT 201, "Products"
    SELECT CustFvar TO Listvar1
    SELECT ProdFvar TO Listvar2

This example demonstrates a coding error. The CLEAR statement is used
to initialize all variables to zero. Since Listvar1 has the value 0,
select list number 0 is used to hold the list. However, the CLEAR
statement also initializes Listvar2 to zero, so the second SELECT
overwrites the first list.

## SEND

<a name="SEND"/>

SEND statement sends a block of data directly to a device.

### COMMAND SYNTAX

    SEND output {:} TO FileVar THEN | ELSE statements

### SYNTAX ELEMENTS

The output is an expression evaluating to a string that will be sent
to the output device (specified by FileVar).  It is expected that
the device has already been opened with [OPENSER](#OPENSER) or
[OPENSEQ](#OPENSEQ).

The SEND statement will append a newline sequence to the final
output expression unless it is terminated with a colon ":" character.

### NOTES

As the expression can be any valid expression, it may have output
formatting applied to it.

The SEND syntax requires you specify either a THEN or ELSE clause,
or both.  It executes the THEN clause if the data is without error.
Else executes, the ELSE clause if the data cannot be sent.

See also: [SENDX](#SENDX)

### EXAMPLES

See also: Sequential File Processing.

## SENDX

<a name="SENDX"/>

SENDX statement sends a block of data (in hexidecimal) directly to a
device.

### COMMAND SYNTAX

    SENDX output {:} TO FileVar THEN | ELSE statements

### SYNTAX ELEMENTS

The output is an expression evaluating to a string that will be sent
to the output device (specified by FileVar).  It is expected that
[OPENSER](#OPENSER) or [OPENSEQ](#OPENSEQ) has already opened the
device.

The SENDX statement will append a newline sequence to the final output
expression unless it is terminated with a colon ":" character.

### NOTES

As the expression can be any valid expression, it may have output
formatting applied to it.

The SENDX syntax requires a specified THEN or ELSE clause, or both.
If the data is send without error, it executes the THEN clause.
If the data cannot be sent, it executes the ELSE clause.

See also: [SEND](#SEND)

### EXAMPLES

See: Sequential File Processing examples.

## SENTENCE

SENTENCE function allows a program to locate the command used to
invoke it and the arguments it was given.

### COMMAND SYNTAX

    SENTENCE({expression})

### SYNTAX ELEMENTS

If expression is specified it should evaluate to a positive integer
value. A negative value will return a null string. A value of null
will return the entire command line.

An integer value of expression will return a specific element of the
command line with the command itself being returned by SENTENCE (0),
the first parameter being returned by SENTENCE(1) and so on.

### NOTES

It is assumed the command line arguments are space separated and when
returning the entire command line they are returned as such. The
SYSTEM(1000) function will return the command line attribute mark
delimited.

### EXAMPLES

       DIM Parm(4)
       ProgName = SENTENCE(0) ;* program is?
       FOR I = 1 TO 4
          Parm(I) = SENTENCE(I) ;* get parameters
       NEXT I

       this_prog = SENTENCE(0)    ;* name of this program
       phrase_part = 'to understand recursion '
       IF SENTENCE(1) EQ '-2' THEN              ;* first parameter
          CRT TRIM( SENTENCE(2), '"', 'B' ):    ;* 2nd parameter
          CRT phrase_part
       END ELSE
          CRT phrase_part:
          EXECUTE this_prog : ' -2 "you firstly need "'
       END

## SEQ

SEQ function returns numeric ASCII value of a character.

### COMMAND SYNTAX

    SEQ(expression)

### SYNTAX ELEMENTS

**expression** may evaluate to any data type. However, the SEQ function
will convert the expression to a string and operate on the first
character of that string.

### INTERNATIONAL MODE

The SEQ function will return numeric values beyond 255 for UTF-8 byte
sequences representing any Unicode values above 0x000000ff.

### EXAMPLE

    EQU ENQ TO 5
    * Get next comms code
    * Time-out after 20 seconds
    INPUT A, 1 FOR 200 ELSE BREAK
    IF SEQ(A) = ENQ THEN
    * Respond to ENQ char

### EXAMPLE 2

    * C5A1: Unicode Character 'LATIN SMALL LETTER S WITH CARON'
       CRT SEQ( ICONV('C5A1', 'MX') )
       CRT ICONV('C5A1', 'MX')

Output:

<pre>
    353
    &#353;</pre>

## SEQS

SEQS function is used to convert a dynamic array of ASCII characters to
their numeric string equivalents.

### COMMAND SYNTAX

    SEQS(dynamic.array)

### SYNTAX ELEMENTS

**dynamic.array** specifies the ASCII characters to be converted. If
dynamic.array evaluates to null, it returns null. If any element of
dynamic.array is null, it returns null for that element.

If you use the subroutine syntax, the resulting dynamic array is
returned as return.array.

By using the SEQS function to convert a character outside its range
results in a run-time message, and the return of an empty string.

### INTERNATIONAL MODE

The SEQS function will return numeric values beyond 255 for UTF-8 byte
sequences representing any Unicode values above 0x000000ff.

### EXAMPLE

    G = 'T' :@VM: "G"
    A = SEQS(G)
    PRINT A
    PRINT SEQS('G')

The output of this program is:

<pre>
    84]71 71</pre>

## SIN

SIN function returns the mathematical sine value of a numeric
expression.

### COMMAND SYNTAX

    SIN(expression)

### SYNTAX ELEMENTS

**expression** should evaluate to a numeric value and is interpreted
as a number of degrees between 0 and 360.

### NOTES

The function will calculate the sine of the angle specified by the
expression as accurately as the host system will allow. It will then
truncate the value according to the PRECISION of the program.

### EXAMPLE

    CRT @(-1):
    FOR I = 0 TO 79
       CRT @(I,12 + INT( SIN(360/80*(I+1))*10)) : "*" :
    NEXT I

## SLEEP

<a name="SLEEP"/>

SLEEP function allows the program to pause execution for a specified
period.

### COMMAND SYNTAX

    SLEEP {expression}

### SYNTAX ELEMENTS

**expression** may evaluate to one of two forms:

Numeric in which case the statement will sleep for the specified number
of seconds or fractions of a second

"nn:nn{:nn}" in which case the statement will sleep until the time
specified.

If expression is not supplied then a default period of 1 second is
assumed.

### NOTES

Sleeping until a specified time works by calculating the time between
the current time and the time supplied and sleeping for that many
seconds. If in the meantime the host clock is changed the program
will not wake up at the desired time;

If invoking the debugger while a program is sleeping and the execution
continued, the user will be prompted:

<pre>
    Continue with SLEEP (Y/N)?</pre>

If "N" is the response, the program will continue at the next statement
after the SLEEP.

See also: MSLEEP to sleep for a specified number of milliseconds.

### EXAMPLES

Sleep until the end of the working day for anyone who doesn't program
computers:

    SLEEP "17:30"
    * 40 winks...
    SLEEP 40
    * Sleep for two and a half seconds...
    SLEEP 2.5

## SMUL

SMUL function performs string multiplication of two base 10-string
numbers.

### COMMAND SYNTAX

    SMUL(expr1, expr2)

### SYNTAX ELEMENTS

**expr1** and **expr2** are strings consisting of numeric characters,
with either optionally including a decimal part.

### NOTES

Use the SMUL function with numbers that may exceed a valid range with
standard arithmetic operators.

The PRECISION declaration does not affect the value returned by SMUL.

### EXAMPLES

    A = 243603310027840922
    B = 3760
    CRT SMUL(A,B)

Displays 915948445704681866720 to the screen

    CRT SMUL(0.0000000000000475,3.61)

Displays 0.0000000000001714 to the screen

## SORT

The SORT function sorts all elements of a dynamic array in ascending
left-justified order.

### COMMAND SYNTAX

    SORT(expression)

### SYNTAX ELEMENTS

**expression** may evaluate to any data type but will only be useful if
it evaluates to a dynamic array.

### NOTES

The dynamic array can contain any number and combination of system
delimiters.

The SORT function will return an attribute-delimited array of the
sorted elements.

All system delimiters in expression will be converted to an attribute
mark '0xFE' in the sorted result. For example, the following code

    MyArray = 'GEORGE':@VM:'FRED':@AM:'JOHN':@SM:'ANDY'
    CRT OCONV( SORT(MyArray), 'MCP')

will display:

<pre>
    ANDY^FRED^GEORGE^JOHN</pre>

MyArray remains unchanged.

The SORT is achieved by the quick sort algorithm, which sorts in situ
and is very fast.

### INTERNATIONAL MODE

When using the SORT function in International Mode, the function will
use the currently configured locale to determine the rules by which
each string is considered less than or greater than the other for
sort purposes.

## SOUNDEX

SOUNDEX function allows phonetic conversions of strings.

### COMMAND SYNTAX

    SOUNDEX(expression)

### SYNTAX ELEMENTS

**expression** may evaluate to any data type but the function will
only give meaningful results for English words.

### NOTES

The phonetic equivalent of a string is calculated as the first
alphabetic character in the string followed by a 1 to 3-digit
representation of the rest of the word.
The digit string is calculated from the following table:

|Characters     | Value code |
|---------------|------------|
|B F P V        |       1    |
|C G J K Q S X Z|       2    |
|D T            |       3    |
|L              |       4    |
|M N            |       5    |
|R              |       6    |

All characters not contained in the above table are ignored. The
function is case insensitive and identical sequences of a character are
interpreted as a single instance of the character.

The idea is to provide a crude method of identifying words such as last
names even if they are not spelt correctly. The function is not
foolproof should not be the sole method of identifying a word.

### EXAMPLE

    INPUT Lastname
    Lastname = SOUNDEX(Lastname)
    *search the databases

## SPACE

<a name="SPACE"/>

SPACE function generates a specific number of ASCII space characters.

### COMMAND SYNTAX

    SPACE(expression)

### SYNTAX ELEMENTS

**expression** should evaluate to a positive integer value.

### NOTES

The SPACE function is useful for padding strings. It should not be
used to position output on the terminal screen as this is
inefficient, accomplish this by using the [@](#@).

### EXAMPLES

    TenSpaces = SPACE(10)

## SPACES

<a name="SPACES"/>

SPACES function is used to return a dynamic array with elements
composed of blank spaces.

### COMMAND SYNTAX

    SPACES(dynamic.array)

### SYNTAX ELEMENTS

**dynamic.array** specifies the number of spaces in each element. If
dynamic.array or any element of dynamic.array evaluates to null, the
SPACES function will enter the debugger.

## SPLICE

<a name="SPLICE"/>

SPLICE function is used to create a dynamic array of the
element-by-element concatenation of two dynamic arrays, separating
concatenated elements by the value of expression.

### COMMAND SYNTAX

    SPLICE(array1, expression, array2)

### SYNTAX ELEMENTS

Each element of array1 is concatenated with expression and with the
corresponding element of array2. The result is returned in the
corresponding element of a new dynamic array. If an element of one
dynamic array has no corresponding element in the other dynamic
array, the element is returned properly concatenated with expression.
If either element of a corresponding pair is null, null is returned
for that element. If expression evaluates to null, null is returned
for the entire dynamic array.

### EXAMPLE

    A = "A" :@VM: "B" :@SM: "C"
    B = "D" :@SM: "E" :@VM: "F"
    C = '-'
    PRINT SPLICE(A,C,B)

The output of this program is:

<pre>
    A-D\-E]B-F\C-</pre>

## SPOOLER

<a name="SPOOLER"/>

SPOOLER function returns information from the jBASE spooler.

### COMMAND SYNTAX

    SPOOLER(n{, Port | User})

### SYNTAX ELEMENTS

Are as follows:

|n  |     Description                |
|---|--------------------------------|
|1  |  returns formqueue information |
|2  |  returns job information       |
|3  |  forms queue assignment        |
|4  |  returns status information    |

**Port** limits the information returned to the specified port.

**User** limits the information returned to the specified user.

### NOTES

SPOOLER(1) returns information about formqueues. The information is
returned in a dynamic array, which contains an attribute for each
formqueue. Each formqueue is structured as follows:

|Multivalue |  Description                      |
|-----------|-----------------------------------|
|1          |  Formqueue name                   |
|2          |  Form type                        |
|3          |  Device                           |
|4          |  Device type                      |
|5          |  Status                           |
|6          |  Number of jobs on the formqueue  |
|7          |  Page skip                        |

SPOOLER(2) returns information about print jobs. The information is
returned in a dynamic array, which contains an attribute for each
print job.

|Multivalue |  Description                      |
|-----------|-----------------------------------|
|1          |  Formqueue name                   |
|2          |  Print job number                 |
|3          |  Effective user id                |
|4          |  Port number job generated on     |
|5          |  Creation date in internal format |
|6          |  Creation time in internal format |
|7          |  Job Status                       |
|8          |  Options                          |
|9          |  Print job size (pages)           |
|10         |  Copies                           |
|11         |  Reserved                         |
|12         |  Reserved                         |
|13         |  Reserved                         |
|14         |  Effective user id                |
|15         |  Real user id                     |
|16         |  Application id as set by         |
|           |  @APPLICATION.ID                  |
|17         |  JBASICLOGNAME id                 |

SPOOLER(3) returns information about current formqueue assignments.
The information is returned in a dynamic array, which contains an
attribute for each assignment. Each attribute is structured as
follows:

|Multivalue |  Description                      |
|-----------|-----------------------------------|
|1          |  Report (channel) number          |
|2          |  Formqueue name                   |
|3          |  Options                          |
|4          |  Copies                           |

SPOOLER(4) returns information about current print jobs. The information
is returned in a dynamic array, which contains an attribute for each job
being generated. Each attribute is structured as follows:

|Multivalue |  Description                      |
|-----------|-----------------------------------|
|1          |  Report (channel) number          |
|2          |  Print job number                 |
|3          |  Print job size (pages)           |
|4          |  Creation date in internal format |
|5          |  Creation date in internal format |
|6          |  Job Status                       |
|7          |  Effective User id                |
|8          |  Real user id                     |
|9          |  JBASICLOGNAME id                 |
|10         |  Banner test from SETPTR BANNER   |
|           |  text command                     |

The values for Job Status are:

|Status|  Description |
|------|--------------|
|1     |  Queued      |
|2     |  Printing    |
|3     |  Finished    |
|4     |  Open        |
|5     |  Hold        |
|6     |  Edited      |

## SQRT

<a name="SQRT"/>

SQRT function returns the mathematical square root of a value.

### COMMAND SYNTAX

    SQRT(expression)

### SYNTAX ELEMENTS

**expression** should evaluate to a positive numeric value as
the authors do not want to introduce a complex number type
within the language. Negative values will cause a math error.

### NOTE

The function calculates the result at the highest precision
available and then truncates the answer to the required
PRECISION.

### EXAMPLE

    FOR I = 1 TO 1000000
        J = SQRT(I)
    NEXT I

## SSELECT

<a name="SSELECT"/>

SSELECT statement is used to create:

A select list of record IDs in sorted order from a jBASE
hashed file

A numbered select list of record IDs from a dynamic array (SSELECTN).

A select list of record IDs from a dynamic array (SSELECTV).

You can then access this select list by a subsequent READNEXT
statement, which removes one record ID at a time from the list.

### COMMAND SYNTAX

    SSELECT [variable] [ TO list.number|select list ] [ ON ERROR statements ]

    SSELECTN [variable] [ TO list.number] [ ON ERROR statements ]

    SSELECTV [variable] TO list.variable [ ON ERROR statements ]

**variable** can specify a dynamic array or a file variable. If
it specifies a dynamic array, the record IDs must be separated by
field marks (ASCII 254). If variable specifies a file variable, the
file variable must have previously been opened. If variable is not
specified, the default file is assumed. If the file is neither
accessible nor open, or if variable evaluates to null, the SSELECT
statement fails and the program enters the debugger with a run-time
error message.

The TO clause specifies the select list that is to be used. list.number
is an integer from 0 through 10. If no list.number is specified, select
list 0 is used.

The record IDs of all the records in the file forms the list. The record
IDs are listed in ascending order. Each record ID is one entry in the
list.

Use the SSELECTV statement to store the select list in a named list
variable instead of to a numbered select list. list.variable is an
expression that evaluates to a valid variable name.

*The ON ERROR Clause*

The ON ERROR clause is optional in SSELECT statements. The ON ERROR
clause lets you specify an alternative for program termination when a
fatal error is encountered during processing of a SSELECT statement.

### INTERNATIONAL MODE

When using the SSELECT statement in International Mode, the statement
will use the currently configured locale to determine the rules by which
each string is considered less than or greater than the other for sort
purposes.

### EXAMPLE

       OPEN 'F.TEMP' TO F.TEMP THEN
          V.ERR = ''
          CLEARFILE F.TEMP SETTING V.ERR
          IF V.ERR NE '' THEN
             CRT 'ERROR ' : V.ERR
             STOP
          END
       END ELSE
          EXECUTE 'CREATE-FILE DATA F.TEMP 1 101 TYPE=J4'
          OPEN 'F.TEMP' TO F.TEMP ELSE ABORT 201, 'F.TEMP'
       END
       V.REC = 'LINE 1' :@FM: 'LINE 2' :@FM: 'LINE 3'
       WRITE V.REC TO F.TEMP, 'REC3'
       WRITE V.REC TO F.TEMP, 'REC1'
       WRITE V.REC TO F.TEMP, 'REC2'
       SSELECT F.TEMP TO V.LIST
       READNEXT V.ID FROM V.LIST THEN CRT V.ID        ;*  REC1

### EXAMPLE 2

Using SSELECTV to sort a dynamic array:

       V.RANDOM = ''
       FOR V.I = 1 TO 1000
          V.STRING = ''
          FOR V.J = 1 TO 8
             V.RND = RND(26) + 65
             V.STRING := CHAR(V.RND)        ;* A...Z
          NEXT V.J
          V.RANDOM<-1> = V.STRING
       NEXT V.I
       SSELECTV V.RANDOM TO V.SORTED
       CRT 'Got strings from ' : V.SORTED<1> : ' to ' : V.SORTED<1000>

Sample output:

<pre>
    Got strings from AALUKTJZ to ZZQTIWFQ</pre>

Or:

<pre>
    Got strings from AAGPKJJP to ZZTMYNNX</pre>

### EXAMPLE 3

Don't try to sort an array with **SSELECTV** if this array has values or subvalues (they all will be lost -
after all, it's intended to sort just select lists). The correct way to do that is also shown below:

    *
    init_array = 3 : @VM : 'Third row'
    init_array<-1> = 2 : @VM : 'Second row'
    init_array<-1> = 4 : @VM : 'Fourth row'
    init_array<-1> = 1 : @VM : 'First row'
    &nbsp;
    the_len = DCOUNT(init_array, @FM)
    &nbsp;
    SSELECTV init_array TO sorted_array
    GOSUB SHOW.RESULT
    * Output:
    * 1
    * 2
    * 3
    * 4
    &nbsp;
    elem_to_sort = 1     ;* sort by 1st value
    GOSUB MAKE.SORT
    GOSUB SHOW.RESULT
    * Output:
    * 1]First row
    * 2]Second row
    * 3]Third row
    * 4]Fourth row
    &nbsp;
    elem_to_sort = 2     ;* sort by 2nd value
    GOSUB MAKE.SORT
    GOSUB SHOW.RESULT
    * Output:
    * 1]First row
    * 4]Fourth row
    * 2]Second row
    * 3]Third row
    &nbsp;
    RETURN
    &nbsp;
    MAKE.SORT:
       seek_array = ''
       sorted_array = ''
       FOR i = 1 TO the_len
          LOCATE init_array<i,elem_to_sort> IN seek_array BY 'AN' SETTING ins_posn ELSE NULL
          INS init_array<i,elem_to_sort> BEFORE seek_array<ins_posn>
          INS init_array<i> BEFORE sorted_array<ins_posn>
       NEXT i
       RETURN
    &nbsp;
    SHOW.RESULT:
       FOR i = 1 TO the_len
          CRT OCONV(sorted_array<i>, 'MCP')
       NEXT i
       RETURN

## SSELECTN

See: [SSELECT](#SSELECT).

## SSELECTV

See: [SSELECT](#SSELECT).

## SSUB

SSUB function performs string subtraction of two base 10-string numbers.

### COMMAND SYNTAX

    SSUB(expr1, expr2)

### SYNTAX ELEMENTS

**expr1** and **expr2** are strings consisting of numeric characters,
optionally including a decimal part.

### NOTES

Use the SSUB function with numbers that may exceed a valid range with
standard arithmetic operators.
The [PRECISION])(#PRECISION) declaration has no effect on the value
returned by SSUB.

### EXAMPLES

    A = 2.3000000123456789
    B = 5.0000000000000001
    CRT SSUB(A,B)

Displays -2.69999998765432 to the screen.

## STATUS

<a name="STATUS"/>

STATUS function after an OPENPATH statement to find the cause of a file
open failure (that is, for an  tatement in which the ELSE clause is
used).
The following values can be returned if the  statement is unsuccessful:

For File access commands

[READ](#READ), [WRITE](#WRITE), [OPEN](#OPEN)

*Previous Operation*

Value = 0 if successful

Value = Operating System error code if previous command failed

13 - permission denied on UNIX systems

*OCONV Conversions*

0 = successful

1 = invalid conversion requested

3 = conversion of possible invalid date

### COMMAND SYNTAX

    STATUS()

### DESCRIPTION

Arguments are required for the STATUS function.

Values of STATUS after [CLOSE](#CLOSE), [DELETE](#DELETE),
[MATREAD](#MATREAD), [MATWRITE](#MATWRITE), [OPEN](#OPEN),
[READ](#READ) and [WRITE](#WRITE)

*After a [DELETE](#DELETE) statement:* After a DELETE statement
with an ON ERROR clause, the value returned is the error number.

Returns 0 if successful else returns ERROR number

*After an [OPEN](#OPEN), [OPENPATH](#OPENPATH), or [OPENSEQ](#OPENSEQ) statement:*
The file type is returned if the file is opened
successfully. If the file is not opened successfully, the following
values may return:

*After a [READ](#READ) statement:* If the file is a distributed file,
the STATUS function returns the following:

*After a [READL](#READL), [READU](#READU), [READVL](#READVL), or [READVU](#READVU) statement:*
If the statement includes the LOCKED
clause, the returned value is the terminal number, as returned by
the
WHO command, of the user who set the lock.

*After a [READSEQ](#READSEQ) statement:*

*After a [READT](#READT), [REWIND](#REWIND), [WEOF](#WEOF), or [WRITET](#WRITET) statement:*
The returned value is
hardware-dependent (that is, it varies according to the
characteristics of the specific tape drive unit).
Consult the documentation that accompanied your tape drive
unit for information about interpreting the values returned
by the STATUS function.

### EXAMPLE

       DELETE not_valid_filevar, 'REC5' SETTING ret_code ON ERROR
          CRT 'REC5 - DELETE ERROR'
       END
       CRT STATUS()           ;*  -1
       CRT ret_code           ;*  32768

## STATUS statement

STATUS statement is used to determine the status of an open
file. It returns the file status as a dynamic array and assigns
it to an array.

### COMMAND SYNTAX

    STATUS array FROM variable THEN statements ELSE statements | ELSE statements

### SYNTAX ELEMENTS

The STATUS statement returns the following values in the following
attributes:

*STATUS Statement Values*

|Attribute  | Description                                         |
|-----------|-----------------------------------------------------|
|1          | Current position in the file Offset in bytes from   |
|           | beginning of file                                   |
|2          | End of file reached 1 if EOF, 0 if not.             |
|3          | Error accessing file 1 if error, 0 if not.          |
|4          | Number of bytes available to read                   |
|5          | File mode Permissions (in octal) 6 File size in     |
|           | bytes.                                              |
|7          | Number of hard links 0 if no links. Where applicable|
|           | else 0                                              |
|8          | O/S User ID. ID based on the user name and domain of|
|           | the user a jBASE pseudo user.                       |
|9          | O/S Group ID.                                       |
|10         | I-node number; Unique ID of file on file system     |
|11         | Device on which i-node resides Number of device. The|
|           | value is an internally calculated value on Windows  |
|           | NT.                                                 |
|12         | Device for special character or block Number of     |
|           | device.                                             |
|13         | Time of last access in internal format              |
|14         | Date of last access in internal format.             |
|15         | Time of last modification in internal format        |
|16         | Date of last modification in internal format.       |
|17         | Time and date of last status change in internal     |
|           | format.                                             |
|18         | Date of last status change in internal format.      |
|19         | Number of bytes left in output queue (applicable to |
|           | terminals only)                                     |
|20         | {  }                                                |
|21         | jBASE File types j3, j4, jPLUS                      |
|22         | jBASE File types j3, j4, jPLUS                      |
|23         | jBASE File types j3, j4, jPLUS                      |
|24         | Part numbers of part files belonging to a           |
|           | distributed file multivalued list                   |


**variable** specifies an open file. If variable evaluates to the null
value, the STATUS statement fails and the program terminates with a
run-time error message.

If the STATUS array is assigned to an array, the THEN statements are
executed and the ELSE statements are ignored. If no THEN statements
are present, program execution continues with the next statement. If
the attempt to assign the array fails, the ELSE statements are
executed; any THEN statements are ignored.

### EXAMPLE

       IF NOT( GETENV('JEDIFILENAME_SYSTEM', FN.SYSTEM) ) THEN ABORT
       OPEN FN.SYSTEM TO F.SYSTEM ELSE NULL
       STATUS V.INFO.L FROM F.SYSTEM ELSE ABORT
       CRT V.INFO.L<5>       ;*  permissions in octal, e.g. 655
       CRT V.INFO.L<6>       ;*  file size in bytes
       CRT V.INFO.L<20>      ;*  full path to file
       CRT V.INFO.L<21>      ;*  file type, e.g. J4, JR, XMLDB2, SEQ

## STOP

<a name="STOP"/>

STOP statement is virtually identical in function to the
[ABORT](#ABORT) statement except that it does not terminate a
calling jCL program.

## STR

STR function allows the duplication of a string a number of times.

### COMMAND SYNTAX

    STR(expression1, expression2)

### SYNTAX ELEMENTS

**expression1** will evaluate to the string to duplicate and may
be of any length.

**expression2** should evaluate to a numeric integer, which specifies
the number of times the string will be duplicated.

### EXAMPLE

    LongString = STR('long string ', 999 )

## STRS

STRS function is used to produce a dynamic array containing the
specified number of repetitions of each element of dynamic.array.

### COMMAND SYNTAX

    STRS(dynamic.array, repeat)

**dynamic.array** is an expression that evaluates to the strings
to be generated.

**repeat** is an expression that evaluates to the number of times
the elements are to be repeated. If it does not evaluate to a value
that can be truncated to a positive integer, an empty string is
returned for dynamic.array.

If dynamic.array evaluates to null, it returns null. If any element
of dynamic.array is null, null is returned for that element. If
repeat evaluates to null, the STRS function fails and the program
enters the debugger.

### EXAMPLES

    ABC= "A" :@VM: "B" :@VM: "C"
    PRINT STRS(ABC,3)

The output of this program is:

<pre>
    AAA]BBB]CCC</pre>

## SUBROUTINE

<a name="SUBROUTINE"/>

SUBROUTINE statement is used at the start of any program that will be
called externally by the [CALL](#CALL) statement. It also declares any
parameters to the compiler.

### COMMAND SYNTAX

    SUB{ROUTINE} Name {({ MAT } variable{,{ MAT } variable...})}

### SYNTAX ELEMENTS

**Name** is the identifier by which the subroutine will be known to the
compilation process. It should always be present as this name (not the
source file name), will be used to call it by. However, if the name is
left out, the compiler will name subroutine as the source file name
(without suffixes). Default naming is not encouraged as it can cause
problems if source files are renamed.

Each comma separated variable in the optional parenthesized list is used
to identify parameters to the compiler. These variables will be assigned
the values passed to the subroutine by a CALL statement.

### NOTES

The SUBROUTINE statement must be the first code line in a subroutine.

All the variables declared using the [COMMON](#COMMON)
statement will be inherited providing an equivalent common
area is declared within the subroutine source file.
The program will fail to compile if the number of common variables
used in each common area exceeds the number defined in the equivalent
area in the main program.

Subroutines can only be called via the jBC [CALL](#CALL) statement.

[PRECISION](#PRECISION) can be redefined but the new setting
will not persist when the subroutine returns to the calling program.

The control will be returned to the CALLing program if the subroutine reaches the
logical end of the program or a [RETURN](#RETURN) is executed with
no outstanding [GOSUB](#GOSUB) statement.

The control will not be returned to the calling program
if a [STOP](#STOP) or [ABORT](#ABORT) statement is executed.

See also: [CALL](#CALL), [CATALOG Command](#CATALOG_Command), [COMMON](#COMMON),
[RETURN](#RETURN).

### EXAMPLES

    SUBROUTINE DialUp(Number, MAT Results)
    DIM Results(8)
    ....

## SUBS

SUBS function returns a dynamic array, the content of which is
derived by subtracting each element of the second dynamic array
argument from the corresponding element of the first dynamic
array argument.

### COMMAND SYNTAX

    SUBS(DynArr1, DynArr2)

### SYNTAX ELEMENTS

**DynArr1** and **DynArr2** represent dynamic arrays.

### NOTES

Null elements of argument arrays are treated as zero. Otherwise,
a non-numeric element in an argument array will cause a run-time
error.

### EXAMPLE

    X = 1 : @VM : @VM : 5 : @VM : 8 : @SM : 27 : @VM : 4
    Y = 1 : @VM : 5 : @VM : 8 : @VM : 70: @VM : 19
    S = SUBS(X, Y)

The variable S is assigned the value:

    0 : @VM : -5 : @VM : -3 : @VM : -62 : @SM : 27 : @VM : -15

## SUBSTRINGS

SUBSTRINGS function returns a dynamic array of elements, which are
sub-strings of the corresponding elements in a supplied dynamic array.

### COMMAND SYNTAX

    SUBSTRINGS(DynArr, Start, Length)

### SYNTAX ELEMENTS

**DynArr** should evaluate to a dynamic array.

**Start** specifies the position from which characters are extracted
from each array element. It should evaluate to an integer greater than
zero.

**Length** specifies the number of characters to extract from each
dynamic array element. If the length specified exceeds the number of
characters remaining in an array element then all characters from
the Start position are extracted.

### INTERNATIONAL MODE

When using the SUBSTRINGS function in International Mode, the function
will use the 'start' and 'length' parameters to the function as character
count values, rather than bytecount

### EXAMPLES

The following program shows how each element of a dynamic array can be
changed with the FIELDS function.

    t = ""
    t<1> = "AAAAA"
    t<2> = "BBBBB" :@VM: "CCCCC" : @SM: "DDDDD"
    t<3> = "EEEEE" :@VM: @SM
    r1 = SUBSTRINGS(t,3,2)
    r2 = SUBSTRINGS(t,4,20)
    r3 = SUBSTRINGS(t,0,1)

The above program creates 3 dynamic arrays. v represents a value mark.
s represents a sub-value mark.

| Array    |  Contents          |
|----------|--------------------|
|r1        |  <1>AA             |
|          |  <2>BB v CC s DD   |
|          |                    |
|          |  <3>EE v s         |
|          |                    |
| r2       |  <1>AA             |
|          |                    |
|          |  <#>BB v CC s      |
|          |                    |
|          |  <3>EE v s         |
|          |                    |
| r3       |  <1>A              |
|          |                    |
|          |  <2>B v C s D      |
|          |                    |
|          |  <3>E v s          |

## SUM

SUM function sums numeric elements in a dynamic array.

### COMMAND SYNTAX

    SUM(expr)

### SYNTAX ELEMENTS

expr is a dynamic array.

### NOTES

Non-numeric sub-values, values and attributes are ignored.

### EXAMPLES

       V.ARRAY = 1 :@FM: 2 :@FM: 3.1
       CRT FMT( SUM(V.ARRAY), 'MCP' )         ;*  6.1
       V.ARRAY<4> = 6
       CRT FMT( SUM(V.ARRAY), 'MCP' )         ;*  12.1
       V.ARRAY<4,2> = 7
       CRT FMT( SUM(V.ARRAY), 'MCP' )         ;*  1^2^3.1^13
       V.ARRAY<4,3> = 'QWERTY'
       CRT FMT( SUM(V.ARRAY), 'MCP' )         ;*  still 1^2^3.1^13
       V.ARRAY<4,3,2> = 8
       CRT FMT( SUM(V.ARRAY), 'MCP' )         ;*  1^2^3.1^6]7]8

## SWAP

SWAP function operates on a variable and replaces all occurrences of
one string with another

### COMMAND SYNTAX

    SWAP(variable, expression1, expression2)

### SYNTAX ELEMENTS

**expression1** may evaluate to any result and is the string of
characters that will be replaced.

**expression2** may also evaluate to any result and is the string of
characters that will replace expression1. The variable may be any
previously assigned variable in the program.

### NOTES

Either string can be of any length and is not required to be the same
length. This function is provided for compatibility with older
systems.

See also: [CHANGE](#CHANGE) function.

### EXAMPLE

    String1 = "Jim"
    String2 = "James"
    Variable = "Pick up the tab Jim"
    CRT SWAP(Variable, String1, String2)
    CRT SWAP(Variable, 'tab', 'check')

## System Functions

The following system functions are supported by TAFC:

| Function     | Description                                                              |
|--------------|--------------------------------------------------------------------------|
|SYSTEM(0)     |Returns the last error code                                               |
|SYSTEM(1)     |Returns 1 if output directed to printer                                   |
|SYSTEM(2)     |Returns page width                                                        |
|SYSTEM(3)     |Returns page depth                                                        |
|SYSTEM(4)     |Returns no of lines to print in current page.                             |
|              |(HEADING statement)                                                       |
|SYSTEM(5)     |Returns current page number (HEADING                                      |
|              |statement)                                                                |
|SYSTEM(6)     |Returns current line number (HEADING                                      |
|              |statement)                                                                |
|SYSTEM(7)     |Returns terminal type                                                     |
|SYSTEM(8)     |Returns record length for tape channel 0                                  |
|SYSTEM(9)     |Returns CPU milliseconds                                                  |
|SYSTEM(10)    |Returns 1 if stacked input available                                      |
|SYSTEM(11)    |Returns the number of items in an active select                           |
|              |list or 0 if no list is active                                            |
|SYSTEM(12)    |Returns 1/1000, ( or 1/10 for ROS), seconds past                          |
|              |midnight                                                                  |
|SYSTEM(13)    |Releases time slice                                                       |
|SYSTEM(14)    |Returns the number of characters available in                             |
|              |input buffer. Invoking SYSTEM(14)                                         |
|              |Causes a slight delay in program execution.                               |
|SYSTEM(15)    |Returns bracket options used to invoke command                            |
|SYSTEM(16)    |Returns current PERFORM/EXECUTE level                                     |
|SYSTEM(17)    |Returns stop code of child process                                        |
|SYSTEM(18)    |Returns port number or JBCPORTNO                                          |
|SYSTEM(19)    |Returns login name or JBASICLOGNAME. If the                               |
|              |system_19_timedate emulation option is set then returns                   |
|              |the number of seconds since midnight December 31, 1967.                   |
|SYSTEM(20)    |Returns last spooler file number created                                  |
|SYSTEM(21)    |Returns port number or JBCPORTNO                                          |
|SYSTEM(22)    |Reserved                                                                  |
|SYSTEM(23)    |Returns status of the break key                                           |
|              |                                                                          |
|              |    0 Enabled                                                             |
|              |                                                                          |
|              |    1 Disabled by BASIC                                                   |
|              |                                                                          |
|              |    2 Disabled by Command                                                 |
|              |                                                                          |
|              |    3 Disabled by Command and BASIC                                       |
|              |                                                                          |
|SYSTEM(24)    |Returns 1 if echo enabled, 0 if echo disabled                             |
|SYSTEM(25)    |Returns 1 if background process                                           |
|SYSTEM(26)    |Returns current prompt character                                          |
|SYSTEM(27)    |Returns 1 if executed by PROC                                             |
|SYSTEM(28)    |Reserved.                                                                 |
|SYSTEM(29)    |Reserved.                                                                 |
|SYSTEM(30)    |Returns 1 if paging is in effect (HEADING statement)                      |
|SYSTEM(31)    |Reserved                                                                  |
|SYSTEM(32)    |Reserved                                                                  |
|SYSTEM(33)    |Reserved                                                                  |
|SYSTEM(34)    |Reserved                                                                  |
|SYSTEM(35)    |Returns language in use as a name or number (ROS)                         |
|SYSTEM(36)    |Reserved                                                                  |
|SYSTEM(37)    |Returns thousands separator                                               |
|SYSTEM(38)    |Returns decimal separator                                                 |
|SYSTEM(39)    |Returns money symbol                                                      |
|SYSTEM(40)    |Returns program name                                                      |
|SYSTEM(41)    |Returns release number                                                    |
|SYSTEM(42)    |Reserved                                                                  |
|SYSTEM(43)    |Returns port number of item lock                                          |
|SYSTEM(44)    |Returns 99 for jBASE system type                                          |
|SYSTEM(45)    |Reserved                                                                  |
|SYSTEM(47)    |Returns 1 if currently in a transaction                                   |
|SYSTEM(48)    |Reserved                                                                  |
|SYSTEM(49)    |Returns PLID environment variable                                         |
|SYSTEM(50)    |Returns login user id                                                     |
|SYSTEM(51)    |Reserved                                                                  |
|SYSTEM(52)    |Returns system node name                                                  |
|SYSTEM(53)    |Reserved                                                                  |
|SYSTEM(100)   |Returns program create information                                        |
|SYSTEM(101)   |Returns port number or JBCPORTNO                                          |
|SYSTEM(102)   |Reserved                                                                  |
|SYSTEM(1000)  |Returns command line separated by attribute marks                         |
|SYSTEM(1001)  |Returns command line and options                                          |
|SYSTEM(1002)  |Returns temporary scratch file name                                       |
|SYSTEM(1003)  |Returns terminfo Binary definitions                                       |
|SYSTEM(1004)  |Returns terminfo Integer definitions                                      |
|SYSTEM(1005)  |Returns terminfo String definitions                                       |
|SYSTEM(1006)  |Reserved                                                                  |
|SYSTEM(1007)  |Returns system time                                                       |
|SYSTEM(1008)  |Returns SYSTEM file path                                                  |
|SYSTEM(1009)  |Returns MD file path                                                      |
|SYSTEM(1010)  |Returns Print Report information                                          |
|SYSTEM(1011)  |Returns jBASE release directory                                           |
|              |path. TAFC_HOME                                                           |
|SYSTEM(1012)  |Returns jBASE global directory                                            |
|              |path. JBCGLOBALDIR                                                        |
|SYSTEM(1013)  |Returns memory usage (UNIX only):                                         |
|              |                                                                          |
|              |<1> Free memory small blocks                                              |
|              |                                                                          |
|              |<2> Free memory large blocks                                              |
|              |                                                                          |
|              |<3> Used memory small blocks                                              |
|              |                                                                          |
|              |<4> Used memory large blocks                                              |
|SYSTEM(1014)  |Returns relative PROC level                                               |
|SYSTEM(1015)  |Returns effective user name. LOGNAME                                      |
|SYSTEM(1016)  |Returns tape assignment information                                       |
|SYSTEM(1017)  |Returns platform. UNIX, WINNT or WIN95                                    |
|SYSTEM(1018)  |Returns configured processors                                             |
|SYSTEM(1019)  |Returns system information (uname -a)                                     |
|SYSTEM(1020)  |Returns login user name                                                   |
|SYSTEM(1021)  |TAFC release information:                                                 |
|              |                                                                          |
|              |<1> Major release number                                                  |
|              |                                                                          |
|              |<2> Minor release number                                                  |
|              |                                                                          |
|              |<3> Patch level                                                           |
|              |                                                                          |
|              |<4> Copyright information                                                 |
|SYSTEM(1022)  |Returns the status of TAFC profiling:                                     |
|              |                                                                          |
|              | 0   no profiling is active                                               |
|              |                                                                          |
|              | 1   full profiling is active                                             |
|              |                                                                          |
|              | 2   short profiling is active                                            |
|              |                                                                          |
|              | 3   jCOVER profiling is active                                           |
|              |                                                                          |
|SYSTEM(1023)  |Used by STATUS() function                                                 |
|SYSTEM(1024)  |Retrieves details about last signals                                      |
|SYSTEM(1025)  |Returns value of International mode for thread                            |
|SYSTEM(1026)  |Total amount of memory in use formatted with                              |
|              |commas                                                                    |
|SYSTEM(1027)  |Returns directory PROC; Used by WHERE, LISTU                              |
|              |Information about running processes can be obtained                       |
|              |via the PROC jedi....                                                     |
|              |This JEDI enables retrieval of information from                           |
|              |executing processes and is the interface now used                         |
|              |by the WHERE command...                                                   |
|              |                                                                          |
|              |                                                                          |
|              | OPEN SYSTEM(1027) TO PROC ELSE STOP 201, "PROC"                        |
|              |            SELECT PROC TO Sel                                          |
|              |             LOOP                                                       |
|              |    WHILE READNEXT key FROM Sel DO                                      |
|              |  READ ProcessRecord FROM PROC, key ELSE CRT "Read Error"; STOP         |
|              |            REPEAT                                                      |
|              |                                                                          |
|              |Info for current user can be returned from the                            |
|              |@USERSTATS variable.                                                      |
|              |                                                                          |
|              |Attribute descriptions for Process Records returned                       |
|              |from the PROC Jedi READ interface.                                        |
|              |                                                                          |
|              | <1>   Port number                                                        |
|              | <2>   Number of programs running                                         |
|              | <3>   Connect time                                                       |
|              | <4>   Process ID                                                         |
|              | <5>   Account name                                                       |
|              | <6>   User name                                                          |
|              | <7>   Terminal name in TAFC format                                       |
|              | <8>   Terminal name in UNIX format                                       |
|              | <9>   Database name                                                      |
|              | <10>  Name of the tty device                                             |
|              | <11>  Language name                                                      |
|              | <12>  Time listening thread executed                                     |
|              | <13>  Mallinfo memory free                                               |
|              | <14>  Mallinfo memory used                                               |
|              | <15>  Type of thread as a number                                         |
|              | <16>  Type of thread as a string WHERE                                   |
|              |                                                                          |
|              |           thread_type_string = "Normal" =1                               |
|              |           thread_type_string = "javaOBjEX" = 2                           |
|              |           thread_type_string = "vbOBjEX" = 3                             |
|              |	       thread_type_string = "jrfs" = 4                            |
|              |           thread_type_string = "Compiler" = 5                            |
|              |           thread_type_string = "jdp" = 6                                 |
|              |           thread_type_string = "Listen" = 7                              |
|              |           thread_type_string = "Daemon"= 8                               |
|              |           thread_type_string = "Admin"                                   |
|              |           thread_type_string = "jrla"                                    |
|              |                                                                          |
|              |<17> Number of instructions executed and licenses allocated to work       |
|              |                                                                          |
|              |     around a bug in Windows. Need to build the buffer in                 |
|              |     separate sprintf's                                                   |
|              |<18> Number of OPEN's                                                     |
|              |<19> Number of READ's                                                     |
|              |<20> Number of WRITE's                                                    |
|              |<21> Number of DELETE's                                                   |
|              |<22> Number of CLEARFILE's                                                |
|              |<23> Number of EXECUTE's                                                  |
|              |<24> Number of INPUT's                                                    |
|              |<25> UNUSED                                                               |
|              |<26>  Number of files the application thinks is open                      |
|              |<27> Number of files that in reality are opened by the OS                 |
|              |<28> Application data set by @USER.ROOT                                   |
|              |<29> Text String to identify process                                      |
|              |<41> Command line arguments < threadnext >                                |
|              |<42> Current Line Number  < threadnext >                                  |
|              |<43> Name of source  <threadnext >                                        |
|              |<44> Status as a text string < threadnext >                               |
|	       |                       status = "Program running normally"                |
|              |                                                                          |
|              |                   status = "Program is SLEEPING"                         |
|              |                                                                          |
|              |                   status = "Program in DEBUGGER"                         |
|              |                                                                          |
|              |                   status = "Program at keyboard INPUT"                   |
|              |                                                                          |
|              |                   status = "Program blocked on record LOCK"              |
|              |                                                                          |
|              |                   status = "Program is doing EXECUTE/PERFORM"            |
|              |                                                                          |
|              |                   status = "Error!! Status unknown"                      |
|              |<47> Status as an integer  <threadnext >                                  |
|              |<48> User CPU time <threadnext >                                          |
|              |<49> System CPU time <threadnext >                                        |
|              |<50> Child User CPU time <threadnext >                                    |
|              |<51> Child System CPU time <threadnext >                                  |
|              |<52> User defined thread data <threadnext >                               |
|              |                                                                          |
|SYSTEM(1028)  | Logged in database name                                                  |
|SYSTEM(1029)  | Shows the CALL stack history so that in error conditions the             |
|              | application, such as database I/O statistics, programs                   |
|              | being performed and so on.  Can be used with @USERDATA.    |
|SYSTEM(1030)  | This new entry into the SYSTEM() function returns the current            |
|              | perform level in the range 1 to 32. This is similar                      |
|              | to SYSTEM(16), which returns the nested execute level.    |
|              | The difference is that SYSTEM(16) does not include any procs,               |
|              | paragraphs or shells and returns the relative  |
|              | application program level.                                                                         |
|              | SYSTEM(1030) returns the relative program level including                        |
|              |  all the proc interpreters, paragraph interpreters and    |
|              | shells.                                                                  |
|SYSTEM(1031)  | Number of free bytes on the current file system                          |
|SYSTEM(1032)  | Returns default frame size                                               |
|SYSTEM(1034)  | Returns handle of the current thread                                     |
|SYSTEM(1035)  | Returns the product ID of the license currently in use   |
|              |  by this process;     |
|              |  1    Enterprise                                                         |
|              |  13.  Server                                                             |

### EXAMPLES

       CRT SYSTEM(40)        ;* e.g. test
    * is there anything in keyboard buffer
       CRT SYSTEM(14)        ;*  0
    * Buffer is not necessarily filled manually
       DATA 'QWE'
       CRT SYSTEM(14)        ;*  4
    * Prompt...
       CRT SYSTEM(26)        ;*  ?
       PROMPT 'Your choice:'
       CRT SYSTEM(26)        ;*  Your choice:
    * Active SELECT
       IF NOT( GETENV('TAFC_HOME', V.HOME) ) THEN
          CRT 'TAFC_HOME not defined'
          STOP
       END
       CLEARDATA             ;* otherwise "QWE" will be executed
       CRT SYSTEM(11)        ;*  0
       HUSH ON
       EXECUTE 'SELECT ' : V.HOME : '/jbcmessages'
       HUSH OFF
       CRT SYSTEM(11)        ;*  490

## TAN

TAN function returns the mathematical tangent of an angle.

### COMMAND SYNTAX

    TAN(expression)

### SYNTAX ELEMENTS

**expression** should evaluate to a numeric type.

### NOTES

The function calculates the result at the highest precision available
on the host system; it truncates the result to the current PRECISION
after calculation.

### EXAMPLES

    Adjacent = 42
    Angle = 34
    CRT "Opposite length = " : TAN(Angle)*Adjacent

## TIME

TIME() function returns the current system time.

### COMMAND SYNTAX

    TIME()

### NOTES

Returns the time as the number of seconds past midnight

### EXAMPLE

    CRT "Time is " : OCONV( TIME(), "MTS" )

## TIMEDATE

<a name="TIMEDATE"/>

TIMEDATE() function returns the current time and date as a printable
string.

### COMMAND SYNTAX

    TIMEDATE()

### NOTES

The function returns a string of the form: hh:mm:ss dd mmm yyyy or
in the appropriate format for your international date setting.

### EXAMPLES

    CRT "The time and date is " : TIMEDATE()

## TIMEDIFF

TIMEDIFF returns the interval between two timestamp values as a dynamic
array.

### COMMAND SYNTAX

    TIMEDIFF(Timestamp1, Timestamp2, Mask)

### SYNTAX ELEMENTS

The TIMEDIFF function returns the interval between two timestamp values
by subtracting the value of Timestamp2 from Timestamp1. The interval is
returned as an attribute delimited array of the time difference.

The Mask is an integer from 0 to 7 and selects one of the following
output formats:

|Mask    |         Array                                             |
|--------|-----------------------------------------------------------|
|0       | Days^Hours^Minutes^Seconds^Milliseconds (Default)         |
|1       | Weeks^Days^Hours^Minutes^Seconds^Milliseconds             |
|2       | Months^Days^Hours^Minutes^Seconds^Milliseconds            |
|3       | Months^Weeks^Days^Hours^Minutes^Seconds^Milliseconds      |
|4       | Years^Days^Hours^Minutes^Seconds^Milliseconds             |
|5       | Years^Weeks^Days^Hours^Minutes^Seconds^Milliseconds       |
|6       | Years^Months^Days^Hours^Minutes^Seconds^Milliseconds      |
|7       | Years^Months^Weeks^Days^Hours^Minutes^Seconds^Milliseconds|

## TIMEOUT

If no data is read in the specified time, use the TIMEOUT statement to
terminate a [READSEQ](#READSEQ) or [READBLK](#READBLK) statement.

### COMMAND SYNTAX

    TIMEOUT file.variable, time

### SYNTAX ELEMENTS

**file.variable** specifies a file opened for sequential access.

**time** is an expression that evaluates to the number of seconds the
program should wait before terminating the [READSEQ](#READSEQ)
statement.

TIMEOUT causes subsequent READSEQ and READBLK statements to terminate
and execute ELSE statements if the number of seconds specified by
time elapses while waiting for data.

If either file.variable or time evaluates to null, the TIMEOUT
statement fails and the program enters the debugger.

### EXAMPLES

    TIMEOUT SLIPPERS, 10
    READBLK Var1 FROM SLIPPERS, 15 THEN PRINT Var1 ELSE
       PRINT "TIMEOUT OCCURRED"
    END

## TIMESTAMP

TIMESTAMP returns a UTC timestamp value as decimal seconds.

### COMMAND SYNTAX

    TIMESTAMP()

### SYNTAX ELEMENTS

The TIMESTAMP function returns a Universal Coordinated Time (UTC)
value as decimal seconds, i.e. Seconds with tenths and hundredths
specified after the decimal point.

"The value is returned as a variable with as many decimal places as
the current precision allows. However, successive calls may return
the same value many times before the operating system updates the
underlying timer. For example, Windows updates the low level timer
every 1/50 second even though it stores the time in billionths
of a second."

### EXAMPLE

       V.TS = TIMESTAMP()
       CRT V.TS                     ;* e.g. 1352316687.1156
       CRT ( MAKETIMESTAMP( DATE(), TIME(), 'Europe/Amsterdam') - V.TS ) / 3600 ;* -1
       CRT ( MAKETIMESTAMP( DATE(), TIME(), 'Asia/Singapore') - V.TS ) / 3600   ;* -8

## TRANS

<a name="TRANS"/>

TRANS function returns the data value of a field, given the name
of the file, the record key, the field number, and an action code.

### COMMAND SYNTAX

    TRANS([ DICT ] filename, key, field#, action.code)

### SYNTAX ELEMENTS

**DICT** is the literal string to be placed before the file name in
the event it is desired to open the dictionary portion of the file,
rather than the data portion.

**filename** is a string containing the name of the file to be
accessed.  Note that it is the actual name of the file, and not a
file unit variable.  This function requires the file name, regardless
of whether or not the file has been opened to a file unit variable.

**key** is an expression that evaluates to the record key, or item ID,
of the record from which data is to be accessed.

**field#** is the field number to be retrieved from the record.

**action.code** indicates what should happen if the field is null, or
the if record is not found.  This is a literal.  The valid codes are:

| Code | Description                                          |
|------|------------------------------------------------------|
|X     | Returns a null string. This is the default action    |
|V     | Prints an error message.                             |
|C     | Returns the value of key.                            |

### NOTES

If the field being accessed is a dynamic array, TRANS will return the
array with the delimiter characters lowered by 1.   For example,
multivalue marks (ASCII-253) are returned as subvalue marks (ASCII-252),
and subvalue marks are returned as text marks (ASCII-251).

If you supply -1 for field#, the entire record will be returned.

The TRANS function is the same as the [XLATE](#XLATE) function.

### EXAMPLES

Retrieval of a simple field:  Given a file called "VENDORS" containing a
record with the record key of "12345" and which contains the value of
"ABC Company" in field 1,

    VENDOR.ID = "12345"
    VENDOR.NAME = TRANS('VENDORS', VENDOR.ID, 1 , 'X')
    CRT VENDOR.NAME

will display: ABC Company

Retrieval of an array:  Suppose field 6 of the VENDORS file contains a
multivalued list of purchase order numbers, such as:

<pre>
    10011]10062]10079</pre>

use the TRANS function to retrieve it:

    PO.LIST = TRANS('VENDORS', VENDOR.ID, 6, 'X')
    CRT PO.LIST

will display: 10011\10062\10079

Notice that the backslashes (\) were substituted for brackets (]),
indicating that the delimiter is now CHAR(252).

Retrieval of an entire dictionary item: Given a dictionary item
called "VENDOR.NAME" with the following content:

<pre>
    001 A
    002 1
    003 Vendor Name
    004
    005
    006
    007
    008
    009 L
    010 30</pre>

these statements

    DIC.ID = "VENDOR.NAME"
    DIC.REC = TRANS('DICT VENDORS', DIC.ID, -1, 'C')
    PRINT DIC.REC

will display

<pre>
    A]1]Vendor Name]]]]]L]30</pre>

## TRANSABORT

<a name="TRANSABORT"/>

TRANSABORT statement is used to abort the current transaction and
reverse any updates to the database.

### COMMAND SYNTAX

    TRANSABORT {abort-text} [ THEN statement | ELSE statement ]

### SYNTAX ELEMENTS

**abort-text** specifies an optional text string to save in the
transaction abort record.

A THEN or ELSE (or both) statement is required. The THEN clause will
be executed if the transaction is successfully aborted. The ELSE
clause will be executed if the transaction abort fails for any reason.

### NOTES

Any record locks set during the transaction will be released upon
successful completion.

## TRANSEND

<a name="TRANSEND"/>

TRANSEND statement is used to mark the end of a successfully
completed transaction.

### COMMAND SYNTAX

    TRANSEND {end-text} [ THEN statement | ELSE statement ]

### SYNTAX ELEMENTS

**end-text** specifies an optional text string to save with the
transaction end record.

A **THEN** or **ELSE** (or both) statement is required. The THEN clause
will be executed if the transaction is successfully ended. The ELSE
clause will be executed if the transaction end fails for any reason.

### NOTES

Any record locks set during the transaction will be released upon
successful completion.

## TRANSQUERY

TRANSQUERY function is used to detect whether or not a transaction is
active on the current process.

### COMMAND SYNTAX

    TRANSQUERY()

### NOTES

TRANSQUERY will return 1 (true) if the process is within a transaction
boundary, and 0 (false) if it is not. In other words, TRANSQUERY will
return true if the [TRANSTART](#TRANSTART) statement has been issued
but a [TRANSEND](#TRANSEND) or [TRANSABORT](#TRANSABORT) statement has
not yet been processed.

By default, all hashed files are marked for inclusion in a transaction
however this can be modified by the jchmod utility.

## TRANSTART

<a name="TRANSTART"/>

In transaction processing, TRANSTART statement is used to mark the
beginning of a transaction.

### COMMAND SYNTAX

    TRANSTART { SYNC }{start-text} [ THEN statement | ELSE statement ]

### SYNTAX ELEMENTS

**SYNC** is an option to force the updates to be flushed at
transaction end or abort. start-text specifies an optional text
string to save with the transaction start record.

**THEN** or **ELSE** (or both) statement is required. The THEN
clause will be executed if the transaction is successfully started.
The ELSE clause will be executed if the transaction start fails for
any reason.

### NOTES

Record locks set during the transaction will not be released until a
[TRANSEND](#TRANSEND) or [TRANSABORT](#TRANSABORT) statement is
processed.

A program (or series of programs) can only have one active
transaction at one time. If another TRANSTART statement is encountered
whilst a transaction is active, a run-time error will be generated.

### Transactions-related examples

### EXAMPLE 1

Write to file without transactions:

       EXECUTE 'DELETE-FILE DATA F.TEMP'
       EXECUTE 'CREATE-FILE DATA F.TEMP 1 101 TYPE=J4'
       OPEN 'F.TEMP' TO F.TEMP ELSE ABORT 201, 'F.TEMP'
       V.REC.INIT = 'LINE 1' :@FM: 'LINE 2' :@FM: 'LINE 3'
       WRITE V.REC.INIT TO F.TEMP, 'REC1'
       EXECUTE 'LIST F.TEMP *A1 *A2 *A3'
       PROMPT 'Press any key to continue'
       INPUT DUMMY
       EXECUTE 'LIST F.TEMP *A1 *A2 *A3'

Output: LIST will show the same results both times:

<pre>
    LIST F.TEMP &lowast;A1 &lowast;A2 &lowast;A3
    &nbsp;
    DICT F.TEMP...    &lowast;A1...........    &lowast;A2...........    &lowast;A3...........
    &nbsp;
    REC1              LINE 1            LINE 2            LINE 3
    &nbsp;
     1 Records Listed</pre>

Write to file in a transaction:

       EXECUTE 'DELETE-FILE DATA F.TEMP'
       EXECUTE 'CREATE-FILE DATA F.TEMP 1 101 TYPE=J4'
       OPEN 'F.TEMP' TO F.TEMP ELSE ABORT 201, 'F.TEMP'
       TRANSTART ELSE
          CRT 'ERROR STARTING TXN'
          STOP
       END
       CRT TRANSQUERY()   ;* 1 - we're inside a transaction
       CRT SYSTEM(47)     ;* another method to check it
       V.REC.INIT = 'LINE 1' :@FM: 'LINE 2' :@FM: 'LINE 3'
       WRITE V.REC.INIT TO F.TEMP, 'REC1'
       EXECUTE 'LIST F.TEMP *A1 *A2 *A3'
       PROMPT 'Press any key to continue'
       INPUT DUMMY
       TRANSEND THEN CRT 'TXN WRITTEN'
       EXECUTE 'LIST F.TEMP *A1 *A2 *A3'

Until transaction is over -- no records will be shown:

<pre>
    LIST F.TEMP &lowast;A1 &lowast;A2 &lowast;A3
    &nbsp;
    DICT F.TEMP...    &lowast;A1...........    &lowast;A2...........    &lowast;A3...........
    &nbsp;
     No Records Listed
    &nbsp;
    Press any key to continue
    &nbsp;
    LIST F.TEMP &lowast;A1 &lowast;A2 &lowast;A3
    &nbsp;
    DICT F.TEMP...    &lowast;A1...........    &lowast;A2...........    &lowast;A3...........
    &nbsp;
    REC1              LINE 1            LINE 2            LINE 3
    &nbsp;
     1 Records Listed</pre>

### EXAMPLE 2

       EXECUTE 'DELETE-FILE DATA F.TEMP'
       EXECUTE 'CREATE-FILE DATA F.TEMP 1 101 TYPE=J4'
       OPEN 'F.TEMP' TO F.TEMP ELSE ABORT 201, 'F.TEMP'
       V.REC.INIT = 'LINE 1' :@FM: 'LINE 2' :@FM: 'LINE 3'
       WRITE V.REC.INIT TO F.TEMP, 'REC1'    ;* write before a transaction
       TRANSTART ELSE
          CRT 'ERROR STARTING TXN'
          STOP
       END
       WRITE V.REC.INIT TO F.TEMP, 'REC2'
       TRANSABORT THEN CRT 'TXN ABORTED'     ;* abandon the second write
       WRITE V.REC.INIT TO F.TEMP, 'REC3'    ;* write after a transaction
       EXECUTE 'LIST F.TEMP *A1 *A2 *A3'

Output:

<pre>
    LIST F.TEMP &lowast;A1 &lowast;A2 &lowast;A3
    &nbsp;
    DICT F.TEMP...    &lowast;A1...........    &lowast;A2...........    &lowast;A3...........
    &nbsp;
    REC1              LINE 1            LINE 2            LINE 3
    REC3              LINE 1            LINE 2            LINE 3
    &nbsp;
     2 Records Listed</pre>

## TRIM

<a name="TRIM"/>

TRIM statement allows characters to be removed from a string in a
number of ways.

### COMMAND SYNTAX

    TRIM(expression1 {, expression2{, expression3}})

### SYNTAX ELEMENTS

**expression1** specifies the string from which to trim characters.

**expression2** may optionally specify the character to remove from
the string. If not specified then the space character is assumed.

**expression3** evaluates to a single character specifies the type
of trim to perform.

### NOTES

The trim types available for expression3 are:

|Type | Operation                                               |
|-----|---------------------------------------------------------|
|L    | removes leading characters only                         |
|T    | removes trailing characters only                        |
|B    | removes leading and trailing characters                 |
|A    | removes all occurrences of the character                |
|R    | removes leading, trailing and redundant characters      |
|F    | removes leading spaces and tabs                         |
|E    | removes trailing spaces and tabs                        |
|D    | removes leading, trailing and redundant spaces and tabs.|

### EXAMPLES

       V.STRING = '   A   string  '
    * Get rid of leading spaces
       CRT '"' : TRIM(V.STRING, ' ', 'L') : '"'   ;*    "A   string  "
    * Get rid of trailing spaces
       CRT '"' : TRIM(V.STRING, ' ', 'T') : '"'   ;*    "   A   string"
    * Get rid of leading and trailing spaces
       CRT '"' : TRIM(V.STRING, ' ', 'B') : '"'   ;*    "A   string"
    * Get rid of leading, trailing and redundant spaces
       CRT '"' : TRIM(V.STRING, ' ', 'R') : '"'   ;*    "A string"
    * Get rid of leading zeroes
       CRT '"' : TRIM('000033', '0', 'L') : '"'   ;*    "33"

## TRIMB

TRIMB() function is equivalent to TRIM(expression, " ", "T")

## TRIMBS

<a name="TRIMBS"/>

TRIMBS function is used to remove all trailing spaces from each element
of dynamic.array.

### COMMAND SYNTAX

    TRIMBS(dynamic.array)

If dynamic.array evaluates to null (i.e. an empty string), null is returned.
If any element of dynamic.array is null, null is returned for that value.

### EXAMPLE

       dyn_array = ' Use    ' :@FM: ' the   ' :@VM: '' :@FM: 'source Luke   !  '
       CRT DQUOTE( OCONV( TRIMBS(dyn_array), 'MCP') )

Output:

<pre>
    " Use^ the]^source Luke   !"</pre>

### NOTE

Leading and redundant spaces are not removed.

## TRIMF

TRIMF() function is equivalent to TRIM(expression, " ", "L")

## TRIMFS

<a name="TRIMFS"/>

TRIMFS function is used to remove all leading spaces
from each element of dynamic.array.

### COMMAND SYNTAX

    TRIMFS(dynamic.array)

If dynamic.array evaluates to null (i.e. an empty string), null is returned.
If any element of dynamic.array is null, null is returned for that value.

### EXAMPLE

       dyn_array = ' Use    ' :@FM: ' the   ' :@VM: '' :@FM: 'source Luke   !  '
       CRT DQUOTE( OCONV( TRIMFS(dyn_array), 'MCP') )
       * Compare this with TRIMBS()
       CRT DQUOTE( OCONV( TRIMBS(dyn_array), 'MCP') )

Output:

<pre>
    "Use    ^the   ]^source Luke   !  "
    " Use^ the]^source Luke   !"</pre>

# jBC Functions and Statements (U - X)

## UNASSIGNED

<a name="UNASSIGNED"/>

UNASSIGNED function allows a program to determine whether a variable
has been assigned a value.

### COMMAND SYNTAX

    UNASSIGNED(variable)

### SYNTAX ELEMENTS

**variable** is the name of variable used elsewhere in the program.

### NOTES

The function returns Boolean TRUE if variable has not yet been
assigned a value. The function returns Boolean FALSE if variable
has already been assigned a value.

See also: [ASSIGNED](#ASSIGNED)

### EXAMPLES

       OPEN 'F.TEMP' TO F.TEMP ELSE
          EXECUTE 'CREATE-FILE DATA F.TEMP 1 101 TYPE=J4'
          OPEN 'F.TEMP' TO F.TEMP ELSE ABORT 201, 'F.TEMP'
       END
       CRT UNASSIGNED(F.TEMP)        ;* 0
       CLOSE F.TEMP
       CRT UNASSIGNED(F.TEMP)        ;* 1
       CRT UNASSIGNED(V.VAR)         ;* 1
       V.VAR = 5
       CRT UNASSIGNED(V.VAR)         ;* 0
       CLEAR
       CRT UNASSIGNED(V.VAR)         ;* 0 - it was assigned the value 0

## UNIQUEKEY

UNIQUEKEY returns a unique 36-byte character key.

### COMMAND SYNTAX

    UNIQUEKEY()

### SYNTAX ELEMENTS

The UNIQUEKEY() function will generate a UUID (Universally Unique IDentifier),
also known as GUID (Globally Unique IDentifier).

### EXAMPLE

       FOR V.I = 1 TO 5
          CRT FMT( DOWNCASE( FMT( UNIQUEKEY(), 'MX')),   \
                'L(########-####-####-############)')
       NEXT V.I

Sample output:

<pre>
    41505741-4141-4445-7935727a6a35
    41505741-4141-4445-7935727a6a36
    41505741-4141-4445-7935727a6a37
    41505741-4141-4445-7935727a6a38
    41505741-4141-4445-7935727a6a39</pre>

## UNLOCK

<a name="UNLOCK"/>

UNLOCK statement releases a previously LOCKed execution lock.

### COMMAND SYNTAX

    UNLOCK {expression}

### SYNTAX ELEMENTS

**expression** should evaluate to the number of a held execution lock,
for release.

If omitting expression then it releases all execution locks held by
the current program.

### NOTES

There is no action if the program attempts to release an execution l
ock that it had not taken.

See also: [LOCK](#LOCK)

### EXAMPLE

    LOCK 23 ; LOCK 32
    ......
    UNLOCK

## UDTEXECUTE

See also: [EXECUTE](#EXECUTE)

## UPCASE

<a name="UPCASE"/>

See: [DOWNCASE](#DOWNCASE)

## UTF8

<a name="UTF8"/>

UTF8 function converts a latin1 or binary string into the UTF-8
equivalent byte sequence.

### COMMAND SYNTAX

    UTF8(expression)

### SYNTAX ELEMENTS

The expression is expected to be a binary/latin1 code page string,
which is converted into a UTF-8 encoded byte sequence.

### EXAMPLE

       lat_line = CHAR(198) : CHAR(189) : CHAR(191)
       utf_line = UTF8(lat_line)
       FOR i = 1 TO 6 STEP 2
          CRT DTX( SEQ(utf_line[i,1]) ), DTX( SEQ(utf_line[i+1,1]) )
       NEXT i

The output of this program is:

<pre>
    C3 86 (latin capital letter ae)
    C2 BD (vulgar fraction one half)
    C2 BF (inverted question mark)</pre>

### NOTE

To run this example the following environment variables are to be set:

<pre>
    JBASE_I18N=1
    JBASE_CODEPAGE=utf8</pre>

## WAKE

<a name="WAKE"/>

WAKE statement is used to wake a suspended process, which has
executed a [PAUSE](#PAUSE) statement.

### COMMAND SYNTAX

    WAKE PortNumber

### SYNTAX ELEMENTS

**PortNumber** is a reference to awaken the target port. The WAKE
statement has no effect on processes, which do not execute the PAUSE
statement.

## WEOF

WEOF statement allows the program to write an EOF mark on an attached
tape device.

### COMMAND SYNTAX

    WEOF { ON expression }

### SYNTAX ELEMENTS

**expression** specifies the device channel to use. It should evaluate
to a numeric integer argument in the range 0-9, the default value is
zero.

### NOTES

If the WEOF fails it then executes the statements associated with
any ELSE clause. SYSTEM(0) will return the reason for the failure
as follows:

| Code | Description                                |
|------|--------------------------------------------|
|1     | There is no media attached to the channel. |
|2     | End of media found.                        |


A "tape" does not refer to magnetic tape devices only but to any
device described previously to TAFC.

If the specified channel has no assigned tape device, it enters the
TAFC debugger with an appropriate message.

### EXAMPLE

    WEOF ON 5 ELSE
        CRT "No tape device exists for channel 5"
    END

## WEOFSEQ

WEOFSEQ truncates a file opened for sequential access.

### COMMAND SYNTAX

    WEOFSEQ FileVar { THEN | ELSE Statements }

### SYNTAX ELEMENTS

**FileVar** specifies the file descriptor of the file opened for
sequential access.

**Statements** are conditional jBC statements.

### NOTES

WEOFSEQ forces truncation of the file at the current file pointer;
nothing is actually written to the sequential file.

### EXAMPLE

       out_dir = '.'
       out_file = 'report.txt'
    &nbsp;
       OPENSEQ out_dir, out_file TO f_out THEN
          CRT 'TARGET FILE EXISTS. OVERWRITE[Y/N]':
          CLEARINPUT          ;* don't take anything in advance
          INPUT reply
          IF UPCASE(reply) NE 'Y' THEN         ;* y or Y
    * exit - user refused to overwrite the file
             STOP             ;* or RETURN
          END
          WEOFSEQ f_out  ;* truncate the file
       END
    &nbsp;
    * We don't need to explicitly create a file; as soon as the first
    * WRITESEQ will be issued - file will be created, otherwise it won't be -
    * "openseq_creates" isn't set to "true" for Prime emulation.
    &nbsp;
    * Processing loop starts
       line_no = 0
       LOOP
          line_no ++
    &nbsp;
    * Provide a way to exit a loop
          IF line_no GT 7 THEN BREAK
    &nbsp;
    * Get an output string into variable and...
          line = 'Line ' : line_no
    * ...either skip it...
          IF line_no EQ 3 THEN CONTINUE
    * ...or write it
          WRITESEQ line TO f_out ELSE
    * Write error - notify user and quit the program
             CRT 'Write error'
             STOP             ;* or RETURN
          END
       REPEAT
    &nbsp;
    * truncate the file at certain position
       SEEK f_out, -5, 2 ELSE CRT 'Seek error'  ;  STOP
       WEOFSEQ f_out
       CLOSESEQ f_out

Contents of file report.txt:

<pre>
    Line 1
    Line 2
    Line 4
    Line 5
    Line 6
    Li</pre>

## WRITE

<a name="WRITE"/>

WRITE statement allows a program to write a record into a previously
opened file.

### COMMAND SYNTAX

    WRITE variable1 ON | TO {variable2,} expression { SETTING setvar }  \
          { ON ERROR statements }

### SYNTAX ELEMENTS

**variable1** is the identifier containing the record to be written.

**variable2**, if specified, should be a previous opened jBC
variable to a file using the OPEN statement. If not specifying
variable2 then it assumes the default file.

The expression should evaluate to a valid record key for the
file.

If specifying the SETTING clause and the write fails, it sets
setvar to one of the following values:

### INCREMENTAL FILE ERRORS

| Code  | Description                           |
|-------|---------------------------------------|
|128    |    No such file or directory          |
|4096   |    Network error                      |
|24576  |    Permission denied                  |
|32768  |    Physical I/O error or unknown error|

### NOTES

If holding a lock on the record by this process, it is released
by the WRITE.
If you wish to retain a lock on a record, you should do so
explicitly with the [WRITEU](#WRITEU) statement.

### EXAMPLE

       OPEN 'F.TEMP' TO F.TEMP THEN
          NULL
       END ELSE
          EXECUTE 'CREATE-FILE DATA F.TEMP 1 101 TYPE=J4'
          OPEN 'F.TEMP' TO F.TEMP ELSE ABORT 201, 'F.TEMP'
       END
       V.REC.INIT = 'LINE 1' :@FM: 'LINE 2' :@FM: 'LINE 3'
       WRITE V.REC.INIT TO F.TEMP, 'REC1'
       CLOSE F.TEMP

## WRITEBLK

<a name="WRITEBLK"/>

WRITEBLK statement writes a block of data to a file opened for
sequential processing.

### COMMAND SYNTAX

    WRITEBLK expression ON | TO file.variable { THEN statements [ ELSE statements ] \
           | ELSE statements}

### SYNTAX ELEMENTS

Each WRITEBLK statement writes the value of expression starting
at the current position in the file. The current position is
incremented to beyond the last byte written. WRITEBLK does not
add a new line at the end of the data.

**file.variable** specifies a file opened for sequential processing.

The value of expression is written to the file, and the THEN
statements are executed. If no THEN statements are specified,
program execution continues with the next statement. If the file
is neither accessible or does not exist, it executes the ELSE
statements; and ignores any THEN statements.

If either expression or file.variable evaluates to null, the WRITEBLK
statement fails and the program enters the debugger with a run-time
error message.

### INTERNATIONAL MODE

When using the WRITEBLK statement in International Mode, care must be
taken to ensure that the write variable is handled properly before the
WRITEBLK statement. The WRITEBLK statement expects the output variable
to be in "bytes", however when manipulating variables in International
Mode character length rather than byte lengths are usually used and
hence possible confusion or program malfunction can occur. If
requiring byte count data the output variable can be converted from
the UTF-8 byte sequence to 'binary/latin1' via the LATIN1 function.

It is not recommended that you use the [READBLK](#READBLK)/
[WRITEBLK](#WRITEBLK) statements when executing in International Mode.
You can obtain similar functionality via the [READSEQ](#READSEQ)/
[WRITESEQ](#WRITESEQ) statement, which can be used to read/write,
characters a line at a time from a file.

### NOTE

We have to explicitly create the output file if it doesnt exist (we didnt have to with
WRITESEQ, for example, under *prime* emulation).

### EXAMPLE

    * Create a file with random name and write to it
       V.ID = ''
       FOR V.J = 1 TO 8
          V.RND = RND(26) + 65
          V.ID := CHAR(V.RND)        ;* A...Z
       NEXT V.J
       V.ID := '.txt'
       OPENSEQ '.', V.ID TO  F.FILE.OUT THEN
          WEOFSEQ F.FILE.OUT  ;* truncate the file
       END ELSE  ;* will have to create - WRITEBLK wouldn't do that
          CREATE F.FILE.OUT ELSE
             CRT 'FILE CREATION FAILURE'
             STOP
          END
       END
       V.BUFFER = 'LINE 1' : CHAR(10) : 'LINE 2' : CHAR(10) : 'LINE 3'
       WRITEBLK V.BUFFER TO F.FILE.OUT ELSE
          CRT 'WRITE ERROR'
          STOP
       END
       CRT 'File ' : V.ID :  ' created'
       CLOSESEQ F.FILE.OUT
       STOP
    END

## WRITELIST

<a name="WRITELIST"/>

WRITELIST allows the program to store a list held in a jBC variable to
the global list file.

### COMMAND SYNTAX

    WRITELIST variable ON | TO expression { SETTING setvar } { ON ERROR statements }

### SYNTAX ELEMENTS

**variable** is the variable in which the list is held.

**expression** should evaluate to the required list name. If expression
is null, it writes the list to the default external list.

If the SETTING clause is specified and the write fails, it sets setvar
to one of the following values:

### INCREMENTAL FILE ERRORS

| Code  | Description                           |
|-------|---------------------------------------|
|128    |    No such file or directory          |
|4096   |    Network error                      |
|24576  |    Permission denied                  |
|32768  |    Physical I/O error or unknown error|

### NOTE

See also: [DELETELIST](#DELETELIST), [READLIST](#READLIST),
[FORMLIST](#FORMLIST)

### EXAMPLE

       EXECUTE 'SELECT . SAMPLE 5' RTNLIST V.LIST
       WRITELIST V.LIST TO 'SOME-FILES'
       GETLIST 'SOME-FILES' TO V.FILES.L ELSE NULL
       CRT OCONV( V.FILES.L, 'MCP' )  ;* e.g. &COMO&^&COMO&]D^&ED&^&ED&]D^&PH&

## WRITESEQ

<a name="WRITESEQ"/>

WRITESEQ writes data to a file opened for sequential access.

### COMMAND SYNTAX

    WRITESEQ Expression { APPEND } ON | TO FileVar THEN | ELSE statements

### SYNTAX ELEMENTS

**Variable** specifies the variable to contain next record from sequential
file.

**FileVar** specifies the file descriptor of the file opened for sequential
access.

**Statements** are conditional jBC statements

### NOTES

Each WRITESEQ writes the data on a line of the sequentially opened file.
Each data is suffixed with a new line character. After each WRITESEQ, the
file pointer moves forward to the end of line. The WRITESEQF statement
forces each data line to be flushed to the file when it is written. The
APPEND option forces each WRITESEQ to advance to the end of the file
before writing the next data line.

### EXAMPLES

Create a file and write to it (overwriting contents each time):

       V.ID = 'report.txt'
       OPENSEQ '.', V.ID TO F.FILE.OUT THEN
          WEOFSEQ F.FILE.OUT  ;* truncate the file
       END
       WRITESEQ 'LINE 1' TO F.FILE.OUT ELSE
          CRT 'WRITE ERROR'
          STOP
       END
       CRT 'File ' : V.ID :  ' written'
       CLOSESEQ F.FILE.OUT

Append data to file:

       V.DIR.OUT = '.'
       V.FILE.OUT = 'time.log'
       OPENSEQ V.DIR.OUT, V.FILE.OUT TO F.FILE.OUT THEN NULL
       WRITESEQ TIMEDATE() APPEND TO F.FILE.OUT ELSE
          CRT 'Write error'
          STOP
       END

If file was opened in read only mode, WRITESEQ will fail and statements defined
after ELSE clause will be processed:

       IF NOT( GETENV('TAFC_HOME', tafc_home) ) THEN
          CRT 'TAFC_HOME not defined'
          STOP
       END
       //
       log_dir = tafc_home : '/tmp'
       log_file = 'jbase_error_trace'
       //
       OPENSEQ log_dir, log_file READONLY TO f_log THEN
       //
          FOR i = 1 TO 3   ;* read the first message
             READSEQ the_line FROM f_log ELSE BREAK
             CRT the_line
          NEXT i
       //
          WRITESEQ 'One more line' APPEND TO f_log ELSE
             CRT 'Write error'
             STOP
          END
       END ELSE
          CRT 'jbase_error_trace not found'
       END

Sample output:

<pre>
    &nbsp;
    Trace message from pid 3588 port 237 at 'Mon May 28 14:02:41 2012'
        Port 1 (Pid 6184) has been inactive for 34317875 seconds, Port cleared
    Write error</pre>

## WRITESEQF

<a name="WRITESEQF"/>

WRITESEQF statement is used to write new lines to a file opened for
sequential processing, and to ensure that data is physically written to
disk (that is, not buffered) before the next statement in the program is
executed.

### COMMAND SYNTAX

    WRITESEQF expression { ON | TO } file.variable [ ON ERROR statements ]  \
              { THEN statements [ ELSE statements ] | ELSE statements }

The sequential file must be open, and the end-of-file marker must be
reached before you can write to the file. You can use the
[FILEINFO](#FILEINFO) function to determine the number of the line
about to be written.

Normally, when you write a record using the [WRITESEQ](#WRITESEQ)
statement, the record is moved to a buffer that is periodically
written to disk. If a system failure occurs, you could lose all
the updated records in the buffer. The WRITESEQF statement forces
the buffer contents to be written to disk; the program does not
execute the statement following the WRITESEQF statement
until the buffer is successfully written to disk.

A WRITESEQF statement following several WRITESEQ
statements ensures that all buffered records are written to disk.
WRITESEQF is intended for logging applications and should not
be used for general programming. It increases the disk I/O of
your program and therefore degrades performance. file.variable
specifies a file opened for sequential access.

The value of expression is written to the file as the next line,
and the THEN statements are executed. If THEN statements are not
specified, program execution continues with the next statement;
if the specified file cannot be accessed or does not exist, the
ELSE statements are executed; any THEN statements are ignored.

If expression or file.variable evaluates to the null value, the
WRITESEQF statement fails and the program terminates with a
run-time error message.

*The ON ERROR Clause*

The ON ERROR clause is optional in the WRITESEQF statement. Its
syntax is the same as that of the ELSE clause. The ON ERROR clause
lets you specify an alternative for program termination when a
fatal error is encountered while the WRITESEQF statement is being
processed.

## WRITET

<a name="WRITET"/>

WRITET statement enables data to be written to a range of tape
devices between 0-9.

### COMMAND SYNTAX

    WRITET variable { ON | TO expression } THEN | ELSE statements

### SYNTAX ELEMENTS

**variable** is the variable that holds the data for writing to
the tape device.

**expression** should evaluate to an integer value in the range
0-9 and specifies from which tape channel to read the data. If
the ON clause is not specified the WRITET will assume channel 0.

If the WRITET fails then the statements associated with any ELSE
clause will be executed. SYSTEM(0) will return the reason for
the failure as follows:

| Code | Description                                |
|------|--------------------------------------------|
|1     | There is no media attached to the channel. |
|2     | End of media found.                        |

### NOTES

A "tape" does not refer to magnetic tape devices only but any
device that has been described to TAFC. Writing device descriptors
for TAFC is beyond the scope of this documentation.

If no tape device has been assigned to the specified channel the
TAFC debugger is entered with an appropriate message.

Where possible the record size is not limited to a single tape
block and the entire record will be written blocked to whatever
block size has been allocated by the T-ATT command. However,
certain devices do not allow TAFC to accomplish this (SCSI
tape devices for instance).

### EXAMPLE

    LOOP
       WRITET TapeRec ON 5 ELSE
          Reason = SYSTEM(0)
          IF Reason = 2 THEN BREAK ;* done
          CRT "ERROR"  ;  STOP
       END
    REPEAT

## WRITEU

<a name="WRITEU"/>

WRITEU statement allows a program to write a record into a
previously opened file. An existing record lock will be
preserved.

### COMMAND SYNTAX

    WRITEU variable1 ON | TO {variable2,} expression { SETTING setvar }  \
           { ON ERROR statements }

### SYNTAX ELEMENTS

**variable1** is the identifier holding the record to be
written.

**variable2**, if specified, should be a jBC variable that
has previously been opened to a file using the OPEN statement.
If variable2 is not specified then the default file is assumed.

The expression should evaluate to a valid record key for the file.

If the SETTING clause is specified and the write fails, setvar
will be set to one of the following values:

### INCREMENTAL FILE ERRORS

| Code  | Description                           |
|-------|---------------------------------------|
|128    |    No such file or directory          |
|4096   |    Network error                      |
|24576  |    Permission denied                  |
|32768  |    Physical I/O error or unknown error|

### NOTES

If the statement fails to write the record then any statements
associated with the ON ERROR clause is executed.

The lock maintained by the [WRITEU](#WRITEU) statement will be
released by any of the following events:

The same program with [WRITE](#WRITE), [WRITEV](#WRITEV) or
[MATWRITE](#MATWRITE) statements writes to the record.

The record lock is released explicitly using the
[RELEASE](#RELEASE) statement.

The program stops normally or abnormally.

See also: [READU](#READU), [MATREADU](#MATREADU),
[RELEASE](#RELEASE)

### EXAMPLE

       OPEN 'F.TEMP' TO F.TEMP ELSE
          EXECUTE 'CREATE-FILE DATA F.TEMP 1 101 TYPE=J4'
          OPEN 'F.TEMP' TO F.TEMP ELSE
             CRT 'OPEN FAILED'
             STOP
          END
       END
       READU V.REC FROM F.TEMP, 'REC1' LOCKED
          CRT 'Lock failure'
          STOP
       END ELSE NULL
       V.REC<-1> = 'A field'
       CRT RECORDLOCKED(F.TEMP, 'REC1')  ;* 2 - "Locked by this process by a READU"
       WRITEU V.REC TO F.TEMP, 'REC1'
       CRT RECORDLOCKED(F.TEMP, 'REC1')  ;* still 2
       RELEASE F.TEMP, 'REC1'
       CRT RECORDLOCKED(F.TEMP, 'REC1')  ;* 0 - not locked

## WRITEV

<a name="WRITEV"/>

WRITEV statement allows a program to write a specific field
of a record in a previously opened file.

### COMMAND SYNTAX

    WRITEV variable1 ON | TO {variable2,} expression1, expression2  \
         { SETTING setvar } { ON ERROR statements }

### SYNTAX ELEMENTS

**variable1** is the identifier holding the record to be written.

**variable2**, if specified, should be a jBC variable that
has previously been opened to a file using the OPEN statement.
If variable2 is not specified then it assumes the default file.

**expression1** should evaluate to a valid record key for the file.

**expression2** should evaluate to a positive integer number. If
the number is greater than the number of fields in the record, it
will add null fields to variable1. If expression2 evaluates to a
non-numeric argument, it will generate a run time error.

If the SETTING clause is specified and the write fails, it sets
setvar to one of the following values:

### INCREMENTAL FILE ERRORS

| Code  | Description                           |
|-------|---------------------------------------|
|128    |    No such file or directory          |
|4096   |    Network error                      |
|24576  |    Permission denied                  |
|32768  |    Physical I/O error or unknown error|

### NOTES

The WRITEV statement will cause the release of any lock held on
the record by this program. If you wish to retain a lock on the
record, do so explicitly with the WRITEVU statement.

### EXAMPLE

       EXECUTE 'DELETE-FILE DATA F.TEMP'
       EXECUTE 'CREATE-FILE DATA F.TEMP 1 101 TYPE=J4'
       OPEN 'F.TEMP' TO f_temp ELSE ABORT 201, 'F.TEMP'
       new_rec = 'LINE 1' :@FM: 'LINE 2' :@FM: 'LINE 3'
       WRITE new_rec TO f_temp, 'REC1'
       WRITEV 'LINE 2v2' TO f_temp, 'REC1', 2 ON ERROR
          CRT 'WRITEV error'
          STOP
       END
       EXECUTE "I-DUMP F.TEMP 'REC1'"     ;* "REC1^LINE 1^LINE 2v2^LINE 3^"
       WRITEV 'LINE 7' TO f_temp, 'REC1', 7 ON ERROR
          CRT 'WRITEV error'
          STOP
       END
       EXECUTE "I-DUMP F.TEMP 'REC1'"     ;* "REC1^LINE 1^LINE 2v2^LINE 3^^^^LINE 7^"

## WRITEVU

<a name="WRITEVU"/>

WRITEVU statement allows a program to write a specific field on a
record in a previously opened file. An existing record lock will
be preserved.

### COMMAND SYNTAX

    WRITEVU variable1 ON | TO {variable2,} expression1, expression2  \
          { SETTING setvar } { ON ERROR statements }

### SYNTAX ELEMENTS

**variable1** is the identifier holding the record to be written.

**variable2**, if specified, should be a jBC variable that has
previously been opened to a file using the OPEN statement. If
variable2 is not specified then the default file is assumed.

**expression1** should evaluate to a valid record key for the file.

**expression2** should evaluate to a positive integer number; if the
number is greater than the number of fields in the record, null fields
will be added to variable1. If expression2 evaluates to a non-numeric
argument, a run time error will be generated.

If the SETTING clause is specified and the write fails, it sets setvar
to one of the following values:

### INCREMENTAL FILE ERRORS

| Code  | Description                           |
|-------|---------------------------------------|
|128    |    No such file or directory          |
|4096   |    Network error                      |
|24576  |    Permission denied                  |
|32768  |    Physical I/O error or unknown error|

### NOTES

If the statement fails to write the record, it executes any statements
associated with the ON ERROR clause.

Any of the following events will release the lock taken by the
[WRITEVU](#WRITEVU) statement:

The same program with [WRITE](#WRITE), [WRITEV](#WRITEV) or
[MATWRITE](#MATWRITE) statements writes to the record.

By explicitly using the [RELEASE](#RELEASE) statement, it
releases the record lock.

The program stops normally or abnormally.

See also: [MATWRITEU](#MATWRITEU), [RELEASE](#RELEASE),
[WRITE](#WRITE), [WRITEU](#WRITEU).

### EXAMPLE

    OPEN "Customers" ELSE ABORT 201, "Customers"
    OPEN "DICT Customers" TO DCusts ELSE
       ABORT 201, "DICT Customers"
    END
    WRITEVU Rec ON DCusts, 'Xref', 1 SETTING Err ON ERROR
       CRT "I/O Error[" :Err: "]"
       ABORT
    END

## WRITEXML

<a name="WRITEXML"/>

Use WRITEXML to write an XML record to a hashed file.

### COMMAND SYNTAX

    WRITEXML rec ON file,id ELSE statements | ON ERROR statements

Writes a dynamic array in xml format using a style sheet from the
DICT; transforms the XML into a dynamic array before being written to
the file.

The transform takes place using the style sheet in DICT (record @WRITEXML).

### EXAMPLE

    WRITEXML rec ON file,id ON ERROR CRT "Broken! " : rec

## XLATE

<a name="XLATE"/>

The XLATE function will return the data value of a field, given the
name of the file, the record key, the field number, and an action code.

### COMMAND SYNTAX

    XLATE([ DICT ] filename, key, field#, action.code)

### SYNTAX ELEMENTS

DICT is the literal string to be placed before the file name in the
event it is desired to open the dictionary portion of the file, rather
than the data portion.

filename is a string containing the name of the file to be accessed.
Note that it is the actual name of the file, and not a file unit
variable.  This function requires the file name, regardless of whether
or not the file has been opened to a file unit variable.

key is an expression that evaluates to the record key, or item ID,
of the record from which data is to be accessed.

field# is the field number to be retrieved from the record.

action.code indicates the procedure if the field is null, or cannot
find the if record.  This is a literal.  The valid codes are:

| Code | Description                                          |
|------|------------------------------------------------------|
|X     | Returns a null string. This is the default action.   |
|V     | Prints an error message.                             |
|C     | Returns the value of key.                            |

### NOTES

If the field being accessed is a dynamic array, XLATE will return the
array with the delimiter characters lowered by 1.   For example,
multivalue marks (ASCII-253) are returned as subvalue marks (ASCII-252),
and subvalue marks are returned as text marks (ASCII-251).
If you supply -1 for field#, it returns the entire record.
The XLATE function is the same as the [TRANS](#TRANS) function.

### EXAMPLE

Retrieval of a simple field:  Given a file called "VENDORS" containing
a record with the record key of "12345" and which contains the value of
"ABC Company" in field 1,

    VENDOR.ID = "12345"
    VENDOR.NAME = XLATE('VENDORS', VENDOR.ID, 1, 'X')
    CRT VENDOR.NAME

will display: ABC Company

Retrieval of an array:  Suppose field 6 of the VENDORS file contains a
multivalued list of purchase order numbers, such as

<pre>
    10011]10062]10079</pre>

use the XLATE function to retrieve it:

    PO.LIST = XLATE('VENDORS', VENDOR.ID, 6, 'X')
    CRT PO.LIST

will display: 10011\10062\10079

Notice that the backslashes (\) were substituted for brackets (]), indicating
that the delimiter is now CHAR(252).

Retrieval of an entire dictionary item:  Given a dictionary item called
"VENDOR.NAME" with the following content:

<pre>
    001 A
    002 1
    003 Vendor Name
    004
    005
    006
    007
    008
    009 L
    010 30</pre>

these statements

    DICT.ID = "VENDOR.NAME"
    DICT.REC = XLATE('DICT VENDORS', VENDOR.ID, -1, 'C')
    PRINT DICT.REC

will display

<pre>
    A]1]Vendor Name]]]]]L]30</pre>

## XMLTODYN##

<a name="XMLTODYN"/>

XMLTODYN converts the XML to a dynamic array using the optional XSL.

### COMMAND SYNTAX

    XMLTODYN(XML, XSL, result)

### SYNTAX ELEMENTS

Array = XMLTODYN(XML,XSL,result)

If result = 0 Array will contain a dynamic array built from the xml / xsl

If result <> 0, Array will contain an error message

There is no requirement for xsl if you are reconverting from generic xml
to dynarray

    a = "Tom" : @AM : "Dick" : @AM : "Harry"
    xml = DYNTOXML(a, '', result)
    b = XMLTODYN(xml, '', result
    CRT CHANGE(b, @AM, ' ')

Screen output:

<pre>
    Tom Dick Harry</pre>

If passing a stylesheet in the second parameter, it performs a transform
to give a different format of the array.

*XML CONTENTS*

<pre>
    &lt;?xml version="1.0" encoding="UTF-8"?&gt;
    &lt;mycustomer&gt;
      &lt;firstname&gt;Tom&lt;/firstname&gt;
      &lt;lastname&gt;Dick&lt;/lastname&gt;
      &lt;address&gt;Harry&lt;/address&gt;
    &lt;/mycustomer></pre>

### EXAMPLE

    a = XMLTODYN(xml, xsl, rc)
    CRT CHANGE(a, @AM, ' ')

### XSL CONTENTS

<pre>
    &lt;xsl:template match="mycustomer"&gt;
    &lt;array&gt;
    &lt;xsl:apply-templates/&gt;
    &lt;/array&gt;
    &lt;/xsl:template&gt;
    &lt;xsl:template match="firstname"&gt;
    &lt;data&gt;
    &lt;xsl:attribute name="attribute"&gt;1&lt;/xsl:attribute&gt;
    &lt;xsl:attribute name="value"&gt;
	  &lt;xsl:number level="single"/&gt;
    &lt;/xsl:attribute&gt;
    &lt;xsl:attribute name="subvalue"&gt;1&lt;/xsl:attribute&gt;
    &lt;xsl:value-of select="."/&gt;
    &lt;/data&gt;
    &lt;/xsl:template&gt;
    Etc</pre>

## XMLTOXML

<a name="XMLTOXML"/>

XMLTOXML transforms the XML using the XSL.

### COMMAND SYNTAX

    XMLTOXML(xml,xsl,result)

### SYNTAX ELEMENTS

If result=0, newxml will contain a transformed version of xml using xsl.

If result=1, newxml will hold an error message.

*XSL CONTENTS*

<pre>
    &lt;?xml version="1.0" ?&gt;
    &lt;xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"&gt;
    &lt;xsl:template match="person"&gt;
    &lt;p&gt;&lt;xsl:value-of select="name" /&gt;&lt;/p&gt;
    &lt;/xsl:template&gt;
    &lt;/xsl:stylesheet&gt;</pre>

*XML CONTENTS*

<pre>
    &lt;list&gt;
    &lt;person&gt;
	    &lt;name&gt;Bob&lt;/name&gt;
    &lt;/person&gt;
    &lt;person&gt;
	    &lt;name&gt;Amy&lt;/name&gt;
    &lt;/person&gt;
    &lt;/list&gt;</pre>

### EXAMPLE

    newxml = XMLTOXML(xml,xsl,rc)
    CRT newxml

*SCREEN OUTPUT*

<pre>
    &lt;p&gt;Bob&lt;/p&gt;&lt;p&gt;Amy&lt;/p&gt;</pre>

## XTD

<a name="XTD"/>

XTD function converts hexadecimal numbers into its decimal equivalent.

### COMMAND SYNTAX

    XTD(expression)

### SYNTAX ELEMENTS

**expression** should evaluate to a valid hexadecimal string.

### NOTES

The conversion process will halt at the first character that is not a
valid base 16 character in the set [0-9, A-F or a-f].

See also: [DTX](#DTX).

### EXAMPLES

       CRT XTD('FF')                                          ;* 255
       CRT FMT( DTX(13), 'R%2' ) : FMT( DTX(10), 'R%2' )      ;* 0D0A
       CRT XTD('BADBEEF')  ;*  195935983 (binary: 00001011101011011011111011101111)
       CRT XTD('DEADBEEF') ;* -559038737 (binary: 11011110101011011011111011101111)
       CRT XTD('1aGHI')    ;* 26 - stopped after processing "1a"
       CRT XTD('GHI')      ;* 0

### NOTE

Negative result in line 4 is caused by the first bit of binary result
being set.

# Embedded SQL for jBC

## Introduction to embedded SQL

The name "SQL" is an abbreviation for "Structured Query Language". The
SQL language enables the defining, manipulating and controlling of data
in a relational database. A relational database is a database that
appears to the user as a collection of tables. A table is defined to be
an unordered collection of rows. Finally the SQL terminology tends to
refer to records as rows and fields within a record as columns within a
row.

Embedded SQL is a version of SQL designed for direct incorporation into
hosts programs or specifically in the case of jBASE, into jBC programs.

An Embedded SQL jBC program contains normal jBC code statements plus an
Embedded SQL declare section, zero or more embedded cursor definitions,
zero or more embedded exception declarations and one or more Embedded
SQL statements.

Embedded SQL declarations, definitions and statements are prefixed by
the reserved words EXEC SQL. This part of the Embedded SQL standard
also enables the jBC preprocessor to recognize and distinguish SQL
statements from the normal jBC code statements. The Embedded SQL
statements are terminated by a semicolon.

Embedded SQL statements can include references to jBC variables. The
jBC variables must be prefixed with a colon to distinguish them from
SQL column names. The jBC variables cannot be qualified or subscripted
and must refer to scalars, i.e. character strings or numbers, not
arrays or expressions.

All jBC variables that will be referenced in Embedded SQL statements
must be defined within an Embedded SQL declare section, the jBC
variable definitions are limited to simple forms. i.e. no expressions
or arrays.

An Embedded SQL cursor must not appear in an Embedded SQL statement
before it has been defined by an Embedded SQL cursor definition.

Any jBC variables that will be referenced in Embedded SQL statements
must have a data type that is compatible with the SQL data type of
the column with which they are to be compared or assigned. However
this requirement does not prevent jBC variables from using the same
name as Embedded SQL column references.

Embedded SQL statement exceptions can be handled either by utilizing
the SYSTEM(0) function or predetermined by the SQL WHENEVER statement.

The following jBC code provides an example of using Embedded SQL for
Oracle.

PartEntry.b listing (Oracle)

<pre>
    *
    *
    * Declare jBC vars to use in Embedded SQL statements ( A )
    *
    *
    EXEC SQL BEGIN DECLARE SECTION ;
    INT PartNo ;
    STRING(20) PartName ;
    STRING(16) User ;
    STRING(16) Passwd ;
    EXEC SQL END DECLARE SECTION ;
    *
    * Predetermine action on SQLERROR ( B )
    *
    EXEC SQL WHENEVER SQLERROR DO SQL_ERROR() ;
    *
    * Connect to database supplying user and password ( C )
    *
    User = "demo" ; Passwd = "demo99"
    EXEC SQL CONNECT :User IDENTIFIED BY :Passwd ;
    *
    * Create Parts table ( D )
    *
    EXEC SQL CREATE TABLE Parts
    (
    PartNo INTEGER NOT NULL PRIMARY KEY,
    PartName CHAR(20)
    );
    *
    * Loop until no more PartNos
    *
    LOOP
    *
    * Prompt for PartNo
    *
        CRT "Part Number :":
        INPUT PartNo
    WHILE PartNo NE '' DO
    *
    *
    * Prompt for PartName
    *
        CRT "Part Name :":
        INPUT PartName
    *
    * Add PartNo and PartName into Parts table ( E )
    *
        EXEC SQL INSERT INTO Parts VALUES (:PartNo, :PartName ) ;
    REPEAT
    *
    *
    * Commit updates to database ( F )
    *
    *
    EXEC SQL COMMIT ;</pre>

( A ) Declare jBC variables to use within Embedded SQL statements

This section declares jBC variables so that they can be used within
Embedded SQL statements. All references to jBC within the Embedded SQL
statement must be prefixed by a colon. This feature of the Embedded SQL
standard is used by the jBC preprocessor to identify jBC variables when
parsing the Embedded SQL statement. The jBC variables must be the same
data type as the source or target Embedded SQL columns.

( B ) Predetermine action on SQLERROR

This section configures the action to take on detecting an error with the
previous executed Embedded SQL statement. Every SQL statement should in
principle be followed by a test of the returned SQLCODE value. This can be
achieved by utilizing the SYSTEM(0) function, which returns the result of
the last SQL statement, or alternatively using the Embedded SQL WHENEVER
statement to predetermine the action for all subsequent Embedded SQL
statements. The SYSTEM(0) function will return three different possible
values.

| Code | Description                         |
|------|-------------------------------------|
|<0    |  Embedded SQL statement failed.     |
|0     |  Embedded SQL statement successful. |
|100   |  NOT FOUND. No rows where found.    |

The format of the Embedded SQL WHENEVER statement is as follows:

**EXEC SQL WHENEVER Condition Action ;**

Where

| Value        | Description                                              |
|--------------|----------------------------------------------------------|
|  Condition   |NOT FOUND                                                 |
|              |SQLERROR                                                  |
|              |                                                          |
|  Action      |DO Function - Oracle implementation.                      |
|              |                                                          |
|              |CALL Function - Ingres and Informix implementations.      |
|              |                                                          |
|              |GOTO proglab_Label - IBM DB2 and Microsoft SQL Server     |
|              |implementations.                                          |
|              |CONTINUE                                                  |
|              |                                                          |
|  Function    |User defined function.                                    |
|              |                                                          |
|              |SQLERROR() - Display Embedded SQL error then return to    |
|              |program.                                                  |
|              |SQLABORT() - Display Embedded SQL error then exit program.|
|              |                                                          |
|  Label       |Label in executing program:                               |
|              |                                                          |
|              |  DOSQLERR:                                               |
|              |  DEFC INT SQL_ERROR                                      |
|              |  CALL SQL_ERROR                                          |
|              |  STOP                                                    |
|              |                                                          |

( C ) Connect to database supplying user and password
This section connects the specified user and password combination to
the SQL database. This command can be Embedded SQL implementation
dependent. The user must be correctly configured for the target
database.

( D ) Create Parts table.
This section creates an SQL table called Parts. The table has two
constituent data types, these are defined as an integer value PartNo
and a character string PartName. The PartNo is defined as a non null
unique value and is defined as the primary key. This definition
provides a close match to the usual format of a record and id. The
only data type that is truly common to all hosts and their languages
is fixed length character strings, the integer value used here is
for demonstration purposes and is not recommended.

( E ) Add PartNo and PartName into table Parts.
This Embedded SQL statement inserts the values entered for PartNo
and PartName into the SQL table Parts. PartNo is inserted as the
first column whereas PartName is inserted as the second column of
each row. Effectively PartNo is the record id and PartName is the
first field in the record PartNo. The jBC pre-processor parses the
Embedded SQL statements and provides code to convert any specified
jBC variables to the format required by the Embedded SQL
implementation. Any returned parameters are then converted back
into jBC variables.

( F ) Commit updates to database.
This Embedded SQL statement makes all updates by Embedded SQL
statements since the last SQL commit statement visible to other
users or programs on the database. If a program executes an Embedded
SQL statement and no transaction is currently active then one is
automatically started. Each subsequent SQL statement update by the
same program without an intervening commit or rollback, is considered
part of the same transaction. A transaction terminates by either an
Embedded SQL COMMIT, normal termination, or an Embedded SQL ROLLBACK
statement, abnormal termination. An abnormal termination does not
change the database with respect to any of the Embedded SQL updates
executed since the last commit or rollback. Database updates made by
a given transaction do not become visible to any other distinct
transaction until and unless the given transaction completes with
a normal termination. i.e. an Embedded SQL COMMIT statement.

## EMBEDDED SQL COMPILER OPTION

In order to compile jBC programs containing Embedded SQL statements the
TAFC compiler option "Jq" must be invoked with the jBC compiler command.
The "Jq" option also expects an SQL implementation specifier, as
described below.

|-Jq<type>  |  RDBMS                                 |
|-----------|----------------------------------------|
|  d        |  IBM DB2                               |
|  m        |  Microsoft SQL Server (Windows only)   |
|  o        |  Oracle                                |
|  I        |  Ingres                                |
|  S        |  Sybase                                |
|  X        |  Informix                              |

e.g. To compile the jBC example program PartEntry.b for an Oracle SQL
implementation database.

<pre>
    jcompile -Jqo PartEntry.b</pre>

In this example the SQL specifier is "o" for Oracle. Other specifiers
are added as and when Embedded SQL implementations are required. e.g.
The "i" option informs the TAFC compiler to invoke mechanisms for the
Ingres Embedded SQL implementation. Although the Embedded SQL standard
is the same, each SQL provider requires different manipulative
techniques in order to compile and connect to the database.

The jcompile compiler pre-processes the jBC program parsing the normal
jBC and Embedded SQL statements to produce an intermediate C program.
The SQL implementation dependent pre-processor is then invoked to
convert the Embedded SQL statements to the implementation defined
internal functions. The resulting program is then compiled and linked.
The jBC compilation should be executed in an user account which has
been enabled for the required Embedded SQL implementation. Attempting
to compile in an account not enabled for the required SQL
implementation may cause compilation failure as certain environment
variables for the implementation may not have been modified for
the correct directory paths, etc.

## TROUBLESHOOTING

When attempting to compile a program with Embedded SQL and you get an
error along the lines of...

<pre>
    Command failed: nsqlprep PartEntry.sqc
    SQL Pre Processor error -1</pre>

...this is an indication that either you have not loaded the Embedded
SQL Kit and do not have the 'nsqlprep' command, or the 'nsqlprep'
command does exist but it is not visible to the PATH environment
variable.
