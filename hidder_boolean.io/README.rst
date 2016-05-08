booleans.io hider (Codename: SagaTo)
====================================

Hider/Unhider information to/from booleans.io.

Booleans.io is a curious service that provices *Booleans as a service (BaaS)*.

What's is Boolean-header
========================

This project allows to hide small chunks of text using boolean.io service. It's get a text, and transform into binary representation and store bit by bit into booleans.io.

Then Boolean-header (BO) save a .db file with the information, that you can use to recover remote info.

Install
=======

BO only have one dependency, you can install it doing:

.. code-block:: bash

    # pip install -r requirements.txt

Examples
========

**Hide** the content of a file:

.. code-block:: bash

    # echo -e "a" > my_text.txt
    # python hide.py -f my_text.txt -o hidden.db
    [i] Storing char: 'a'
        |- Storing bit '0'
        |- Storing bit '1'
        |- Storing bit '1'
        |- Storing bit '0'
        |- Storing bit '0'
        |- Storing bit '0'
        |- Storing bit '0'
        |- Storing bit '1'
    [i] Storing char: '
    '
        |- Storing bit '0'
        |- Storing bit '0'
        |- Storing bit '0'
        |- Storing bit '0'
        |- Storing bit '1'
        |- Storing bit '0'
        |- Storing bit '1'
        |- Storing bit '0'

**Unhide** with the file content:

.. code-block:: bash

    # python unhide.py -f hidden.db
    [i] Starting ...
        |- Reading: 'dc342f87-39dd-4f97-8188-32ab312bc0a8'
        |- Reading: '60375eb1-7f02-4398-a8b7-a2ea1eedccd8'
        |- Reading: 'aa0aada9-5ae5-46a3-b2f9-de269ebc986b'
        |- Reading: '4311b005-e958-422d-bb4c-f625d23924ca'
        |- Reading: 'd254560a-5351-4a48-a2c0-008faa1b1a9a'
        |- Reading: '6a31180e-1394-4b70-a305-599beb5114da'
        |- Reading: '7523af15-e7c8-45a4-81e6-f989570dac0d'
        |- Reading: 'b1fbdcfc-531c-47d5-9d9c-b97ab26927a5'
        |- Reading: 'a3f8f3a9-cab5-4e84-b83a-b5c758085f49'
        |- Reading: '13910781-907c-43c9-9fcd-66e255380628'
        |- Reading: '4606d74c-4b46-42f5-8ebc-846e5680b816'
        |- Reading: '80c13529-818e-4761-91c6-55dd0d427935'
        |- Reading: '2a02bcd0-0458-4d4f-b50c-c5a5d6647965'
        |- Reading: 'e81021ce-cd73-42dc-ae55-e520a5fd9fc7'
        |- Reading: '1dd260fc-7ad6-4046-b5ab-4386cce9957f'
        |- Reading: 'fc8d3490-a189-4ae9-9d29-dee8da2fe56d'

    [i] Hidden message: 'a
    '