Commits and Releases
####################

Commits
=======

All commits must follow the `Conventional Commits <https://www.conventionalcommits.org>`_
specification.

These standardized commit messages are used to automatically publish releases using
`semantic-release <https://semantic-release.gitbook.io/semantic-release>`_ after commits
are merged to `main` from successful PRs.

.. code-block:: text

    feat: add API support for assigning labels to existing samples


Descriptive bodies and footers are required where necessary to describe the impact of
the commit. Use bullets where appropriate.

Types
-----

* ``test``

  * The commit affects tests, test snapshots, or test tooling.

* ``feat``

  * The commit introduces a new feature to the application or consumer of the code.


* ``style``

  * The commit is mostly related to style like code format or variable naming and imports.

* ``fix``

  * The commit fixes a bug or corrects a shortcoming in the application.
  * This commit _type_ will lead to the commit message being included in release notes.
  * This includes security fixes. For example, updating a package with a known vulnerability.
  * This includes perf improvements.

* ``refactor``

  * The commit changes code without impacting performance or interfaces.
  * Usually this is going to be an improvement to existing code.

* ``chore``

  * The commit impacts functionality to the application without impacting the user or code consumer noticeably.
  * This commit should be used when added features are protected by a feature flag.

* ``docs``

  * The commit modifies the developer or API docs.

Tips
----

* Don’t use ``fix`` or ``feat`` if your commit doesn’t affect the user or consumer of
  the code.
* Focus ``fix`` and ``feat`` commit messages on the impact on the application or code
  user.




Additional Requirements
-----------------------

1. **Write in the imperative**. For example, "fix bug", not "fixed bug" or "fixes bug".
2. **Don't refer to issues or code reviews**. For example, don't write something like
   this: "make style changes requested in review". Instead, "update styles to improve
   accessibility".
3. **Commits aren't a personal journal**. For example, don't write something like this:
   "got server running again" or "oops. fixed my code smell".

From Tim Pope: `A Note About Git Commit Messages <https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`_.

Releases
========

Releases are automated using `semantic-release <https://semantic-release.gitbook.io/semantic-release>`_.

Compatibility
-------------

Be careful to use the ``BREAKING CHANGE`` keyword when your changes break compatibility.

Example:

* Removing a field from a response from an API endpoint.
* Changing the shape of a response from an API endpoint.
* Changing paths or search query parameters.
* Removing deprecated functionality.
* Making changes that require a certain migration to have been applied.
* Changing configuration options that could break configurations in 
  production and development environments.
* Making changes that require a certain version of a service like Postgres, or Redis.

