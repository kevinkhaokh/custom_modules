==========================
DIH Sum Accounting Entries
==========================

Extend and Customize Account Module:

- 8.0.0.1: [Add Treasury Menu, View and Functionality]
    + Duplicate the Journal Entries Menu and View with the domain (Journal Type = Bank & Cash)
    + Set Default Value to 4 fields of account.move.line (name:blank, account:blank, credit:0, debit:0)
    + Add a button name Generate a Balance record with the functionality specify below:
        - if the sum of all record's debit > credit generate record with
            x account of journal's default credit account
            x credit value with amount of different between debit and credit
        - if the sum of all record's credit > debit generate record with
            x account of journal's default debit account
            x debit value with amount of different between debit and credit
        - On regeneration the record that's generated will be delete before new generation


